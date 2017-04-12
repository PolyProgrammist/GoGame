from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QLCDNumber

class Timer:
    initsec = 30
    gosec = 10
    def __init__(self, maingo, layout, turn):
        self.lcd = QLCDNumber()
        self.sec = self.initsec
        self.turn = turn
        self.updui()
        self.lcd.setFrameStyle(QFrame.NoFrame)
        self.maingo = maingo
        self.timer = QTimer(self.maingo.goui)
        self.timer.timeout.connect(self.count_time)
        self.timer.start(1000)
        layout.addWidget(self.lcd)

    def get_stime(self, seconds):
        min = seconds // 60
        sec = seconds % 60
        return '{:0>2}'.format(min) + ':' + '{:0>2}'.format(sec)

    def updui(self):
        self.lcd.display(self.get_stime(self.sec))

    def count_time(self):
        if not self.turn:
            return
        self.sec -= 1
        self.updui()
        #hack
        if self.sec == 0 and self.maingo.protor.step == self.turn:
            self.maingo.protor.surrender()
            self.timer.stop()

    def go(self):
        self.turn = not self.turn
        if self.turn:
            self.sec += self.gosec