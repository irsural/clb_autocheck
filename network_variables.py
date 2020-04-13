import re


class VariableInfo:
    def __init__(self, a_number=0, a_index=0, a_name="", a_type="", a_bit_idx=0):
        self.number = a_number
        self.index = a_index
        self.name = a_name
        self.type = a_type
        self.bit_index = a_bit_idx

    def __str__(self):
        return f"{self.number}, {self.index}, {self.bit_index}, {self.name}, {self.type}"


class NetworkVariables:
    VARIABLE_RE = re.compile(r"^(?P<parameter>Name|Type)_(?P<number>\d+)=(?P<value>.*)")

    def __init__(self, a_variables_ini_path: str):
        self.__variables_info = []
        self.get_variables_from_ini(a_variables_ini_path)

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

    def get_variables_from_ini(self, a_ini_path: str):
        with open(a_ini_path) as config:
            for line in config:
                variable_re = self.VARIABLE_RE.match(line)
                if variable_re is not None:
                    number = int(variable_re.group('number'))
                    value = variable_re.group('value')

                    if number >= len(self.__variables_info):
                        assert (number - len(self.__variables_info)) < 1, \
                            f"Переменные в конфиге расположены не по порядку"
                        self.__variables_info.append(VariableInfo(a_number=number))

                    if variable_re.group('parameter') == "Name":
                        self.__variables_info[number].name = value
                    else:
                        self.__variables_info[number].type = value

                        if number != 0:
                            current_var = self.__variables_info[number]
                            prev_var = self.__variables_info[number - 1]

                            if current_var.type == "bit":
                                if prev_var.type == "bit":
                                    if prev_var.bit_index == 7:
                                        current_var.index = prev_var.index + 1
                                        current_var.bit_index = 0
                                    else:
                                        current_var.index = prev_var.index
                                        current_var.bit_index = prev_var.bit_index + 1
                                else:
                                    current_var.index = prev_var.index + self.get_type_size(prev_var.type)
                            else:
                                current_var.index = prev_var.index + self.get_type_size(prev_var.type)

    def get_variables_info(self):
        return self.__variables_info

    def read_variable(self, a_variable_number: int):
        return self.__variables_info[a_variable_number].name

    def write_variable(self, a_variable_number: int):
        pass
