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
        MARK = 2
        NAME = 3
        GRAPH = 4
        TYPE = 5
        VALUE = 6

    def __init__(self, a_variables: nv.NetworkVariables, a_settings: Settings, a_parent=None):
        super().__init__(a_parent)

        self.ui = TstlanForm()
        self.ui.setupUi(self)
        self.show()

        self.netvars = a_variables

        self.settings = a_settings
        self.restoreGeometry(self.settings.get_last_geometry(self.__class__.__name__))

        # Обязательно вызывать до восстановления состояния таблицы !!!
        self.fill_variables_table()

        self.ui.variables_table.horizontalHeader().restoreState(self.settings.get_last_geometry(
            self.ui.variables_table.__class__.__name__))
        self.ui.variables_table.resizeRowsToContents()

        self.ui.show_marked_checkbox.setChecked(self.settings.tstlan_show_marks)

        self.ui.upadte_time_spinbox.setValue(self.settings.tstlan_update_time)

        self.read_variables_timer = QtCore.QTimer(self)
        self.read_variables_timer.timeout.connect(self.read_variables)
        self.read_variables_timer.start(1000)

        self.ui.variables_table.itemChanged.connect(self.write_variable)
        self.ui.name_filter_edit.textChanged.connect(self.filter_variables)
        self.ui.upadte_time_spinbox.valueChanged.connect(self.update_time_changed)
        self.ui.show_marked_checkbox.toggled.connect(self.show_marked_toggled)

        self.filter_variables()

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

                widget = QtWidgets.QWidget()
                cb = QtWidgets.QCheckBox()
                try:
                    cb.setChecked(self.settings.tstlan_marks[row])
                except IndexError:
                    cb.setChecked(False)

                layout = QtWidgets.QHBoxLayout(widget)
                layout.addWidget(cb)
                layout.setAlignment(QtCore.Qt.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                self.ui.variables_table.setCellWidget(row, self.Column.MARK, widget)

                item = QtWidgets.QTableWidgetItem(variable.name)
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                self.ui.variables_table.setItem(row, self.Column.NAME, item)

                item = QtWidgets.QTableWidgetItem(variable.type)
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                self.ui.variables_table.setItem(row, self.Column.TYPE, item)

                self.ui.variables_table.setItem(row, self.Column.VALUE, NumberTableWidgetItem(""))

    def read_variables(self):
        self.ui.variables_table.blockSignals(True)

        try:
            if self.netvars.connected():
                for visual_row in range(self.ui.variables_table.rowCount()):
                    row = int(self.ui.variables_table.item(visual_row, self.Column.NUMBER).text())

                    value = self.netvars.read_variable(row)
                    self.ui.variables_table.item(visual_row, self.Column.VALUE).setText(
                        utils.float_to_string(round(value, 7)))

        except Exception as err:
            logging.debug(utils.exception_handler(err))

        self.ui.variables_table.blockSignals(False)

    def write_variable(self, a_item: QtWidgets.QTableWidgetItem):
        try:
            if self.netvars.connected():
                variable_number = int(self.ui.variables_table.item(a_item.row(), self.Column.NUMBER).text())
                try:
                    variable_value = utils.parse_input(a_item.text())
                    self.netvars.write_variable(variable_number, variable_value)
                except ValueError:
                    pass
        except Exception as err:
            logging.debug(utils.exception_handler(err))

    def filter_variables(self):
        filter_text = self.ui.name_filter_edit.text()
        regexp = QtCore.QRegExp(filter_text)
        regexp.setPatternSyntax(QtCore.QRegExp.Wildcard)
        regexp.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        for i in range(self.ui.variables_table.rowCount()):
            cell_text = self.ui.variables_table.item(i, self.Column.NAME).text()
            if any(regex_symb in filter_text for regex_symb in ['?', '*', '[', ']']):
                match = regexp.exactMatch(cell_text)
            else:
                match = filter_text in cell_text

            if self.ui.show_marked_checkbox.isChecked():
                marked_cb = self.ui.variables_table.cellWidget(i, self.Column.MARK).layout().itemAt(0).widget()
                match = match & marked_cb.isChecked()
            self.ui.variables_table.setRowHidden(i, not match)

    def show_marked_toggled(self, a_enable):
        self.filter_variables()
        self.settings.tstlan_show_marks = int(a_enable)

    def update_time_changed(self, a_value):
        self.read_variables_timer.start(a_value * 1000)
        self.settings.tstlan_update_time = a_value

    def closeEvent(self, a_event: QtGui.QCloseEvent) -> None:
        self.settings.save_geometry(self.ui.variables_table.__class__.__name__,
                                    self.ui.variables_table.horizontalHeader().saveState())
        self.settings.save_geometry(self.__class__.__name__, self.saveGeometry())

        cb_states = [0] * self.ui.variables_table.rowCount()
        for i in range(self.ui.variables_table.rowCount()):
            cb_number = int(self.ui.variables_table.item(i, self.Column.NUMBER).text())
            state = int(self.ui.variables_table.cellWidget(i, self.Column.MARK).layout().itemAt(0).widget().isChecked())
            cb_states[cb_number] = state

        self.settings.tstlan_marks = cb_states

        a_event.accept()


class NumberTableWidgetItem(QtWidgets.QTableWidgetItem):
    def __lt__(self, other: QtWidgets.QTableWidgetItem):
        return float(self.text()) < float(other.text())
