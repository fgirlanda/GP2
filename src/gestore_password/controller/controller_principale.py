from PyQt6.QtWidgets import QMainWindow
from views.view_principale import Ui_MainWindow
from utility.criptatore import *
from utility.gestore_database import GestoreDatabase


class Principale(QMainWindow):
    def __init__(self, db: GestoreDatabase):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.titolo = "Gestore Password"
        self.db = db

    def set_utente_loggato(self, utente: tuple):
        self.utente_loggato = utente
