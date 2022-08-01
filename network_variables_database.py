from typing import Tuple, Generator
from enum import IntEnum
from math import floor
import logging

from PyQt5 import QtGui, QtCore, QtWidgets, QtSql

from irspy.clb.network_variables import VariableInfo


class NetvarsDatabase(QtCore.QObject):
    class Column(IntEnum):
        ID = 0
        NAME = 1
        INDEX = 2
        TYPE = 3
        MIN = 4
        MAX = 5
        DEFAULT = 6

    model_updated = QtCore.pyqtSignal()

    def __init__(self, a_db_filename: str, a_parent: QtCore.QObject):
        super().__init__(a_parent)
        self.__db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.__db.setDatabaseName(a_db_filename)
        self.__db.open()
        self.__query = QtSql.QSqlQuery()
        self.__query.exec("CREATE TABLE IF NOT EXISTS netvars (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                          "name TEXT, _index REAL, type TEXT, min REAL, max REAL, _default REAL)")
        self.__allowed_types = ("double", "float", "bit", "u32", "i32", "u8", "i8", "u16", "i16", "bool", "u64", "i64")

        self.__model = QtSql.QSqlTableModel(a_parent)
        self.__model.setTable("netvars")
        self.__model.setSort(NetvarsDatabase.Column.INDEX, QtCore.Qt.AscendingOrder)

        headers = ["id", "Имя", "Индекс", "Тип", "Мин.", "Макс.", "По умолч."]
        for i in range(self.__model.columnCount()):
            self.__model.setHeaderData(i, QtCore.Qt.Horizontal, headers[i])
        self.__real_columns = (NetvarsDatabase.Column.INDEX, NetvarsDatabase.Column.MIN, NetvarsDatabase.Column.MAX,
                               NetvarsDatabase.Column.DEFAULT)
        self.__model.select()

        self.__model.dataChanged.connect(self.update_data)

    def update_data(self, a_top_left: QtCore.QModelIndex, a_bottom_right: QtCore.QModelIndex, a_roles):
        if a_top_left == a_bottom_right:
            # Фильтрация ввода пользователя
            column = a_top_left.column()
            data = a_top_left.data()
            input_is_correct = True
            if column in self.__real_columns:
                try:
                    float(data)
                except ValueError:
                    input_is_correct = False
            elif column == NetvarsDatabase.Column.TYPE:
                if data not in self.__allowed_types:
                    input_is_correct = False

            if input_is_correct:
                self.__model.submit()
            self.__model.select()
            self.model_updated.emit()

    def add_netvar(self):
        self.__query.exec("INSERT INTO netvars (name, _index, type, min, max, _default) "
                          "VALUES (NULL, NULL, 'double', NULL, NULL, NULL)")
        self.__model.select()
        self.model_updated.emit()

    def delete_netvar(self, a_row):
        self.__model.removeRow(a_row)
        self.__model.select()
        self.model_updated.emit()

    def get_variables(self) -> Generator[Tuple[VariableInfo, float, float, float], None, None]:
        for row in range(self.__model.rowCount()):
            float_index = float(self.__model.index(row, NetvarsDatabase.Column.INDEX).data())
            _type = self.__model.index(row, NetvarsDatabase.Column.TYPE).data()
            name = self.__model.index(row, NetvarsDatabase.Column.NAME).data()
            if _type == "bit":
                index = floor(float_index)
                bit_index = int(round((float_index - index) * 10, 2))
            else:
                index = int(float_index)
                bit_index = 0
            _min = self.__model.index(row, NetvarsDatabase.Column.MIN).data()
            _max = self.__model.index(row, NetvarsDatabase.Column.MAX).data()
            _default = self.__model.index(row, NetvarsDatabase.Column.DEFAULT).data()
            yield VariableInfo(a_index=index, a_bit_index=bit_index, a_type=_type, a_name=name), _min, _max, _default

    def model(self):
        return self.__model

    def allowed_types(self):
        return self.__allowed_types
