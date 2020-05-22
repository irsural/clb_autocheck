from enum import IntEnum
from typing import Dict
import logging

from network_variables import NetworkVariables
from clb_tests.tests_base import ClbTest
import utils


class AuxControl:
    pass


class Aux60vControl(AuxControl):
    name = "60 В"

    @staticmethod
    def set_voltage(a_voltage: float, a_netvats: NetworkVariables) -> bool:
        # Убедиться, что все переменные в нужных значениях
        # Выставить уставку
        return True

    @staticmethod
    def get_voltage(a_netvars: NetworkVariables) -> float:
        return a_netvars.aux_stabilizer_adc_dc_40v_voltage.get()

    @staticmethod
    def stop(a_netvars: NetworkVariables):
        pass


class Aux600vControl(AuxControl):
    name = "600 В"

    @staticmethod
    def set_voltage(a_voltage: float, a_netvats: NetworkVariables) -> bool:
        return True

    @staticmethod
    def get_voltage(a_netvars: NetworkVariables) -> float:
        return a_netvars.aux_stabilizer_adc_dc_600v_voltage.get()

    @staticmethod
    def stop(a_netvars: NetworkVariables):
        pass


class Aux4vControl(AuxControl):
    name = "4 В"

    @staticmethod
    def set_voltage(a_voltage: float, a_netvats: NetworkVariables) -> bool:
        return True

    @staticmethod
    def get_voltage(a_netvars: NetworkVariables) -> float:
        return a_netvars.aux_stabilizer_adc_dc_4v_voltage.get()

    @staticmethod
    def stop(a_netvars: NetworkVariables):
        pass


class AuxStabilizersTest(ClbTest):
    class AuxType(IntEnum):
        V60 = 0,
        V600 = 1,
        V4 = 2

    AUX_TYPE_TO_AUX_CONTROL = {
        AuxType.V60: Aux60vControl,
        AuxType.V600: Aux600vControl,
        AuxType.V4: Aux4vControl,
    }

    AUX_CONTROL_TO_AUX_TYPE = {
        Aux60vControl:  AuxType.V60,
        Aux600vControl:  AuxType.V600,
        Aux4vControl:  AuxType.V4,
    }

    class Stage(IntEnum):
        PREPARE = 0
        WAIT_VOLTAGE = 1

    def __init__(self, a_ref_v_map: Dict[AuxType, float], a_netvars: NetworkVariables,
                 a_aux_fail_timeout_s: int = 40, a_hold_voltage_timeout_s: int = 10, a_timeout_s: int = 100):
        super().__init__()

        self.ref_v_map = a_ref_v_map
        self.netvars = a_netvars
        self.__timeout_s = a_timeout_s
        self.error_message = ""

        self.hold_voltage_timer = utils.Timer(a_hold_voltage_timeout_s)
        self.aux_fail_timer = utils.Timer(a_aux_fail_timeout_s)

        self.aux_iter = iter(self.ref_v_map.keys())
        self.current_aux = None

        self.__stage = AuxStabilizersTest.Stage.PREPARE
        self.__status = ClbTest.Status.NOT_CHECKED

        self.allow_deviation_percents = 10

    def prepare(self) -> bool:
        return True

    def start(self):
        self.__status = ClbTest.Status.IN_PROCESS
        self.__stage = AuxStabilizersTest.Stage.PREPARE
        self.aux_iter = iter(self.ref_v_map.keys())
        self.current_aux = self.get_next_aux()

    def stop(self):
        self.__status = ClbTest.Status.NOT_CHECKED
        self.error_message = ""
        self.hold_voltage_timer.stop()
        self.aux_fail_timer.stop()
        for aux_type in reversed(list(self.ref_v_map.keys())):
            AuxStabilizersTest.AUX_TYPE_TO_AUX_CONTROL[aux_type].stop(self.netvars)

    def tick(self):
        voltage_setpoint = self.ref_v_map[AuxStabilizersTest.AUX_CONTROL_TO_AUX_TYPE[self.current_aux]]

        if self.__stage == AuxStabilizersTest.Stage.PREPARE:
            if self.current_aux.set_voltage(voltage_setpoint, self.netvars):
                self.aux_fail_timer.start()
                self.hold_voltage_timer.start()
                self.__stage = AuxStabilizersTest.Stage.WAIT_VOLTAGE

        elif self.__stage == AuxStabilizersTest.Stage.WAIT_VOLTAGE:
            aux_current_voltage = self.current_aux.get_voltage(self.netvars)

            if self.get_deviation_percents(aux_current_voltage, voltage_setpoint) < self.allow_deviation_percents:
                if self.hold_voltage_timer.check():
                    self.next_test()
            else:
                self.hold_voltage_timer.start()

            if self.aux_fail_timer.check():
                self.error_message += f"Стабилизатор {self.current_aux.name} не вышел на " \
                                      f"уставку {voltage_setpoint} В. Измеренное значение {aux_current_voltage}\n"
                self.next_test()

    def next_test(self):
        if self.current_aux is Aux60vControl and self.has_error():
            self.error_message += "Тесты остальных стабилизаторов отменены\n"
            self.__status = ClbTest.Status.FAIL
        else:
            self.__stage = AuxStabilizersTest.Stage.PREPARE
            self.hold_voltage_timer.stop()
            self.aux_fail_timer.stop()

            self.current_aux = self.get_next_aux()
            if self.current_aux is None:
                # Текущий стабилизатор был последним
                self.__status = ClbTest.Status.FAIL if self.has_error() else ClbTest.Status.SUCCESS

    def get_next_aux(self):
        try:
            return AuxStabilizersTest.AUX_TYPE_TO_AUX_CONTROL[next(self.aux_iter)]
        except StopIteration:
            return None

    @staticmethod
    def get_deviation_percents(a_first_val, a_second_val):
        return abs(a_first_val - a_second_val) / a_first_val * 100

    def status(self) -> ClbTest.Status:
        return self.__status

    def timeout(self) -> float:
        return self.__timeout_s

    def has_error(self) -> bool:
        return bool(self.error_message)

    def get_last_error(self) -> str:
        return self.error_message

    def abort_on_fail(self) -> bool:
        return False
