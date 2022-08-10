from enum import IntEnum
import logging

from irspy.clb.network_variables import NetworkVariables
from clb_tests.tests_base import ClbTest
from irspy import utils


class CoolerTest(ClbTest):
    class CoolerLocation(IntEnum):
        MAIN_BOARD = 0
        TRANSISTOR_DC = 1

    COOLER_LOCATION_TO_TEXT = {
        CoolerLocation.MAIN_BOARD: "Основная плата",
        CoolerLocation.TRANSISTOR_DC: "Транзистор DC"
    }

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
        if self.speed_variable.get() == 0:
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

    def abort_on_fail(self) -> bool:
        return False
