from Client.Connection.GoClientConnect import GoClientConnect
from queue import Queue


class Protogo:
    def __init__(self, maingo):
        self.q = Queue()
        self.connector = GoClientConnect(maingo, self)
        self.maingo = maingo
        self.availibleUsers = []
    def receive(self):
        t = self.q.get()
        if (t == 'end'):
            self.connector.finish()
        if t.find('connect') == 0:
            t = t[8:]
            self.othername = t[:t.find(' ')]
            t = t[t.find(' ') + 1:]
            self.step = int(t)
            self.maingo.goui.connectWidget.startGame()
        if t.find('go') == 0:
            ind = t.find(' ', 3)
            one = int(t[3:ind])
            two = int(t[ind + 1:])
            self.step = not self.step
            self.maingo.goui.gameWidget.timmy.go()
            self.maingo.goui.gameWidget.timop.go()
            self.maingo.goui.gameWidget.justBoard.letsgo((one, two))
        if t.find('list') == 0:
            self.availibleUsers = [i for i in t[5:].split(' ') if i != '']
            self.maingo.goui.connectWidget.refresh()
        if t.find('auth') == 0:
            self.maingo.goui.authorizeWidget.answerRequest(t)
        if t == 'win':
            self.maingo.goui.gameWidget.win()
        if t == 'lose':
            self.maingo.goui.gameWidget.lose()

    def auth(self, name):
        self.myname = name
        self.send('auth ' + name)
    def get_list(self):
        self.send('list')
    def connect(self, user):
        self.send('connect ' + user)
    def go(self, t):
        self.send('go ' + str(t[0]) + ' ' + str(t[1]))
    def surrender(self):
        self.send('surrender')

    def send(self, t):
        self.connector.snd(t)