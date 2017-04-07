import pygame
import threading
import socket
import sys
import GoState
import GoClientConnect

class Client:
    name = ''
    def __init__(self, t):
        self.c = t[0]
        self.addr = t[1]
        self.authorized = False
        self.running = True
        self.playing = False
        self.name = (str(self.addr))
    def set_name(self, s):
        if not self.authorized:
            self.name = s
            self.authorized = True

class GoServer:
    clients = {}
    states = {}
    def __init__(self):
        self.s = socket.socket()         # Create a socket object
        self.host = socket.gethostname() # Get local machine name
        self.port = 12345                # Reserve a port for your service.
        self.s.bind((self.host, self.port))        # Bind to the port
        self.s.listen(5)                 # Now wait for client connection.
        self.working = True
        threading.Thread(target=self.ent).start()
        while self.working:
            cl = Client(self.s.accept())
            if not self.working:
                break
            self.clients[str(cl.addr)] = cl     # Establish connection with client.
            print ('Got connection from', cl.addr)
            threading.Thread(target=self.handleConnection, args=[cl]).start()

    def ent(self):
        while (True):
            if(input() == "end"):
                break
        self.finish()

    def handleConnection(self, cl):
        self.snd(cl.c, 'Thank you for connecting')
        runs = True
        while self.working and runs:
            t = self.rcv(cl)
            if t != "":
                print(cl.name + ' ::  ' + t)
                if t.find("auth") == 0:
                    tst = t[5:]
                    if tst in self.clients:
                        self.snd(cl.c, 'autherror')
                        continue
                    del self.clients[cl.name]
                    cl.set_name(t[5:])
                    self.clients[cl.name] = cl
                    self.snd(cl.c, 'authok')
                    self.sendall()
                if cl.authorized:
                    if t.find("connect") == 0:
                        op = t[8:]
                        name1 = cl.name
                        name2 = op
                        self.snd(self.clients[name1].c, 'connect')
                        self.snd(self.clients[name2].c, 'connect')

                        state = GoState.GoState(name1, name2)
                        self.states[name1] = state
                        self.states[name2] = state
                        self.clients[name2].playing = True
                        self.clients[name1].playing = True
                    if t.find("go") == 0 and cl.playing:
                        ind = t.find(' ', 3)
                        one = int(t[3:ind])
                        two = int(t[ind + 1:])
                        if self.states[cl.name].try_pas((one, two), cl.name == self.states[cl.name].name1):
                            self.snd(self.clients[self.states[cl.name].name1].c, t)
                            self.snd(self.clients[self.states[cl.name].name2].c, t)

                    if t.find('list') == 0:
                        self.snd(self.clients[cl.name].c, 'list ' + self.getUserList(cl))

            else:
                runs = False
                cl.running = False
                del self.clients[cl.name]
                if cl.name in self.states:
                    name1 = self.states[cl.name].name1
                    name2 = self.states[cl.name].name2
                    del self.states[name1]
                    del self.states[name2]
                self.sendall()
                print('good bye' + cl.name)

    def getUserList(self, cl):
        print('getUserList')
        print([name for name in self.clients])
        t =  ' '.join([key for key in self.clients if key not in self.states and key != cl.name
              and self.clients[key].authorized])
        print(t)
        print([name for name in self.clients])
        return t

    def sendall(self):
        print('startsendall')
        for client in self.clients:
            p = self.clients[client]
            print('tryp' + client)
            if p.authorized:
                print('authorized')
                self.snd(p.c, 'list ' + self.getUserList(p))

    def finish(self):
        self.working = False
        for cl in self.clients:
            cl.c.close()
        socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM).connect((self.host, self.port))

        self.s.close()

    def snd(self, s, st):
        print('sended ' + st)
        s.send(bytearray(st, 'utf-8'))
    def rcv(self, cl):
        while self.working:
            try:
                t = str(cl.c.recv(1024), 'utf-8')
                if len(t):
                    return t
            except:
                return ""


if __name__ == "__main__":
    GoServer()