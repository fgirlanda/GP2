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
        self.ui.verticalLayout.setSpacing(15)
        self.ui.verticalLayout.setContentsMargins(50, 20, 50, 20)
        self.ui.verticalLayout.addStretch(1)
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
        self.utente_creato.emit()
