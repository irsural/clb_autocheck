import abc
from enum import IntEnum
import utils

import calibrator_constants as clb
from clb_dll import ClbDrv


class ClbTest(abc.ABC):
    class Status(IntEnum):
        NOT_CHECKED = 0
        IN_PROCESS = 1
        FAIL = 2
        SUCCESS = 3

    @abc.abstractmethod
    def prepare(self) -> bool:
        pass

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass

    @abc.abstractmethod
    def tick(self):
        pass

    @abc.abstractmethod
    def status(self) -> Status:
        pass


class SignalTest(ClbTest):
    def __init__(self, a_amplitude: float, a_signal_type: clb.SignalType, a_calibrator: ClbDrv,
                 a_hold_signal_timeout_s: int = 10, a_timeout_s: int = 30, a_log=None):
        super().__init__()
        self.amplitude = a_amplitude
        self.signal_type = a_signal_type
        self.calibrator = a_calibrator
        self.timeout_s = a_timeout_s
        self.log = a_log

        self.timeout_timer = utils.Timer(a_timeout_s)
        self.hold_signal_timer = utils.Timer(a_hold_signal_timeout_s)
        self.__status = ClbTest.Status.NOT_CHECKED

    def prepare(self) -> bool:
        if clb.is_ac_signal[self.signal_type]:
            # Замкнуть клеммы
            pass

        if self.calibrator.amplitude == self.amplitude and self.calibrator.signal_type == self.signal_type and \
                not self.calibrator.signal_enable:
            return True
        else:
            self.calibrator.amplitude = self.amplitude
            self.calibrator.signal_type = self.signal_type
            self.calibrator.signal_enable = False
            return False

    def start(self):
        self.__status = ClbTest.Status.IN_PROCESS
        self.calibrator.signal_type = True
        self.timeout_timer.start()

    def stop(self):
        self.calibrator.signal_type = False
        self.timeout_timer.stop()

    def tick(self):
        if not self.timeout_timer.check():
            if self.calibrator.state in (clb.State.WAITING_SIGNAL, clb.State.READY):
                if self.calibrator.state == clb.State.WAITING_SIGNAL:
                    self.hold_signal_timer.start()
                else:
                    if self.hold_signal_timer.check():
                        self.__status = ClbTest.Status.SUCCESS
            else:
                self.__status = ClbTest.Status.FAIL
        else:
            self.__status = ClbTest.Status.FAIL

    def status(self) -> ClbTest.Status:
        return self.__status
