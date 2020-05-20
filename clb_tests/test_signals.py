import logging

from network_variables import NetworkVariables
from clb_tests.tests_base import ClbTest
import calibrator_constants as clb
from clb_dll import ClbDrv
import utils


class SignalTest(ClbTest):
    def __init__(self, a_amplitude: float, a_signal_type: clb.SignalType, a_calibrator: ClbDrv,
                 a_netvars: NetworkVariables, a_hold_signal_timeout_s: int = 10, a_timeout_s: int = 30):
        super().__init__()
        self.amplitude = a_amplitude
        self.signal_type = a_signal_type
        self.calibrator = a_calibrator
        self.netvars = a_netvars
        self.__timeout_s = a_timeout_s

        self.hold_signal_timer = utils.Timer(a_hold_signal_timeout_s)
        self.__status = ClbTest.Status.NOT_CHECKED

    def prepare(self) -> bool:
        if not clb.is_voltage_signal[self.signal_type]:
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
        self.calibrator.signal_enable = True
        self.hold_signal_timer.start()

    def stop(self):
        self.__status = ClbTest.Status.NOT_CHECKED
        self.calibrator.signal_enable = False
        self.hold_signal_timer.stop()

    def tick(self):
        if self.calibrator.state in (clb.State.WAITING_SIGNAL, clb.State.READY):
            if self.calibrator.state == clb.State.WAITING_SIGNAL:
                self.hold_signal_timer.start()
            else:
                if self.hold_signal_timer.check():
                    self.__status = ClbTest.Status.SUCCESS
        else:
            logging.debug("Обнаружено выключение сигнала")
            self.__status = ClbTest.Status.FAIL

    def status(self) -> ClbTest.Status:
        return self.__status

    def timeout(self) -> float:
        return self.__timeout_s

    def has_error(self) -> bool:
        return ClbTest.does_calibrator_has_error(self.netvars)

    def get_last_error(self) -> str:
        return ClbTest.get_calibrator_last_error(self.netvars)

    def abort_on_fail(self) -> bool:
        return False
