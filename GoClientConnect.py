import pygame
import threading
import socket
import sys
import GoUI

class GoClientConnect:
    def __init__(self, maingo):
        self.maingo = maingo
        self.s = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 12345                # Reserve a port for your service.
        self.s.connect((host, port))
        self.working = True
        threading.Thread(target=self.inputDoing).start()
        threading.Thread(target=self.receiving).start()

    def snd(self, st):
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
            print(t)
            if (t == 'end'):
                self.finish()
            if (t == 'connect'):
                self.maingo.createUI()
            if (t.find('go') == 0):
                ind = t.find(' ', 3)
                one = int(t[3:ind])
                two = int(t[ind + 1:])
                self.maingo.goui.letsgo((one, two))

    def finish(self):
        self.working = False
        self.s.close()
    def go(self, t):
        self.snd('go ' + str(t[0]) + ' ' + str(t[1]))

if __name__ == "__main__":
    GoClientConnect()