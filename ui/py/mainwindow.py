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
        MainWindow.resize(870, 625)
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
        self.splitter_2 = QtWidgets.QSplitter(self.centralWidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.layoutWidget = QtWidgets.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tests_tree = QtWidgets.QTreeWidget(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tests_tree.sizePolicy().hasHeightForWidth())
        self.tests_tree.setSizePolicy(sizePolicy)
        self.tests_tree.setAnimated(True)
        self.tests_tree.setObjectName("tests_tree")
        self.verticalLayout_2.addWidget(self.tests_tree)
        self.autocheck_start_button = QtWidgets.QPushButton(self.layoutWidget)
        self.autocheck_start_button.setObjectName("autocheck_start_button")
        self.verticalLayout_2.addWidget(self.autocheck_start_button)
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.log_text_edit = QtWidgets.QPlainTextEdit(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.log_text_edit.sizePolicy().hasHeightForWidth())
        self.log_text_edit.setSizePolicy(sizePolicy)
        self.log_text_edit.setObjectName("log_text_edit")
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.source_mode_widget = QtWidgets.QWidget(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.source_mode_widget.sizePolicy().hasHeightForWidth())
        self.source_mode_widget.setSizePolicy(sizePolicy)
        self.source_mode_widget.setObjectName("source_mode_widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.source_mode_widget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.source_mode_layout = QtWidgets.QVBoxLayout()
        self.source_mode_layout.setSpacing(6)
        self.source_mode_layout.setObjectName("source_mode_layout")
        self.verticalLayout_4.addLayout(self.source_mode_layout)
        self.verticalLayout.addWidget(self.source_mode_widget)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.loader_label = QtWidgets.QLabel(self.layoutWidget1)
        self.loader_label.setText("")
        self.loader_label.setObjectName("loader_label")
        self.horizontalLayout_2.addWidget(self.loader_label)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addWidget(self.splitter_2)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 870, 21))
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
        self.tests_tree.headerItem().setText(0, _translate("MainWindow", "Тест"))
        self.tests_tree.headerItem().setText(1, _translate("MainWindow", "Кол-во"))
        self.tests_tree.headerItem().setText(2, _translate("MainWindow", "Успешно"))
        self.tests_tree.headerItem().setText(3, _translate("MainWindow", "Статус"))
        self.autocheck_start_button.setText(_translate("MainWindow", "Старт"))
        self.settings_menu.setTitle(_translate("MainWindow", "Настройки"))
        self.menu.setTitle(_translate("MainWindow", "Справка"))
        self.change_fixed_range_action.setText(_translate("MainWindow", "Изменить фиксированный шаг"))
        self.enter_settings_action.setText(_translate("MainWindow", "Настройки..."))
        self.action.setText(_translate("MainWindow", "О программе"))
import icons_rc
