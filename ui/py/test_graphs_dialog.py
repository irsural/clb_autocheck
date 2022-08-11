# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test_graphs_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_test_graph_dialog(object):
    def setupUi(self, test_graph_dialog):
        test_graph_dialog.setObjectName("test_graph_dialog")
        test_graph_dialog.resize(838, 554)
        self.verticalLayout = QtWidgets.QVBoxLayout(test_graph_dialog)
        self.verticalLayout.setContentsMargins(0, 5, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.test_number_tabbar_layout = QtWidgets.QHBoxLayout()
        self.test_number_tabbar_layout.setObjectName("test_number_tabbar_layout")
        self.verticalLayout.addLayout(self.test_number_tabbar_layout)
        self.graph_name_tabbar_layout = QtWidgets.QHBoxLayout()
        self.graph_name_tabbar_layout.setObjectName("graph_name_tabbar_layout")
        self.verticalLayout.addLayout(self.graph_name_tabbar_layout)
        self.chart_layout = QtWidgets.QHBoxLayout()
        self.chart_layout.setObjectName("chart_layout")
        self.verticalLayout.addLayout(self.chart_layout)

        self.retranslateUi(test_graph_dialog)
        QtCore.QMetaObject.connectSlotsByName(test_graph_dialog)

    def retranslateUi(self, test_graph_dialog):
        _translate = QtCore.QCoreApplication.translate
        test_graph_dialog.setWindowTitle(_translate("test_graph_dialog", "Dialog"))
