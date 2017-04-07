import sys, random

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import  QApplication
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QWidgetItem

from GoUIQT import GoUIQT


class GOQT(QWidget):
    def __init__(self, maingo):
        super().__init__()
        self.maingo = maingo
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Go')
        self.authorizeWidget = AuthorizeWidget(self, self.maingo)
        self.connectWidget = ConnectWidget(self, self.maingo)
        self.gameWidget = GoUIQT(self.maingo)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.authorizeWidget)
        self.stack.addWidget(self.connectWidget)
        self.stack.addWidget(self.gameWidget)

        self.changeWidget(self.authorizeWidget)
        hb = QHBoxLayout()
        hb.addWidget(self.stack)

        self.setLayout(hb)
        self.show()

    def changeWidget(self, widget):
        widget.recreate()
        self.stack.setCurrentWidget(widget)
        self.setFixedSize(*widget.sizes)

class AuthorizeWidget(QWidget):
    def __init__(self, mainWidget, maingo):
        super().__init__()
        self.mainWidget = mainWidget
        self.maingo = maingo
        self.sizes = (200, 200)

    def recreate(self):
        self.setLayout(self.authorizeLayout())

    def authorizeLayout(self):
        btnok = QPushButton("OK")
        btnGoGuest = QPushButton("Go guest")
        tfName = QLineEdit()
        tfName.setPlaceholderText('Enter the name')
        tfName.returnPressed.connect(btnok.click)
        vl = QVBoxLayout()
        vl.addWidget(tfName)
        vl.addWidget(btnok)
        vl.addWidget(btnGoGuest)
        btnok.clicked.connect(lambda: self.changeWidget(tfName))
        return vl

    def changeWidget(self, tfName):
        if tfName.text() == '':
            QMessageBox.critical(self, 'Go', "You have not entered a name")
            return
        self.maingo.connector.snd('auth ' + tfName.text())
        self.mainWidget.changeWidget(self.mainWidget.connectWidget)
        self.maingo.connector.snd('list')

class ConnectWidget(QWidget):
    def __init__(self, mainWidget, maingo):
        super().__init__()
        self.mainWidget = mainWidget
        self.maingo = maingo
        self.sizes = (350, 350)

    def recreate(self):
        self.setLayout(self.findMateLayout())

    def findMateLayout(self):
        layout = QVBoxLayout()
        refresh = QPushButton('Refresh')
        self.vl = QVBoxLayout()
        refresh.clicked.connect(lambda : self.maingo.connector.snd('list'))

        layout.addWidget(refresh)
        layout.addWidget(self.getScrollWidget())
        return layout

    def getNames(self):
        return self.maingo.connector.availibleUsers

    def refresh(self):
        self.getNamesLayout(self.getNames())

    def getNamesLayout(self, names):
        self.clearLayout(self.vl)
        for m in names:
            lbname = QLabel(m)
            self.setFontSize(lbname, 14)

            bconnect = QPushButton('Connect')
            bconnect.setFixedWidth(100)
            bconnect.clicked.connect(lambda sl, tm=m: self.connectUser(tm))

            qh = QHBoxLayout()
            qh.addWidget(lbname)
            qh.addWidget(bconnect)

            self.vl.addLayout(qh)

    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if isinstance(item, QWidgetItem):
                item.widget().close()
            elif isinstance(item, QSpacerItem):
                a = 0
            else:
                self.clearLayout(item.layout())
            layout.removeItem(item)

    def setFontSize(self, label, fontSize):
        font = QFont()
        font.setPointSize(fontSize)
        label.setFont(font)

    def getScrollWidget(self):
        contentLayout = self.vl
        tmpWidget = QWidget()
        tmpWidget.setLayout(contentLayout)
        scroll = QScrollArea()
        scroll.setWidget(tmpWidget)
        scroll.setWidgetResizable(True)
        scroll.maximumSize()
        return scroll

    def connectUser(self, user):
        self.maingo.connector.snd('connect ' + user)
        #self.mainWidget.changeWidget(self.mainWidget.gameWidget)
    def startGame(self):
        self.mainWidget.changeWidget(self.mainWidget.gameWidget)

if __name__ == '__main__':
    app = QApplication([])
    go = GOQT()
    sys.exit(app.exec_())