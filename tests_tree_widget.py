from typing import List
import logging

from PyQt5 import QtCore, QtWidgets, QtGui

from clb_tests import ClbTest
import utils


class TestsTreeWidget:
    def __init__(self, a_tree_widget: QtWidgets.QTreeWidget):
        self.tree_widget = a_tree_widget

        self.tree_widget.expandAll()
        # self.tree_widget.setColumnWidth(0, 270)
        self.tree_widget.setColumnWidth(1, 50)

        self.tests_map = {}

        test_number = 0
        it = QtWidgets.QTreeWidgetItemIterator(self.tree_widget)
        while it.value():
            # Если у узла нет дочерних узлов, считаем его тестом, если есть, то считаем его группой
            if it.value().childCount() == 0:
                logging.debug(it.value().text(0))
                self.tests_map[test_number] = it.value()
                test_number += 1
            it += 1

    def lock_interface(self, a_lock: bool):
        try:
            it = QtWidgets.QTreeWidgetItemIterator(self.tree_widget)
            while it.value():
                item = it.value()
                if a_lock:
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsUserCheckable)
                else:
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                it += 1
        except Exception as err:
            print(utils.exception_handler(err))

    def get_enabled_tests(self) -> List[bool]:
        return [True] * len(self.tests_map)

    def set_test_status(self, a_test_number, a_status: ClbTest.Status):
        status_label = QtWidgets.QLabel()
        if a_status == ClbTest.Status.NOT_CHECKED:
            status_label.setText("...")
        if a_status == ClbTest.Status.IN_PROCESS:
            status_label.setText("wait")
        if a_status == ClbTest.Status.SUCCESS:
            status_label.setText("ok")
        if a_status == ClbTest.Status.FAIL:
            status_label.setText("fail")
