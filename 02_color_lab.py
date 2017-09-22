import collections, json, os, re, sys
# import hou
from PySide import QtGui, QtCore

class ColorLab(QtGui.QWidget):
    def __init__(self):
        super(ColorLab, self).__init__()
        self.initUI()

    def initUI(self):
        app = QtGui.QApplication.instance()
        cursor_pos = QtGui.QCursor().pos()
        parent = app.topLevelAt(cursor_pos)

        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("Color Lab")
        self.setWindowFlags(QtCore.Qt.Window)

        header = QtGui.QLabel("Color Node")
        header.setStyleSheet('front-size: 30px; font-family: Arial;')
        header.move(10, 10)



        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = ColorLab()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()