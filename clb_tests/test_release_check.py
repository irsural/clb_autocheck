from irspy.clb.network_variables import NetworkVariables
from clb_tests.tests_base import ClbTest


class ReleaseCheckTest(ClbTest):

    def __init__(self, a_netvars: NetworkVariables, a_timeout_s: int = 30):
        super().__init__()

        self.netvars = a_netvars
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
        if self.netvars.release_firmware.get() == 0:
            self.error_message += f"Используется DEBUG версия прошивки!\n"

        if self.netvars.has_correction.get() == 0:
            self.error_message += f"Обнаружены пустые массивы коррекции!\n"

        if self.netvars.ui_correct_off.get() == 1:
            self.error_message += f"Коррекция отключена!\n"

        if self.netvars.use_eeprom_instead_of_sd_for_correct.get() == 0:
            self.error_message += f"Для хранения коррекции используется SD карта!\n"

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
