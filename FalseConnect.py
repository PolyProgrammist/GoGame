import random, string

class GoClientConnect:
    availibleUsers = []
    def __init__(self, maingo):
        self.maingo = maingo
        self.availibleUsers = [self.randomword(5) for i in range(random.randint(3, 7))]
    def snd(self, st):
        if st == 'list':
            self.availibleUsers.append(self.randomword(5))
            self.maingo.goui.connectWidget.refresh()
        if st.find('connect') == 0:
            self.maingo.goui.connectWidget.startGame()

    def randomword(self, length):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))