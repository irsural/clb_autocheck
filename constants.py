from enum import IntEnum
from typing import List

from calibrator_constants import SignalType, is_dc_signal


FLOAT_EPSILON = 1e-9
FIRST_POINT_START_DEVIATION_PERCENT = 15


class DeviceSystem(IntEnum):
    MAGNETOELECTRIC = 0
    ELECTRODYNAMIC = 1
    ELECTROMAGNETIC = 2


enum_to_device_system = {
    DeviceSystem.MAGNETOELECTRIC: "Магнитоэлектрическая",
    DeviceSystem.ELECTRODYNAMIC: "Электродинамическая",
    DeviceSystem.ELECTROMAGNETIC: "Электромагнитная",
}


class OperationDB(IntEnum):
    ADD = 0
    EDIT = 1


class Scale:
    class Limit:
        def __init__(self, a_id=0, a_limit: float = 1, a_device_class: float = 1,
                     a_signal_type: SignalType = SignalType.ACI, a_frequency: str = ""):
            self.id = a_id
            self.limit = a_limit
            self.device_class = a_device_class
            self.signal_type = a_signal_type

            if a_frequency is not None:
                self.frequency = a_frequency
            elif is_dc_signal[a_signal_type]:
                self.frequency = "0"
            else:
                self.frequency = "50"

        def __str__(self):
            return str(self.limit) + str(self.signal_type) + str(self.device_class)

    def __init__(self, a_id=0, a_number=1, a_scale_points: List[float] = None, a_limits: List[Limit] = None):
        self.id = a_id
        self.number = a_number
        self.points = a_scale_points if a_scale_points is not None else []
        self.limits = a_limits if a_limits is not None else [Scale.Limit()]

    def __str__(self):
        return "Points: {0}\nLimits: {1}".format(self.points, [str(lim) for lim in self.limits])
