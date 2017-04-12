import socket
import threading

from Common import GoState


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
                    self.sendall({cl})
                if cl.authorized:
                    if t.find("connect") == 0:
                        op = t[8:]
                        name1 = cl.name
                        name2 = op
                        self.snd(self.clients[name1].c, 'connect ' + name2 + ' 1')
                        self.snd(self.clients[name2].c, 'connect ' + name1 + ' 0')

                        state = GoState.GoState(name1, name2)
                        self.states[name1] = state
                        self.states[name2] = state
                    if t.find("go") == 0 and cl.name in self.states:
                        ind = t.find(' ', 3)
                        one = int(t[3:ind])
                        two = int(t[ind + 1:])
                        if self.states[cl.name].try_pas((one, two), cl.name == self.states[cl.name].name1):
                            self.snd(self.clients[self.states[cl.name].name1].c, t)
                            self.snd(self.clients[self.states[cl.name].name2].c, t)

                    if t.find('list') == 0:
                        self.snd(self.clients[cl.name].c, 'list ' + self.getUserList(cl))

                    if t.find('surrender') == 0:
                        self.lose(cl.name)


            else:
                runs = False
                cl.running = False
                if cl.name in self.states:
                    self.lose(cl.name)
                    name1 = self.states[cl.name].name1
                    name2 = self.states[cl.name].name2
                    del self.states[name1]
                    del self.states[name2]
                del self.clients[cl.name]
                self.sendall({})

    def lose(self, looser):
        if self.states[looser].name1 == looser:
            winner = self.states[looser].name2
        else:
            winner = self.states[looser].name1
        self.snd(self.clients[looser].c, 'lose')
        self.snd(self.clients[winner].c, 'win')

    def getUserList(self, cl):
        t =  ' '.join([key for key in self.clients if key not in self.states and key != cl.name
              and self.clients[key].authorized])
        return t

    def sendall(self, donot):
        for client in self.clients:
            if not client in donot:
                p = self.clients[client]
                if p.authorized:
                    self.snd(p.c, 'list ' + self.getUserList(p))

    def finish(self):
        self.working = False
        for cl in self.clients:
            cl.c.close()
        socket.socket(socket.AF_INET,
                      socket.SOCK_STREAM).connect((self.host, self.port))

        self.s.close()

    def snd(self, s, st):
        try:
            s.send(bytearray(st, 'utf-8'))
            print('sended ' + st)
        except:
            pass
    def rcv(self, cl):
        while self.working:
            try:
                t = str(cl.c.recv(1024), 'utf-8')
                if len(t):
                    return t
            except:
                return ''


if __name__ == "__main__":
    GoServer()