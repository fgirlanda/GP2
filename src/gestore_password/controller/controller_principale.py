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

    def set_utente_loggato(self, utente: tuple, raw_pass: str):
        self.utente_loggato = utente
        self.ui.main_dlbl_utente.setText(utente[1])
        self.ui.main_dlbl_password.setText(raw_pass)
