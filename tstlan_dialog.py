import re
from enum import IntEnum

from PyQt5 import QtGui, QtWidgets, QtCore

from ui.py.tstlan_dialog import Ui_Dialog as TstlanForm
from settings_ini_parser import Settings
import calibrator_constants as clb


class VariableInfo:
    def __init__(self, a_number=0, a_index=0, a_name="", a_type="", a_bit_idx=0):
        self.number = a_number
        self.index = a_index
        self.name = a_name
        self.type = a_type
        self.bit_index = a_bit_idx

    def __str__(self):
        return f"{self.number}, {self.index}, {self.bit_index}, {self.name}, {self.type}"


class TstlanDialog(QtWidgets.QDialog):
    class Column(IntEnum):
        NUMBER = 0
        INDEX = 1
        NAME = 2
        TYPE = 3
        VALUE = 4

    CLB_CONFIG_PATH = "./Calibrator 2.ini"
    VARIABLE_RE = re.compile(r"^(?P<parameter>Name|Type)_(?P<number>\d+)=(?P<value>.*)")

    def __init__(self, a_settings: Settings, a_parent=None):
        super().__init__(a_parent)

        self.ui = TstlanForm()
        self.ui.setupUi(self)
        self.show()

        self.settings = a_settings
        self.restoreGeometry(self.settings.get_last_geometry(self.__class__.__name__))
        self.ui.variables_table.horizontalHeader().restoreState(self.settings.get_last_geometry(
            self.ui.variables_table.__class__.__name__))

        self.variables_info = []

        self.get_variables_from_ini(self.CLB_CONFIG_PATH)
        self.fill_variables_table()

    def __del__(self):
        print("tstlan deleted")

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

                    if number >= len(self.variables_info):
                        assert (number - len(self.variables_info)) < 1, \
                            f"Переменные в конфиге расположены не по порядку"
                        self.variables_info.append(VariableInfo(a_number=number))

                    if variable_re.group('parameter') == "Name":
                        self.variables_info[number].name = value
                    else:
                        self.variables_info[number].type = value

                        if number != 0:
                            current_var = self.variables_info[number]
                            prev_var = self.variables_info[number - 1]

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

    # noinspection PyTypeChecker
    def fill_variables_table(self):
        for row, variable in enumerate(self.variables_info):
            if variable.name:
                self.ui.variables_table.insertRow(row)
                index = variable.index if variable.type != "bit" else f"{variable.index}.{variable.bit_index}"

                item = NumberTableWidgetItem(f"{variable.number}")
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                self.ui.variables_table.setItem(row, self.Column.NUMBER, item)

                item = NumberTableWidgetItem(f"{index}")
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                self.ui.variables_table.setItem(row, self.Column.INDEX, item)

                item = QtWidgets.QTableWidgetItem(variable.name)
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                self.ui.variables_table.setItem(row, self.Column.NAME, item)

                item = QtWidgets.QTableWidgetItem(variable.type)
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                self.ui.variables_table.setItem(row, self.Column.TYPE, item)

    def closeEvent(self, a_event: QtGui.QCloseEvent) -> None:
        self.settings.save_geometry(self.ui.variables_table.__class__.__name__,
                                    self.ui.variables_table.horizontalHeader().saveState())
        self.settings.save_geometry(self.__class__.__name__, self.saveGeometry())
        a_event.accept()


class NumberTableWidgetItem(QtWidgets.QTableWidgetItem):
    def __lt__(self, other: QtWidgets.QTableWidgetItem):
        return float(self.text()) < float(other.text())
