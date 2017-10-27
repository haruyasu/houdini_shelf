import sys
from PySide.QtGui import *
from PySide.QtCore import *

class GUI(QWidget):
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        self.initUI()

    def initUI(self):
        pass

def main():
    app = QApplication(sys.argv)
    ui = GUI()
    ui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()