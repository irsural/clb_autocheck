from enum import IntEnum
from typing import List
import configparser
import base64
import os

from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore

import utils


class BadIniException(Exception):
    pass


class Settings(QtCore.QObject):
    CONFIG_PATH = "./settings.ini"

    class ValueType(IntEnum):
        INT = 0
        FLOAT = 1
        LIST_FLOAT = 2
        LIST_INT = 3
        STRING = 4

    ValueTypeConvertFoo = {
        ValueType.INT: int,
        ValueType.FLOAT: float,
        ValueType.LIST_FLOAT: lambda s: [float(val) for val in s.split(',')],
        ValueType.LIST_INT: lambda s: [int(val) for val in s.split(',')],
        ValueType.STRING: str
    }

    MEASURE_SECTION = "Measure"
    FIXED_STEP_KEY = "fixed_step_list"
    FIXED_STEP_DEFAULT = "0.0001,0.01,0.1,1,10,20,100"

    FIXED_STEP_IDX_KEY = "fixed_step_idx"
    FIXED_STEP_IDX_DEFAULT = "0"

    STEP_ROUGH_KEY = "rough_step"
    STEP_ROUGH_DEFAULT = "0.5"

    STEP_COMMON_KEY = "common_step"
    STEP_COMMON_DEFAULT = "0.05"

    STEP_EXACT_KEY = "exact_step"
    STEP_EXACT_DEFAULT = "0.002"

    START_DEVIATION_KEY = "start_deviation"
    START_DEVIATION_DEFAULT = "5"

    MOUSE_INVERSION_KEY = "mouse_inversion"
    MOUSE_INVERSION_DEFAULT = "0"

    DISABLE_SCROLL_ON_TABLE_KEY = "disable_scroll_on_table"
    DISABLE_SCROLL_ON_TABLE_DEFAULT = "0"

    GEOMETRY_SECTION = "Geometry"
    HEADERS_SECTION = "Headers"

    PROTOCOL_SECTION = "Protocol"
    TEMPLATE_FILEPATH_KEY = "template_filepath"
    SAVE_FOLDER_KEY = "save_folder"

    # В ini файлы сохраняются QByteArray, в которых могут быть переносы строки, которые херят ini файл
    LF = '\n'
    LF_SUBSTITUTE = "\t\t\t\t"
    CR = '\r'
    CR_SUBSTITUTE = '\f\f\f\f'

    fixed_step_changed = pyqtSignal()

    def __init__(self, a_parent=None):
        super().__init__(a_parent)

        self.__fixed_step_list = []
        self.__fixed_step_idx = 0

        self.__rough_step = 0
        self.__common_step = 0
        self.__exact_step = 0
        self.__start_deviation = 0
        self.__mouse_inversion = 0

        self.__disable_scroll_on_table = 0

        self.__template_filepath = ""
        self.__save_folder = ""

        self.settings = configparser.ConfigParser()
        try:
            self.restore_settings()
        except configparser.ParsingError:
            raise BadIniException

    # noinspection DuplicatedCode
    def restore_settings(self):
        if not os.path.exists(self.CONFIG_PATH):
            self.settings[self.MEASURE_SECTION] = {self.FIXED_STEP_KEY: self.FIXED_STEP_DEFAULT,
                                                   self.FIXED_STEP_IDX_KEY: self.FIXED_STEP_IDX_DEFAULT,
                                                   self.STEP_ROUGH_KEY: self.STEP_ROUGH_DEFAULT,
                                                   self.STEP_COMMON_KEY: self.STEP_COMMON_DEFAULT,
                                                   self.STEP_EXACT_KEY: self.STEP_EXACT_DEFAULT,
                                                   self.START_DEVIATION_KEY: self.START_DEVIATION_DEFAULT,
                                                   self.MOUSE_INVERSION_KEY: self.MOUSE_INVERSION_DEFAULT,
                                                   self.DISABLE_SCROLL_ON_TABLE_KEY:
                                                       self.DISABLE_SCROLL_ON_TABLE_DEFAULT}
            self.settings[self.PROTOCOL_SECTION] = {self.TEMPLATE_FILEPATH_KEY: "",
                                                    self.SAVE_FOLDER_KEY: ""}
            utils.save_settings(self.CONFIG_PATH, self.settings)
        else:
            self.settings.read(self.CONFIG_PATH)
            self.add_ini_section(self.MEASURE_SECTION)
            self.add_ini_section(self.PROTOCOL_SECTION)

        self.__fixed_step_list = self.check_ini_value(self.MEASURE_SECTION, self.FIXED_STEP_KEY,
                                                      self.FIXED_STEP_DEFAULT, self.ValueType.LIST_FLOAT)

        self.__fixed_step_idx = self.check_ini_value(self.MEASURE_SECTION, self.FIXED_STEP_IDX_KEY,
                                                     self.FIXED_STEP_IDX_DEFAULT, self.ValueType.INT)
        self.__fixed_step_idx = utils.bound(self.__fixed_step_idx, 0, len(self.__fixed_step_list) - 1)

        self.__rough_step = self.check_ini_value(self.MEASURE_SECTION, self.STEP_ROUGH_KEY,
                                                 self.STEP_ROUGH_DEFAULT, self.ValueType.FLOAT)
        self.__rough_step = utils.bound(self.__rough_step, 0., 100.)

        self.__common_step = self.check_ini_value(self.MEASURE_SECTION, self.STEP_COMMON_KEY,
                                                  self.STEP_COMMON_DEFAULT, self.ValueType.FLOAT)
        self.__common_step = utils.bound(self.__common_step, 0., 100.)

        self.__exact_step = self.check_ini_value(self.MEASURE_SECTION, self.STEP_EXACT_KEY,
                                                 self.STEP_EXACT_DEFAULT, self.ValueType.FLOAT)
        self.__exact_step = utils.bound(self.__exact_step, 0., 100.)

        self.__start_deviation = self.check_ini_value(self.MEASURE_SECTION, self.START_DEVIATION_KEY,
                                                      self.START_DEVIATION_DEFAULT, self.ValueType.INT)
        self.__start_deviation = utils.bound(self.__start_deviation, 0, 100)

        self.__mouse_inversion = self.check_ini_value(self.MEASURE_SECTION, self.MOUSE_INVERSION_KEY,
                                                      self.MOUSE_INVERSION_DEFAULT, self.ValueType.INT)
        self.__mouse_inversion = utils.bound(self.__mouse_inversion, 0, 1)

        self.__disable_scroll_on_table = self.check_ini_value(self.MEASURE_SECTION, self.DISABLE_SCROLL_ON_TABLE_KEY,
                                                              self.DISABLE_SCROLL_ON_TABLE_DEFAULT, self.ValueType.INT)
        self.__disable_scroll_on_table = utils.bound(self.__disable_scroll_on_table, 0, 1)

        self.__template_filepath = self.check_ini_value(self.PROTOCOL_SECTION, self.TEMPLATE_FILEPATH_KEY,
                                                        "", self.ValueType.STRING)

        self.__save_folder = self.check_ini_value(self.PROTOCOL_SECTION, self.SAVE_FOLDER_KEY,
                                                  "", self.ValueType.STRING)
        # Выводит ini файл в консоль
        # for key in settings:
        #     print(f"[{key}]")
        #     for subkey in settings[key]:
        #         print(f"{subkey} = {settings[key][subkey]}")

    def add_ini_section(self, a_name: str):
        if not self.settings.has_section(a_name):
            self.settings.add_section(a_name)

    def check_ini_value(self, a_section, a_key, a_default, a_value_type: ValueType):
        try:
            value = self.ValueTypeConvertFoo[a_value_type](self.settings[a_section][a_key])
        except (KeyError, ValueError):
            self.settings[a_section][a_key] = a_default
            utils.save_settings(self.CONFIG_PATH, self.settings)
            value = self.ValueTypeConvertFoo[a_value_type](a_default)
        return value

    def save(self):
        utils.save_settings(self.CONFIG_PATH, self.settings)

    def save_geometry(self, a_window_name: str, a_geometry: QtCore.QByteArray):
        try:
            self.add_ini_section(self.GEOMETRY_SECTION)

            self.settings[self.GEOMETRY_SECTION][a_window_name] = self.__to_base64(a_geometry)

            self.save()
        except Exception as err:
            utils.exception_handler(err)

    def get_last_geometry(self, a_window_name: str):
        try:
            geometry_bytes = self.settings[self.GEOMETRY_SECTION][a_window_name]
            return QtCore.QByteArray(self.__from_base64(geometry_bytes))
        except (KeyError, ValueError):
            return QtCore.QByteArray()

    def save_header_state(self, a_header_name: str, a_state: QtCore.QByteArray):
        self.add_ini_section(self.HEADERS_SECTION)

        self.settings[self.HEADERS_SECTION][a_header_name] = self.__to_base64(a_state)
        self.save()

    def get_last_header_state(self, a_header_name: str):
        try:
            state_bytes = self.settings[self.HEADERS_SECTION][a_header_name]
            return QtCore.QByteArray(self.__from_base64(state_bytes))
        except (KeyError, ValueError):
            return QtCore.QByteArray()

    @staticmethod
    def __to_base64(a_qt_bytes: QtCore.QByteArray):
        return base64.b64encode(bytes(a_qt_bytes)).decode()

    @staticmethod
    def __from_base64(a_string: str):
        return base64.b64decode(a_string)

    @property
    def fixed_step_list(self):
        return self.__fixed_step_list

    @fixed_step_list.setter
    def fixed_step_list(self, a_list: List[float]):
        # Удаляет дубликаты
        final_list = list(dict.fromkeys(a_list))
        final_list.sort()

        saved_string = ','.join(str(val) for val in final_list)
        saved_string = saved_string.strip(',')

        self.settings[self.MEASURE_SECTION][self.FIXED_STEP_KEY] = saved_string
        self.save()

        self.__fixed_step_list = [val for val in final_list]
        self.__fixed_step_idx = utils.bound(self.__fixed_step_idx, 0, len(self.__fixed_step_list) - 1)
        self.fixed_step_changed.emit()

    @property
    def fixed_step_idx(self):
        return self.__fixed_step_idx

    @fixed_step_idx.setter
    def fixed_step_idx(self, a_idx: int):
        self.settings[self.MEASURE_SECTION][self.FIXED_STEP_IDX_KEY] = str(a_idx)
        self.save()

        self.__fixed_step_idx = a_idx
        self.__fixed_step_idx = utils.bound(self.__fixed_step_idx, 0, len(self.__fixed_step_list) - 1)

    @property
    def rough_step(self):
        return self.__rough_step

    @rough_step.setter
    def rough_step(self, a_step: float):
        self.settings[self.MEASURE_SECTION][self.STEP_ROUGH_KEY] = str(a_step)
        self.save()

        self.__rough_step = a_step
        self.__rough_step = utils.bound(self.__rough_step, 0., 100.)

    @property
    def common_step(self):
        return self.__common_step

    @common_step.setter
    def common_step(self, a_step: float):
        self.settings[self.MEASURE_SECTION][self.STEP_COMMON_KEY] = str(a_step)
        self.save()

        self.__common_step = a_step
        self.__common_step = utils.bound(self.__common_step, 0., 100.)

    @property
    def exact_step(self):
        return self.__exact_step

    @exact_step.setter
    def exact_step(self, a_step: float):
        self.settings[self.MEASURE_SECTION][self.STEP_EXACT_KEY] = str(a_step)
        self.save()

        self.__exact_step = a_step
        self.__exact_step = utils.bound(self.__exact_step, 0., 100.)

    @property
    def start_deviation(self):
        return self.__start_deviation

    @start_deviation.setter
    def start_deviation(self, a_step: int):
        self.settings[self.MEASURE_SECTION][self.START_DEVIATION_KEY] = str(a_step)
        self.save()

        self.__start_deviation = a_step
        self.__start_deviation = utils.bound(self.__start_deviation, 0, 100)

    @property
    def mouse_inversion(self):
        return self.__mouse_inversion

    @mouse_inversion.setter
    def mouse_inversion(self, a_enable: int):
        self.settings[self.MEASURE_SECTION][self.MOUSE_INVERSION_KEY] = str(a_enable)
        self.save()

        self.__mouse_inversion = a_enable
        self.__mouse_inversion = utils.bound(self.__mouse_inversion, 0, 1)

    @property
    def disable_scroll_on_table(self):
        return self.__disable_scroll_on_table

    @disable_scroll_on_table.setter
    def disable_scroll_on_table(self, a_enable: int):
        self.settings[self.MEASURE_SECTION][self.DISABLE_SCROLL_ON_TABLE_KEY] = str(a_enable)
        self.save()

        self.__disable_scroll_on_table = a_enable
        self.__disable_scroll_on_table = utils.bound(self.__disable_scroll_on_table, 0, 1)

    @property
    def template_filepath(self):
        return self.__template_filepath

    @template_filepath.setter
    def template_filepath(self, a_filepath: str):
        self.settings[self.PROTOCOL_SECTION][self.TEMPLATE_FILEPATH_KEY] = a_filepath
        self.save()

        self.__template_filepath = a_filepath

    @property
    def save_folder(self):
        return self.__save_folder

    @save_folder.setter
    def save_folder(self, a_filepath: str):
        self.settings[self.PROTOCOL_SECTION][self.SAVE_FOLDER_KEY] = a_filepath
        self.save()

        self.__save_folder = a_filepath
