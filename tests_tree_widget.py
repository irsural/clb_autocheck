from typing import List, Tuple
from enum import IntEnum
import logging

from PyQt5 import QtCore, QtWidgets, QtGui

from clb_tests_base import ClbTest
from settings_ini_parser import Settings
import utils


class TestsTreeWidget:
    class Column(IntEnum):
        TESTS_TREE = 0
        REPEAT_COUNT = 1
        SUCCESS_COUNT = 2
        STATUS = 3

    def __init__(self, a_tests: List[ClbTest], a_tree_widget: QtWidgets.QTreeWidget, a_settings: Settings):
        self.tree_widget = a_tree_widget
        self.settings = a_settings

        self.create_tree(a_tests)
        self.tree_widget.expandAll()

        try:
            self.restore_checkboxes_state()
        except IndexError:
            pass

    # noinspection PyTypeChecker
    def create_tree(self, a_tests: List[ClbTest]):
        top_item = QtWidgets.QTreeWidgetItem(self.tree_widget, ["Тесты"])
        top_item.setCheckState(0, QtCore.Qt.Checked)
        top_item.setFlags(top_item.flags() | QtCore.Qt.ItemIsTristate)
        self.tree_widget.addTopLevelItem(top_item)
        for idx, test in enumerate(a_tests):
            group_items = self.tree_widget.findItems(test.group(), QtCore.Qt.MatchFixedString |
                                                     QtCore.Qt.MatchCaseSensitive | QtCore.Qt.MatchRecursive)
            if group_items:
                assert len(group_items) == 1, "Группы не должны повторяться !"
                group_item = group_items[0]
            else:
                group_item = QtWidgets.QTreeWidgetItem(top_item, [test.group()])
                group_item.setCheckState(0, QtCore.Qt.Checked)
                group_item.setFlags(group_item.flags() | QtCore.Qt.ItemIsTristate)

                status_label = QtWidgets.QLabel()
                status_label.setAlignment(QtCore.Qt.AlignCenter)
                self.set_status_icon(status_label, ClbTest.Status.NOT_CHECKED)
                self.tree_widget.setItemWidget(group_item, TestsTreeWidget.Column.STATUS, status_label)

                top_item.addChild(group_item)

            test_item = QtWidgets.QTreeWidgetItem(group_item, [test.name()])
            test_item.setCheckState(0, QtCore.Qt.Checked)

            status_label = QtWidgets.QLabel()
            status_label.setAlignment(QtCore.Qt.AlignCenter)
            self.set_status_icon(status_label, ClbTest.Status.NOT_CHECKED)
            self.tree_widget.setItemWidget(test_item, TestsTreeWidget.Column.STATUS, status_label)

            repeat_spinbox = SpinBoxIgnoreWheel()
            repeat_spinbox.setMinimum(1)
            repeat_spinbox.setMaximum(99)
            try:
                repeat_spinbox.setValue(self.settings.tests_repeat_count[idx])
            except IndexError:
                repeat_spinbox.setValue(1)

            self.tree_widget.setItemWidget(test_item, TestsTreeWidget.Column.REPEAT_COUNT, repeat_spinbox)

            success_label = QtWidgets.QLabel("0")
            success_label.setAlignment(QtCore.Qt.AlignCenter)
            self.tree_widget.setItemWidget(test_item, TestsTreeWidget.Column.SUCCESS_COUNT, success_label)

            group_item.addChild(test_item)

    @staticmethod
    def set_status_icon(a_label: QtWidgets.QLabel, a_status: ClbTest.Status):
        a_label.setProperty("status", int(a_status))
        if a_status == ClbTest.Status.NOT_CHECKED:
            pixmap = QtGui.QPixmap(":/icons/icons/checkbox_empty.png")

        elif a_status == ClbTest.Status.IN_PROCESS:
            pixmap = None

            loader = QtGui.QMovie(":/icons/gif/loader.gif")
            loader.setScaledSize(QtCore.QSize(25, 25))
            a_label.setMovie(loader)
            loader.start()

        elif a_status == ClbTest.Status.SUCCESS:
            pixmap = QtGui.QPixmap(":/icons/icons/checkbox_ok.png")

        else: # a_status == ClbTest.Status.FAIL:
            pixmap = QtGui.QPixmap(":/icons/icons/checkbox_fail.png")

        if pixmap is not None:
            a_label.setPixmap(pixmap.scaled(25, 25))

    # noinspection PyTypeChecker
    def lock_interface(self, a_lock: bool):
        it = QtWidgets.QTreeWidgetItemIterator(self.tree_widget)
        while it.value():
            item = it.value()
            if a_lock:
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsUserCheckable)
            else:
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)

            repeat_count_widget = self.tree_widget.itemWidget(item, self.Column.REPEAT_COUNT)
            if repeat_count_widget is not None:
                repeat_count_widget.setDisabled(a_lock)

            it += 1

    def get_tests_repeat_count(self) -> List[Tuple[str, str, int]]:
        enabled_tests = []
        it = QtWidgets.QTreeWidgetItemIterator(self.tree_widget)
        while it.value():
            item = it.value()
            # Если у узла нет дочерних узлов, считаем его тестом, если есть, то считаем его группой
            if item.childCount() == 0 and item.checkState(TestsTreeWidget.Column.TESTS_TREE) == QtCore.Qt.Checked:
                test_group = item.parent().text(TestsTreeWidget.Column.TESTS_TREE)
                test_name = item.text(TestsTreeWidget.Column.TESTS_TREE)
                test_repeat_count = self.tree_widget.itemWidget(item, self.Column.REPEAT_COUNT).value()
                enabled_tests.append((test_group, test_name, test_repeat_count))
            it += 1
        return enabled_tests

    def find_test_item(self, a_group_name: str, a_test_name: str) -> QtWidgets.QTreeWidgetItem:
        matched_tests = self.tree_widget.findItems(a_test_name, QtCore.Qt.MatchFixedString |
                                                   QtCore.Qt.MatchCaseSensitive | QtCore.Qt.MatchRecursive)
        for test in matched_tests:
            if test.parent().text(TestsTreeWidget.Column.TESTS_TREE) == a_group_name and test.childCount() == 0:
                return test
        assert True, f'Тест "{a_group_name}: {a_test_name}" не найден !!'

    def get_group_status(self, a_group_item) -> ClbTest.Status:
        group_status = ClbTest.Status.NOT_CHECKED
        all_success = True
        for child_idx in range(a_group_item.childCount()):
            child = a_group_item.child(child_idx)
            child_status = self.tree_widget.itemWidget(child, TestsTreeWidget.Column.STATUS).property("status")
            if child_status == ClbTest.Status.IN_PROCESS:
                group_status = ClbTest.Status.IN_PROCESS
                all_success = False
                break
            elif child_status == ClbTest.Status.FAIL:
                group_status = ClbTest.Status.FAIL
                all_success = False
            elif child_status == ClbTest.Status.NOT_CHECKED:
                all_success = False

        if all_success:
            group_status = ClbTest.Status.SUCCESS
        return group_status

    # noinspection PyTypeChecker
    def set_test_status(self, a_group_name: str, a_test_name: str, a_status: ClbTest.Status):
        test_item = self.find_test_item(a_group_name, a_test_name)
        status_label = self.tree_widget.itemWidget(test_item, TestsTreeWidget.Column.STATUS)
        self.set_status_icon(status_label, a_status)

        group_item = test_item.parent()
        status_label = self.tree_widget.itemWidget(group_item, TestsTreeWidget.Column.STATUS)
        self.set_status_icon(status_label, self.get_group_status(group_item))

    def restore_checkboxes_state(self):
        enabled_list = self.settings.enabled_tests_list
        idx = 0
        it = QtWidgets.QTreeWidgetItemIterator(self.tree_widget)
        while it.value():
            it.value().setCheckState(0, QtCore.Qt.CheckState(enabled_list[idx]))
            idx += 1
            it += 1

    def save_checkboxes_state(self):
        enabled_list = []
        idx = 0
        it = QtWidgets.QTreeWidgetItemIterator(self.tree_widget)
        while it.value():
            enabled_list += [it.value().checkState(TestsTreeWidget.Column.TESTS_TREE)]
            idx += 1
            it += 1

        self.settings.enabled_tests_list = enabled_list

    def save_repeat_count(self):
        repeat_count = []

        it = QtWidgets.QTreeWidgetItemIterator(self.tree_widget)
        while it.value():
            item = it.value()
            repeat_count_widget = self.tree_widget.itemWidget(item, self.Column.REPEAT_COUNT)
            if repeat_count_widget is not None:
                repeat_count.append(repeat_count_widget.value())

            it += 1

        self.settings.tests_repeat_count = repeat_count

    def save(self):
        self.save_checkboxes_state()
        self.save_repeat_count()


class SpinBoxIgnoreWheel(QtWidgets.QSpinBox):
    def wheelEvent(self, event):
        event.ignore()
