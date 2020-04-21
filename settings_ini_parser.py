from enum import IntEnum
from typing import List
import configparser
import logging
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

    CHECKBOX_STATES_DEFAULT = "0"

    FIXED_STEP_IDX_KEY = "fixed_step_idx"
    FIXED_STEP_IDX_DEFAULT = "0"

    STEP_ROUGH_KEY = "rough_step"
    STEP_ROUGH_DEFAULT = "0.5"

    STEP_COMMON_KEY = "common_step"
    STEP_COMMON_DEFAULT = "0.05"

    STEP_EXACT_KEY = "exact_step"
    STEP_EXACT_DEFAULT = "0.002"

    TSTLAN_UPDATE_TIME_KEY = "tstlan_update_time"
    TSTLAN_UPDATE_TIME_DEFAULT = "1"

    TSTLAN_SHOW_MARKS_KEY = "tstlan_show_marks"
    TSTLAN_SHOW_MARKS_DEFAULT = "0"

    TSTLAN_MARKS_KEY = "tstlan_marks"
    TSTLAN_MARKS_DEFAULT = "0"

    TESTS_REPEAT_COUNT_KEY = "tests_repeat_count"
    TESTS_REPEAT_COUNT_DEFAULT = "0"

    TESTS_COLLAPSED_STATES_KEY = "tests_collapsed_states"
    TESTS_COLLAPSED_STATES_DEFAULT = "0"

    GEOMETRY_SECTION = "Geometry"
    HEADERS_SECTION = "Headers"

    CHECKBOX_STATES_KEY = "checkbox_states"

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

        self.__checkbox_states = []

        self.__rough_step = 0
        self.__common_step = 0
        self.__exact_step = 0

        self.__tstlan_update_time = 0
        self.__tstlan_show_marks = 0
        self.__tstlan_makrs = []

        self.__tests_repeat_count = []
        self.__tests_collapsed_states = []

        self.settings = configparser.ConfigParser()
        try:
            self.restore_settings()
        except configparser.ParsingError:
            raise BadIniException

    # noinspection DuplicatedCode
    def restore_settings(self):
        if not os.path.exists(self.CONFIG_PATH):
            self.settings[self.MEASURE_SECTION] = {
                self.FIXED_STEP_KEY: self.FIXED_STEP_DEFAULT,
                self.FIXED_STEP_IDX_KEY: self.FIXED_STEP_IDX_DEFAULT,
                self.STEP_ROUGH_KEY: self.STEP_ROUGH_DEFAULT,
                self.STEP_COMMON_KEY: self.STEP_COMMON_DEFAULT,
                self.STEP_EXACT_KEY: self.STEP_EXACT_DEFAULT,
                self.TSTLAN_UPDATE_TIME_KEY: self.TSTLAN_UPDATE_TIME_DEFAULT,
                self.TSTLAN_SHOW_MARKS_KEY: self.TSTLAN_SHOW_MARKS_DEFAULT,
                self.TSTLAN_MARKS_KEY: self.TSTLAN_MARKS_DEFAULT,
                self.TESTS_REPEAT_COUNT_KEY: self.TESTS_REPEAT_COUNT_DEFAULT,
                self.TESTS_COLLAPSED_STATES_KEY: self.TESTS_COLLAPSED_STATES_DEFAULT
            }
            utils.save_settings(self.CONFIG_PATH, self.settings)
        else:
            self.settings.read(self.CONFIG_PATH)
            self.add_ini_section(self.MEASURE_SECTION)

        self.__fixed_step_list = self.check_ini_value(self.MEASURE_SECTION, self.FIXED_STEP_KEY,
                                                      self.FIXED_STEP_DEFAULT, self.ValueType.LIST_FLOAT)

        self.__checkbox_states = self.check_ini_value(self.MEASURE_SECTION, self.CHECKBOX_STATES_KEY,
                                                      self.CHECKBOX_STATES_DEFAULT, self.ValueType.LIST_INT)

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

        self.__tstlan_update_time = self.check_ini_value(self.MEASURE_SECTION, self.TSTLAN_UPDATE_TIME_KEY,
                                                         self.TSTLAN_UPDATE_TIME_DEFAULT, self.ValueType.FLOAT)
        self.__tstlan_update_time = utils.bound(self.__tstlan_update_time, 0.1, 100.)

        self.__tstlan_show_marks = self.check_ini_value(self.MEASURE_SECTION, self.TSTLAN_SHOW_MARKS_KEY,
                                                        self.TSTLAN_SHOW_MARKS_DEFAULT, self.ValueType.INT)
        self.__tstlan_show_marks = utils.bound(self.__tstlan_show_marks, 0, 1)

        self.__tstlan_makrs = self.check_ini_value(self.MEASURE_SECTION, self.TSTLAN_MARKS_KEY,
                                                   self.TSTLAN_MARKS_DEFAULT, self.ValueType.LIST_INT)

        self.__tests_repeat_count = self.check_ini_value(self.MEASURE_SECTION, self.TESTS_REPEAT_COUNT_KEY,
                                                         self.TESTS_REPEAT_COUNT_DEFAULT, self.ValueType.LIST_INT)

        self.__tests_collapsed_states = self.check_ini_value(self.MEASURE_SECTION, self.TESTS_COLLAPSED_STATES_KEY,
                                                             self.TESTS_COLLAPSED_STATES_DEFAULT,
                                                             self.ValueType.LIST_INT)

    def add_ini_section(self, a_name: str):
        if not self.settings.has_section(a_name):
            self.settings.add_section(a_name)

    def check_ini_value(self, a_section, a_key, a_default, a_value_type: ValueType):
        try:
            value = self.ValueTypeConvertFoo[a_value_type](self.settings[a_section][a_key])
        except (KeyError, ValueError) as err:
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
            print(utils.exception_handler(err))

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
    def enabled_tests_list(self):
        return self.__checkbox_states

    @enabled_tests_list.setter
    def enabled_tests_list(self, a_list: List[int]):
        saved_string = ','.join(str(val) for val in a_list)
        saved_string = saved_string.strip(',')

        self.settings[self.GEOMETRY_SECTION][self.CHECKBOX_STATES_KEY] = saved_string
        self.save()

        self.__checkbox_states = a_list

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
    def tstlan_update_time(self):
        return self.__tstlan_update_time

    @tstlan_update_time.setter
    def tstlan_update_time(self, a_time: float):
        self.settings[self.MEASURE_SECTION][self.TSTLAN_UPDATE_TIME_KEY] = str(a_time)
        self.save()

        self.__tstlan_update_time = a_time
        self.__tstlan_update_time = utils.bound(self.__tstlan_update_time, 0.1, 100.)

    @property
    def tstlan_show_marks(self):
        return self.__tstlan_show_marks

    @tstlan_show_marks.setter
    def tstlan_show_marks(self, a_enable: int):
        self.settings[self.MEASURE_SECTION][self.TSTLAN_SHOW_MARKS_KEY] = str(a_enable)
        self.save()

        self.__tstlan_show_marks = a_enable
        self.__tstlan_show_marks = utils.bound(self.__tstlan_show_marks, 0, 1)

    @property
    def tstlan_marks(self):
        return self.__tstlan_makrs

    @tstlan_marks.setter
    def tstlan_marks(self, a_list: List[int]):
        saved_string = ','.join(str(val) for val in a_list)
        saved_string = saved_string.strip(',')

        self.settings[self.MEASURE_SECTION][self.TSTLAN_MARKS_KEY] = saved_string
        self.save()

        self.__tstlan_makrs = a_list

    @property
    def tests_repeat_count(self):
        return self.__tests_repeat_count

    @tests_repeat_count.setter
    def tests_repeat_count(self, a_list: List[int]):
        saved_string = ','.join(str(val) for val in a_list)
        saved_string = saved_string.strip(',')

        self.settings[self.MEASURE_SECTION][self.TESTS_REPEAT_COUNT_KEY] = saved_string
        self.save()

        self.__tests_repeat_count = a_list

    @property
    def tests_collapsed_states(self):
        return self.__tests_collapsed_states

    @tests_collapsed_states.setter
    def tests_collapsed_states(self, a_list: List[int]):
        saved_string = ','.join(str(val) for val in a_list)
        saved_string = saved_string.strip(',')

        self.settings[self.MEASURE_SECTION][self.TESTS_COLLAPSED_STATES_KEY] = saved_string
        self.save()

        self.__tests_collapsed_states = a_list
