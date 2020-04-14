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

        self.ui.upadte_time_spinbox.setValue(self.settings.tstlan_update_time)

        self.fill_variables_table()

        self.read_variables_timer = QtCore.QTimer(self)
        self.read_variables_timer.timeout.connect(self.read_variables)
        self.read_variables_timer.start(1000)

        self.ui.variables_table.itemChanged.connect(self.write_variable)
        self.ui.name_filter_edit.textChanged.connect(self.filter_variables)
        self.ui.upadte_time_spinbox.valueChanged.connect(self.update_time_changed)

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

                self.ui.variables_table.setItem(row, self.Column.VALUE, NumberTableWidgetItem(""))

    def read_variables(self):
        self.ui.variables_table.blockSignals(True)

        for visual_row in range(self.ui.variables_table.rowCount()):
            row = int(self.ui.variables_table.item(visual_row, self.Column.NUMBER).text())

            value = self.netvars.read_variable(row)
            self.ui.variables_table.item(visual_row, self.Column.VALUE).setText(str(round(value, 7)))

        self.ui.variables_table.blockSignals(False)

    def write_variable(self, a_item: QtWidgets.QTableWidgetItem):
        try:
            variable_number = int(self.ui.variables_table.item(a_item.row(), self.Column.NUMBER).text())
            try:
                variable_value = utils.parse_input(a_item.text())
                self.netvars.write_variable(variable_number, variable_value)
            except ValueError:
                pass
        except Exception as err:
            print(utils.exception_handler(err))

    def filter_variables(self):
        filter_text = self.ui.name_filter_edit.text()
        for i in range(self.ui.variables_table.rowCount()):
            match = filter_text.lower() not in self.ui.variables_table.item(i, self.Column.NAME).text()
            self.ui.variables_table.setRowHidden(i, match)

    def update_time_changed(self, a_value):
        self.read_variables_timer.start(a_value * 1000)
        self.settings.tstlan_update_time = a_value

    def closeEvent(self, a_event: QtGui.QCloseEvent) -> None:
        self.settings.save_geometry(self.ui.variables_table.__class__.__name__,
                                    self.ui.variables_table.horizontalHeader().saveState())
        self.settings.save_geometry(self.__class__.__name__, self.saveGeometry())
        a_event.accept()


class NumberTableWidgetItem(QtWidgets.QTableWidgetItem):
    def __lt__(self, other: QtWidgets.QTableWidgetItem):
        return float(self.text()) < float(other.text())
