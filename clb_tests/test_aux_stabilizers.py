from math import floor
from enum import IntEnum
from typing import Dict, Tuple
import logging

from network_variables import NetworkVariables
from clb_tests.tests_base import ClbTest
import calibrator_constants as clb
import utils


class AuxControl:
    pass


def voltage_to_dac_code(a_voltage: float, r1: float, r2: float, r3: float, v0: float):
    v_max = 3.3
    u1 = v0 + r1 * (v0 / r2 - (a_voltage - v0) / r3)
    float_code = 1 - u1/v_max
    float_code = utils.bound(float_code, 0, 1)

    float_code_discrete = floor(float_code * 255) / 255
    voltage_discrete = (v0 / r2 - (v_max * (1 - float_code_discrete) - v0) / r1) * r3 + v0

    return float_code, voltage_discrete


class Aux60vControl(AuxControl):
    name = "60 В"

    @staticmethod
    def set_voltage(a_voltage: float, a_netvats: NetworkVariables) -> float:
        # Этот метод должен вызываться не чаще, чем раз в секунду !!!

        real_voltage = 0.
        if a_netvats.source_manual_mode_password.get() == clb.MANUAL_MODE_ENABLE_PASSWORD:
            dac_code, voltage = voltage_to_dac_code(a_voltage, r1=110.+4420., r2=7680., r3=62000.+4700., v0=2.5)
            if round(a_netvats.aux_stabilizer_45v_dac_code_float.get(), 5) == round(dac_code, 5):
                logging.debug(f"60 В: Установлено {a_voltage} В, dac_code: {dac_code}")
                real_voltage = voltage
            else:
                a_netvats.aux_stabilizer_45v_dac_code_float.set(dac_code)
        else:
            a_netvats.source_manual_mode_password.set(clb.MANUAL_MODE_ENABLE_PASSWORD)

        return real_voltage

    @staticmethod
    def get_voltage(a_netvars: NetworkVariables) -> float:
        return a_netvars.aux_stabilizer_adc_dc_40v_voltage.get()

    @staticmethod
    def stop(a_netvars: NetworkVariables):
        a_netvars.source_manual_mode_password.set(clb.MANUAL_MODE_DISABLE_PASSWORD)


class Aux600vControl(AuxControl):
    name = "600 В"

    @staticmethod
    def set_voltage(a_voltage: float, a_netvats: NetworkVariables) -> float:
        # Этот метод должен вызываться не чаще, чем раз в секунду !!!

        real_voltage = 0.
        if a_netvats.source_manual_mode_password.get() == clb.MANUAL_MODE_ENABLE_PASSWORD:
            if a_netvats.relay_200_600.get() == 0:
                if a_netvats.relay_aux_stabilizer_600v.get() == 1:
                    dac_code, voltage = voltage_to_dac_code(a_voltage, r1=100.+5490., r2=9100., r3=330000., v0=2.5)
                    if round(a_netvats.aux_stabilizer_600v_dac_code_float.get(), 5) == round(dac_code, 5):
                        logging.debug(f"600 В: Установлено {a_voltage} В, dac_code: {dac_code}")
                        real_voltage = voltage
                    else:
                        a_netvats.aux_stabilizer_600v_dac_code_float.set(dac_code)
                else:
                    a_netvats.relay_aux_stabilizer_600v.set(1)
            else:
                a_netvats.relay_200_600.set(0)
        else:
            a_netvats.source_manual_mode_password.set(clb.MANUAL_MODE_ENABLE_PASSWORD)

        return real_voltage

    @staticmethod
    def get_voltage(a_netvars: NetworkVariables) -> float:
        return a_netvars.aux_stabilizer_adc_dc_600v_voltage.get()

    @staticmethod
    def stop(a_netvars: NetworkVariables):
        pass


class Aux200vControl(AuxControl):
    name = "200 В"

    @staticmethod
    def set_voltage(a_voltage: float, a_netvars: NetworkVariables) -> float:
        # Этот метод должен вызываться не чаще, чем раз в секунду !!!

        real_voltage = 0.
        if a_netvars.source_manual_mode_password.get() == clb.MANUAL_MODE_ENABLE_PASSWORD:
            if a_netvars.relay_200_600.get() == 1:
                if a_netvars.relay_aux_stabilizer_600v.get() == 1:
                    dac_code, voltage = voltage_to_dac_code(a_voltage, r1=100.+5490., r2=9100., r3=330000., v0=2.5)
                    if round(a_netvars.aux_stabilizer_600v_dac_code_float.get(), 5) == round(dac_code, 5):
                        logging.debug(f"200 В: Установлено {a_voltage} В, dac_code: {dac_code}")
                        real_voltage = voltage
                    else:
                        a_netvars.aux_stabilizer_600v_dac_code_float.set(dac_code)
                else:
                    a_netvars.relay_aux_stabilizer_600v.set(1)
            else:
                a_netvars.relay_200_600.set(1)
        else:
            a_netvars.source_manual_mode_password.set(clb.MANUAL_MODE_ENABLE_PASSWORD)

        return real_voltage

    @staticmethod
    def get_voltage(a_netvars: NetworkVariables) -> float:
        return a_netvars.aux_stabilizer_adc_dc_600v_voltage.get()

    @staticmethod
    def stop(a_netvars: NetworkVariables):
        pass


class Aux4vControl(AuxControl):
    name = "4 В"

    @staticmethod
    def set_voltage(a_voltage: float, a_netvars: NetworkVariables) -> bool:
        # Этот метод должен вызываться не чаще, чем раз в секунду !!!

        real_voltage = False
        if a_netvars.source_manual_mode_password.get() == clb.MANUAL_MODE_ENABLE_PASSWORD:
            dac_code, voltage = voltage_to_dac_code(a_voltage, r1=8200., r2=2200., r3=8200., v0=0.8)
            logging.debug(f"60 В: Установлено {a_voltage} В, dac_code: {dac_code}")
            if round(a_netvars.aux_stabilizer_45v_dac_code_float.get(), 5) == round(dac_code, 5):
                real_voltage = voltage
            else:
                a_netvars.aux_stabilizer_45v_dac_code_float.set(dac_code)
        else:
            a_netvars.source_manual_mode_password.set(clb.MANUAL_MODE_ENABLE_PASSWORD)

        return real_voltage

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
        WAIT_STOP = 2

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
        self.wait_stop_timer = utils.Timer(5)

        self.aux_iter = iter(self.ref_v_map.keys())
        self.current_aux = None

        self.voltage_iter = None
        self.current_voltage = 0
        # Напряжение с учетом дискрета DAC
        self.real_voltage = 0

        self.__stage = AuxStabilizersTest.Stage.PREPARE
        self.__saved_status = ClbTest.Status.NOT_CHECKED
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
                self.real_voltage = self.current_aux.set_voltage(self.current_voltage, self.netvars)
                if self.real_voltage != 0:
                    self.aux_fail_timer.start()
                    self.hold_voltage_timer.start()
                    self.__stage = AuxStabilizersTest.Stage.WAIT_VOLTAGE
                else:
                    self.check_prepare_timer.start()

        elif self.__stage == AuxStabilizersTest.Stage.WAIT_VOLTAGE:
            aux_current_voltage = self.current_aux.get_voltage(self.netvars)

            deviation = self.get_deviation_percents(aux_current_voltage, self.real_voltage)
            if deviation < self.allow_deviation_percents:
                if self.hold_voltage_timer.check():
                    logging.warning(f"Aux {self.current_aux.name}. Уставка {self.current_voltage} В. "
                                    f"Измерено {aux_current_voltage} В. Отклонение {deviation}%. "
                                    f"Выставлено в DAC вольт: {self.real_voltage}")
                    self.next_test()
            else:
                self.hold_voltage_timer.start()

            if self.aux_fail_timer.check():
                self.error_message += f"Стабилизатор {self.current_aux.name} не вышел на " \
                                      f"уставку {self.current_voltage} В. " \
                                      f"Измеренное значение {aux_current_voltage} В. Отклонение {deviation}%. " \
                                      f"Выставлено в DAC вольт: {self.real_voltage}"
                self.next_test()
        elif self.__stage == AuxStabilizersTest.Stage.WAIT_STOP:
            if self.wait_stop_timer.check():
                self.__status = self.__saved_status

    def next_test(self):
        if self.current_aux is Aux60vControl and self.has_error() and len(self.ref_v_map) > 1:
            # Если это не тест 60 В стабилизатора и 60 В стабилизатор не вышел на уставку, выдаем ошибку
            self.error_message += "Тесты остальных стабилизаторов отменены\n"
            self.__saved_status = ClbTest.Status.FAIL
            self.wait_stop_timer.start()
            self.__stage = AuxStabilizersTest.Stage.WAIT_STOP
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
                    self.__saved_status = ClbTest.Status.FAIL if self.has_error() else ClbTest.Status.SUCCESS
                    self.wait_stop_timer.start()
                    self.__stage = AuxStabilizersTest.Stage.WAIT_STOP

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
