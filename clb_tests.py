import utils
import logging
from enum import IntEnum

from network_variables import NetworkVariables
from clb_tests_base import ClbTest
import calibrator_constants as clb
from clb_dll import ClbDrv


class SignalTest(ClbTest):
    def __init__(self, a_amplitude: float, a_signal_type: clb.SignalType, a_calibrator: ClbDrv,
                 a_netvars: NetworkVariables, a_hold_signal_timeout_s: int = 10, a_timeout_s: int = 30):
        super().__init__()
        self.amplitude = a_amplitude
        self.signal_type = a_signal_type
        self.calibrator = a_calibrator
        self.netvars = a_netvars
        self.__timeout_s = a_timeout_s

        self.hold_signal_timer = utils.Timer(a_hold_signal_timeout_s)
        self.__status = ClbTest.Status.NOT_CHECKED

    def prepare(self) -> bool:
        if not clb.is_voltage_signal[self.signal_type]:
            # Замкнуть клеммы
            pass

        if self.calibrator.amplitude == self.amplitude and self.calibrator.signal_type == self.signal_type and \
                not self.calibrator.signal_enable:
            return True
        else:
            self.calibrator.amplitude = self.amplitude
            self.calibrator.signal_type = self.signal_type
            self.calibrator.signal_enable = False
            return False

    def start(self):
        self.__status = ClbTest.Status.IN_PROCESS
        self.calibrator.signal_enable = True
        self.hold_signal_timer.start()

    def stop(self):
        self.__status = ClbTest.Status.NOT_CHECKED
        self.calibrator.signal_enable = False
        self.hold_signal_timer.stop()

    def tick(self):
        if self.calibrator.state in (clb.State.WAITING_SIGNAL, clb.State.READY):
            if self.calibrator.state == clb.State.WAITING_SIGNAL:
                self.hold_signal_timer.start()
            else:
                if self.hold_signal_timer.check():
                    self.__status = ClbTest.Status.SUCCESS
        else:
            logging.debug("Обнаружено выключение сигнала")
            self.__status = ClbTest.Status.FAIL

    def status(self) -> ClbTest.Status:
        return self.__status

    def timeout(self) -> float:
        return self.__timeout_s

    def has_error(self) -> bool:
        return ClbTest.does_calibrator_has_error(self.netvars)

    def get_last_error(self) -> str:
        return ClbTest.get_calibrator_last_error(self.netvars)


class CoolerTest(ClbTest):
    class CoolerLocation(IntEnum):
        MAIN_BOARD = 0
        TRANSISTOR_DC = 1

    def __init__(self, a_cooler_location: CoolerLocation, a_netvars: NetworkVariables,
                 a_wait_cooler_timeout_s: int = 10, a_timeout_s: int = 30):
        super().__init__()

        if a_cooler_location == CoolerTest.CoolerLocation.MAIN_BOARD:
            self.setpoint_variable = a_netvars.main_board_fun_temperature_setpoint
            self.speed_variable = a_netvars.main_board_fun_speed
            self.current_temp_variable = a_netvars.main_board_temperature
        else: # a_cooler_location == CoolerTest.CoolerLocation.TRANSISTOR_DC
            self.setpoint_variable = a_netvars.transistor_dc_10a_fun_temperature_setpoint
            self.speed_variable = a_netvars.transistor_dc_10a_fun_speed
            self.current_temp_variable = a_netvars.transistor_dc_10a_temperature

        self.setpoint_decrease = 10
        self.prev_setpoint = self.setpoint_variable.get()

        self.netvars = a_netvars
        self.__timeout_s = a_timeout_s

        self.wait_cooler_timer = utils.Timer(a_wait_cooler_timeout_s)
        self.__status = ClbTest.Status.NOT_CHECKED

    def prepare(self) -> bool:
        return True

    def start(self):
        self.__status = ClbTest.Status.IN_PROCESS
        self.wait_cooler_timer.start()

        self.prev_setpoint = self.setpoint_variable.get()
        self.setpoint_variable.set(self.current_temp_variable.get() - self.setpoint_decrease)

    def stop(self):
        self.__status = ClbTest.Status.NOT_CHECKED
        self.wait_cooler_timer.stop()

        self.setpoint_variable.set(self.prev_setpoint)

    def tick(self):
        if self.speed_variable == 0:
            self.wait_cooler_timer.start()
        else:
            if self.wait_cooler_timer.check():
                self.__status = ClbTest.Status.SUCCESS

    def status(self) -> ClbTest.Status:
        return self.__status

    def timeout(self) -> float:
        return self.__timeout_s

    def has_error(self) -> bool:
        return ClbTest.does_calibrator_has_error(self.netvars)

    def get_last_error(self) -> str:
        return ClbTest.get_calibrator_last_error(self.netvars)






class EmptyTest(ClbTest):
    def __init__(self):
        super().__init__()
        self.__status = ClbTest.Status.NOT_CHECKED

    def prepare(self) -> bool:
        return True

    def start(self):
        pass

    def stop(self):
        pass

    def tick(self):
        self.__status = ClbTest.Status.SUCCESS

    def status(self):
        return self.__status

    def timeout(self) -> float:
        return 0

    def has_error(self) -> bool:
        return True

    def get_last_error(self) -> str:
        return "Пустой тест"
