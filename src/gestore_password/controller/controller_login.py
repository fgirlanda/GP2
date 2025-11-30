from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import pyqtSignal
from views.view_login import Ui_MainWindow
from utility.criptatore import *
from utility.gestore_database import GestoreDatabase


class Login(QMainWindow):
    login_successo = pyqtSignal(tuple)

    def __init__(self, db: GestoreDatabase):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.titolo = "Gestore Password - Login"
        self.db = db

        # Nota: i widget ora stanno dentro self.ui
        self.ui.login_btn_login.clicked.connect(self.prova_login)

    def prova_login(self):
        utente = self.ui.login_edit_utente.text()
        raw_password = self.ui.login_edit_password.text()
        password_cifrata = genera_hash(raw_password)
        dati_utente = self.db.get_utente(utente)
        hash = dati_utente[2]
        if verifica_password(password_cifrata, hash):
            self.login_successo.emit(dati_utente)
        else:
            self.login_successo.emit(None)
