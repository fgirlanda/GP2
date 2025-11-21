from PyQt6.QtWidgets import QMainWindow
from views import ui_registrati
class Registrazione(QMainWindow, ui_registrati):
    def __init__(self):
        super.__init__()
        self.setupUi(self)