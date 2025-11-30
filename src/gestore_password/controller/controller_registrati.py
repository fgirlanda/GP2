from PyQt6.QtWidgets import QApplication, QMainWindow
from views.view_registrati import Ui_MainWindow
from utility.criptatore import *
from utility.gestore_database import GestoreDatabase


class Registrazione(QMainWindow):
    def __init__(self, db: GestoreDatabase):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.titolo = "Gestore Password - Registrati"
        self.db = db

        # Nota: i widget ora stanno dentro self.ui
        self.ui.reg_btn_crea_utente.clicked.connect(self.registrati)

    def registrati(self):
        utente = self.ui.reg_edit_utente.text()
        raw_password = self.ui.reg_edit_password.text()
        password_cifrata = genera_hash(raw_password)
        salt_servizi = os.urandom(16)
        dati_utente = (utente, password_cifrata, salt_servizi)
        self.db.inserisci_utente(dati_utente)
