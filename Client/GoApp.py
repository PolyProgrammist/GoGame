import sys

from PyQt5.QtWidgets import QApplication

from Client.Connection.Protogo import Protogo
from Client.GoUI.GoWindows import GOQT


class GoMain:
    def __init__(self):
        self.goui = GOQT(self)
        self.protor = Protogo(self)

# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

if __name__ == "__main__":
    app = QApplication([])
    GoMain()
    try:
        sys.exit(app.exec_())
    except:
        print(sys.exc_info())