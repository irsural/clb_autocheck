from enum import IntEnum
import logging

from network_variables import NetworkVariables
from clb_tests.tests_base import ClbTest
import utils


class CablesTest(ClbTest):
    class CableLocation(IntEnum):
        FRONT = 0
        REAR = 1

    def __init__(self, a_netvars: NetworkVariables, a_timeout_s: int = 30):
        super().__init__()

        self.netvars = a_netvars
        self.__timeout_s = a_timeout_s

        self.temperature_min = 28
        self.temperature_max = 45

        self.dependent_variables = {
            "transistor_dc_10a_temperature": self.netvars.transistor_dc_10a_temperature,
            "peltier_1_temperature": self.netvars.peltier_1_temperature,
            "peltier_2_temperature": self.netvars.peltier_2_temperature,
            "peltier_3_temperature": self.netvars.peltier_3_temperature,
            "peltier_4_temperature": self.netvars.peltier_4_temperature
        }

        self.__status = ClbTest.Status.NOT_CHECKED
        self.error_message = ""

    def prepare(self) -> bool:
        return True

    def start(self):
        self.__status = ClbTest.Status.IN_PROCESS

    def stop(self):
        self.__status = ClbTest.Status.NOT_CHECKED
        self.error_message = ""

    def tick(self):
        for variable_name in self.dependent_variables.keys():
            value = self.dependent_variables[variable_name].get()
            if value < self.temperature_min or value > self.temperature_max:
                self.error_message += f"Переменная {variable_name} имеет странное значение {value}\n"
                logging.debug(f"Переменная {variable_name} имеет странное значение {value}\n")

        if not self.error_message:
            self.__status = ClbTest.Status.SUCCESS
        else:
            self.__status = ClbTest.Status.FAIL

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
