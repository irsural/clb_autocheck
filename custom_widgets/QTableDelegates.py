from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget

from custom_widgets.CustomLineEdit import QEditDoubleClick


class NonOverlappingPainter(QtWidgets.QStyledItemDelegate):
    def __init__(self, a_parent=None):
        super().__init__(a_parent)

    def paint(self, painter: QtGui.QPainter, option, index: QtCore.QModelIndex):
        background = index.data(QtCore.Qt.BackgroundRole)
        if isinstance(background, QtGui.QBrush):
            if background.color() != QtCore.Qt.white:
                # WARNING Чтобы drawText работал правильно, нужно чтобы в ui форме в QTable
                # был явно прописан размер шрифта!!!
                painter.fillRect(option.rect, background)
                text_rect = option.rect
                # Не знаю как получить нормальный прямоугольник для отрисовки текста, поэтому только так
                text_rect.setLeft(text_rect.left() + 3)
                painter.drawText(text_rect, option.displayAlignment, index.data())
            else:
                super().paint(painter, option, index)
        else:
            super().paint(painter, option, index)


class TableEditDoubleClick(QtWidgets.QItemDelegate):
    def __init__(self, a_parent):
        super().__init__(a_parent)

    def createEditor(self, parent: QWidget, option, index: QtCore.QModelIndex) -> QWidget:
        return QEditDoubleClick(parent)


class NonOverlappingDoubleClick(NonOverlappingPainter, TableEditDoubleClick):
    def __init__(self, a_parent):
        super().__init__(a_parent)
