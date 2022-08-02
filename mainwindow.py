import os.path
from typing import Dict, Tuple
import logging
import json

from PyQt5 import QtWidgets, QtCore, QtGui

from irspy.qt.custom_widgets.tstlan_dialog import TstlanDialog
import irspy.clb.clb_dll as clb_dll
import irspy.clb.calibrator_constants as clb

from irspy.qt.custom_widgets.source_mode_widget import SourceModeWidget
from irspy.qt.custom_widgets.dialog_with_text import DialogWithText
from irspy.clb.network_variables import NetworkVariables
from ui.py.mainwindow import Ui_MainWindow as MainForm
from network_variables_database import NetvarsDatabase
from irspy.settings_ini_parser import BadIniException
from settings import get_clb_autocheck_settings
from tests_tree_widget import TestsTreeWidget
from test_graph_dialog import TestGraphDialog
from settings_dialog import SettingsDialog
from test_conductor import TestsConductor
from irspy.qt.qt_utils import QTextEditLogger
from clb_tests import tests_base
import tests_factory
from irspy import utils


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
            self.settings = get_clb_autocheck_settings()
        except BadIniException:
            QtWidgets.QMessageBox.critical(
                self, "Ошибка", 'Файл конфигурации поврежден. Пожалуйста, удалите файл '
                                '"settings.ini" и запустите программу заново')
            self.close()
            return

        self.settings.restore_qwidget_state(self)
        self.settings.restore_qwidget_state(self.ui.splitter)
        self.settings.restore_qwidget_state(self.ui.splitter_2)
        self.settings.restore_qwidget_state(self.ui.tests_tree)

        self.set_up_logger()

        self.clb_driver = clb_dll.clb_dll

        modbus_registers_count = 700
        self.usb_driver = clb_dll.UsbDrv(self.clb_driver, modbus_registers_count * 2)
        self.usb_state = clb_dll.UsbDrv.UsbState.DISABLED
        self.calibrator = clb_dll.ClbDrv(self.clb_driver)
        self.clb_state = clb.State.DISCONNECTED

        if not os.path.isfile(f"./{clb.CLB_CONFIG_NAME}"):
            QtWidgets.QMessageBox.critical(
                self, "Ошибка", f'Не найден файл конфигурации сетевых переменных калибратора '
                                f'"./{clb.CLB_CONFIG_NAME}"')
            self.close()
            return

        self.netvars = NetworkVariables(f"./{clb.CLB_CONFIG_NAME}", self.calibrator)
        self.netvars_db = NetvarsDatabase("./netvars.db", self)

        self.clb_signal_off_timer = QtCore.QTimer()
        # noinspection PyTypeChecker
        self.clb_signal_off_timer.timeout.connect(self.close)
        self.SIGNAL_OFF_TIME_MS = 200

        self.previous_id = 0

        self.ui.enter_settings_action.triggered.connect(self.open_settings)

        self.ui.errors_out_button.clicked.connect(self.start_errors_output)

        self.source_mode_widget = self.set_up_source_mode_widget()
        self.show()

        self.tests = tests_factory.create_tests(self.calibrator, self.netvars, self.netvars_db,
                                                self.settings)

        self.tests_widget = TestsTreeWidget(self.tests, self.ui.tests_tree, self.settings)
        self.tests_widget.show_graph_requested.connect(self.show_test_graph)
        self.tests_widget.show_errors_requested.connect(self.show_test_errors)
        self.graphs_dialogs: Dict[Tuple[str, str], QtWidgets.QDialog] = {}
        self.errors_dialogs: Dict[Tuple[str, str], QtWidgets.QDialog] = {}

        self.test_conductor = TestsConductor(self.tests)
        self.ui.autocheck_start_button.clicked.connect(self.autocheck_button_clicked)
        self.test_conductor.tests_done.connect(self.stop_autocheck)
        self.test_conductor.test_status_changed.connect(self.set_test_status)

        self.ui.open_tstlan_button.clicked.connect(self.open_tstlan)

        self.ui.save_button.clicked.connect(self.save_button_clicked)
        self.ui.load_button.clicked.connect(self.load_results)
        self.ui.clear_results_button.clicked.connect(self.clear_results)

        self.tick_timer = QtCore.QTimer(self)
        self.tick_timer.timeout.connect(self.tick)
        self.tick_timer.start(10)

        self.update_netvars_timer = QtCore.QTimer()
        self.update_netvars_timer.timeout.connect(self.update_netvars)
        self.update_netvars_timer.start(self.settings.tstlan_update_time * 1000)

        self.next_error_timer = QtCore.QTimer()
        self.next_error_timer.timeout.connect(self.show_next_error)
        self.next_error_index = 0

    def set_up_logger(self):
        log = QTextEditLogger(self.ui.log_text_edit)
        log.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%H:%M:%S'))

        logging.getLogger().addHandler(log)
        # logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger().setLevel(logging.INFO)
        # logging.getLogger().setLevel(logging.WARN)

    def set_up_source_mode_widget(self) -> SourceModeWidget:
        source_mode_widget = SourceModeWidget(self.settings, self.calibrator, self)
        self.clb_list_changed.connect(source_mode_widget.update_clb_list)
        self.usb_status_changed.connect(source_mode_widget.update_clb_status)
        self.signal_enable_changed.connect(source_mode_widget.signal_enable_changed)
        self.ui.control_box.layout().addWidget(source_mode_widget)
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

        current_id = self.netvars.id.get()
        if current_id != self.previous_id:
            if current_id != 0:
                self.previous_id = current_id
                self.clear_results()

    def update_netvars(self):
        self.ui.fast_adc_label.setText(
            f"{utils.float_to_string(self.netvars.fast_adc_slow.get())}")

        firmware_type = "RELEASE" if self.netvars.release_firmware.get() else "DEBUG"
        self.ui.firmware_info_label.setText(
            f"{self.netvars.software_revision.get()} {firmware_type}")

        self.ui.errors_count_label.setText(str(self.netvars.error_count.get()))
        if self.netvars.error_count.get() > 0:
            self.ui.errors_label.setStyleSheet("QLabel { color : red; }")
        else:
            self.ui.errors_label.setStyleSheet("QLabel { color : black; }")

    def lock_interface(self, a_lock):
        self.ui.control_box.setDisabled(a_lock)
        self.tests_widget.lock_interface(a_lock)
        self.ui.load_button.setDisabled(a_lock)
        self.ui.save_button.setDisabled(a_lock)
        self.ui.clear_results_button.setDisabled(a_lock)

    def autocheck_button_clicked(self):
        try:
            if self.test_conductor.started():
                self.test_conductor.stop()
                self.stop_autocheck()
            else:
                self.start_autocheck()
        except Exception as err:
            logging.debug(utils.exception_handler(err))

    def start_autocheck(self):
        if self.calibrator.state != clb.State.DISCONNECTED:
            aux_group_enabled = self.tests_widget.is_group_enabled("Предварительные стабилизаторы")
            if aux_group_enabled is None:
                logging.warning('Группа Предварительные стабилизаторы" не найдена')

            elif self.netvars.software_revision.get() < 295 and aux_group_enabled:
                QtWidgets.QMessageBox.warning(
                    self, "Ошибка", "Тест предварительных стабилизаторов доступен для прошивок "
                    "старше 294 ревизии", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.Yes)
            elif self.netvars.source_manual_mode_password.get() != clb.MANUAL_MODE_ENABLE_PASSWORD:
                self.lock_interface(True)
                self.test_conductor.set_enabled_tests(self.tests_widget.get_tests_repeat_count())
                self.ui.autocheck_start_button.setText("Остановить")
                self.test_conductor.start()

                self.ui.loader_label.show()
                self.loader.start()
            else:
                logging.warning(
                    "Включен ручной режим. Перезагрузите калибратор, чтобы запустить проверку")
        else:
            logging.warning("Калибратор не подключен, невозможно провести проверку")

    def stop_autocheck(self):
        self.lock_interface(False)
        self.ui.autocheck_start_button.setText("Старт")
        logging.info("Проверка завершена")

        self.ui.loader_label.hide()
        self.loader.stop()

    def set_test_status(self, a_group_name, a_test_name: str, a_status: tests_base.ClbTest.Status,
                        a_success_count: int):
        try:
            self.tests_widget.set_test_status(a_group_name, a_test_name, a_status, a_success_count)
        except AssertionError as err:
            logging.debug(utils.exception_handler(err))

    def open_tstlan(self):
        try:
            tstlan_dialog = TstlanDialog(self.netvars, self.calibrator, self.settings, self)
            tstlan_dialog.exec()
        except Exception as err:
            logging.debug(utils.exception_handler(err))

    def show_test_graph(self, a_group: str, a_name: str):
        try:
            graph_data = self.test_conductor.get_test_graph(a_group, a_name)
            if graph_data:
                try:
                    graphs_dialog = self.graphs_dialogs[(a_group, a_name)]
                    graphs_dialog.activateWindow()
                except KeyError:
                    graphs_dialog = TestGraphDialog(graph_data, self.settings, self)
                    graphs_dialog.setWindowTitle(f'Графики теста "{a_group}: {a_name}"')
                    self.graphs_dialogs[(a_group, a_name)] = graphs_dialog
                    self.test_conductor.graphs_have_been_updated.connect(graphs_dialog.update_graphs)
                    graphs_dialog.exec()
                    del self.graphs_dialogs[(a_group, a_name)]
            else:
                logging.warning("График для выбранного измерения не создан")
        except Exception as err:
            logging.debug(utils.exception_handler(err))

    def show_test_errors(self, a_group: str, a_name: str):
        try:
            errors_list = self.test_conductor.get_test_errors(a_group, a_name)
            has_errors = True if any(error != "" for error in errors_list) else False
            if has_errors:
                try:
                    errors_dialog = self.errors_dialogs[(a_group, a_name)]
                    errors_dialog.activateWindow()
                except KeyError:
                    nl = "\n"
                    errors_list = [
                        f'<p style=" color:#ff0000;">Тест №{num + 1}</p>{error.replace(nl, "<br>")}'
                        for num, error in enumerate(errors_list)
                    ]

                    errors_dialog = DialogWithText(errors_list, self.settings, self)
                    errors_dialog.setWindowTitle(f'Ошибки теста "{a_group}: {a_name}"')
                    self.errors_dialogs[(a_group, a_name)] = errors_dialog
                    errors_dialog.exec()
                    del self.errors_dialogs[(a_group, a_name)]
            else:
                logging.warning("Выбранный тест не содержит ошибок")
        except Exception as err:
            logging.debug(utils.exception_handler(err))

    @utils.exception_decorator
    def save_button_clicked(self, _):
        suggest_filename = \
            f"{QtCore.QDate.currentDate().toString('yyyyMMdd')} N4-25 №{self.netvars.id.get()}"
        chosen_file, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Сохранить результаты",
            f"{self.settings.last_save_results_folder}/{suggest_filename}",
            "Результаты проверки (*.car)")
        if chosen_file != "":
            results = {}
            for test in self.tests:
                test_results = self.test_conductor.get_test_results(test.group(), test.name())
                results[f"{test.group()}:{test.name()}"] = test_results.data_to_serialize()
            results["log"] = self.ui.log_text_edit.toPlainText()

            with open(chosen_file, 'w') as file:
                file.write(json.dumps(results, indent=4))

    @utils.exception_decorator
    def load_results(self, _):
        chosen_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Выберите файл", self.settings.last_save_results_folder,
            "Результаты проверки (*.car)")
        if chosen_file != "":
            self.settings.last_save_results_folder = chosen_file[:chosen_file.rfind("/")]

            with open(chosen_file, 'r') as file:
                test_results: Dict[str, Dict] = json.load(file)

            self.ui.log_text_edit.setPlainText(test_results["log"])
            del test_results["log"]

            for test_name in test_results.keys():
                sep = test_name.find(':')
                group, name = test_name[:sep], test_name[sep + 1:]

                try:
                    self.test_conductor.set_test_results(group, name, test_results[test_name])
                except ValueError:
                    logging.warning(f"Тест {group}: {name} не найден! Результаты не восстановлены")

    def clear_results(self):
        for test in self.tests:
            test_results = self.test_conductor.get_test_results(test.group(), test.name())
            test_results.delete_results()
            self.tests_widget.set_test_status(
                test.group(), test.name(), test_results.get_final_status(),
                test_results.get_success_results_count())

    def start_errors_output(self):
        if self.netvars.error_count.get() > 0:
            self.next_error_index = 0
            self.next_error_timer.start(1200)

    def show_next_error(self):
        error_index = self.netvars.error_index.get()
        error_count = self.netvars.error_count.get()
        if error_index >= error_count:
            # На случай если во время вывода ошибок их состояние было изменено извне
            self.next_error_timer.stop()
        else:
            if self.next_error_index == error_index:
                error_code = self.netvars.error_code.get()
                logging.warning(f"Ошибка №{error_index + 1}: "
                                f"Код {error_code}. {clb.error_code_to_message[error_code]}.")

                next_error_index = error_index + 1
                if next_error_index >= error_count:
                    self.netvars.clear_error_occurred_status.set(1)
                    self.next_error_timer.stop()
                else:
                    self.next_error_index = next_error_index
                    self.netvars.error_index.set(next_error_index)

    def open_settings(self):
        try:
            settings_dialog = SettingsDialog(self.settings, self.netvars_db, self)
            settings_dialog.exec()
        except Exception as err:
            logging.debug(utils.exception_handler(err))

    def closeEvent(self, a_event: QtGui.QCloseEvent):
        if self.calibrator.signal_enable:
            self.calibrator.signal_enable = False
            self.clb_signal_off_timer.start(self.SIGNAL_OFF_TIME_MS)
            a_event.ignore()
        else:
            self.settings.save_qwidget_state(self.ui.splitter_2)
            self.settings.save_qwidget_state(self.ui.splitter)
            self.settings.save_qwidget_state(self.ui.tests_tree)
            self.settings.save_qwidget_state(self)
            self.tests_widget.save()
            a_event.accept()
