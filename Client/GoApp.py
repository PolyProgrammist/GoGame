import sys

from PyQt5.QtWidgets import QApplication

from Client.Connection import Protogo
from Client.GoUI.GoWindows import GOQT


class GoMain:
    def __init__(self):
        self.goui = GOQT(self)
        self.protor = Protogo.Protogo(self)


if __name__ == "__main__":
    try:
        app = QApplication([])
        GoMain()
        sys.exit(app.exec_())
    except:
        print(sys.exc_info())