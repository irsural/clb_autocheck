from sys import float_info
import logging

from network_variables_database import NetvarsDatabase
from network_variables import BufferedVariable
from clb_tests.tests_base import ClbTest
from clb_dll import ClbDrv

import utils


class EepromVariablesTest(ClbTest):
    def __init__(self, a_netvars_db: NetvarsDatabase, a_calibrator: ClbDrv, a_timeout_s: int = 30):
        super().__init__()

        self.netvars_db = a_netvars_db
        self.calibrator = a_calibrator
        self.__timeout_s = a_timeout_s

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
        for variable, _min, _max, _default in self.netvars_db.get_variables():
            value_from_clb = BufferedVariable(variable, BufferedVariable.Mode.R, self.calibrator).get()
            if variable.type == "double":
                match_default = abs(value_from_clb - _default) < float_info.epsilon
            elif variable.index == 1098:
                # Это переменная id, у нее особый обработчик
                match_default = True
            else:
                match_default = value_from_clb == _default

            if not match_default:
                self.error_message += f"Значение переменной {variable.name} = {value_from_clb} не соответствует " \
                                      f"значению по умолчанию '{utils.float_to_string(_default)}'\n"

            if _min != "" and value_from_clb < float(_min):
                self.error_message += f"Значение переменной {variable.name} = {value_from_clb} меньше минимально " \
                                      f"допустимого значения '{utils.float_to_string(_min)}'\n"
            if _max != "" and value_from_clb > float(_max):
                self.error_message += f"Значение переменной {variable.name} = {value_from_clb} больше максимально " \
                                      f"допустимого значения '{utils.float_to_string(_max)}'\n"

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
        return False
