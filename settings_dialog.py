import logging

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal

from custom_widgets.EditListDialog import EditedListWithUnits
from ui.py.settings_form import Ui_Dialog as SettingsForm
from custom_widgets.QTableDelegates import ComboboxCellDelegate, TableEditDoubleClick
from network_variables_database import NetvarsDatabase
from settings_ini_parser import Settings
import calibrator_constants as clb

import utils


class SettingsDialog(QtWidgets.QDialog):
    class SettingPages:
        MARKS = 0
        FIXED_RANGE = 1

    fixed_range_changed = pyqtSignal()

    def __init__(self, a_settings: Settings, a_netvars_db: NetvarsDatabase, a_parent=None):
        super().__init__(a_parent)

        self.ui = SettingsForm()
        self.ui.setupUi(self)

        self.netvars_db = a_netvars_db
        self.settings = a_settings
        self.restoreGeometry(self.settings.get_last_geometry(self.__class__.__name__))
        self.ui.netvars_table.horizontalHeader().restoreState(
            self.settings.get_last_header_state(self.ui.netvars_table.__class__.__name__))

        self.ui.save_and_exit_button.clicked.connect(self.save_and_exit)
        self.ui.save_button.clicked.connect(self.save)
        self.ui.cancel_button.clicked.connect(self.close)

        self.edit_fixed_range_widget = EditedListWithUnits(self, "В", self.settings.fixed_step_list, clb.MIN_VOLTAGE,
                                                           clb.MAX_VOLTAGE,
                                                           a_optional_widget=QtWidgets.QLabel("Шаг", self))
        self.ui.fixed_range_groupbox.layout().addWidget(self.edit_fixed_range_widget)

        self.ui.exact_step_spinbox.setValue(self.settings.exact_step)
        self.ui.rough_step_spinbox.setValue(self.settings.rough_step)
        self.ui.common_step_spinbox.setValue(self.settings.common_step)

        self.ui.correction_deviation_spinbox.setValue(self.settings.aux_correction_deviation)
        self.ui.deviation_spinbox.setValue(self.settings.aux_deviation)
        self.ui.voltage_25_discretes_60v_spinbox.setValue(self.settings.aux_voltage_25_discretes_60v)
        self.ui.voltage_230_discretes_60v_spinbox.setValue(self.settings.aux_voltage_230_discretes_60v)
        self.ui.voltage_25_discretes_200v_spinbox.setValue(self.settings.aux_voltage_25_discretes_200v)
        self.ui.voltage_230_discretes_200v_spinbox.setValue(self.settings.aux_voltage_230_discretes_200v)
        self.ui.voltage_25_discretes_600v_spinbox.setValue(self.settings.aux_voltage_25_discretes_600v)
        self.ui.voltage_230_discretes_600v_spinbox.setValue(self.settings.aux_voltage_230_discretes_600v)
        self.ui.voltage_25_discretes_4v_spinbox.setValue(self.settings.aux_voltage_25_discretes_4v)
        self.ui.voltage_230_discretes_4v_spinbox.setValue(self.settings.aux_voltage_230_discretes_4v)

        self.ui.netvars_table.setModel(self.netvars_db.model())
        self.ui.netvars_table.setItemDelegateForColumn(NetvarsDatabase.Column.TYPE,
                                                       ComboboxCellDelegate(self, self.netvars_db.allowed_types()))
        self.ui.netvars_table.setItemDelegateForColumn(NetvarsDatabase.Column.INDEX, TableEditDoubleClick(self))
        self.ui.netvars_table.setItemDelegateForColumn(NetvarsDatabase.Column.MIN, TableEditDoubleClick(self))
        self.ui.netvars_table.setItemDelegateForColumn(NetvarsDatabase.Column.MAX, TableEditDoubleClick(self))
        self.ui.netvars_table.setItemDelegateForColumn(NetvarsDatabase.Column.DEFAULT, TableEditDoubleClick(self))
        self.ui.netvars_table.setColumnHidden(NetvarsDatabase.Column.ID, True)
        self.ui.netvars_table.resizeRowsToContents()

        self.netvars_db.model_updated.connect(self.show_table_comboboxes)
        self.show_table_comboboxes()

        self.ui.add_row_button.clicked.connect(self.add_netvar_button_clicked)
        self.ui.delete_row_button.clicked.connect(self.delete_netvar_button_clicked)

        self.open_first_tab()

    def __del__(self):
        print("settings deleted")

    def open_first_tab(self):
        self.ui.settings_menu_list.setCurrentRow(0)
        self.ui.settings_stackedwidget.setCurrentIndex(0)

    def show_table_comboboxes(self):
        for row in range(self.netvars_db.model().rowCount()):
            self.ui.netvars_table.openPersistentEditor(self.netvars_db.model().index(row, NetvarsDatabase.Column.TYPE))

    def add_netvar_button_clicked(self):
        try:
            self.netvars_db.add_netvar()
        except AssertionError as err:
            logging.debug(utils.exception_handler(err))

    def delete_netvar_button_clicked(self):
        indexes = self.ui.netvars_table.selectedIndexes()
        if indexes and len(indexes) == 1:
            row = indexes[0].row()
            self.netvars_db.delete_netvar(row)

    def save(self):
        fixed_step_list = self.edit_fixed_range_widget.sort_list()
        if self.settings.fixed_step_list != fixed_step_list:
            self.settings.fixed_step_list = fixed_step_list

        if self.settings.rough_step != self.ui.rough_step_spinbox.value():
            self.settings.rough_step = self.ui.rough_step_spinbox.value()

        if self.settings.common_step != self.ui.common_step_spinbox.value():
            self.settings.common_step = self.ui.common_step_spinbox.value()

        if self.settings.exact_step != self.ui.exact_step_spinbox.value():
            self.settings.exact_step = self.ui.exact_step_spinbox.value()

        self.settings.aux_correction_deviation = self.ui.correction_deviation_spinbox.value()
        self.settings.aux_deviation = self.ui.deviation_spinbox.value()
        self.settings.aux_voltage_25_discretes_60v = self.ui.voltage_25_discretes_60v_spinbox.value()
        self.settings.aux_voltage_230_discretes_60v = self.ui.voltage_230_discretes_60v_spinbox.value()
        self.settings.aux_voltage_25_discretes_200v = self.ui.voltage_25_discretes_200v_spinbox.value()
        self.settings.aux_voltage_230_discretes_200v = self.ui.voltage_230_discretes_200v_spinbox.value()
        self.settings.aux_voltage_25_discretes_600v = self.ui.voltage_25_discretes_600v_spinbox.value()
        self.settings.aux_voltage_230_discretes_600v = self.ui.voltage_230_discretes_600v_spinbox.value()
        self.settings.aux_voltage_25_discretes_4v = self.ui.voltage_25_discretes_4v_spinbox.value()
        self.settings.aux_voltage_230_discretes_4v = self.ui.voltage_230_discretes_4v_spinbox.value()

        return True

    def save_and_exit(self):
        if self.save():
            self.close()

    def closeEvent(self, a_event: QtGui.QCloseEvent) -> None:
        self.settings.save_geometry(self.__class__.__name__, self.saveGeometry())
        self.settings.save_header_state(self.ui.netvars_table.__class__.__name__,
                                        self.ui.netvars_table.horizontalHeader().saveState())
        a_event.accept()
