# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/tstlan_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(743, 645)
        font = QtGui.QFont()
        font.setPointSize(10)
        Dialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.doubleSpinBox.setDecimals(1)
        self.doubleSpinBox.setSingleStep(0.5)
        self.doubleSpinBox.setProperty("value", 1.5)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.gridLayout.addWidget(self.doubleSpinBox, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.variables_table = QtWidgets.QTableWidget(Dialog)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.variables_table.setFont(font)
        self.variables_table.setObjectName("variables_table")
        self.variables_table.setColumnCount(5)
        self.variables_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.variables_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.variables_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.variables_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.variables_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.variables_table.setHorizontalHeaderItem(4, item)
        self.variables_table.horizontalHeader().setSortIndicatorShown(True)
        self.variables_table.horizontalHeader().setStretchLastSection(True)
        self.variables_table.verticalHeader().setVisible(False)
        self.variables_table.verticalHeader().setDefaultSectionSize(22)
        self.variables_table.verticalHeader().setMinimumSectionSize(22)
        self.verticalLayout.addWidget(self.variables_table)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Tstlan"))
        self.label.setText(_translate("Dialog", "Время обновления, с"))
        self.label_2.setText(_translate("Dialog", "Фильтр по имени"))
        self.variables_table.setSortingEnabled(True)
        item = self.variables_table.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "№"))
        item = self.variables_table.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Индекс"))
        item = self.variables_table.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Имя"))
        item = self.variables_table.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Тип"))
        item = self.variables_table.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "Значение"))
