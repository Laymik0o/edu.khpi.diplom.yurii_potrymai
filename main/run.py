import sys
from PyQt5 import QtWidgets
import main.work_with_ui as start


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = start.MyApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()