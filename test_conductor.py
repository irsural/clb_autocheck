from typing import List
import logging
from PyQt5 import QtCore

import clb_tests
import calibrator_constants as clb
from clb_dll import ClbDrv
import utils


class TestsConductor(QtCore.QObject):
    test_status_changed = QtCore.pyqtSignal(int, clb_tests.ClbTest.Status)
    tests_done = QtCore.pyqtSignal()

    def __init__(self, a_calibrator: ClbDrv,  a_test_repeat_count: int = 1):
        super().__init__()

        self.test_repeat_count = a_test_repeat_count

        self.tests = (
            clb_tests.EmptyTest(),
            clb_tests.EmptyTest(),
            clb_tests.EmptyTest(),
            clb_tests.EmptyTest(),
            clb_tests.EmptyTest(),
            clb_tests.EmptyTest(),
            clb_tests.EmptyTest(),
            clb_tests.EmptyTest(),
            clb_tests.EmptyTest(),
            clb_tests.EmptyTest(),
            clb_tests.SignalTest(a_amplitude=20*(10**-3),
                                 a_signal_type=clb.SignalType.DCV,
                                 a_calibrator=a_calibrator),
            clb_tests.SignalTest(a_amplitude=4,
                                 a_signal_type=clb.SignalType.DCV,
                                 a_calibrator=a_calibrator),
            clb_tests.SignalTest(a_amplitude=43,
                                 a_signal_type=clb.SignalType.DCV,
                                 a_calibrator=a_calibrator),
            clb_tests.SignalTest(a_amplitude=200,
                                 a_signal_type=clb.SignalType.DCV,
                                 a_calibrator=a_calibrator),
            clb_tests.EmptyTest(),
            clb_tests.EmptyTest(),
            clb_tests.EmptyTest(),
        )

        self.enabled_tests = [True] * len(self.tests)
        self.prepare_timer = utils.Timer(1.5)
        self.timeout_timer = utils.Timer(30)

        self.__started = False
        self.current_test_idx = 0

    def set_enabled_tests(self, a_enabled_tests: List[bool]):
        assert len(self.enabled_tests) == len(a_enabled_tests), "Количество тестов не совпадает с заданным"
        self.enabled_tests = a_enabled_tests

    def start(self):
        self.current_test_idx = 0
        if self.find_enabled_test():
            self.__started = True
            self.next_test()

    def stop(self):
        if self.current_test_idx < len(self.enabled_tests):
            self.tests[self.current_test_idx].stop()

        self.__started = False
        self.current_test_idx = 0
        self.prepare_timer.stop()
        self.timeout_timer.stop()

    def find_enabled_test(self):
        if self.current_test_idx >= len(self.enabled_tests):
            return False

        while not self.enabled_tests[self.current_test_idx]:
            logging.debug(f"ТЕСТ {self.current_test_idx} отключен, пропускаем")
            self.current_test_idx += 1

            if self.current_test_idx >= len(self.enabled_tests):
                return False
        return True

    def next_test(self):
        try:
            if self.find_enabled_test():
                logging.debug(f"----------------------------------------------------")
                logging.debug(f"Старт ТЕСТ {self.current_test_idx}")
                self.prepare_timer.start()
                self.timeout_timer.start(self.tests[self.current_test_idx].timeout())
                self.test_status_changed.emit(self.current_test_idx, clb_tests.ClbTest.Status.IN_PROCESS)
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
                            logging.debug(f"ТЕСТ {self.current_test_idx} успешная подготовка")
                            current_test.start()
                        else:
                            self.prepare_timer.start()

                elif current_test.status() == clb_tests.ClbTest.Status.IN_PROCESS:
                    current_test.tick()

                elif current_test.status() in (clb_tests.ClbTest.Status.SUCCESS, clb_tests.ClbTest.Status.FAIL):
                    logging.info(f"ТЕСТ {self.current_test_idx} результат {current_test.status().name}")

                    self.test_status_changed.emit(self.current_test_idx, current_test.status())
                    current_test.stop()
                    self.current_test_idx += 1
                    self.next_test()
            else:
                logging.info(f"ТЕСТ {self.current_test_idx} таймаут")

                self.test_status_changed.emit(self.current_test_idx, clb_tests.ClbTest.Status.FAIL)
                current_test.stop()
                self.current_test_idx += 1
                self.next_test()

    def started(self):
        return self.__started
