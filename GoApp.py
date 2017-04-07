import pygame
import threading
import socket
import sys

from PyQt5.QtWidgets import QApplication

import GoClientConnect
import GoBoardUI
from QTwindow import GOQT
import FalseConnect

class GoMain:
    def __init__(self):
        self.goui = GOQT(self)
        self.connector = GoClientConnect.GoClientConnect(self)


if __name__ == "__main__":
    try:
        app = QApplication([])
        GoMain()
        sys.exit(app.exec_())
    except:
        print(sys.exc_info())