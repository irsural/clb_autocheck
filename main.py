import ui_to_py
ui_to_py.convert_ui("./ui", "./ui/py")
ui_to_py.convert_resources("./resources", ".")

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

from mainwindow import MainWindow
from utils import exception_decorator_print


@exception_decorator_print
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    translator = QtCore.QTranslator(app)
    path = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)
    translator.load("/".join([path, "qtbase_ru.qm"]))
    app.installTranslator(translator)

    w = MainWindow()
    sys.exit(app.exec())

# Сборка через pyinstaller
# Закомментарить первые 3 строки этого файла
# pyinstaller -n clb_autocheck --onefile --noconsole --icon=main_icon.ico --add-data C:\Windows\System32\vcruntime140d.dll;. --add-data C:\Windows\System32\ucrtbased.dll;. main.py



if __name__ == "__main__":
    main()
    input("Error. Press enter to continue...")
