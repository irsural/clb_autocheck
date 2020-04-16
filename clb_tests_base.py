import abc
from enum import IntEnum
from typing import List, Dict

from network_variables import NetworkVariables, BufferedVariable


class ClbTest(abc.ABC):
    class Status(IntEnum):
        NOT_CHECKED = 0
        IN_PROCESS = 1
        FAIL = 2
        SUCCESS = 3

    @staticmethod
    def does_calibrator_has_error(a_netvars: NetworkVariables) -> bool:
        return a_netvars.error_occurred.get()

    @staticmethod
    def get_calibrator_last_error(a_netvars: NetworkVariables) -> str:
        error_code = a_netvars.error_code.get()
        error_count = a_netvars.error_count.get()
        error_index = a_netvars.error_index.get()
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
            error_msg += f"Незарегистрированная ошибка"

        error_msg += f". Код {error_code}"

        a_netvars.clear_error_occurred_status.set(1)
        return error_msg

    @abc.abstractmethod
    def __init__(self):
        self.__group = ""
        self.__name = ""
        self.__variables_to_graph = {}

    def set_group(self, a_group: str):
        self.__group = a_group

    def group(self) -> str:
        return self.__group

    def set_name(self, a_name: str):
        self.__name = a_name

    def name(self) -> str:
        return self.__name

    def set_variables_to_graph(self, a_names: Dict[str, BufferedVariable]):
        self.__variables_to_graph = a_names

    def get_variables_to_graph(self) -> Dict[str, BufferedVariable]:
        return self.__variables_to_graph

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
