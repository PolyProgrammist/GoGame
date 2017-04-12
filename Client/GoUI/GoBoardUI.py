from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from Client.GoUI.JustBoardUI import JustBoardUI
from Client.GoUI.GoTimer import Timer


class GoBoardUI(QWidget):
    def __init__(self, maingo):
        super().__init__()
        self.maingo = maingo
        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSizeConstraint(QLayout.SetFixedSize)

        self.setLayout(self.layout)
        self.setlabels()
        self.setbuttons()
        self.setboard()

    def setlabels(self):
        lt = QHBoxLayout()
        self.layout.addLayout(lt)
        self.labmy = self.getLabelWithFont('You: ' + self.maingo.protor.myname, 20)
        self.labop = self.getLabelWithFont('Opponent: ' + self.maingo.protor.othername, 20)

        ltmy = QHBoxLayout()
        ltop = QHBoxLayout()
        ltmy.addWidget(self.labmy)
        self.timmy = Timer(self.maingo, ltmy, self.maingo.protor.step)
        ltop.addWidget(self.labop)
        self.timop = Timer(self.maingo, ltop, not self.maingo.protor.step)

        lt.addLayout(ltmy)
        lt.addLayout(ltop)


    def setbuttons(self):
        lt = QHBoxLayout()
        self.layout.addLayout(lt)

        btlose = QPushButton('Surrender')
        btchangegame = QPushButton('Change Game')

        btlose.clicked.connect(self.maingo.protor.surrender)
        btchangegame.clicked.connect(self.change_game)

        self.setFontSize(btlose, 16)
        self.setFontSize(btchangegame, 16)

        lt.addWidget(btlose)
        lt.addWidget(btchangegame)

    def setboard(self):
        board_size = 800
        step = 50
        self.maingo.goui.setFixedWidth(board_size)
        self.justBoard = JustBoardUI(self.maingo, board_size, self)
        self.layout.addWidget(self.justBoard)

    def change_game(self):
        self.maingo.protor.surrender()
        self.maingo.protor.get_list()
        self.maingo.goui.authorizeWidget.answerRequest('authok')

    def getLabelWithFont(self, s, fontSize):
        label = QLabel(s)
        self.setFontSize(label, fontSize)
        return label

    def setFontSize(self, label, fontSize):
        font = QFont()
        font.setPointSize(fontSize)
        label.setFont(font)

    def win(self):
        self.gameover()
        QMessageBox.about(self, 'Win', 'You win!')
    def lose(self):
        self.gameover()
        QMessageBox.about(self, 'Lose', 'You lose!')

    def gameover(self):
        self.timmy.timer.stop()
        self.timop.timer.stop()
        self.justBoard.set_lab_color(self.labmy, 2)
        self.justBoard.set_lab_color(self.labop, 2)


