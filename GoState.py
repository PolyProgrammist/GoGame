class GoState:
    board_size = 9
    freez = -1
    now_color = 1
    cnt = 0
    def __init__(self, name1 = '$first', name2 = '$second'):
        self.places = [[self.freez] * (self.board_size + 1) for _ in range(self.board_size + 1)]
        self.name1 = name1
        self.name2 = name2
    def try_pas(self, t, color):
        if (t[0] != self.freez and self.places[t[0]][t[1]] == self.freez
            and self.now_color == color):
            self.places[t[0]][t[1]] = self.now_color
            self.now_color = int(not self.now_color)
            return True
        else:
            return False