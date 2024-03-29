# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(870, 619)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setAnimated(True)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setSpacing(0)
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
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.save_button = QtWidgets.QPushButton(self.layoutWidget)
        self.save_button.setObjectName("save_button")
        self.horizontalLayout_3.addWidget(self.save_button)
        self.load_button = QtWidgets.QPushButton(self.layoutWidget)
        self.load_button.setObjectName("load_button")
        self.horizontalLayout_3.addWidget(self.load_button)
        self.clear_results_button = QtWidgets.QPushButton(self.layoutWidget)
        self.clear_results_button.setObjectName("clear_results_button")
        self.horizontalLayout_3.addWidget(self.clear_results_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
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
        self.log_text_edit = QtWidgets.QTextEdit(self.splitter)
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
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.errors_count_label = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.errors_count_label.sizePolicy().hasHeightForWidth())
        self.errors_count_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.errors_count_label.setFont(font)
        self.errors_count_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.errors_count_label.setObjectName("errors_count_label")
        self.gridLayout.addWidget(self.errors_count_label, 2, 1, 1, 1)
        self.errors_out_button = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.errors_out_button.sizePolicy().hasHeightForWidth())
        self.errors_out_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.errors_out_button.setFont(font)
        self.errors_out_button.setObjectName("errors_out_button")
        self.gridLayout.addWidget(self.errors_out_button, 2, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 1)
        self.open_tstlan_button = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_tstlan_button.sizePolicy().hasHeightForWidth())
        self.open_tstlan_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.open_tstlan_button.setFont(font)
        self.open_tstlan_button.setObjectName("open_tstlan_button")
        self.gridLayout.addWidget(self.open_tstlan_button, 0, 0, 1, 3)
        self.firmware_info_label = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.firmware_info_label.sizePolicy().hasHeightForWidth())
        self.firmware_info_label.setSizePolicy(sizePolicy)
        self.firmware_info_label.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.firmware_info_label.setFont(font)
        self.firmware_info_label.setText("")
        self.firmware_info_label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.firmware_info_label.setObjectName("firmware_info_label")
        self.gridLayout.addWidget(self.firmware_info_label, 1, 1, 1, 2)
        self.errors_label = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.errors_label.sizePolicy().hasHeightForWidth())
        self.errors_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.errors_label.setFont(font)
        self.errors_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.errors_label.setObjectName("errors_label")
        self.gridLayout.addWidget(self.errors_label, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.fast_adc_label = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.fast_adc_label.setFont(font)
        self.fast_adc_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.fast_adc_label.setObjectName("fast_adc_label")
        self.gridLayout.addWidget(self.fast_adc_label, 3, 1, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        self.control_box = QtWidgets.QGroupBox(self.layoutWidget1)
        self.control_box.setFlat(True)
        self.control_box.setCheckable(False)
        self.control_box.setObjectName("control_box")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.control_box)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout.addWidget(self.control_box)
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
        self.save_button.setText(_translate("MainWindow", "Сохранить"))
        self.load_button.setText(_translate("MainWindow", "Загрузить"))
        self.clear_results_button.setText(_translate("MainWindow", "Сбросить"))
        self.tests_tree.headerItem().setText(0, _translate("MainWindow", "Тест"))
        self.tests_tree.headerItem().setText(1, _translate("MainWindow", "Кол-во"))
        self.tests_tree.headerItem().setText(2, _translate("MainWindow", "Успех"))
        self.tests_tree.headerItem().setText(3, _translate("MainWindow", "Статус"))
        self.autocheck_start_button.setText(_translate("MainWindow", "Старт"))
        self.errors_count_label.setText(_translate("MainWindow", "0"))
        self.errors_out_button.setText(_translate("MainWindow", "Вывести ошибки"))
        self.label_7.setText(_translate("MainWindow", "Прошивка:"))
        self.open_tstlan_button.setText(_translate("MainWindow", "Открыть tstlan"))
        self.errors_label.setText(_translate("MainWindow", "Ошибки:"))
        self.label.setText(_translate("MainWindow", "АЦП:"))
        self.fast_adc_label.setText(_translate("MainWindow", "0"))
        self.control_box.setTitle(_translate("MainWindow", "Управление"))
        self.settings_menu.setTitle(_translate("MainWindow", "Настройки"))
        self.menu.setTitle(_translate("MainWindow", "Справка"))
        self.change_fixed_range_action.setText(_translate("MainWindow", "Изменить фиксированный шаг"))
        self.enter_settings_action.setText(_translate("MainWindow", "Настройки..."))
        self.action.setText(_translate("MainWindow", "О программе"))
import icons
