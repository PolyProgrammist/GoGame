class Protogo:
    def __init__(self, maingo):
        self.maingo = maingo
        self.availibleUsers = []
    def receive(self):
        # if t == 'win':
        #     self.maingo.goui.gameWidget.win()
        # if t == 'lose':
        #     self.maingo.goui.gameWidget.lose()
        a = 0

    def auth(self, name):
        self.send('auth ' + name)
        self.maingo.name = name
        self.maingo.goui.authorizeWidget.answerRequest('authok')
        self.get_list()
    def get_list(self):
        self.send('list')
        self.availibleUsers = ['kek', 'lol']
        self.maingo.goui.connectWidget.refresh()
    def connect(self, user):
        self.send('connect ' + user)
        self.othername = user
        t = 1
        self.step = int(t)
        self.maingo.goui.connectWidget.startGame()
    def go(self, t):
        self.send('go ' + str(t[0]) + ' ' + str(t[1]))
        one = t[0]
        two = t[1]
        self.step = not self.step
        self.maingo.goui.gameWidget.justBoard.letsgo((one, two))
        print('checking following game')
        state = self.maingo.goui.gameWidget.justBoard.gost
        if not state.can_any_go():
            print('game over for ')
            a, b = state.count_answer()
            looser = state.name2 if a > b else state.name1
    def surrender(self):
        self.send('surrender')

    def send(self, t):
        print(t)
#[[-1, 1, 1, 1, -1, 1, -1, 1, -1, 1], [0, 0, 0, 0, 1, 1, 1, -1, 1, 1], [0, 0, 1, 1, 1, -1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, -1, 1], [0, 0, 1, 0, 1, 1, 1, 1, 1, 1], [0, 0, 1, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 0, 1, 1, 1, 1, -1], [0, 0, 0, 0, 0, 1, 1, 1, 1, 0], [-1, 0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, -1, 0, 0, 0, 0, 0]]