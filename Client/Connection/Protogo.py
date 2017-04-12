from Client.Connection.GoClientConnect import GoClientConnect
from queue import Queue


class Protogo:
    def __init__(self, maingo):
        self.connector = GoClientConnect(maingo, self)
        self.maingo = maingo
        self.availibleUsers = []
        self.q = Queue()
    def receive(self):
        t = self.q.get()
        if (t == 'end'):
            self.connector.finish()
        if t.find('connect') == 0:
            t = t[8:]
            self.othername = t[:t.find(' ')]
            t = t[t.find(' ') + 1:]
            self.step = int(t)
            print(self.step)
            self.maingo.goui.connectWidget.startGame()
        if t.find('go') == 0:
            ind = t.find(' ', 3)
            one = int(t[3:ind])
            two = int(t[ind + 1:])
            self.step = not self.step
            self.maingo.goui.gameWidget.justBoard.letsgo((one, two))
        if t.find('list') == 0:
            self.availibleUsers = [i for i in t[5:].split(' ') if i != '']
            self.maingo.goui.connectWidget.refresh()
        if t.find('auth') == 0:
            self.maingo.goui.authorizeWidget.answerRequest(t)

    def auth(self, name):
        self.myname = name
        self.connector.snd('auth ' + name)
    def get_list(self):
        self.connector.snd('list')
    def connect(self, user):
        self.connector.snd('connect ' + user)
    def go(self, t):
        self.connector.snd('go ' + str(t[0]) + ' ' + str(t[1]))