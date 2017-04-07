import threading
import sys
from PyQt5.QtCore import Qt

from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QStyle
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

import GoState

class GoUIQT(QWidget):
    def __init__(self, maingo):
        super().__init__()
        self.maingo = maingo
    def recreate(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.buttonHello = QPushButton('hello')
        layout.addWidget(self.buttonHello)
        board_display_size = 800
        step = 50
        self.justBoard = JustBoard(self.maingo, board_display_size)
        layout.addWidget(self.justBoard)
        self.sizes = (800, 850)
        self.justBoard.recreate()

class JustBoard(QWidget):
    gost = GoState.GoState()
    board_color = (0xC0, 0x40, 0x0)
    stone_color = ((50, 50, 50),(200, 200, 200))
    stone_Q_color = [QColor(*cl) for cl in stone_color]
    stone_diameter_fix = 0.9

    board_places = gost.board_size + 1

    need_now_stone = False

    def __init__(self, maingo, board_display_size):
        super().__init__()
        self.maingo = maingo
        self.board_display_size = board_display_size
        self.calc_constants()
        self.setFixedSize(self.board_display_size, self.full_display_height)
        #self.inlol()

    def calc_constants(self):
        self.score_display_height = 0
        self.full_display_height = self.score_display_height + self.board_display_size
        self.gap_size = self.board_display_size // 20
        self.full_add = self.score_display_height + self.gap_size
        self.ungap_coordY = self.full_display_height - self.gap_size
        self.ungap_coordX = self.board_display_size - self.gap_size
        self.field_size = self.board_display_size - 2 * self.gap_size
        self.cell_size = self.field_size // self.gost.board_size
        self.stone_radius = (int)((self.cell_size * self.stone_diameter_fix) / 2)


    def point_to_tuple(self, p):
        return (p.x(), p.y())


    def mouseMoveEvent(self, QMouseEvent):
        t = self.analyze_pos(self.point_to_tuple(QMouseEvent.pos()))
        if (t[0] != self.gost.freez and self.gost.places[t[0]][t[1]] == self.gost.freez):
            self.need_now_stone = True
            self.now_stone_pos = (self.gap_size + t[0] * self.cell_size, self.full_add + t[1] * self.cell_size)
        else:
            self.need_now_stone = False
        self.update()

    def mousePressEvent(self, QMouseEvent):
        t = self.analyze_pos(self.point_to_tuple(QMouseEvent.pos()))
        self.maingo.connector.go(t)
        #self.letsgo(t)

    def inlol(self):
        self.recreate()
        self.gost.now_color = 1  # black

    def letsgo(self, t):
        print('now')
        print(t)
        self.gost.try_pas(t, self.gost.now_color)
        self.update()

    def printtable(self):
        for i in self.places:
            for j in i:
                print(str(j) + ' ', end='', flush=True)
            print('')
        print()

    def analyze_coordinate(self, pos):
        pos -= self.gap_size
        t = round(pos / self.cell_size)
        if 0 <= t <= self.gost.board_size:
            return t
        else:
            return self.error_coordinate

    def analyze_pos(self, pos):
        a, b = self.analyze_coordinate(pos[0]), self.analyze_coordinate(pos[1] - self.score_display_height)
        if (a == self.gost.freez or b == self.gost.freez):
            return self.gost.freez, self.gost.freez
        else:
            return a, b

    def recreate(self):
        self.setMouseTracking(True)
        self.setFixedSize(self.board_display_size, self.full_display_height)
        self.setWindowTitle('Go')
        pal = QPalette()
        color = QColor(0xC0, 0x40, 0x0)
        pal.setColor(QPalette.Background, color)
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.show()

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.setBrush(QColor(100, 100, 100))
        self.redraw_background(painter)



    def draw_transparent_stone(self, painter, pos):
        painter = QPainter()
        painter.drawEllipse()

    def get_Qrect(self, x, y, r):
        return QRect(x - r, y - r, 2 * r, 2 * r)


    def redraw_background(self, painter):
        painter.drawLine(self.gap_size, self.full_add, self.gap_size, self.ungap_coordY)
        painter.drawLine(self.gap_size, self.full_add, self.ungap_coordX, self.full_add)
        painter.drawLine(self.gap_size, self.ungap_coordY, self.ungap_coordX, self.ungap_coordY)
        painter.drawLine(self.ungap_coordX, self.full_add, self.ungap_coordX, self.ungap_coordY)
        for i in range(self.gost.board_size):
            painter.drawLine(self.gap_size, self.full_add + i * self.cell_size,
                             self.ungap_coordX, self.full_add + i * self.cell_size)
            painter.drawLine(self.gap_size + i * self.cell_size, self.full_add,
                             self.gap_size + i * self.cell_size, self.ungap_coordY)

        if self.need_now_stone:
            painter.setBrush(self.stone_Q_color[self.gost.now_color])
            qrect = self.get_Qrect(self.now_stone_pos[0], self.now_stone_pos[1], self.stone_radius * 0.75)
            painter.drawEllipse(qrect)

        for i in range(self.board_places):
            for j in range(self.board_places):
                if self.gost.places[i][j] != self.gost.freez:
                    x, y, r = self.gap_size + i * self.cell_size, self.full_add + j * self.cell_size,self.stone_radius
                    cl = self.stone_Q_color[self.gost.places[i][j]]
                    painter.setBrush(cl)
                    painter.drawEllipse(self.get_Qrect(x, y, r))

if __name__ == '__main__':
    app = QApplication([])
    goqt = GoUIQT(5)
    sys.exit(app.exec_())