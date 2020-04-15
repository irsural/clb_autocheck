import abc
from enum import IntEnum
import utils
import logging

from network_variables import NetworkVariables
import calibrator_constants as clb
from clb_dll import ClbDrv


class ClbTest(abc.ABC):
    class Status(IntEnum):
        NOT_CHECKED = 0
        IN_PROCESS = 1
        FAIL = 2
        SUCCESS = 3

    @staticmethod
    def does_calibrator_has_error(a_netvars: NetworkVariables) -> bool:
        return a_netvars.error_occurred

    @staticmethod
    def get_calibrator_last_error(a_netvars: NetworkVariables) -> str:
        error_code = a_netvars.error_code
        error_count = a_netvars.error_count
        error_index = a_netvars.error_index
        error_msg = f"({error_index + 1} из {error_count}). "

        if error_code == 257:
            error_msg += "Перегрев аналоговой платы"
        elif error_code == 258:
            error_msg += "Перегрев платы питания"
        elif error_code == 259:
            error_msg += "Перегрев транзистора постоянного тока 10 А"
        elif error_code == 260:
            error_msg += "Перегрев элемента Пельтье №1"
        elif error_code == 261:
            error_msg += "Перегрев элемента Пельтье №2"
        elif error_code == 262:
            error_msg += "Перегрев элемента Пельтье №3"
        elif error_code == 263:
            error_msg += "Перегрев элемента Пельтье №4"
        elif error_code == 4104:
            error_msg += "Нестабильное напряжение на стабилизаторе 12 В"
        elif error_code == 4105:
            error_msg += "Нестабильное напряжение на стабилизаторе 9 В"
        elif error_code == 4106:
            error_msg += "Нестабильное напряжение на стабилизаторе 5 В"
        elif error_code == 4107:
            error_msg += "Нестабильное напряжение на стабилизаторе +2,5 В"
        elif error_code == 4108:
            error_msg += "Нестабильное напряжение на стабилизаторе -2,5 В"
        elif error_code == 4109:
            error_msg += "Нестабильное напряжение на источнике питания вентиляторов"
        elif error_code == 4110:
            error_msg += "Стабилизатор 4 В не вышел на режим"
        elif error_code == 4111:
            error_msg += "Стабилизатор 45 В не вышел на режим"
        elif error_code == 4112:
            error_msg += "Стабилизатор 650 В не вышел на режим"
        elif error_code == 4113:
            error_msg += "Не удалось выйти на режим"
        elif error_code == 4114:
            error_msg += "Не удалось выйти на режим, слишком большое сопротивление"
        elif error_code == 4115:
            error_msg += "Превышение тока"
        elif error_code == 4116:
            error_msg += "Не удалось выделить память"
        elif error_code == 4117:
            error_msg += "Сторожевой таймер перезагрузил установку"
        elif error_code == 4118:
            error_msg += "Ошибка при чтении основных настроек"
        elif error_code == 4119:
            error_msg += "Слишком много ошибок"
        elif error_code == 4120:
            error_msg += "Сброс EEPROM Пельтье 4"
        elif error_code == 4121:
            error_msg += "Слишком низкое сопротивление нагрузки. Прибор не может выйти на режим"
        elif error_code == 4122:
            error_msg += "Обнаружено короткое замыкание"
        elif error_code == 129:
            error_msg += "SD карта не обнаружена. Калибровка прибора нарушена"
        elif error_code == 140:
            error_msg += "Не удалось смонтировать файловую систему. Калибровка прибора нарушена"
        else:
            error_msg += f"Незарегистрированная ошибка (Код {error_code})"

        a_netvars.clear_error_occurred_status = 1
        return error_msg

    @abc.abstractmethod
    def __init__(self):
        self.__group = ""
        self.__name = ""

    def set_group(self, a_group: str):
        self.__group = a_group

    def group(self) -> str:
        return self.__group

    def set_name(self, a_name: str):
        self.__name = a_name

    def name(self) -> str:
        return self.__name

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

    @abc.abstractmethod
    def timeout(self) -> float:
        pass

    @abc.abstractmethod
    def has_error(self) -> bool:
        pass

    @abc.abstractmethod
    def get_last_error(self) -> str:
        pass


class SignalTest(ClbTest):
    def __init__(self, a_amplitude: float, a_signal_type: clb.SignalType, a_calibrator: ClbDrv,
                 a_netvars: NetworkVariables, a_hold_signal_timeout_s: int = 10, a_timeout_s: int = 30):
        super().__init__()
        self.amplitude = a_amplitude
        self.signal_type = a_signal_type
        self.calibrator = a_calibrator
        self.netvars = a_netvars
        self.__timeout_s = a_timeout_s

        self.timeout_timer = utils.Timer(a_timeout_s)
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
        self.timeout_timer.start()
        self.hold_signal_timer.start()

    def stop(self):
        self.__status = ClbTest.Status.NOT_CHECKED
        self.calibrator.signal_enable = False
        self.timeout_timer.stop()
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


class EmptyTest(ClbTest):
    def __init__(self):
        super().__init__()
        self.__status = ClbTest.Status.NOT_CHECKED

    def prepare(self) -> bool:
        return True

    def start(self):
        pass

    def stop(self):
        pass

    def tick(self):
        self.__status = ClbTest.Status.SUCCESS

    def status(self):
        return self.__status

    def timeout(self) -> float:
        return 0

    def has_error(self) -> bool:
        return True

    def get_last_error(self) -> str:
        return "Пустой тест"
