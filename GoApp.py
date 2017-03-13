import pygame
import threading
import socket
import sys

import GoClientConnect

class GoMain:
    def __init__(self):
        GoClientConnect.GoClientConnect()

if __name__ == "__main__":
    GoMain()