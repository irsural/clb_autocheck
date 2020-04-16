from typing import List, Tuple
import logging
from PyQt5 import QtCore

import clb_tests_base
import utils


class TestResults:
    def __init__(self):
        self.statuses = []

    def add_result(self, a_status: clb_tests_base.ClbTest.Status):
        self.statuses.append(a_status)

    def reset_results(self):
        self.statuses = []

    def get_final_status(self) -> clb_tests_base.ClbTest.Status:
        if not self.statuses:
            return clb_tests_base.ClbTest.Status.NOT_CHECKED

        for status in self.statuses:
            assert status not in (clb_tests_base.ClbTest.Status.IN_PROCESS, clb_tests_base.ClbTest.Status.NOT_CHECKED)
            if status == clb_tests_base.ClbTest.Status.FAIL:
                return clb_tests_base.ClbTest.Status.FAIL
        return clb_tests_base.ClbTest.Status.SUCCESS

    def get_results_count(self) -> int:
        return len(self.statuses)

    def get_success_results_count(self) -> int:
        return self.statuses.count(clb_tests_base.ClbTest.Status.SUCCESS)


class TestsConductor(QtCore.QObject):
    test_status_changed = QtCore.pyqtSignal(str, str, clb_tests_base.ClbTest.Status, int)
    tests_done = QtCore.pyqtSignal()

    def __init__(self, a_tests: List[clb_tests_base.ClbTest]):
        super().__init__()

        self.tests = a_tests
        self.test_results = [TestResults()] * len(self.tests)

        self.enabled_tests = []
        self.prepare_timer = utils.Timer(1.5)
        self.timeout_timer = utils.Timer(30)

        self.__started = False
        self.current_test_idx = 0

    def set_enabled_tests(self, a_enabled_tests: List[int]):
        self.enabled_tests = a_enabled_tests

    def start(self):
        self.current_test_idx = 0
        if self.find_enabled_test():
            self.__started = True
            self.next_test(a_first_test=True)
        else:
            self.stop()
            self.tests_done.emit()

    def stop(self):
        if self.current_test_idx < len(self.tests):
            # Если тест прервали до его окончания
            self.tests[self.current_test_idx].stop()
            self.test_status_changed.emit(self.tests[self.current_test_idx].group(),
                                          self.tests[self.current_test_idx].name(),
                                          self.test_results[self.current_test_idx].get_final_status(),
                                          self.test_results[self.current_test_idx].get_success_results_count())

        self.__started = False
        self.current_test_idx = 0
        self.prepare_timer.stop()
        self.timeout_timer.stop()

    def find_enabled_test(self):
        if self.current_test_idx >= len(self.tests):
            return False

        while not (self.enabled_tests[self.current_test_idx] > 0):
            self.current_test_idx += 1

            if self.current_test_idx >= len(self.tests):
                return False

        return True

    def next_test(self, a_first_test):
        try:
            reset_status = False
            if not a_first_test:
                if self.enabled_tests[self.current_test_idx] <= 0:
                    self.test_status_changed.emit(self.tests[self.current_test_idx].group(),
                                                  self.tests[self.current_test_idx].name(),
                                                  self.test_results[self.current_test_idx].get_final_status(),
                                                  self.test_results[self.current_test_idx].get_success_results_count())
                    self.current_test_idx += 1
                    reset_status = True
            else:
                reset_status = True

            if self.find_enabled_test():
                self.enabled_tests[self.current_test_idx] -= 1
                current_test = self.tests[self.current_test_idx]
                logging.debug(f"----------------------------------------------------")
                logging.debug(f'ТЕСТ "{current_test.group()}: {current_test.name()}" старт')
                self.prepare_timer.start()
                self.timeout_timer.start(current_test.timeout())

                if reset_status:
                    self.test_results[self.current_test_idx].reset_results()

                self.test_status_changed.emit(current_test.group(), current_test.name(),
                                              clb_tests_base.ClbTest.Status.IN_PROCESS,
                                              self.test_results[self.current_test_idx].get_success_results_count())
            else:
                self.stop()
                self.tests_done.emit()
        except Exception as err:
            logging.debug(utils.exception_handler(err))

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

                    self.test_results[self.current_test_idx].add_result(current_test.status())
                    current_test.stop()
                    self.next_test(a_first_test=False)
            else:
                logging.warning(f'ТЕСТ "{current_test.group()}: {current_test.name()}" TIMEOUT')
                if current_test.has_error():
                    logging.warning(f'ТЕСТ "{current_test.group()}: {current_test.name()}" ' 
                                    f'Ошибка: {current_test.get_last_error()}')

                self.test_results[self.current_test_idx].add_result(clb_tests_base.ClbTest.Status.FAIL)
                current_test.stop()
                self.next_test(a_first_test=False)

    def started(self):
        return self.__started
