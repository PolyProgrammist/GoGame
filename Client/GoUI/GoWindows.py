import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import  QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QWidgetItem

from Client.GoUI.GoBoardUI import GoBoardUI


class GOQT(QWidget):
    def __init__(self, maingo):
        super().__init__()
        self.maingo = maingo
        self.initUI()

    def initUI(self):
        self.move(0, 0)
        self.setWindowTitle('Go')

        self.hb = QHBoxLayout()
        self.hb.setContentsMargins(0, 0, 0, 0)
        self.oldSizeConstraing = self.hb.sizeConstraint()

        self.stack = QStackedWidget()
        self.authorizeWidget = AuthorizeWidget(self.maingo, self)
        self.changeWidget(self.authorizeWidget)

        self.hb.addWidget(self.stack)
        self.setLayout(self.hb)
        self.show()

    def changeWidget(self, widget, oldsize=True):
        if oldsize:
            self.hb.setSizeConstraint(self.oldSizeConstraing)
        else:
            self.hb.setSizeConstraint(QLayout.SetFixedSize)
        if self.stack.currentWidget() != 0:
            self.stack.removeWidget(self.stack.currentWidget())
        self.stack.addWidget(widget)
        self.stack.setCurrentWidget(widget)

class AuthorizeWidget(QWidget):
    def __init__(self, maingo, mainWidget):
        super().__init__()
        self.maingo = maingo
        self.mainWidget = mainWidget
        self.mainWidget.setFixedSize(200, 100)
        self.setLayout(self.authorizeLayout())

    def authorizeLayout(self):
        btnok = QPushButton("OK")
        tfName = QLineEdit()
        tfName.setPlaceholderText('Enter the name')
        tfName.setMaxLength(16)
        tfName.returnPressed.connect(btnok.click)
        vl = QVBoxLayout()
        vl.addWidget(tfName)
        vl.addWidget(btnok)
        btnok.clicked.connect(lambda: self.changeWidget(tfName))
        return vl

    def changeWidget(self, tfName):
        text = tfName.text()
        if text == '':
            text = 'guest'
        self.maingo.protor.auth(text)
        self.maingo.name = text

    def answerRequest(self, answer):
        if answer.find('authok') == 0:
            answer = answer[7:]
            self.maingo.protor.myname = answer
            self.maingo.goui.connectWidget = ConnectWidget(self.maingo)
            self.mainWidget.changeWidget(self.maingo.goui.connectWidget)
        else:
            QMessageBox.critical(self, 'Go', "This user already exists")

class ConnectWidget(QWidget):
    def __init__(self, maingo):
        super().__init__()
        self.maingo = maingo
        self.mainWidget = self.maingo.goui
        self.mainWidget.setFixedSize(350, 350)
        self.find_mate_layout = self.findMateLayout()
        self.clearLayout(self.vl)
        self.setLayout(self.find_mate_layout)

    def findMateLayout(self):
        layout = QVBoxLayout()
        self.vl = QVBoxLayout()
        from PyQt5.QtCore import Qt
        self.vl.setAlignment(Qt.AlignTop)
        # refresh = QPushButton('Refresh')
        # refresh.clicked.connect(self.maingo.protor.get_list)
        # layout.addWidget(refresh)
        s = ('You are: ' + self.maingo.name)
        layout.addWidget(self.getLabelWithFont(s, 14))
        layout.addWidget(self.getScrollWidget())
        return layout

    def getNames(self):
        return self.maingo.protor.availibleUsers

    def refresh(self):
        self.getNamesLayout(self.getNames())

    def getNamesLayout(self, names):
        self.clearLayout(self.vl)
        if len(names) == 0:
            self.vl.addWidget(self.getLabelWithFont('No availible opponnets', 14))
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

    def getLabelWithFont(self, s, fontSize):
        label = QLabel(s)
        self.setFontSize(label, fontSize)
        return label

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
        self.maingo.protor.connect(user)
        #self.mainWidget.changeWidget(self.mainWidget.gameWidget)
    def startGame(self):
        self.maingo.goui.gameWidget = GoBoardUI(self.maingo)
        self.mainWidget.changeWidget(self.maingo.goui.gameWidget, False)