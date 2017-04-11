import socket

from PyQt5.QtCore import QThread
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSignal

class MyThread(QThread):
    trigger = pyqtSignal(int)

    def __init__(self, parent, meth):
        super(MyThread, self).__init__(parent)
        self.meth = meth
    def run(self):
        self.meth()




class GoClientConnect:
    def __init__(self, maingo, protor):
        self.maingo = maingo
        self.availibleUsers = []
        self.s = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 12345                # Reserve a port for your service.
        self.s.connect((host, port))
        self.working = True
        self.argument = (-1, -1)
        self.protor = protor

        #MyThread(self.maingo.goui, self.receiving).start()
        self.thread1 = MyThread(self.maingo.goui, self.receiving)
        self.thread1.trigger.connect(self.protor.receive)
        self.thread1.start()
        MyThread(self.maingo.goui, self.inputDoing).start()

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
            self.protor.q.put(self.rcv())
            self.thread1.trigger.emit(0)
    def finish(self):
        self.working = False
        self.s.close()

if __name__ == "__main__":
    GoClientConnect()