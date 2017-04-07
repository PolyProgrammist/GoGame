import threading
import socket
import sys

from PyQt5.QtCore import QRunnable
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QThreadPool
from PyQt5.QtCore import pyqtSignal

import GoUI

class MyThread(QThread):
    trigger = pyqtSignal(int)
    trigger2 = pyqtSignal(int)
    trigger3 = pyqtSignal(int)
    trigger4 = pyqtSignal(int)

    def __init__(self, parent, meth):
        super(MyThread, self).__init__(parent)
        self.meth = meth
    def run(self):
        self.meth()

class GoClientConnect:
    def __init__(self, maingo):
        self.maingo = maingo
        self.availibleUsers = []
        self.s = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 12345                # Reserve a port for your service.
        self.s.connect((host, port))
        self.working = True
        self.argument = (-1, -1)
        self.thread1 = MyThread(self.maingo.goui, self.receiving)    # create a thread
        self.thread1.trigger.connect(self.lllgo)  # connect to it's signal
        self.thread1.trigger2.connect(self.maingo.goui.connectWidget.refresh)
        self.thread1.trigger3.connect(self.maingo.goui.connectWidget.startGame)
        self.thread1.trigger4.connect(self.authans)
        self.thread1.start()
        self.thread2 = MyThread(self.maingo.goui, self.inputDoing)  # create a thread
        self.thread2.start()
    def lllgo(self):
        print('lllgo')
        self.maingo.goui.gameWidget.justBoard.letsgo(self.argument)
    def authans(self):
        self.maingo.goui.authorizeWidget.answerRequest(self.authAnswer)

    def snd(self, st):
        if not self.working:
            return
        print('sended ' + st)
        self.s.send(bytearray(st, 'utf-8'))
    def rcv(self):
        while self.working:
            try:
                t = str(self.s.recv(1024), 'utf-8')
                if len(t):
                    print('received ' + t)
                    return t
            except:
                self.finish()

    def inputDoing(self):
        while self.working:
            t = input()
            if self.working:
                if (t == 'end'):
                    self.finish()
            if self.working:
                self.snd(t)

    def receiving(self):
        while self.working:
            t = self.rcv()
            if (t == 'end'):
                self.finish()
            if (t == 'connect'):
                self.thread1.trigger3.emit(0)
            if (t.find('go') == 0):
                ind = t.find(' ', 3)
                one = int(t[3:ind])
                two = int(t[ind + 1:])
                self.argument = (one, two)
                print('argum')
                self.thread1.trigger.emit(0)
            if (t.find('list') == 0):
                self.availibleUsers = [i for i in t[5:].split(' ') if i != '']
                self.thread1.trigger2.emit(0)
            if (t.find('auth') == 0):
                self.authAnswer = t
                self.thread1.trigger4.emit(0)

    def finish(self):
        self.working = False
        self.s.close()
    def go(self, t):
        self.snd('go ' + str(t[0]) + ' ' + str(t[1]))

if __name__ == "__main__":
    GoClientConnect()