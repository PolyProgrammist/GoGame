import socket               # Import socket module
import threading
import time
from clar import *

class GoClient:
    def __init__(self):
        self.s = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 12345                # Reserve a port for your service.
        self.s.connect((host, port))
        self.working = True
        threading.Thread(target=self.inputDoing).start()
        threading.Thread(target=self.receiving).start()

    def snd(self, st):
        self.s.send(bytearray(st, 'utf-8'))
    def rcv(self):
        while self.working:
            try:
                t = str(self.s.recv(1024), 'utf-8')
                if len(t):
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
            self.define_received(t)
            print(t)
            if (t == 'end'):
                self.finish()
            if (t == 'connect'):
                self.goui = GoUI()
            if (t.find('go') == 0):
                ind = t.find(' ', 4)
                one = int(t[4:ind])
                two = int(t[ind + 1:])
                self.goui.gost.try_pas(one, two)

    def finish(self):
        self.working = False
        self.s.close()

if __name__ == "__main__":
    Client()