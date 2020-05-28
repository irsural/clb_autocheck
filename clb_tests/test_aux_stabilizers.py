from enum import IntEnum
from typing import Dict, Tuple
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
        logging.debug(f"60 В: SET {a_voltage} В")
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
        logging.debug(f"600 В: SET {a_voltage} В")
        return True

    @staticmethod
    def get_voltage(a_netvars: NetworkVariables) -> float:
        return a_netvars.aux_stabilizer_adc_dc_600v_voltage.get()

    @staticmethod
    def stop(a_netvars: NetworkVariables):
        pass


class Aux200vControl(AuxControl):
    name = "600 В"

    @staticmethod
    def set_voltage(a_voltage: float, a_netvats: NetworkVariables) -> bool:
        logging.debug(f"200 В: SET {a_voltage} В")
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
        logging.debug(f"4 В: SET {a_voltage} В")
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
        V200 = 1,
        V600 = 2,
        V4 = 3

    AUX_TYPE_TO_AUX_CONTROL = {
        AuxType.V60: Aux60vControl,
        AuxType.V200: Aux200vControl,
        AuxType.V600: Aux600vControl,
        AuxType.V4: Aux4vControl,
    }

    AUX_CONTROL_TO_AUX_TYPE = {
        Aux60vControl:  AuxType.V60,
        Aux200vControl:  AuxType.V200,
        Aux600vControl:  AuxType.V600,
        Aux4vControl:  AuxType.V4,
    }

    class Stage(IntEnum):
        PREPARE = 0
        WAIT_VOLTAGE = 1

    def __init__(self, a_ref_v_map: Dict[AuxType, Tuple[float]], a_netvars: NetworkVariables,
                 a_aux_fail_timeout_s: int = 40, a_hold_voltage_timeout_s: int = 10, a_timeout_s: int = 100):
        super().__init__()

        assert AuxStabilizersTest.AuxType.V60 in a_ref_v_map, "Тест обязательно должен содержать стабилизатор 60 В"
        if len(a_ref_v_map) > 1:
            assert len(a_ref_v_map[AuxStabilizersTest.AuxType.V60]) == 1, "Тесты стабилизаторов 600 В и 4 В должны " \
                                                                          "содержать только одно напряжение для " \
                                                                          "стабилизатора 60 В"

        self.ref_v_map = a_ref_v_map
        self.netvars = a_netvars
        self.__timeout_s = a_timeout_s
        self.error_message = ""

        self.check_prepare_timer = utils.Timer(1.1)
        self.hold_voltage_timer = utils.Timer(a_hold_voltage_timeout_s)
        self.aux_fail_timer = utils.Timer(a_aux_fail_timeout_s)

        self.aux_iter = iter(self.ref_v_map.keys())
        self.current_aux = None

        self.voltage_iter = None
        self.current_voltage = 0

        self.__stage = AuxStabilizersTest.Stage.PREPARE
        self.__status = ClbTest.Status.NOT_CHECKED

        self.allow_deviation_percents = 10

    def start(self):
        self.__status = ClbTest.Status.IN_PROCESS
        self.__stage = AuxStabilizersTest.Stage.PREPARE
        self.aux_iter = iter(self.ref_v_map.keys())
        self.current_aux = self.get_next_aux()
        self.voltage_iter = iter(self.ref_v_map[AuxStabilizersTest.AUX_CONTROL_TO_AUX_TYPE[self.current_aux]])
        self.current_voltage = self.get_next_voltage()
        self.check_prepare_timer.start()

    def stop(self):
        self.__status = ClbTest.Status.NOT_CHECKED
        self.error_message = ""
        self.hold_voltage_timer.stop()
        self.aux_fail_timer.stop()
        self.check_prepare_timer.stop()
        for aux_type in reversed(list(self.ref_v_map.keys())):
            AuxStabilizersTest.AUX_TYPE_TO_AUX_CONTROL[aux_type].stop(self.netvars)

    def prepare(self) -> bool:
        return True

    def tick(self):
        if self.__stage == AuxStabilizersTest.Stage.PREPARE:
            if self.check_prepare_timer.check():
                if self.current_aux.set_voltage(self.current_voltage, self.netvars):
                    self.aux_fail_timer.start()
                    self.hold_voltage_timer.start()
                    self.__stage = AuxStabilizersTest.Stage.WAIT_VOLTAGE
                else:
                    self.check_prepare_timer.start()

        elif self.__stage == AuxStabilizersTest.Stage.WAIT_VOLTAGE:
            aux_current_voltage = self.current_aux.get_voltage(self.netvars)

            if self.get_deviation_percents(aux_current_voltage, self.current_voltage) < self.allow_deviation_percents:
                if self.hold_voltage_timer.check():
                    self.next_test()
            else:
                self.hold_voltage_timer.start()

            if self.aux_fail_timer.check():
                self.error_message += f"Стабилизатор {self.current_aux.name} не вышел на " \
                                      f"уставку {self.current_voltage} В. Измеренное значение {aux_current_voltage}\n"
                self.next_test()

    def next_test(self):
        if self.current_aux is Aux60vControl and self.has_error() and len(self.ref_v_map) > 1:
            # Если это не тест 60 В стабилизатора и 60 В стабилизатор не вышел на уставку, выдаем ошибку
            self.error_message += "Тесты остальных стабилизаторов отменены\n"
            self.__status = ClbTest.Status.FAIL
        else:
            self.__stage = AuxStabilizersTest.Stage.PREPARE
            self.check_prepare_timer.start()
            self.hold_voltage_timer.stop()
            self.aux_fail_timer.stop()

            self.current_voltage = self.get_next_voltage()
            if self.current_voltage is None:
                # Напряжения для текущего стабилизатора кончились
                self.current_aux = self.get_next_aux()

                if self.current_aux is not None:
                    self.voltage_iter = iter(self.ref_v_map[AuxStabilizersTest.AUX_CONTROL_TO_AUX_TYPE[self.current_aux]])
                    self.current_voltage = self.get_next_voltage()
                else:
                    # Текущий стабилизатор был последним
                    self.__status = ClbTest.Status.FAIL if self.has_error() else ClbTest.Status.SUCCESS

    def get_next_aux(self):
        try:
            return AuxStabilizersTest.AUX_TYPE_TO_AUX_CONTROL[next(self.aux_iter)]
        except StopIteration:
            return None

    def get_next_voltage(self):
        try:
            return next(self.voltage_iter)
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
