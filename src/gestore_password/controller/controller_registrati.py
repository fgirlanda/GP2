from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal
from views.view_registrati import Ui_Registrazione
from utility.criptatore import *
from utility.gestore_database import GestoreDatabase


class Registrazione(QWidget):
    utente_creato = pyqtSignal()

    def __init__(self, db: GestoreDatabase):
        super().__init__()
        self.ui = Ui_Registrazione()
        self.ui.setupUi(self)
        self.titolo = "Gestore Password - Registrati"
        self.db = db

        self.ui.reg_btn_crea_utente.clicked.connect(self.registrati)

    def registrati(self):
        utente = self.ui.reg_edit_utente.text()
        raw_password = self.ui.reg_edit_password.text()
        hash_password = genera_hash(raw_password)
        salt = os.urandom(16)
        self.db.inserisci_utente(utente, hash_password, salt)
        self.utente_creato.emit()
