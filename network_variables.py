import re
import struct
import logging
from typing import List
from clb_dll import ClbDrv

import utils


class VariableInfo:
    def __init__(self, a_number=0):
        self.number = a_number
        self.index = 0
        self.name = ""
        self.type = ""
        self.size = 0
        self.c_type = ""
        self.bit_index = 0

    def __str__(self):
        return f"{self.number}, {self.index}, {self.bit_index}, {self.name}, {self.type}"


class NetworkVariables:
    VARIABLE_RE = re.compile(r"^(?P<parameter>Name|Type)_(?P<number>\d+)=(?P<value>.*)")

    def __init__(self, a_variables_ini_path: str, a_calibrator: ClbDrv):
        self.__calibrator = a_calibrator
        self.__variables_info = self.get_variables_from_ini(a_variables_ini_path)

    @staticmethod
    def get_variables_from_ini(a_ini_path: str):
        variables_info = []
        with open(a_ini_path) as config:
            for line in config:
                variable_re = NetworkVariables.VARIABLE_RE.match(line)
                if variable_re is not None:
                    number = int(variable_re.group('number'))
                    value = variable_re.group('value')

                    if number >= len(variables_info):
                        assert (number - len(variables_info)) < 1, \
                            f"Переменные в конфиге расположены не по порядку"
                        variables_info.append(VariableInfo(a_number=number))

                    if variable_re.group('parameter') == "Name":
                        variables_info[number].name = value
                    else:
                        variables_info[number].type = value
                        variables_info[number].c_type = NetworkVariables.__get_c_type(value)
                        variables_info[number].size = NetworkVariables.get_type_size(value)

                        if number != 0:
                            current_var = variables_info[number]
                            prev_var = variables_info[number - 1]

                            if current_var.type == "bit":
                                if prev_var.type == "bit":
                                    if prev_var.bit_index == 7:
                                        current_var.index = prev_var.index + 1
                                        current_var.bit_index = 0
                                    else:
                                        current_var.index = prev_var.index
                                        current_var.bit_index = prev_var.bit_index + 1
                                else:
                                    current_var.index = prev_var.index + prev_var.size
                            else:
                                current_var.index = prev_var.index + prev_var.size
        return variables_info

    def get_variables_info(self) -> List[VariableInfo]:
        return self.__variables_info

    def get_data_size(self) -> int:
        return self.__variables_info[-1].index + self.__variables_info[-1].size

    def read_variable(self, a_variable_number: int):
        variable_info = self.__variables_info[a_variable_number]
        if variable_info.c_type == 'o':
            return self.__calibrator.read_bit(variable_info.index, variable_info.bit_index)
        else:
            _bytes = self.__calibrator.read_raw_bytes(variable_info.index, variable_info.size)
            return struct.unpack(variable_info.c_type, _bytes)[0]

    def write_variable(self, a_variable_number: int, a_variable_value: float):
        variable_info = self.__variables_info[a_variable_number]
        if variable_info.c_type == 'o':
            value = int(utils.bound(a_variable_value, 0, 1))
            return self.__calibrator.write_bit(variable_info.index, variable_info.bit_index, value)
        else:
            if variable_info.c_type != 'd' and variable_info.c_type != 'f':
                a_variable_value = int(a_variable_value)

            _bytes = struct.pack(variable_info.c_type, a_variable_value)
            self.__calibrator.write_raw_bytes(variable_info.index, variable_info.size, _bytes)

    @property
    def peltier_3_temperature(self) -> float:
        _bytes = self.__calibrator.read_raw_bytes(938, 8)
        return struct.unpack('d', _bytes)[0]

    @peltier_3_temperature.setter
    def peltier_3_temperature(self, a_value: float):
        _bytes = struct.pack('d', a_value)
        self.__calibrator.write_raw_bytes(938, 8, _bytes)

    @staticmethod
    def get_type_size(a_type_name: str):
        if a_type_name == "double":
            return 8
        elif a_type_name == "float":
            return 4
        elif "32" in a_type_name:
            return 4
        elif "16" in a_type_name:
            return 2
        elif "8" in a_type_name:
            return 1
        elif a_type_name == "bit":
            return 1
        elif a_type_name == "bool":
            return 1
        elif "64" in a_type_name:
            return 8
        elif "long" in a_type_name:
            return 10
        else:
            assert False, "Незарегистрированый тип"

    @staticmethod
    def __get_c_type(a_type_name: str):
        if a_type_name == "double":
            return 'd'
        elif a_type_name == "float":
            return 'f'
        elif a_type_name == "bit":
            # Используется как флаг
            return 'o'
        elif a_type_name == "u32":
            return 'I'
        elif a_type_name == "i32":
            return 'i'
        elif a_type_name == "u8":
            return 'B'
        elif a_type_name == "i8":
            return 'b'
        elif a_type_name == "u16":
            return 'H'
        elif a_type_name == "i16":
            return 'h'
        elif a_type_name == "bool":
            return 'B'
        elif a_type_name == "u64":
            return 'Q'
        elif a_type_name == "i64":
            return 'q'
        else:
            logging.debug(f"WARNING! Незарегистрированый тип '{a_type_name}'")
            return ''
