import sys
from PySide.QtGui import *
from PySide.QtCore import *

parm = kwargs["parms"][0]
parmTmp = parm.parmTemplate()
node = parm.node()
parmGroup = node.parmTemplateGroup()

class GUI(QWidget):
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        self.initUI()

    def initUI(self):
        mpos = QCursor().pos()
        self.setGeometry(mpos.x() - 100, mpos.y() - 100, 300, 200)
        self.setWindowTitle("Insert Parm")

        label_Name = QLabel("Name: ")
        label_Label = QLabel("Label: ")
        Type_Label = QLabel("Type: ")

        text_Name = QLineEdit("newParm")
        text_Name.textChanged.connect(lambda: self.onTextChanged(text_Name, text_Label))
        text_Label = QLineEdit("newLabel")

        parmType = QComboBox(self)
        parmType.addItems(["Float",
                           "Vector",
                           "Int",
                           "String",
                           "Ramp_Float",
                           "Ramp_Color"
                           ])

        button = QPushButton("Create Parm")
        button.clicked.connect(lambda: self.pressButon(text_Name.text(), text_Label.text(), parmType.currentText()))
        self.onTextChanged(text_Name, text_Label)

        Lbox = QGridLayout()
        Lbox.addWidget(label_Name, 0, 0)
        Lbox.addWidget(label_Label, 1, 0)
        Lbox.addWidget(Type_Label, 2, 0)
        Lbox.addWidget(text_Name, 0, 1)
        Lbox.addWidget(text_Label, 1, 1)
        Lbox.addWidget(parmType, 2, 1)
        Lbox.addWidget(button, 3, 1)
        self.setLayout(Lbox)

    def pressButton(self, name, label, ptype):
        if not parmGroup.find(name):
            if ptype == "Float":
                newParm = hou.FloatParmTemplate(name, label, 1)
            elif ptype == "Vector":
                newParm = hou.FloatParmTemplate(name, label, 3)
            elif ptype == "Int":
                newParm = hou.IntParmTemplate(name, label, 1)
            elif ptype == "String":
                newParm = hou.StringParmTemplate(name, label, 1)
            elif ptype == "Ramp_Float":
                newParm = hou.RampParmTemplate(name, label, ramp_parm_type=hou.rampParmType.Float)
            elif ptype == "Ramp_Color":
                newParm = hou.RampParmTemplate(name, label, ramp_parm_type=hou.rampParmType.Color)

            parmGroup.insertAfter(parmTmp, newParm)
            node.setParmTemplateGroup(parmGroup)
        else:
            msgBox = QMessageBox(self)
            msgBox.setText('"%s" is Already Exist' % name)
            msgBox.show()
        self.close()

    def onTextChanged(self, name, label):
        if not parmGroup.find(name.text()):
            name.setStyleSheet("background-color: rgb(255, 255, 255);")
        else:
            name.setStyleSheet("background-color: rgb(255, 107, 107);")
        text = name.text()
        label.setText(text[0].upper() + text[1:])

def main():
    app = QApplication(sys.argv)
    ui = GUI()
    ui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()