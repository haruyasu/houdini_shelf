import collections, json, os, re, sys
# import hou
from PySide import QtGui, QtCore

CURRENT_PATH = os.path.dirname(__file__)
JSON_PATH = os.path.join(CURRENT_PATH, "config/color_config.json")
ROW_COUNT = 0
COL_DIC = {}
COL_DIC["ALL_COLORS"] = {}
COL_DIC["ALL_NODES"] = {}

def buildTypeList(a_grid):
    old_list = []
    for temp_row in range(a_grid.rowCount()):
        temp_layout = a_grid.itemAtPosition(temp_row, 2)
        if temp_layout is not None:
            old_list.extend(str(temp_layout.widget().text()).split(","))
    old_set = set(old_list)
    old_list = list(old_set)

    return old_list

def colorDict(grid):
    global COL_DIC
    default = '"Node Type",'

    COL_DIC["ALL_COLORS"] = {}
    COL_DIC["ALL_NODES"] = {}

    for row in range(grid.rowCount()):
        col_layout = grid.itemAtPosition(row, 1)
        if col_layout is not None:
            col_widget = col_layout.widget()
            col_text = col_widget.text()

            if not col_widget.text() == "Seclect Color":
                col_name = col_widget.palette().color(QtGui.QPalette.Window).name()
                col_rgbf = col_widget.palette().color(QtGui.QPalette.Window).getRgbF()

                text = grid.itemAtPosition(row, 2).widget().text()

                if not text == default and len(text):
                    label = grid.itemAtPosition(row, 0).widget().text()
                    idx = "".join([i for i in label if i.isdigit()])
                    COL_DIC["ALL_COLORS"]["".join([idx, "_", col_name])] = text

                    type_list = text.split(",")
                    col_tuple = (col_rgbf[0], col_rgbf[1], col_rgbf[2])
                    for entry in type_list:
                        COL_DIC["ALL_NODES"][entry] = col_tuple
    pass

class ColorLab(QtGui.QWidget):
    def __init__(self):
        super(ColorLab, self).__init__()
        self.initUI()

    def initUI(self):
        app = QtGui.QApplication.instance()
        cursor_pos = QtGui.QCursor().pos()
        parent = app.topLevelAt(cursor_pos)

        self.setGeometry(200, 200, 500, 300)
        self.setWindowTitle("Color Lab")
        self.setWindowFlags(QtCore.Qt.Window)

        # header = QtGui.QLabel("Color Node")
        # header.setStyleSheet('font-size: 30px; font-family: Arial;')
        # header.move(10, 10)

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
        save_button.clicked.connect(lambda: self.saveChanges())

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

        grid_label = QtGui.QLabel(" Color {}".format(str(ROW_COUNT+1).zfill(2)))
        grid_label.setFixedWidth(80)

        grid_color = QtGui.QPushButton("")
        grid_color.setText("Color")
        # grid_color.setFixedHeight(30)
        grid_color.setFixedWidth(80)
        grid_color.clicked.connect(lambda: self.setColor(grid, grid_color))

        grid_text = DropLineEdit(self, grid)
        # grid_text.setFixedHeight(30)
        grid_text.setText("")
        grid_text.setDragEnabled(True)
        grid_text.setFocusPolicy(QtCore.Qt.ClickFocus)
        grid_text.returnPressed.connect(lambda: colorDict(grid))
        grid_text.returnPressed.connect(lambda: self.nodeTypeCheck(grid_text, grid))

        grid_node = QtGui.QPushButton("")
        grid_node.setText("Add Node")
        # grid_node.setFixedHeight(30)
        grid_node.setToolTip('Add selected node')
        grid_node.clicked.connect(lambda: self.addNode(grid, grid_node))

        grid_del = QtGui.QPushButton("")
        grid_del.setText("Del")
        # grid_del.setFixedHeight(30)
        grid_del.setToolTip('Delete this row')
        grid_del.clicked.connect(lambda: self.deleteRow(grid, grid_del))

        cur_row = grid.rowCount()

        grid.addWidget(grid_label, cur_row, 0)
        grid.addWidget(grid_color, cur_row, 1)
        grid.addWidget(grid_text, cur_row, 2)
        grid.addWidget(grid_node, cur_row, 3)
        grid.addWidget(grid_del, cur_row, 4)

        ROW_COUNT += 1

        dummy = QtGui.QWidget()
        dummy.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        grid.addWidget(dummy, grid.rowCount(), 4)

        ROW_COUNT += 1

        return (grid_color, grid_text)

    def setColor(self, a_grid, button):
        col = QtGui.QColorDialog.getColor()
        col_css = 'QPushButton {background-color: %s;}' % str(col.name())

        button.setStyleSheet(col_css)
        button.setText(" ")

        if hou.selectedNodes():
            idx = a_grid.indexOf(button)
            row = a_grid.getItemPosition(idx)[0]
            str_field = a_grid.itemAtPosition(row, 2)
            if str_field is not None:
                cur_str_ls = [str(i) for i in str_field.widget().text().split(",")]
                col = col.getRgbF()
                hcol = hou.Color()
                hcol.setRGB((col[0], col[1], col[2]))

                for n in hou.selectedNodes():
                    if n.type().name() in cur_str_ls:
                        n.setColor(hcol)

        colorDict(a_grid)

    def deleteRow(self, a_grid, button):
        global ROW_COUNT

        idx = a_grid.indexOf(button)
        row = a_grid.getItemPosition(idx)[0]
        for col in range(a_grid.columnCount()):
            layout = a_grid.itemAtPosition(row, col)
            if layout is not None:
                layout.widget().deleteLater()
                a_grid.removeItem(layout)

        ROW_COUNT -= 1

        item_count = 1
        for row in range(a_grid.rowCount()):
            layout = a_grid.itemAtPosition(row, 0)
            if layout is not None:
                label = layout.widget()
                label.setText(" Color {}".format(str(item_count).zfill(2)))
                item_count += 1

        colorDict(a_grid)

    def addNode(self, a_grid, button):
        if hou.selectedNodes():
            idx = a_grid.indexOf(button)
            row = a_grid.getItemPosition(idx)[0]
            layout = a_grid.itemAtPosition(row, 2)
            str_list = []
            old_list = buildTypeList(a_grid)

            for n in hou.selectedNodes():
                add_str = n.type().name()
                if not add_str in str_list:
                    str_list.append(add_str)

            if layout is not None:
                content = layout.widget()
                nodeToQLineEdit(content, str_list, old_list, a_grid)
                colorNode(content, a_grid, None)

            colorDict(a_grid)

    def applyToScene(self, grid):
        global COL_DIC
        root = hou.node("/")

        colorDict(grid)

        for cur_node in root.allNodes():
            try:
                colors = tuple(COL_DIC["ALL_NODES"][cur_node.type().name()])
                hcol = hou.Color()
                hcol.setRGB(colors)
                cur_node.setColor(hcol)
            except:
                pass

    def saveChanges(self):
        global JSON_PATH
        global COL_DIC

        file_open = open(JSON_PATH, "w")
        b = json.dump(COL_DIC, file_open, indent=4, sort_keys=True)
        file_open.close()
        del b
        print "Save Changes"

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
            str_obj.setText(value)
        del stored

class DropLineEdit(QtGui.QLineEdit):
    def __init__(self, parent, a_grid):
        super(DropLineEdit, self).__init__(parent)
        self.a_grid = a_grid
        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        if data.text():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        if data.text():
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData()

        if data.text():
            idx = self.a_grid.indexOf(self)
            row = self.a_grid.getItemPosition(idx)[0]
            cur_str = self.text()
            str_list = []
            node_list = []

            old_list = buildTypeList(self.a_grid)

            node_paths = data.text().split(",")

            for entry in node_paths:
                if not hou.node(entry) is None:
                    node_list.append(hou.node(entry))
                    cur_type = hou.node(entry).type().name()
                    if not cur_type in str_list:
                        str_list.append(cur_type)

            nodeToQLineEdit(self, str_list, old_list, self.a_grid)
            colorNode(self, self.a_grid, node_list)
            colorDict(self.a_grid)

def main():
    app = QtGui.QApplication(sys.argv)
    ex = ColorLab()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()