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

        self.setGeometry(200, 200, 800, 300)
        self.setWindowTitle("Color Lab")
        self.setWindowFlags(QtCore.Qt.Window)

        header = QtGui.QLabel("Color Node")
        # header.setStyleSheet('font-size: 30px; font-family: Arial;')
        header.move(10, 10)

        grid = QtGui.QGridLayout()
        grid_widget = QtGui.QWidget()
        grid_widget.setLayout(grid)

        scroll = QtGui.QScrollArea()
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(grid_widget)

        save_button = QtGui.QPushButton('Save')
        # save_button.setStyleSheet('font-size: 20px; font-family: Arial;')
        save_button.setFixedWidth(100)
        save_button.clicked.connect(lambda: self._saveChanged())

        apply_button = QtGui.QPushButton('Apply')
        # apply_button.setStyleSheet('font-size: 20px; font-family: Arial;')
        apply_button.setFixedWidth(100)
        apply_button.clicked.connect(lambda: self._applyToScene(grid))

        add_button = QtGui.QPushButton('Add')
        # add_button.setStyleSheet('font-size: 20px; font-family: Arial;')
        add_button.setFixedWidth(100)
        add_button.clicked.connect(lambda: self._addRow(grid))

        qhbox = QtGui.QHBoxLayout()
        qhbox.addWidget(save_button)
        qhbox.addWidget(apply_button)
        qhbox.addWidget(add_button)
        qhbox.insertStretch(2)

        qvbox = QtGui.QVBoxLayout()
        qvbox.addWidget(scroll)
        qvbox.addLayout(qhbox)

        self.setLayout(qvbox)


        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = ColorLab()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()