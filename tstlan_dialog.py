import logging
from enum import IntEnum

from PyQt5 import QtGui, QtWidgets, QtCore

from ui.py.tstlan_dialog import Ui_Dialog as TstlanForm
from settings_ini_parser import Settings
import network_variables as nv
import utils


class TstlanDialog(QtWidgets.QDialog):
    class Column(IntEnum):
        NUMBER = 0
        INDEX = 1
        NAME = 2
        TYPE = 3
        VALUE = 4

    def __init__(self, a_variables: nv.NetworkVariables, a_settings: Settings, a_parent=None):
        super().__init__(a_parent)

        self.ui = TstlanForm()
        self.ui.setupUi(self)
        self.show()

        self.netvars = a_variables

        self.settings = a_settings
        self.restoreGeometry(self.settings.get_last_geometry(self.__class__.__name__))
        self.ui.variables_table.horizontalHeader().restoreState(self.settings.get_last_geometry(
            self.ui.variables_table.__class__.__name__))

        self.fill_variables_table()

        self.read_variables_timer = QtCore.QTimer(self)
        # self.read_variables_timer.timeout.connect(self.read_variables)
        self.read_variables_timer.start(1000)

        # self.ui.variables_table.itemChanged.connect(self.write_variable)

    def __del__(self):
        print("tstlan deleted")

    # noinspection PyTypeChecker
    def fill_variables_table(self):
        for row, variable in enumerate(self.netvars.get_variables_info()):
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

                self.ui.variables_table.setItem(row, self.Column.VALUE, QtWidgets.QTableWidgetItem(""))

    def read_variables(self):
        self.ui.variables_table.blockSignals(True)

        for var_number in range(self.ui.variables_table.rowCount()):
            value = self.netvars.read_variable(var_number)
            self.ui.variables_table.item(var_number, self.Column.VALUE).setText(value)

        self.ui.variables_table.blockSignals(False)

    def write_variable(self, a_item: QtWidgets.QTableWidgetItem):
        variable_number = self.ui.variables_table.item(a_item.row(), self.Column.NUMBER).text()
        self.netvars.write_variable(variable_number)

    def closeEvent(self, a_event: QtGui.QCloseEvent) -> None:
        self.settings.save_geometry(self.ui.variables_table.__class__.__name__,
                                    self.ui.variables_table.horizontalHeader().saveState())
        self.settings.save_geometry(self.__class__.__name__, self.saveGeometry())
        a_event.accept()


class NumberTableWidgetItem(QtWidgets.QTableWidgetItem):
    def __lt__(self, other: QtWidgets.QTableWidgetItem):
        return float(self.text()) < float(other.text())
