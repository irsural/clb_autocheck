from math import floor
from enum import IntEnum
from typing import Dict, Tuple
import logging

from network_variables import NetworkVariables, BufferedVariable
from clb_tests.tests_base import ClbTest
from settings_ini_parser import Settings
import calibrator_constants as clb
import utils


def voltage_to_dac_code(a_voltage: float, r1: float, r2: float, r3: float, v0: float):
    v_max = 3.3
    u1 = v0 + r1 * (v0 / r2 - (a_voltage - v0) / r3)
    float_code = 1 - u1 / v_max
    float_code = utils.bound(float_code, 0, 1)

    float_code_discrete = floor(float_code * 255) / 255
    voltage_discrete = (v0 / r2 - (v_max * (1 - float_code_discrete) - v0) / r1) * r3 + v0

    return float_code, voltage_discrete


class AuxControl:
    class Stage(IntEnum):
        SET_LOW = 0
        WAIT_LOW = 1
        SET_HIGH = 2
        WAIT_HIGH = 3
        DONE = 4

    NEXT_STAGE = {
        Stage.SET_LOW: Stage.WAIT_LOW,
        Stage.WAIT_LOW: Stage.SET_HIGH,
        Stage.SET_HIGH: Stage.WAIT_HIGH,
        Stage.WAIT_HIGH: Stage.DONE,
        Stage.DONE: Stage.DONE,
    }

    CORRECT_POINT_LOW_DISCRETES = 25
    CORRECT_POINT_HIGH_DISCRETES = 230

    def __init__(self, a_deviation: float, a_correct_point_low: float, a_correct_point_high: float):
        self.k = 0
        self.b = 0

        self.__stage = AuxControl.Stage.SET_LOW
        self.wait_setpoint_timer = utils.Timer(2)

        self.allow_deviation_percents = a_deviation
        self.correct_point_low_voltage = a_correct_point_low
        self.correct_point_high_voltage = a_correct_point_high

        self.measured_point_low_voltage = 0
        self.measured_point_high_voltage = 0

    @staticmethod
    def get_deviation_percents(a_first_val, a_second_val):
        if a_first_val == 0:
            return a_first_val
        else:
            return abs(a_first_val - a_second_val) / a_first_val * 100

    @staticmethod
    def discretes_to_float(a_discretes: int) -> float:
        return (a_discretes + 0.1) / 255

    @staticmethod
    def float_to_discretes(a_float_code: float):
        return a_float_code * 255 - 0.1

    def make_correction(self, a_dac_float_var: BufferedVariable, a_get_voltage_var: BufferedVariable) -> bool:
        if self.__stage == AuxControl.Stage.SET_LOW:
            if AuxControl.CORRECT_POINT_LOW_DISCRETES == round(self.float_to_discretes(a_dac_float_var.get()), 5):
                logging.info("Коррекция точки 25 дискретов ЦАП")
                self.wait_setpoint_timer.start()
                self.__stage = AuxControl.NEXT_STAGE[self.__stage]
            else:
                a_dac_float_var.set(self.discretes_to_float(AuxControl.CORRECT_POINT_LOW_DISCRETES))

        elif self.__stage == AuxControl.Stage.WAIT_LOW:
            self.measured_point_low_voltage = a_get_voltage_var.get()
            if self.get_deviation_percents(self.correct_point_low_voltage, self.measured_point_low_voltage) < self.allow_deviation_percents:
                if self.wait_setpoint_timer.check():
                    logging.info(self.get_correction_info_low_point())

                    self.wait_setpoint_timer.stop()
                    self.__stage = AuxControl.NEXT_STAGE[self.__stage]
            else:
                self.wait_setpoint_timer.start()

        elif self.__stage == AuxControl.Stage.SET_HIGH:
            if AuxControl.CORRECT_POINT_HIGH_DISCRETES == round(self.float_to_discretes(a_dac_float_var.get()), 5):
                logging.info("Коррекция точки 230 дискретов ЦАП")
                self.wait_setpoint_timer.start()
                self.__stage = AuxControl.NEXT_STAGE[self.__stage]
            else:
                a_dac_float_var.set(self.discretes_to_float(AuxControl.CORRECT_POINT_HIGH_DISCRETES))

        elif self.__stage == AuxControl.Stage.WAIT_HIGH:
            self.measured_point_high_voltage = a_get_voltage_var.get()
            if self.get_deviation_percents(self.correct_point_high_voltage, self.measured_point_high_voltage) < self.allow_deviation_percents:
                if self.wait_setpoint_timer.check():
                    logging.info(self.get_correction_info_high_point())

                    self.wait_setpoint_timer.stop()
                    self.k_b_calc()
                    self.__stage = AuxControl.NEXT_STAGE[self.__stage]
            else:
                self.wait_setpoint_timer.start()

        elif self.__stage == AuxControl.Stage.DONE:
            pass

        return self.__stage == AuxControl.Stage.DONE

    def k_b_calc(self):
        self.k = (self.measured_point_high_voltage - self.measured_point_low_voltage) / \
                 (AuxControl.CORRECT_POINT_HIGH_DISCRETES - AuxControl.CORRECT_POINT_LOW_DISCRETES)
        self.b = self.measured_point_low_voltage - self.k * AuxControl.CORRECT_POINT_LOW_DISCRETES
        logging.debug(f"k={self.k};\tb={self.b}")

    def get_corrected_voltage(self, a_discretes: int):
        return self.k * a_discretes + self.b

    def get_correction_info_low_point(self):
        return f"Измерено в точке 25 дискретов ЦАП: {self.measured_point_low_voltage}. Ожидаемое напряжение: " \
               f"{self.correct_point_low_voltage}. Отклонение: " \
               f"{self.get_deviation_percents(self.measured_point_low_voltage, self.correct_point_low_voltage)}"

    def get_correction_info_high_point(self):
        return f"Измерено в точке 230 дискретов ЦАП: {self.measured_point_high_voltage}. "\
               f"Ожидаемое напряжение: {self.correct_point_high_voltage}. Отклонение: " \
               f"{self.get_deviation_percents(self.measured_point_high_voltage, self.correct_point_high_voltage)}"


class Aux60vControl(AuxControl):
    name = "60 В"

    def __init__(self, a_deviation: float, a_correct_point_low: float, a_correct_point_high: float):
        super().__init__(a_deviation, a_correct_point_low, a_correct_point_high)

    def set_voltage_discretes(self, a_discretes: int, a_netvats: NetworkVariables) -> float:
        # Этот метод должен вызываться не чаще, чем раз в секунду !!!

        real_voltage = 0.
        if a_netvats.source_manual_mode_password.get() == clb.MANUAL_MODE_ENABLE_PASSWORD:
            if self.make_correction(a_netvats.aux_stabilizer_45v_dac_code_float,
                                    a_netvats.aux_stabilizer_adc_dc_40v_voltage):

                discretes_float = self.discretes_to_float(a_discretes)
                if round(a_netvats.aux_stabilizer_45v_dac_code_float.get(), 5) == round(discretes_float, 5):
                    real_voltage = self.get_corrected_voltage(a_discretes)
                    logging.info(f"Aux 60 В: Установлено (float) {discretes_float}. В дискретах ЦАП: {a_discretes}")
                else:
                    a_netvats.aux_stabilizer_45v_dac_code_float.set(discretes_float)
        else:
            a_netvats.source_manual_mode_password.set(clb.MANUAL_MODE_ENABLE_PASSWORD)

        return real_voltage

    @staticmethod
    def get_voltage(a_netvars: NetworkVariables) -> float:
        return a_netvars.aux_stabilizer_adc_dc_40v_voltage.get()

    @staticmethod
    def stop(a_netvars: NetworkVariables):
        pass


class Aux600vControl(AuxControl):
    name = "600 В"

    def __init__(self, a_deviation: float, a_correct_point_low: float, a_correct_point_high: float):
        super().__init__(a_deviation, a_correct_point_low, a_correct_point_high)

    def set_voltage_discretes(self, a_discretes: int, a_netvars: NetworkVariables) -> float:
        # Этот метод должен вызываться не чаще, чем раз в секунду !!!

        real_voltage = 0.
        if a_netvars.source_manual_mode_password.get() == clb.MANUAL_MODE_ENABLE_PASSWORD:
            if a_netvars.relay_200_600.get() == 0:
                if a_netvars.relay_aux_stabilizer_600v.get() == 1:
                    if self.make_correction(a_netvars.aux_stabilizer_600v_dac_code_float,
                                            a_netvars.aux_stabilizer_adc_dc_600v_voltage):

                        discretes_float = self.discretes_to_float(a_discretes)
                        if round(a_netvars.aux_stabilizer_600v_dac_code_float.get(), 5) == round(discretes_float, 5):
                            logging.info(f"Aux 600 В: Установлено (float) {discretes_float}. В дискретах ЦАП: {a_discretes}")
                            real_voltage = self.get_corrected_voltage(a_discretes)
                        else:
                            a_netvars.aux_stabilizer_600v_dac_code_float.set(discretes_float)
                else:
                    a_netvars.relay_aux_stabilizer_600v.set(1)
            else:
                a_netvars.relay_200_600.set(0)
        else:
            a_netvars.source_manual_mode_password.set(clb.MANUAL_MODE_ENABLE_PASSWORD)

        return real_voltage

    @staticmethod
    def get_voltage(a_netvars: NetworkVariables) -> float:
        return a_netvars.aux_stabilizer_adc_dc_600v_voltage.get()

    @staticmethod
    def stop(a_netvars: NetworkVariables):
        pass


class Aux200vControl(AuxControl):
    name = "200 В"

    def __init__(self, a_deviation: float, a_correct_point_low: float, a_correct_point_high: float):
        super().__init__(a_deviation, a_correct_point_low, a_correct_point_high)

    def set_voltage_discretes(self, a_discretes: int, a_netvars: NetworkVariables) -> float:
        # Этот метод должен вызываться не чаще, чем раз в секунду !!!

        real_voltage = 0.
        if a_netvars.source_manual_mode_password.get() == clb.MANUAL_MODE_ENABLE_PASSWORD:
            if a_netvars.relay_200_600.get() == 1:
                if a_netvars.relay_aux_stabilizer_600v.get() == 1:
                    if self.make_correction(a_netvars.aux_stabilizer_600v_dac_code_float,
                                            a_netvars.aux_stabilizer_adc_dc_600v_voltage):

                        discretes_float = self.discretes_to_float(a_discretes)
                        if round(a_netvars.aux_stabilizer_600v_dac_code_float.get(), 5) == round(discretes_float, 5):
                            logging.info(f"Aux 200 В: Установлено (float) {discretes_float}. В дискретах ЦАП: {a_discretes}")
                            real_voltage = self.get_corrected_voltage(a_discretes)
                        else:
                            a_netvars.aux_stabilizer_600v_dac_code_float.set(discretes_float)
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

    def __init__(self, a_deviation: float, a_correct_point_low: float, a_correct_point_high: float):
        super().__init__(a_deviation, a_correct_point_low, a_correct_point_high)

    def set_voltage_discretes(self, a_discretes: int, a_netvars: NetworkVariables) -> bool:
        # Этот метод должен вызываться не чаще, чем раз в секунду !!!

        real_voltage = False
        if a_netvars.source_manual_mode_password.get() == clb.MANUAL_MODE_ENABLE_PASSWORD:
            if a_netvars.relay_aux_stabilizer_4v.get() == 1:
                if self.make_correction(a_netvars.aux_stabilizer_4v_dac_code_float,
                                        a_netvars.aux_stabilizer_adc_dc_4v_voltage):

                    discretes_float = self.discretes_to_float(a_discretes)
                    if round(a_netvars.aux_stabilizer_4v_dac_code_float.get(), 5) == round(discretes_float, 5):
                        logging.info(f"Aux 4 В: Установлено (float) {discretes_float}. В дискретах ЦАП: {a_discretes}")
                        real_voltage = self.get_corrected_voltage(a_discretes)
                    else:
                        a_netvars.aux_stabilizer_4v_dac_code_float.set(discretes_float)
            else:
                a_netvars.relay_aux_stabilizer_4v.set(1)
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
        Aux60vControl: AuxType.V60,
        Aux200vControl: AuxType.V200,
        Aux600vControl: AuxType.V600,
        Aux4vControl: AuxType.V4,
    }

    class Stage(IntEnum):
        PREPARE = 0
        WAIT_VOLTAGE = 1
        WAIT_STOP = 2

    def __init__(self, a_settings: Settings, a_ref_v_map: Dict[AuxType, Tuple[int]], a_netvars: NetworkVariables,
                 a_aux_fail_timeout_s: int = 40, a_hold_voltage_timeout_s: int = 10, a_timeout_s: int = 100):
        super().__init__()

        assert AuxStabilizersTest.AuxType.V60 in a_ref_v_map, "Тест обязательно должен содержать стабилизатор 60 В"
        if len(a_ref_v_map) > 1:
            assert len(a_ref_v_map[AuxStabilizersTest.AuxType.V60]) == 1, "Тесты стабилизаторов 600 В и 4 В должны " \
                                                                          "содержать только одно напряжение для " \
                                                                          "стабилизатора 60 В"
        self.settings = a_settings
        self.ref_v_map = a_ref_v_map
        self.netvars = a_netvars
        self.__timeout_s = a_timeout_s
        self.error_message = ""

        self.check_prepare_timer = utils.Timer(1.1)
        self.prepare_fail_timer = utils.Timer(20)
        self.hold_voltage_timer = utils.Timer(a_hold_voltage_timeout_s)
        self.aux_fail_timer = utils.Timer(a_aux_fail_timeout_s)
        self.wait_stop_timer = utils.Timer(5)

        self.aux_iter = iter(self.ref_v_map.keys())
        self.current_aux = None

        self.voltage_iter = None
        self.current_voltage_in_discretes = 0

        self.real_voltage = 0

        self.cancel_test = False

        self.__stage = AuxStabilizersTest.Stage.PREPARE
        self.__saved_status = ClbTest.Status.NOT_CHECKED
        self.__status = ClbTest.Status.NOT_CHECKED

        self.allow_deviation_percents = 10

    def start(self):
        self.__status = ClbTest.Status.IN_PROCESS if not self.cancel_test else ClbTest.Status.FAIL
        self.__stage = AuxStabilizersTest.Stage.PREPARE
        self.aux_iter = iter(self.ref_v_map.keys())
        self.current_aux = self.get_next_aux()
        self.voltage_iter = iter(self.ref_v_map[AuxStabilizersTest.AUX_CONTROL_TO_AUX_TYPE[type(self.current_aux)]])
        self.current_voltage_in_discretes = self.get_next_voltage()
        self.check_prepare_timer.start()
        self.prepare_fail_timer.start()

    def stop(self):
        self.__status = ClbTest.Status.NOT_CHECKED
        self.error_message = ""
        self.hold_voltage_timer.stop()
        self.aux_fail_timer.stop()
        self.check_prepare_timer.stop()
        self.prepare_fail_timer.stop()
        self.cancel_test = False
        # for aux_type in reversed(list(self.ref_v_map.keys())):
        #     AuxStabilizersTest.AUX_TYPE_TO_AUX_CONTROL[aux_type].stop(self.netvars)
        self.netvars.source_manual_mode_password.set(0)
        self.netvars.shutdown_execute_password.set(clb.SHUTDOWN_EXECUTE_PASSWORD)

    def prepare(self) -> bool:
        if self.netvars.source_manual_mode_password.get() == clb.MANUAL_MODE_ENABLE_PASSWORD or \
                self.netvars.aux_stabilizer_4v_dac_code_float.get() != 0 or \
                self.netvars.aux_stabilizer_45v_dac_code_float.get() != 0 or \
                self.netvars.aux_stabilizer_600v_dac_code_float.get() != 0 or \
                self.netvars.relay_aux_stabilizer_4v.get() != 0 or \
                self.netvars.relay_aux_stabilizer_600v.get() != 0:
            logging.warning("При начале теста предварительного стабилизатора был включен ручной режим. "
                            "Перезагрузите калибратор и повторите попытку")
            self.cancel_test = True
        return True

    def tick(self):
        if self.__stage == AuxStabilizersTest.Stage.PREPARE:
            if self.check_prepare_timer.check():
                self.real_voltage = self.current_aux.set_voltage_discretes(self.current_voltage_in_discretes, self.netvars)
                if self.real_voltage != 0:
                    self.aux_fail_timer.start()
                    self.hold_voltage_timer.start()
                    self.__stage = AuxStabilizersTest.Stage.WAIT_VOLTAGE

                elif self.prepare_fail_timer.check():
                    self.error_message += f"Не удалось провести коррекцию\n" \
                                          f"{self.current_aux.get_correction_info_low_point()}\n" \
                                          f"{self.current_aux.get_correction_info_high_point()}\n"
                    self.__saved_status = ClbTest.Status.FAIL
                    self.wait_stop_timer.start()
                    self.__stage = AuxStabilizersTest.Stage.WAIT_STOP
                    self.netvars.source_manual_mode_password.set(0)
                    self.check_prepare_timer.start()

                else:
                    self.check_prepare_timer.start()

        elif self.__stage == AuxStabilizersTest.Stage.WAIT_VOLTAGE:
            aux_current_voltage = self.current_aux.get_voltage(self.netvars)

            deviation = self.get_deviation_percents(aux_current_voltage, self.real_voltage)
            if deviation < self.allow_deviation_percents:
                if self.hold_voltage_timer.check():
                    logging.warning(f"Aux {self.current_aux.name}. Ожидаемое напряжение {self.real_voltage}. "
                                    f"Измерено {aux_current_voltage} В. Отклонение {deviation}%.")
                    self.next_test()
            else:
                self.hold_voltage_timer.start()

            if self.aux_fail_timer.check():
                logging.warning(f"Aux {self.current_aux.name}. Ожидаемое напряжение {self.real_voltage}. "
                                f"Измерено {aux_current_voltage} В. Отклонение {deviation}% !!!")

                self.error_message += f"Стабилизатор {self.current_aux.name} не вышел на " \
                                      f"уставку {self.current_voltage_in_discretes} дискретов ЦАП. " \
                                      f"Измеренное значение {aux_current_voltage} В. Отклонение {deviation}%. " \
                                      f"Ожидаемое напряжение: {self.real_voltage}"
                self.next_test()
        elif self.__stage == AuxStabilizersTest.Stage.WAIT_STOP:
            if self.check_prepare_timer.check():
                if self.netvars.source_manual_mode_password.get() == 0:
                    self.netvars.shutdown_execute_password.set(clb.SHUTDOWN_EXECUTE_PASSWORD)
                    self.check_prepare_timer.stop()
                else:
                    self.check_prepare_timer.start()

            if self.wait_stop_timer.check():
                self.__status = self.__saved_status

    def next_test(self):
        if self.current_aux is Aux60vControl and self.has_error() and len(self.ref_v_map) > 1:
            # Если это не тест 60 В стабилизатора и 60 В стабилизатор не вышел на уставку, выдаем ошибку
            self.error_message += "Тесты остальных стабилизаторов отменены\n"
            self.__saved_status = ClbTest.Status.FAIL
            self.wait_stop_timer.start()
            self.__stage = AuxStabilizersTest.Stage.WAIT_STOP
            self.netvars.source_manual_mode_password.set(0)
            self.check_prepare_timer.start()

        else:
            self.__stage = AuxStabilizersTest.Stage.PREPARE
            self.check_prepare_timer.start()
            self.prepare_fail_timer.start()
            self.hold_voltage_timer.stop()
            self.aux_fail_timer.stop()

            self.current_voltage_in_discretes = self.get_next_voltage()
            if self.current_voltage_in_discretes is None:
                # Напряжения для текущего стабилизатора кончились
                self.current_aux = self.get_next_aux()

                if self.current_aux is not None:
                    self.voltage_iter = iter(
                        self.ref_v_map[AuxStabilizersTest.AUX_CONTROL_TO_AUX_TYPE[type(self.current_aux)]])
                    self.current_voltage_in_discretes = self.get_next_voltage()
                else:
                    # Текущий стабилизатор был последним
                    self.__saved_status = ClbTest.Status.FAIL if self.has_error() else ClbTest.Status.SUCCESS
                    self.wait_stop_timer.start()
                    self.__stage = AuxStabilizersTest.Stage.WAIT_STOP
                    self.netvars.source_manual_mode_password.set(0)
                    self.check_prepare_timer.start()

    def get_next_aux(self):
        try:
            aux_control_type = AuxStabilizersTest.AUX_TYPE_TO_AUX_CONTROL[next(self.aux_iter)]

            if aux_control_type is Aux60vControl:
                correct_expected_low_voltage = self.settings.aux_voltage_25_discretes_60v
                correct_expected_high_voltage = self.settings.aux_voltage_230_discretes_60v
            elif aux_control_type is Aux200vControl:
                correct_expected_low_voltage = self.settings.aux_voltage_25_discretes_200v
                correct_expected_high_voltage = self.settings.aux_voltage_230_discretes_200v
            elif aux_control_type is Aux600vControl:
                correct_expected_low_voltage = self.settings.aux_voltage_25_discretes_600v
                correct_expected_high_voltage = self.settings.aux_voltage_230_discretes_600v
            else: # aux_control_type is Aux4vControl:
                correct_expected_low_voltage = self.settings.aux_voltage_25_discretes_4v
                correct_expected_high_voltage = self.settings.aux_voltage_230_discretes_4v

            correction_deviation = self.settings.aux_correction_deviation
            self.allow_deviation_percents = self.settings.aux_deviation

            return aux_control_type(correction_deviation, correct_expected_low_voltage, correct_expected_high_voltage)
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
        return True
