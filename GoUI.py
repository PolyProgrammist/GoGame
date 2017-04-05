import pygame
import threading
import socket
import sys
import GoState
import GoClientConnect

class GoUI:
    gost = GoState.GoState()
    board_color = (0xC0, 0x40, 0x0)
    score_display_height = 50
    board_display_size = 700
    gap_size = board_display_size // 20
    stone_color = [(50, 50, 50),(200, 200, 200)]
    stone_diameter_fix = 0.9

    full_display_height = score_display_height + board_display_size
    full_add = score_display_height + gap_size
    ungap_coordY = full_display_height - gap_size
    ungap_coordX = board_display_size - gap_size
    field_size = board_display_size - 2 * gap_size
    cell_size = field_size // gost.board_size
    stone_radius = (int) ((cell_size * stone_diameter_fix) / 2)
    board_places = gost.board_size + 1

    def __init__(self, maingo):
        self.maingo = maingo
        threading.Thread(target=self.inlol, args=[]).start()

    def inlol(self):
        self.init_screen()
        self.gost.now_color = 1  # black
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    t = self.analyze_pos(event.pos)
                    self.redraw_background()
                    if (t[0] != -5 and self.gost.places[t[0]][t[1]] == self.gost.freez):
                        self.draw_transparent_stone(
                            (self.gap_size + t[0] * self.cell_size, self.full_add + t[1] * self.cell_size))
                    pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    t = self.analyze_pos(event.pos)
                    self.maingo.connector.go(t)
    def letsgo(self, t):
        self.gost.try_pas(t, self.gost.now_color)
        self.redraw_background()
        pygame.display.update()

    def printtable(self):
        for i in self.places:
            for j in i:
                print(str(j) + ' ', end='', flush=True)
            print('')
        print()

    def analyze_coordinate(self, pos):
        pos -= self.gap_size
        t = round(pos / self.cell_size)
        if 0 <= t <= self.gost.board_size:
            return t
        else:
            return self.gost.freez

    def analyze_pos(self, pos):
        a, b = self.analyze_coordinate(pos[0]), self.analyze_coordinate(pos[1] - self.score_display_height)
        if (a == self.gost.freez or b == self.gost.freez):
            return self.gost.freez, self.gost.freez
        else:
            return a, b

    def init_screen(self):
        self.screen = pygame.display.set_mode((self.board_display_size, self.full_display_height))
        self.redraw_background()
        pygame.display.update()

    def draw_transparent_stone(self, pos):
        s = pygame.Surface((2 * self.stone_radius, 2 * self.stone_radius))
        ck = (127, 33, 33)
        s.fill(ck)
        s.set_colorkey(ck)
        pygame.draw.circle(s, self.stone_color[self.gost.now_color], (self.stone_radius, self.stone_radius), self.stone_radius)
        s.set_alpha(180)
        self.screen.blit(s, (pos[0] - self.stone_radius, pos[1] - self.stone_radius))

    def redraw_background(self):
        self.screen.fill(self.board_color)
        pygame.draw.line(self.screen, (0, 0, 0), (self.gap_size, self.full_add), (self.gap_size, self.ungap_coordY), 4)
        pygame.draw.line(self.screen, (0, 0, 0), (self.gap_size, self.full_add), (self.ungap_coordX, self.full_add), 4)
        pygame.draw.line(self.screen, (0, 0, 0), (self.gap_size, self.ungap_coordY),
                         (self.ungap_coordX, self.ungap_coordY), 4)
        pygame.draw.line(self.screen, (0, 0, 0), (self.ungap_coordX, self.full_add),
                         (self.ungap_coordX, self.ungap_coordY), 4)
        for i in range(self.gost.board_size):
            pygame.draw.line(self.screen, (0, 0, 0), (self.gap_size, self.full_add + i * self.cell_size),
                             (self.ungap_coordX, self.full_add + i * self.cell_size), 4)
            pygame.draw.line(self.screen, (0, 0, 0), (self.gap_size + i * self.cell_size, self.full_add),
                             (self.gap_size + i * self.cell_size, self.ungap_coordY), 4)
        for i in range(self.board_places):
            for j in range(self.board_places):
                if self.gost.places[i][j] != self.gost.freez:
                    pygame.draw.circle(self.screen, self.stone_color[self.gost.places[i][j]],
                                   (self.gap_size + i * self.cell_size, self.full_add + j * self.cell_size),self.stone_radius)
