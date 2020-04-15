from enum import IntEnum
import logging
import struct
import re

import calibrator_constants as clb
from clb_dll import ClbDrv
import utils


class NetworkVariables:
    VARIABLE_RE = re.compile(r"^(?P<parameter>Name|Type)_(?P<number>\d+)=(?P<value>.*)")

    def __init__(self, a_variables_ini_path: str, a_calibrator: ClbDrv):
        self.__calibrator = a_calibrator
        self.__variables_info = self.get_variables_from_ini(a_variables_ini_path)

        # Обязательно объявлять через класс, а не через self, иначе не будут вызываться __get__ и __set__
        NetworkVariables.fast_adc_slow = BufferedVariable(VariableInfo(a_index=229, a_type="double"),
                                                          a_mode=BufferedVariable.Mode.R,
                                                          a_calibrator=self.__calibrator)

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

    def get_variables_info(self):
        return self.__variables_info

    def get_data_size(self) -> int:
        return self.__variables_info[-1].index + self.__variables_info[-1].size

    def connected(self):
        return self.__calibrator.state != clb.State.DISCONNECTED

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
            self.__calibrator.write_bit(variable_info.index, variable_info.bit_index, value)
        else:
            if variable_info.c_type != 'd' and variable_info.c_type != 'f':
                a_variable_value = int(a_variable_value)

            _bytes = struct.pack(variable_info.c_type, a_variable_value)
            self.__calibrator.write_raw_bytes(variable_info.index, variable_info.size, _bytes)


class VariableInfo:
    def __init__(self, a_number=0, a_index=0, a_bit_index=0, a_type="u32"):
        self.number = a_number
        self.index = a_index
        self.name = ""
        self.size = 0
        self.c_type = ""
        self.bit_index = a_bit_index

        self.__type = a_type
        self.type = self.__type

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, a_type: str):
        self.__type = a_type
        self.c_type = VariableInfo.__get_c_type(self.__type)
        self.size = VariableInfo.__get_type_size(self.__type)

    @staticmethod
    def __get_type_size(a_type_name: str):
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
            assert False, f"Незарегистрированый тип '{a_type_name}'"

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

    def __str__(self):
        return f"{self.number}, {self.index}, {self.bit_index}, {self.name}, {self.__type}"


class BufferedVariable:
    class Mode(IntEnum):
        R = 0
        RW = 1

    def __init__(self, a_variable_info: VariableInfo, a_mode: Mode, a_calibrator: ClbDrv, a_buffer_delay_s=1):
        assert a_variable_info.c_type != "", "variable must have a c_type"
        assert a_variable_info.type != "", "variable must have a type"
        assert a_variable_info.size != 0, "variable must have a non-zero size"

        self.__variable_info = a_variable_info
        self.__is_bit = True if a_variable_info.c_type == 'o' else False
        self.__mode = a_mode
        self.__calibrator = a_calibrator

        self.__buffer = 0
        self.__delay_timer = utils.Timer(a_buffer_delay_s)

    def __get(self):
        if self.__delay_timer.check() or not self.__delay_timer.started():
            if self.__is_bit:
                return self.__calibrator.read_bit(self.__variable_info.index, self.__variable_info.bit_index)
            else:
                _bytes = self.__calibrator.read_raw_bytes(self.__variable_info.index, self.__variable_info.size)
                return struct.unpack(self.__variable_info.c_type, _bytes)[0]
        else:
            return self.__buffer

    def __set(self, a_value):
        assert self.__mode == BufferedVariable.Mode.RW, "Режим переменной должен быть RW !!"

        if self.__is_bit:
            a_value = int(utils.bound(a_value, 0, 1))
            self.__calibrator.write_bit(self.__variable_info.index, self.__variable_info.bit_index, a_value)
        else:
            if self.__variable_info.c_type != 'd' and self.__variable_info.c_type != 'f':
                a_value = int(a_value)

            _bytes = struct.pack(self.__variable_info.c_type, a_value)
            self.__calibrator.write_raw_bytes(self.__variable_info.index, self.__variable_info.size, _bytes)

        self.__buffer = a_value
        self.__delay_timer.start()

    def __get__(self, instance, owner):
        return self.__get()

    def __set__(self, instance, value):
        return self.__set(value)
