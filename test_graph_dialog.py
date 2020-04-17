import logging
from typing import List, Dict, Tuple
from enum import IntEnum

from PyQt5 import QtGui, QtWidgets, QtCore

from ui.py.test_graphs_dialog import Ui_Dialog as GraphForm
from settings_ini_parser import Settings
import network_variables as nv
import utils


class TestGraphDialog(QtWidgets.QDialog):
    def __init__(self, a_graph_data: List[Dict[str, List[Tuple[float, float]]]], a_settings: Settings, a_parent=None):
        super().__init__(a_parent)

        self.ui = GraphForm()
        self.ui.setupUi(self)

        self.settings = a_settings
        self.restoreGeometry(self.settings.get_last_geometry(self.__class__.__name__))
        self.show()

        self.graph_data = a_graph_data
        logging.debug(self.graph_data)

    def __del__(self):
        print("graphs deleted")

    def closeEvent(self, a_event: QtGui.QCloseEvent) -> None:
        self.settings.save_geometry(self.__class__.__name__, self.saveGeometry())
        a_event.accept()
