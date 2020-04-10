from typing import List, Tuple
import logging
from PyQt5 import QtCore

import clb_tests
import utils


class TestsConductor(QtCore.QObject):
    test_status_changed = QtCore.pyqtSignal(str, clb_tests.ClbTest.Status)
    tests_done = QtCore.pyqtSignal()

    def __init__(self, a_tests: List[clb_tests.ClbTest], a_test_repeat_count: int = 1):
        super().__init__()

        self.test_repeat_count = a_test_repeat_count

        self.tests = a_tests

        self.enabled_tests = []
        self.prepare_timer = utils.Timer(1.5)
        self.timeout_timer = utils.Timer(30)

        self.__started = False
        self.current_test_idx = 0

    def set_enabled_tests(self, a_enabled_tests: List[str]):
        self.enabled_tests = a_enabled_tests

    def start(self):
        self.current_test_idx = 0
        if self.find_enabled_test():
            self.__started = True
            self.next_test()
        else:
            self.stop()
            self.tests_done.emit()

    def stop(self):
        if self.current_test_idx < len(self.tests):
            self.tests[self.current_test_idx].stop()

        self.__started = False
        self.current_test_idx = 0
        self.prepare_timer.stop()
        self.timeout_timer.stop()

    def find_enabled_test(self):
        if self.current_test_idx >= len(self.tests):
            return False

        while not ((self.tests[self.current_test_idx].group(), self.tests[self.current_test_idx].name()) in
                   self.enabled_tests):
            # logging.debug(f"----------------------------------------------------")
            # logging.debug(f'ТЕСТ "{self.tests[self.current_test_idx].group()}: '
            #               f'{self.tests[self.current_test_idx].name()}" отключен, пропускаем')
            self.current_test_idx += 1

            if self.current_test_idx >= len(self.tests):
                return False
        return True

    def next_test(self):
        try:
            if self.find_enabled_test():
                current_test = self.tests[self.current_test_idx]
                logging.debug(f"----------------------------------------------------")
                logging.debug(f'ТЕСТ "{current_test.group()}: {current_test.name()}" старт')
                self.prepare_timer.start()
                self.timeout_timer.start(current_test.timeout())
                self.test_status_changed.emit(current_test.name(), clb_tests.ClbTest.Status.IN_PROCESS)
            else:
                self.stop()
                self.tests_done.emit()
        except Exception as err:
            print(utils.exception_handler(err))

    def tick(self):
        if self.__started:
            current_test = self.tests[self.current_test_idx]

            if not self.timeout_timer.check():
                if current_test.status() == clb_tests.ClbTest.Status.NOT_CHECKED:
                    if self.prepare_timer.check():
                        if current_test.prepare():
                            logging.debug(f"Успешная подготовка")
                            current_test.start()
                        else:
                            self.prepare_timer.start()

                elif current_test.status() == clb_tests.ClbTest.Status.IN_PROCESS:
                    current_test.tick()

                elif current_test.status() in (clb_tests.ClbTest.Status.SUCCESS, clb_tests.ClbTest.Status.FAIL):
                    logging.info(f'ТЕСТ "{current_test.group()}: {current_test.name()}" '
                                 f'результат {current_test.status().name}')

                    self.test_status_changed.emit(current_test.name(), current_test.status())
                    current_test.stop()
                    self.current_test_idx += 1
                    self.next_test()
            else:
                logging.info(f'ТЕСТ "{current_test.group()}: {current_test.name()}" TIMEOUT')

                self.test_status_changed.emit(current_test.name(), clb_tests.ClbTest.Status.FAIL)
                current_test.stop()
                self.current_test_idx += 1
                self.next_test()

    def started(self):
        return self.__started
