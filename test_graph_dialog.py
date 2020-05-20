from typing import List, Dict, Tuple
import logging

from PyQt5 import QtGui, QtWidgets
import pyqtgraph

from ui.py.test_graphs_dialog import Ui_Dialog as GraphForm
from settings_ini_parser import Settings
import utils


class TestGraphDialog(QtWidgets.QDialog):
    def __init__(self, a_graph_data: List[Dict[str, Tuple[List[float], List[float]]]], a_settings: Settings,
                 a_parent=None):
        super().__init__(a_parent)

        self.ui = GraphForm()
        self.ui.setupUi(self)

        self.settings = a_settings
        self.restoreGeometry(self.settings.get_last_geometry(self.__class__.__name__))
        self.show()

        self.graph_data = a_graph_data
        assert len(self.graph_data), "graph_data должен быть ненулевого размера !!!"

        self.current_test_number = 0

        if len(self.graph_data) > 1:
            self.test_number_tab_bar = QtWidgets.QTabBar(self)
            for i in range(len(self.graph_data)):
                self.test_number_tab_bar.addTab(f"Тест №{i + 1}")
            self.test_number_tab_bar.currentChanged.connect(self.change_test)
            self.ui.test_number_tabbar_layout.addWidget(self.test_number_tab_bar)

        self.graph_name_tab_bar = QtWidgets.QTabBar(self)
        for graph_name in self.graph_data[0].keys():
            self.graph_name_tab_bar.addTab(graph_name)
        self.graph_name_tab_bar.currentChanged.connect(self.change_graph)
        self.ui.graph_name_tabbar_layout.addWidget(self.graph_name_tab_bar)

        self.current_graph_name = self.graph_name_tab_bar.tabText(self.current_test_number)

        self.graph_widget = pyqtgraph.PlotWidget()
        self.graph_widget.setBackground('w')
        self.graph_widget.setLabel('bottom', 'Время, с', color='black', size=20)
        self.graph_widget.showGrid(x=True, y=True)
        self.pen = pyqtgraph.mkPen(color=(255, 0, 0), width=2)

        self.ui.chart_layout.addWidget(self.graph_widget)

        self.current_graph = None

        self.redraw_graph()

    def change_test(self, a_index: int):
        self.current_test_number = a_index
        self.redraw_graph()

    def change_graph(self, a_index: int):
        self.current_graph_name = self.graph_name_tab_bar.tabText(a_index)
        self.redraw_graph()

    def redraw_graph(self):
        try:
            plot_data = self.graph_data[self.current_test_number][self.current_graph_name]
            self.graph_widget.clear()
            self.current_graph = self.graph_widget.plot(plot_data[0], plot_data[1], pen=self.pen)
        except Exception as err:
            logging.debug(utils.exception_handler(err))

    def update_graphs(self):
        try:
            plot_data = self.graph_data[self.current_test_number][self.current_graph_name]
            self.current_graph.setData(plot_data[0], plot_data[1])
        except Exception as err:
            logging.debug(utils.exception_handler(err))

    def __del__(self):
        print("graphs deleted")

    def closeEvent(self, a_event: QtGui.QCloseEvent) -> None:
        self.settings.save_geometry(self.__class__.__name__, self.saveGeometry())
        a_event.accept()
