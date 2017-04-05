import pygame
import threading
import socket
import sys

import GoClientConnect
import GoUI

class GoMain:
    def __init__(self):
        self.connector = GoClientConnect.GoClientConnect(self)
    def createUI(self):
        self.goui = GoUI.GoUI(self)

if __name__ == "__main__":
    GoMain()