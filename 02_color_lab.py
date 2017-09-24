import collections, json, os, re, sys
# import hou
from PySide import QtGui, QtCore

CURRENT_PATH = os.path.dirname(__file__)
JSON_PATH = os.path.join(CURRENT_PATH, "config/color_config.json")
ROW_COUNT = 0

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
        save_button.clicked.connect(lambda: self.saveChanged())

        apply_button = QtGui.QPushButton('Apply')
        # apply_button.setStyleSheet('font-size: 20px; font-family: Arial;')
        apply_button.setFixedWidth(100)
        apply_button.clicked.connect(lambda: self.applyToScene(grid))

        add_button = QtGui.QPushButton('Add')
        # add_button.setStyleSheet('font-size: 20px; font-family: Arial;')
        add_button.setFixedWidth(100)
        add_button.clicked.connect(lambda: self.addRow(grid))

        qhbox = QtGui.QHBoxLayout()
        qhbox.addWidget(save_button)
        qhbox.addWidget(apply_button)
        qhbox.addWidget(add_button)
        qhbox.insertStretch(2)

        qvbox = QtGui.QVBoxLayout()
        qvbox.addWidget(scroll)
        qvbox.addLayout(qhbox)

        self.setLayout(qvbox)

        self.buidInterface(grid)

        self.show()

    def addRow(self, grid):
        global ROW_COUNT
        temp = grid.itemAtPosition(grid.rowCount() - 1, 4)
        if temp is not None:
            temp.widget().deleteLater()
            grid.removeItem(temp)
            ROW_COUNT -= 1

        grid_label = QtGui.QLabel("  Color {}".format(str(ROW_COUNT+1).zfill(2)))
        grid_label.setFixedWidth(110)

        grid_color = QtGui.QPushButton("")
        grid_color.setText("Select Color")
        grid_color.setFixedHeight(30)
        grid_color.setFixedWidth(150)
        grid_color.clicked.connect(lambda: self.setColor(grid, grid_color))

        grid_text = "test"
        # grid_text = DropLineEdit(self, grid)
        # grid_text.setFiexdHeight(30)
        # grid_text.setText('"Node Type",')
        # grid_text.setDragEnable(True)
        # grid_text.setFocusPolicy(QtCore.Qt.ClickFocus)
        # grid_text.returnPressed.connect(lambda: colorDict(grid))
        # grid_text.returnPressed.connect(lambda: self.nodeTypeCheck(grid_text, grid))

        grid_node = QtGui.QPushButton("")
        grid_node.setText("Add Node")
        grid_node.setFixedHeight(30)
        grid_node.setToolTip('Add selected node')
        grid_node.clicked.connect(lambda: self.addNode(grid, grid_node))

        grid_del = QtGui.QPushButton("")
        grid_del.setText("X")
        grid_del.setFixedHeight(30)
        grid_del.setToolTip('Delete this row')
        grid_del.clicked.connect(lambda: self.deleteRow(grid, grid_del))

        cur_row = grid.rowCount()

        grid.addWidget(grid_label, cur_row, 0)
        grid.addWidget(grid_color, cur_row, 1)
        # grid.addWidget(grid_text, cur_row, 2)
        grid.addWidget(grid_node, cur_row, 3)
        grid.addWidget(grid_del, cur_row, 4)

        ROW_COUNT += 1

        dummy = QtGui.QWidget()
        dummy.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        grid.addWidget(dummy, grid.rowCount(), 4)

        ROW_COUNT += 1

        return (grid_color, grid_text)

    def buidInterface(self, grid):
        global JSON_PATH
        file_open = open(JSON_PATH)
        stored = json.loads(file_open.read())
        file_open.close()
        stored = collections.OrderedDict(sorted(stored["ALL_COLORS"].items()))
        for key, value in stored.iteritems():
            new_obj = self.addRow(grid)
            col_obj = new_obj[0]
            str_obj = new_obj[1]
            idx = int(key.split("_")[0])
            color = key.split("_")[1]

            col_obj.setStyleSheet('QPushButton {background-color: %s}' % str(color))
            col_obj.setText(" ")
            # str_obj.setText(value)
        del stored

def main():
    app = QtGui.QApplication(sys.argv)
    ex = ColorLab()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()