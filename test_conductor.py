from typing import List, Tuple
import logging
from PyQt5 import QtCore

import clb_tests_base
import utils


class TestsConductor(QtCore.QObject):
    test_status_changed = QtCore.pyqtSignal(str, str, clb_tests_base.ClbTest.Status)
    tests_done = QtCore.pyqtSignal()

    def __init__(self, a_tests: List[clb_tests_base.ClbTest]):
        super().__init__()

        self.tests = a_tests

        self.enabled_tests = []
        self.prepare_timer = utils.Timer(1.5)
        self.timeout_timer = utils.Timer(30)

        self.__started = False
        self.current_test_idx = 0

    def set_enabled_tests(self, a_enabled_tests: List[Tuple[str, str]]):
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
            self.test_status_changed.emit(self.tests[self.current_test_idx].group(),
                                          self.tests[self.current_test_idx].name(),
                                          self.tests[self.current_test_idx].status())
        self.__started = False
        self.current_test_idx = 0
        self.prepare_timer.stop()
        self.timeout_timer.stop()

    def find_enabled_test(self):
        if self.current_test_idx >= len(self.tests):
            return False

        while not ((self.tests[self.current_test_idx].group(), self.tests[self.current_test_idx].name()) in
                   self.enabled_tests):
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
                self.test_status_changed.emit(current_test.group(), current_test.name(),
                                              clb_tests_base.ClbTest.Status.IN_PROCESS)
            else:
                self.stop()
                self.tests_done.emit()
        except Exception as err:
            print(utils.exception_handler(err))

    def tick(self):
        if self.__started:
            current_test = self.tests[self.current_test_idx]

            if not self.timeout_timer.check():
                if current_test.status() == clb_tests_base.ClbTest.Status.NOT_CHECKED:
                    if self.prepare_timer.check():
                        if current_test.prepare():
                            logging.debug(f"Успешная подготовка")
                            current_test.start()
                        else:
                            self.prepare_timer.start()

                elif current_test.status() == clb_tests_base.ClbTest.Status.IN_PROCESS:
                    current_test.tick()

                elif current_test.status() in (clb_tests_base.ClbTest.Status.SUCCESS,
                                               clb_tests_base.ClbTest.Status.FAIL):
                    logging.info(f'ТЕСТ "{current_test.group()}: {current_test.name()}" '
                                 f'результат {current_test.status().name}')
                    if current_test.has_error():
                        logging.warning(f'ТЕСТ "{current_test.group()}: {current_test.name()}" ' 
                                        f'Ошибка: {current_test.get_last_error()}')

                    self.test_status_changed.emit(current_test.group(), current_test.name(), current_test.status())
                    current_test.stop()
                    self.current_test_idx += 1
                    self.next_test()
            else:
                logging.warning(f'ТЕСТ "{current_test.group()}: {current_test.name()}" TIMEOUT')
                if current_test.has_error():
                    logging.warning(f'ТЕСТ "{current_test.group()}: {current_test.name()}" ' 
                                    f'Ошибка: {current_test.get_last_error()}')

                self.test_status_changed.emit(current_test.group(), current_test.name(),
                                              clb_tests_base.ClbTest.Status.FAIL)
                current_test.stop()
                self.current_test_idx += 1
                self.next_test()

    def started(self):
        return self.__started
