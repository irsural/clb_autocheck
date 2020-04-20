import abc
from enum import IntEnum
from typing import Dict

from network_variables import NetworkVariables, BufferedVariable
import calibrator_constants as clb


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

        try:
            error_msg += clb.error_code_to_message[error_code]
        except KeyError:
            error_msg += "Незарегистрированная ошибка"

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
