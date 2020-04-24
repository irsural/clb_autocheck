from enum import IntEnum
import logging

from network_variables import NetworkVariables
from clb_tests.tests_base import ClbTest
import utils


class PeltierTest(ClbTest):
    class PeltierNumber(IntEnum):
        FIRST = 0
        SECOND = 1
        THIRD = 2
        FOURTH = 3

    class Stage(IntEnum):
        TEMP_UP = 0
        WAIT_TEMP_UP = 1
        TEMP_DOWN = 2
        WAIT_TEMP_DOWN = 3
        DONE = 4

    def __init__(self, a_peltier_number: PeltierNumber, a_netvars: NetworkVariables,
                 a_wait_peltier_timeout_s: int = 10, a_timeout_s: int = 30):
        super().__init__()

        if a_peltier_number == PeltierTest.PeltierNumber.FIRST:
            self.temp_setpoint = a_netvars.peltier_1_temperature_setpoint
            self.temp_max = a_netvars.peltier_1_temperature_max
            self.current_temp = a_netvars.peltier_1_temperature
            self.polarity_pin = a_netvars.peltier_1_polarity_pin
            self.is_peltier_ready = a_netvars.peltier_1_ready
        elif a_peltier_number == PeltierTest.PeltierNumber.SECOND:
            self.temp_setpoint = a_netvars.peltier_2_temperature_setpoint
            self.temp_max = a_netvars.peltier_2_temperature_max
            self.current_temp = a_netvars.peltier_2_temperature
            self.polarity_pin = a_netvars.peltier_2_polarity_pin
            self.is_peltier_ready = a_netvars.peltier_2_ready
        elif a_peltier_number == PeltierTest.PeltierNumber.THIRD:
            self.temp_setpoint = a_netvars.peltier_3_temperature_setpoint
            self.temp_max = a_netvars.peltier_3_temperature_max
            self.current_temp = a_netvars.peltier_3_temperature
            self.polarity_pin = a_netvars.peltier_3_polarity_pin
            self.is_peltier_ready = a_netvars.peltier_3_ready
        else: # a_peltier_number == PeltierTest.PeltierNumber.FOUTH
            self.temp_setpoint = a_netvars.peltier_4_temperature_setpoint
            self.temp_max = a_netvars.peltier_4_temperature_max
            self.current_temp = a_netvars.peltier_4_temperature
            self.polarity_pin = a_netvars.peltier_4_polarity_pin
            self.is_peltier_ready = a_netvars.peltier_4_ready

        self.setpoint_shift = 5
        self.prev_setpoint = self.temp_setpoint.get()
        self.start_temp = self.current_temp.get()
        self.expected_temp = 0
        self.error_message = ""

        self.temp_has_not_changes_window_percent = 5
        self.wrong_polarity_window_percents = 5

        self.netvars = a_netvars
        self.__timeout_s = a_timeout_s

        self.wait_peltier_timer = utils.Timer(a_wait_peltier_timeout_s)
        self.__status = ClbTest.Status.NOT_CHECKED
        self.__stage = PeltierTest.Stage.TEMP_UP

    def prepare(self) -> bool:
        return True

    def start(self):
        self.__status = ClbTest.Status.IN_PROCESS
        self.prev_setpoint = self.temp_setpoint.get()

    def stop(self):
        self.__status = ClbTest.Status.NOT_CHECKED
        self.wait_peltier_timer.stop()
        self.error_message = ""

        self.__stage = PeltierTest.Stage.TEMP_UP
        self.temp_setpoint.set(self.prev_setpoint)

    def tick(self):
        if self.__stage in (PeltierTest.Stage.TEMP_UP, PeltierTest.Stage.TEMP_DOWN):
            logging.debug(f"Stage {self.__stage.name}")

            self.start_temp = self.current_temp.get()
            self.expected_temp = self.start_temp + self.setpoint_shift \
                if self.__stage == PeltierTest.Stage.TEMP_UP else self.start_temp - self.setpoint_shift

            self.temp_setpoint.set(self.expected_temp)
            # Чтобы тесты не проходили успешно еще до изменения уставки
            self.is_peltier_ready.set(0)

            self.wait_peltier_timer.start()
            self.__stage = PeltierTest.Stage.WAIT_TEMP_UP if self.__stage == PeltierTest.Stage.TEMP_UP \
                else PeltierTest.Stage.WAIT_TEMP_DOWN

        elif self.__stage in (PeltierTest.Stage.WAIT_TEMP_UP, PeltierTest.Stage.WAIT_TEMP_DOWN):
            if self.is_peltier_ready.get() != 0:
                logging.debug(f"Stage {self.__stage.name}. Success.")
                self.__stage = PeltierTest.Stage.TEMP_DOWN if self.__stage == PeltierTest.Stage.WAIT_TEMP_UP \
                    else PeltierTest.Stage.DONE
            elif self.wait_peltier_timer.check():
                logging.debug(f"Stage {self.__stage.name}. Bad.")

                current_temp = self.current_temp.get()
                logging.debug(f"Stage {self.__stage.name}. Peltier timeout.")
                self.error_message += f"Не удалось выйти на уставку {self.expected_temp}. " \
                                      f"Измеренное значение {current_temp}.\n"
                if not self.__is_temperature_changed(current_temp, self.expected_temp):
                    logging.debug(f"Stage {self.__stage.name}. Broken.")
                    self.error_message += "Пельтье сломано\n"
                elif self.__is_wrong_polarity(self.start_temp, current_temp, self.expected_temp):
                    logging.debug(f"Stage {self.__stage.name}. Wrong polarity.")
                    self.polarity_pin.set(int(not self.polarity_pin.get()))
                    self.error_message += "Установлена неверная полярность\n" \
                                          "Полярность была изменена. Повторите тест\n"
                else:
                    logging.debug(f"Stage {self.__stage.name}. Timeout.")
                    self.error_message += "Истек таймаут"

                self.__stage = PeltierTest.Stage.TEMP_DOWN if self.__stage == PeltierTest.Stage.WAIT_TEMP_UP \
                    else PeltierTest.Stage.DONE

        elif self.__stage == PeltierTest.Stage.DONE:
            logging.debug(f"Stage {self.__stage.name}. Done.")

            if not self.error_message:
                self.__status = ClbTest.Status.SUCCESS
            else:
                self.__status = ClbTest.Status.FAIL

    def __is_temperature_changed(self, a_current_temp: float, a_expected_temp: float):
        return abs((a_expected_temp - a_current_temp) / a_current_temp * 100) < self.temp_has_not_changes_window_percent

    def __is_wrong_polarity(self, a_start_temp: float, a_current_temp: float, a_expected_temp: float):
        increase_is_expected = (a_expected_temp - a_start_temp) > 0

        if increase_is_expected:
            return ((a_start_temp - a_current_temp) / a_start_temp * 100) > self.wrong_polarity_window_percents
        else:
            return ((a_current_temp - a_start_temp) / a_start_temp * 100) > self.wrong_polarity_window_percents

    def status(self) -> ClbTest.Status:
        return self.__status

    def timeout(self) -> float:
        return self.__timeout_s

    def has_error(self) -> bool:
        return bool(self.error_message)

    def get_last_error(self) -> str:
        return self.error_message