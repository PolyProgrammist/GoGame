from Client.Connection.GoClientConnect import GoClientConnect
from queue import Queue


class Protogo:
    def __init__(self, maingo):
        self.connector = GoClientConnect(maingo, self)
        self.maingo = maingo
        self.q = Queue()
    def receive(self):
        self.t = self.q.get()

        print('rec ' + self.t)
        if (self.t == 'end'):
            self.connector.finish()
        if self.t.find('connect') == 0:
            self.maingo.goui.connectWidget.startGame()
        if self.t.find('go') == 0:
            ind = self.t.find(' ', 3)
            one = int(self.t[3:ind])
            two = int(self.t[ind + 1:])
            self.maingo.goui.gameWidget.justBoard.letsgo((one, two))
        if self.t.find('list') == 0:
            self.connector.availibleUsers = [i for i in self.t[5:].split(' ') if i != '']
            self.maingo.goui.connectWidget.refresh()
        if self.t.find('auth') == 0:
            self.maingo.goui.authorizeWidget.answerRequest(self.t)

    def auth(self, name):
        self.connector.snd('auth ' + name)
    def get_list(self):
        self.connector.snd('list')
    def connect(self, user):
        self.connector.snd('connect ' + user)
    def go(self, t):
        self.connector.snd('go ' + str(t[0]) + ' ' + str(t[1]))