# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(868, 405)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setAnimated(True)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.label_7 = QtWidgets.QLabel(self.centralWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 2, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.enable_all_checkbox = QtWidgets.QCheckBox(self.centralWidget)
        self.enable_all_checkbox.setText("")
        self.enable_all_checkbox.setObjectName("enable_all_checkbox")
        self.horizontalLayout_4.addWidget(self.enable_all_checkbox)
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralWidget)
        self.checkBox_2.setStyleSheet("margin-left: 20\n"
"\n"
"")
        self.checkBox_2.setText("")
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout.addWidget(self.checkBox_2, 2, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.centralWidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 1)
        self.checkBox_4 = QtWidgets.QCheckBox(self.centralWidget)
        self.checkBox_4.setStyleSheet("margin-left: 20\n"
"\n"
"")
        self.checkBox_4.setText("")
        self.checkBox_4.setObjectName("checkBox_4")
        self.gridLayout.addWidget(self.checkBox_4, 4, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 2, 1, 1)
        self.checkBox_3 = QtWidgets.QCheckBox(self.centralWidget)
        self.checkBox_3.setStyleSheet("margin-left: 20\n"
"\n"
"")
        self.checkBox_3.setText("")
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout.addWidget(self.checkBox_3, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.centralWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 4, 2, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.centralWidget)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 4, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.centralWidget)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 3, 1, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.centralWidget)
        self.checkBox.setStyleSheet("margin-left: 20\n"
"\n"
"")
        self.checkBox.setText("")
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 1, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.autocheck_start_button = QtWidgets.QPushButton(self.centralWidget)
        self.autocheck_start_button.setObjectName("autocheck_start_button")
        self.verticalLayout_2.addWidget(self.autocheck_start_button)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.splitter = QtWidgets.QSplitter(self.centralWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.log_text_edit = QtWidgets.QPlainTextEdit(self.splitter)
        self.log_text_edit.setObjectName("log_text_edit")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.source_mode_layout = QtWidgets.QVBoxLayout()
        self.source_mode_layout.setSpacing(6)
        self.source_mode_layout.setObjectName("source_mode_layout")
        self.verticalLayout.addLayout(self.source_mode_layout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 868, 21))
        self.menuBar.setObjectName("menuBar")
        self.settings_menu = QtWidgets.QMenu(self.menuBar)
        self.settings_menu.setObjectName("settings_menu")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menuBar)
        self.change_fixed_range_action = QtWidgets.QAction(MainWindow)
        self.change_fixed_range_action.setObjectName("change_fixed_range_action")
        self.enter_settings_action = QtWidgets.QAction(MainWindow)
        self.enter_settings_action.setObjectName("enter_settings_action")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.settings_menu.addAction(self.enter_settings_action)
        self.menu.addAction(self.action)
        self.menuBar.addAction(self.settings_menu.menuAction())
        self.menuBar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_7.setText(_translate("MainWindow", "..."))
        self.label_3.setText(_translate("MainWindow", "Вкл."))
        self.label_9.setText(_translate("MainWindow", "U~ 4 В"))
        self.label_2.setText(_translate("MainWindow", "..."))
        self.label_6.setText(_translate("MainWindow", "..."))
        self.label_5.setText(_translate("MainWindow", "Статус"))
        self.label.setText(_translate("MainWindow", "U~ 40 мВ"))
        self.label_8.setText(_translate("MainWindow", "..."))
        self.label_11.setText(_translate("MainWindow", "U~ 200 В"))
        self.label_4.setText(_translate("MainWindow", "Тест"))
        self.label_10.setText(_translate("MainWindow", "U~ 43 В"))
        self.autocheck_start_button.setText(_translate("MainWindow", "Старт"))
        self.settings_menu.setTitle(_translate("MainWindow", "Настройки"))
        self.menu.setTitle(_translate("MainWindow", "Справка"))
        self.change_fixed_range_action.setText(_translate("MainWindow", "Изменить фиксированный шаг"))
        self.enter_settings_action.setText(_translate("MainWindow", "Настройки..."))
        self.action.setText(_translate("MainWindow", "О программе"))
import icons_rc
