import os, sys
from hutil.Qt.QtCore import *
from hutil.Qt.QtGui import *
from hutil.Qt.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(hou.qt.styleSheet())
        self.setProperty("houdiniStyle", True)
        self.setWindowTitle('Houdini16 Python Test')

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        g_layout = QVBoxLayout()
        layout = QFormLayout()
        main_widget.setLayout(g_layout)

        self.parm = QSpinBox()
        self.parm.setValue(30)
        layout.addRow('Parameter', self.parm)
        self.exec_btn = QPushButton('Button')

        g_layout.addLayout(layout)
        g_layout.addWidget(self.exec_btn)

w = MainWindow()

w.show()
