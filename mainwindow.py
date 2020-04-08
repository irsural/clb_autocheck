import logging

from PyQt5 import QtWidgets, QtCore, QtGui

from settings_ini_parser import Settings, BadIniException
from ui.py.mainwindow import Ui_MainWindow as MainForm
from source_mode_window import SourceModeWidget
from settings_dialog import SettingsDialog
import calibrator_constants as clb
import clb_dll
import utils

from test_conductor import TestsConductor
from clb_tests import ClbTest

from qt_utils import QTextEditLogger


class MainWindow(QtWidgets.QMainWindow):
    clb_list_changed = QtCore.pyqtSignal([list])
    usb_status_changed = QtCore.pyqtSignal(clb.State)
    signal_enable_changed = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.ui = MainForm()
        self.ui.setupUi(self)

        try:
            self.settings = Settings(self)
            ini_ok = True
        except BadIniException:
            ini_ok = False
            QtWidgets.QMessageBox.critical(self, "Ошибка", 'Файл конфигурации поврежден. Пожалуйста, '
                                                           'удалите файл "settings.ini" и запустите программу заново')
        if ini_ok:
            self.restoreGeometry(self.settings.get_last_geometry(self.__class__.__name__))
            self.ui.splitter.restoreGeometry(self.settings.get_last_geometry(self.ui.splitter.__class__.__name__))

            log = QTextEditLogger(self, self.ui.log_text_edit)
            log.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s'))
            logging.getLogger().addHandler(log)
            logging.getLogger().setLevel(logging.DEBUG)

            self.clb_driver = clb_dll.set_up_driver(clb_dll.debug_dll_path)
            self.usb_driver = clb_dll.UsbDrv(self.clb_driver)
            self.usb_state = clb_dll.UsbDrv.UsbState.DISABLED
            self.calibrator = clb_dll.ClbDrv(self.clb_driver)
            self.clb_state = clb.State.DISCONNECTED

            self.clb_signal_off_timer = QtCore.QTimer()
            # noinspection PyTypeChecker
            self.clb_signal_off_timer.timeout.connect(self.close)
            self.SIGNAL_OFF_TIME_MS = 200

            self.tick_timer = QtCore.QTimer(self)
            self.tick_timer.timeout.connect(self.tick)
            self.tick_timer.start(10)

            self.ui.enter_settings_action.triggered.connect(self.open_settings)

            source_mode_widget = SourceModeWidget(self.settings, self.calibrator, self)
            self.clb_list_changed.connect(source_mode_widget.update_clb_list)
            self.usb_status_changed.connect(source_mode_widget.update_clb_status)
            self.signal_enable_changed.connect(source_mode_widget.signal_enable_changed)
            self.ui.source_mode_layout.addWidget(source_mode_widget)
            self.show()

            self.test_conductor = TestsConductor(self.calibrator)
            self.ui.autocheck_start_button.clicked.connect(self.start_autocheck)
        else:
            self.close()

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

    def start_autocheck(self):
        self.test_conductor.start()

    def open_settings(self):
        try:
            settings_dialog = SettingsDialog(self.settings, self)
            settings_dialog.exec()
        except Exception as err:
            utils.exception_handler(err)

    def closeEvent(self, a_event: QtGui.QCloseEvent):
        if self.calibrator.signal_enable:
            self.calibrator.signal_enable = False
            self.clb_signal_off_timer.start(self.SIGNAL_OFF_TIME_MS)
            a_event.ignore()
        else:
            self.settings.save_geometry(self.ui.splitter.__class__.__name__, self.ui.splitter.saveGeometry())
            self.settings.save_geometry(self.__class__.__name__, self.saveGeometry())
            a_event.accept()
