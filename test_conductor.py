from typing import List
import logging
from PyQt5.QtCore import pyqtSignal

import clb_tests
import calibrator_constants as clb
from clb_dll import ClbDrv
import utils


class TestsConductor:
    test_status_changed = pyqtSignal(int, clb_tests.ClbTest.Status)
    tests_done = pyqtSignal()

    def __init__(self, a_calibrator: ClbDrv,  a_test_repeat_count: int = 1):
        self.test_repeat_count = a_test_repeat_count

        self.tests = (
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
                                 a_calibrator=a_calibrator)
        )

        self.enabled_tests = [1] * len(self.tests)
        self.prepare_timer = utils.Timer(1.5)

        self.started = False
        self.current_test_idx = 0

    def set_enabled_tests(self, a_enabled_tests: List[bool]):
        assert len(self.enabled_tests) == len(a_enabled_tests)
        self.enabled_tests = a_enabled_tests

    def start(self):
        self.started = True
        self.prepare_timer.start()

    def stop(self):
        self.started = False
        self.current_test_idx = 0
        self.prepare_timer.stop()

    def next(self):
        while not self.enabled_tests[self.current_test_idx]:
            self.current_test_idx += 1
            if len(self.tests) == self.current_test_idx:
                self.stop()
                self.tests_done.emit()
                break

    def tick(self):
        if self.started:
            current_test = self.tests[self.current_test_idx]
            current_test.tick()

            if current_test.status() == clb_tests.ClbTest.Status.NOT_CHECKED:
                if self.prepare_timer.check():
                    if current_test.prepare():
                        logging.debug(f"test {self.current_test_idx} success prepare")
                        current_test.start()
                    else:
                        self.prepare_timer.start()
            elif current_test.status() in (clb_tests.ClbTest.Status.SUCCESS, clb_tests.ClbTest.Status.FAIL):
                logging.debug(f"test {self.current_test_idx} result {current_test.status().name}")
                current_test.stop()
                # self.test_status_changed.emit(self.current_test_idx, current_test.status())
                self.next()
