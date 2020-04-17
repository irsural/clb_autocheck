import logging

from PyQt5 import QtWidgets, QtCore, QtGui

from settings_ini_parser import Settings, BadIniException
from ui.py.mainwindow import Ui_MainWindow as MainForm
from source_mode_window import SourceModeWidget
from network_variables import NetworkVariables
from tests_tree_widget import TestsTreeWidget
from test_graph_dialog import TestGraphDialog
from settings_dialog import SettingsDialog
from test_conductor import TestsConductor
from tstlan_dialog import TstlanDialog
from qt_utils import QTextEditLogger
import calibrator_constants as clb
import constants as cfg
import tests_factory
import clb_tests_base
import clb_dll
import utils


class MainWindow(QtWidgets.QMainWindow):
    clb_list_changed = QtCore.pyqtSignal([list])
    usb_status_changed = QtCore.pyqtSignal(clb.State)
    signal_enable_changed = QtCore.pyqtSignal(bool)

    TEST_START_ROW = 1
    CHECK_BOX_COLUMN = 0

    STATUS_COLUMN = 2

    def __init__(self):
        super().__init__()

        self.ui = MainForm()
        self.ui.setupUi(self)

        self.loader = QtGui.QMovie(":/icons/gif/loader2.gif")
        self.loader.setScaledSize(QtCore.QSize(132, 99))
        self.ui.loader_label.setMovie(self.loader)

        try:
            self.settings = Settings(self)
            ini_ok = True
        except BadIniException:
            ini_ok = False
            QtWidgets.QMessageBox.critical(self, "Ошибка", 'Файл конфигурации поврежден. Пожалуйста, '
                                                           'удалите файл "settings.ini" и запустите программу заново')
        if ini_ok:
            self.restoreGeometry(self.settings.get_last_geometry(self.__class__.__name__))
            self.ui.splitter.restoreState(self.settings.get_last_geometry(self.ui.splitter.__class__.__name__ + "1"))
            self.ui.splitter_2.restoreState(self.settings.get_last_geometry(
                self.ui.splitter_2.__class__.__name__ + "2"))
            self.ui.tests_tree.header().restoreState(self.settings.get_last_geometry(
                self.ui.tests_tree.__class__.__name__))

            self.set_up_logger()

            self.clb_driver = clb_dll.set_up_driver(clb_dll.debug_dll_path)

            modbus_registers_count = 700
            self.usb_driver = clb_dll.UsbDrv(self.clb_driver, modbus_registers_count * 2)
            self.usb_state = clb_dll.UsbDrv.UsbState.DISABLED
            self.calibrator = clb_dll.ClbDrv(self.clb_driver)
            self.clb_state = clb.State.DISCONNECTED

            self.netvars = NetworkVariables(cfg.CLB_CONFIG_PATH, self.calibrator)

            self.clb_signal_off_timer = QtCore.QTimer()
            # noinspection PyTypeChecker
            self.clb_signal_off_timer.timeout.connect(self.close)
            self.SIGNAL_OFF_TIME_MS = 200

            self.ui.enter_settings_action.triggered.connect(self.open_settings)

            self.source_mode_widget = self.set_up_source_mode_widget()
            self.show()

            self.tests = tests_factory.create_tests(self.calibrator, self.netvars)

            self.tests_widget = TestsTreeWidget(self.tests, self.ui.tests_tree, self.settings)
            self.tests_widget.show_graph_requested.connect(self.show_test_graph)

            self.test_conductor = TestsConductor(self.tests)
            self.ui.autocheck_start_button.clicked.connect(self.autocheck_button_clicked)
            self.test_conductor.tests_done.connect(self.stop_autocheck)
            self.test_conductor.test_status_changed.connect(self.set_test_status)

            self.source_mode_widget.ui.open_tstlan_button.clicked.connect(self.open_tstlan)

            self.tick_timer = QtCore.QTimer(self)
            self.tick_timer.timeout.connect(self.tick)
            self.tick_timer.start(10)
        else:
            self.close()

    def set_up_logger(self):
        log = QTextEditLogger(self, self.ui.log_text_edit)
        # log.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s',
        #                                    datefmt='%Y-%m-%d %H:%M:%S'))
        log.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%H:%M:%S'))

        logging.getLogger().addHandler(log)
        logging.getLogger().setLevel(logging.DEBUG)
        # logging.getLogger().setLevel(logging.WARN)

    def set_up_source_mode_widget(self) -> SourceModeWidget:
        source_mode_widget = SourceModeWidget(self.settings, self.calibrator, self.netvars, self)
        self.clb_list_changed.connect(source_mode_widget.update_clb_list)
        self.usb_status_changed.connect(source_mode_widget.update_clb_status)
        self.signal_enable_changed.connect(source_mode_widget.signal_enable_changed)
        self.ui.source_mode_layout.addWidget(source_mode_widget)
        return source_mode_widget

    def tick(self):
        self.usb_tick()
        self.test_conductor.tick()

    def usb_tick(self):
        self.usb_driver.tick()

        if self.usb_driver.is_dev_list_changed():
            self.clb_list_changed.emit(self.usb_driver.get_dev_list())

        if self.usb_driver.is_status_changed():
            self.usb_state = self.usb_driver.get_status()

        current_state = clb.State.DISCONNECTED
        if self.usb_state == clb_dll.UsbDrv.UsbState.CONNECTED:
            if self.calibrator.signal_enable_changed():
                self.signal_enable_changed.emit(self.calibrator.signal_enable)

            if not self.calibrator.signal_enable:
                current_state = clb.State.STOPPED
            elif not self.calibrator.is_signal_ready():
                current_state = clb.State.WAITING_SIGNAL
            else:
                current_state = clb.State.READY

        if self.clb_state != current_state:
            self.clb_state = current_state
            self.calibrator.state = current_state
            self.usb_status_changed.emit(self.clb_state)

    def lock_interface(self, a_lock):
        self.source_mode_widget.ui.control_box.setDisabled(a_lock)
        self.tests_widget.lock_interface(a_lock)

    def autocheck_button_clicked(self):
        try:
            if self.test_conductor.started():
                self.test_conductor.stop()
                self.stop_autocheck()
            else:
                self.start_autocheck()
        except AssertionError as err:
            logging.debug(utils.exception_handler(err))

    def start_autocheck(self):
        if self.calibrator.state != clb.State.DISCONNECTED:
            self.lock_interface(True)
            self.test_conductor.set_enabled_tests(self.tests_widget.get_tests_repeat_count())
            self.ui.autocheck_start_button.setText("Остановить")
            self.test_conductor.start()

            self.ui.loader_label.show()
            self.loader.start()
        else:
            logging.warning("Калибратор не подключен, невозможно провести проверку")

    def stop_autocheck(self):
        self.lock_interface(False)
        self.ui.autocheck_start_button.setText("Старт")
        logging.info("Проверка завершена")

        self.ui.loader_label.hide()
        self.loader.stop()

    def set_test_status(self, a_group_name, a_test_name: str, a_status: clb_tests_base.ClbTest.Status,
                        a_success_count: int):
        try:
            self.tests_widget.set_test_status(a_group_name, a_test_name, a_status, a_success_count)
        except AssertionError as err:
            logging.debug(utils.exception_handler(err))

    def open_tstlan(self):
        try:
            tstlan_dialog = TstlanDialog(self.netvars, self.settings)
            tstlan_dialog.exec()
        except Exception as err:
            logging.debug(utils.exception_handler(err))

    def show_test_graph(self, a_group: str, a_name: str):
        try:
            graph_data = self.test_conductor.get_test_graph(a_group, a_name)
            if graph_data:
                graphs_dialog = TestGraphDialog(graph_data, self.settings, self)
                self.test_conductor.graphs_have_been_updated.connect(graphs_dialog.update_graphs)
                graphs_dialog.exec()
            else:
                logging.warning("График для выбранного измерения не создан")
        except Exception as err:
            logging.debug(utils.exception_handler(err))

    def open_settings(self):
        try:
            settings_dialog = SettingsDialog(self.settings, self)
            settings_dialog.exec()
        except Exception as err:
            logging.debug(utils.exception_handler(err))

    def closeEvent(self, a_event: QtGui.QCloseEvent):
        if self.calibrator.signal_enable:
            self.calibrator.signal_enable = False
            self.clb_signal_off_timer.start(self.SIGNAL_OFF_TIME_MS)
            a_event.ignore()
        else:
            self.settings.save_geometry(self.ui.splitter.__class__.__name__ + "1", self.ui.splitter.saveState())
            self.settings.save_geometry(self.ui.splitter_2.__class__.__name__ + "2", self.ui.splitter_2.saveState())
            self.settings.save_geometry(self.ui.tests_tree.__class__.__name__, self.ui.tests_tree.header().saveState())
            self.settings.save_geometry(self.__class__.__name__, self.saveGeometry())
            self.tests_widget.save()
            a_event.accept()
