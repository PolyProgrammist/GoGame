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
            self.handle_kills(t)
            return True
        else:
            return False

    odi = [0, 1, 0, -1]
    odj = [1, 0, -1, 0]

    def handle_kills(self, t):
        self.was2 = [[False] * (self.board_size + 1) for _ in range(self.board_size + 1)]
        self.was = [[False] * (self.board_size + 1) for _ in range(self.board_size + 1)]
        for i in range(4):
            ti = t[0] + self.odi[i]
            tj = t[1] + self.odj[i]
            if self.ok(ti, tj) and self.places[ti][tj] == self.now_color:
                if not self.was[ti][tj] and not self.dfs_free((ti, tj)):
                    self.dfs_del((ti, tj))

    def dfs_free(self, t):
        self.was[t[0]][t[1]] = True
        if self.places[t[0]][t[1]] == -1:
            return True
        if self.places[t[0]][t[1]] != self.now_color:
            return False
        for i in range(4):
            ti = t[0] + self.odi[i]
            tj = t[1] + self.odj[i]
            if self.ok(ti, tj) and not self.was[ti][tj]:
                if self.dfs_free((ti, tj)):
                    return True
        return False

    def dfs_del(self, t):
        self.was2[t[0]][t[1]] = True
        if self.places[t[0]][t[1]] != self.now_color:
            return
        self.places[t[0]][t[1]] = self.freez
        for i in range(4):
            ti = t[0] + self.odi[i]
            tj = t[1] + self.odj[i]
            if self.ok(ti, tj) and not self.was2[t[0]][t[1]]:
                self.dfs_del((ti, tj))

    def ok(self, ti, tj):
        return ti >= 0 and tj >= 0 and ti <= self.board_size and tj <= self.board_size
