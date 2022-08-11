import logging

from irspy.clb.network_variables import NetworkVariables
from clb_tests.tests_base import ClbTest
from irspy import utils


class SupplyVoltageTest(ClbTest):
    def __init__(self, a_netvars: NetworkVariables, a_success_timeout_s: int = 10, a_timeout_s: int = 30):
        super().__init__()

        self.netvars = a_netvars
        self.__timeout_s = a_timeout_s

        self.__status = ClbTest.Status.NOT_CHECKED

        self.voltages = (
            (self.netvars.inner_stabilizer_12v_voltage, 12., utils.Timer(a_success_timeout_s)),
            (self.netvars.inner_stabilizer_9v_voltage, 9., utils.Timer(a_success_timeout_s)),
            (self.netvars.inner_stabilizer_5v_voltage, 5., utils.Timer(a_success_timeout_s)),
            (self.netvars.inner_stabilizer_2_5v_pos_voltage, 2.5, utils.Timer(a_success_timeout_s)),
            (self.netvars.inner_stabilizer_2_5v_neg_voltage, -2.5, utils.Timer(a_success_timeout_s)),
            (self.netvars.cooling_power_supply_voltage, 12, utils.Timer(a_success_timeout_s))
        )
        self.allow_deviation_percents = 10

    def prepare(self) -> bool:
        return True

    def start(self):
        self.__status = ClbTest.Status.IN_PROCESS
        for voltage in self.voltages:
            voltage[2].start()

    def stop(self):
        self.__status = ClbTest.Status.NOT_CHECKED
        for voltage_info in self.voltages:
            voltage_info[2].start()

    def tick(self):
        all_voltages_are_ok = True
        for voltage_info in self.voltages:
            if (abs(voltage_info[0].get() - voltage_info[1]) / voltage_info[1] * 100) > self.allow_deviation_percents:
                voltage_info[2].start()
                all_voltages_are_ok = False
            else:
                if not voltage_info[2].check():
                    all_voltages_are_ok = False

        if all_voltages_are_ok:
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
        return True
