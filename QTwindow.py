import sys, random

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QErrorMessage
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QStackedLayout
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


class GOQT(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(150, 200)
        self.setWindowTitle('Go')

        self.authorizeWidget = QWidget()
        self.authorizeWidget.setLayout(self.authorizeLayout())
        self.connectWidgettttt = QWidget()
        self.connectWidget = QWidget()

        self.stack = QStackedWidget()
        self.stack.addWidget(self.authorizeWidget)
        self.stack.addWidget(self.connectWidget)
        self.stack.setCurrentWidget(self.authorizeWidget)

        hb = QHBoxLayout()
        hb.addWidget(self.stack)

        self.setLayout(hb)
        self.show()

    def authorizeLayout(self):
        btnok = QPushButton("OK")
        btnGoGuest = QPushButton("Go guest")
        tfName = QLineEdit()
        tfName.setPlaceholderText('Enter the name')
        vl = QVBoxLayout()
        vl.addWidget(tfName)
        vl.addWidget(btnok)
        vl.addWidget(btnGoGuest)
        btnok.clicked.connect(lambda: self.lololo(tfName))
        return vl

    def lololo(self, tfName):
        if tfName.text() == '':
            QMessageBox.critical(self, 'Go', "You have not entered a name")
            return
        #if not self.authorize(tfName.text()):
           # return
        self.findMateLayout()

    def findMateLayout(self):
        self.mates = ['Bazilio', 'Alice']
        self.mates += ['a' * 16] * 100
        vl = QVBoxLayout()
        for m in self.mates:
            bconnect = QPushButton('Connect')
            bconnect.setFixedWidth(100)
            font = QFont()
            font.setPointSize(14)
            lbname = QLabel(m)
            lbname.setFont(font)
            bconnect.clicked.connect(lambda sl, tm = m: self.connectUser(tm))
            qh = QHBoxLayout()
            qh.addWidget(lbname)
            qh.addWidget(bconnect)
            vl.addLayout(qh)

        self.connectWidgettttt.setLayout(vl)

        scroll = QScrollArea()
        scroll.setWidget(self.connectWidgettttt)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(300)
        scroll.setFixedWidth(300)
        layout = QVBoxLayout()
        layout.addWidget(scroll)
        self.connectWidget.setLayout(layout)

        self.stack.setCurrentWidget(self.connectWidget)

    def connectUser(self, user):
        print(user)


if __name__ == '__main__':
    app = QApplication([])
    go = GOQT()
    sys.exit(app.exec_())