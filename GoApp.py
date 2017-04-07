import pygame
import threading
import socket
import sys

from PyQt5.QtWidgets import QApplication

import GoClientConnect
import GoUIQT
from QTwindow import GOQT
import FalseConnect

class GoMain:
    def __init__(self):

        self.goui = GOQT(self)
        self.connector = GoClientConnect.GoClientConnect(self)

if __name__ == "__main__":
    app = QApplication([])
    GoMain()
    sys.exit(app.exec_())