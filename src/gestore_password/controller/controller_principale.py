from PyQt6.QtWidgets import QWidget, QHeaderView
from views.view_principale import Ui_Main
from utility.criptatore import *
from utility.gestore_database import GestoreDatabase


class Principale(QWidget):
    def __init__(self, db: GestoreDatabase):
        super().__init__()
        self.ui = Ui_Main()
        self.ui.setupUi(self)
        self.titolo = "Gestore Password"
        self.db = db

    def set_utente_loggato(self, utente: tuple, raw_pass: str):
        self.utente_loggato = utente
        self.key = derive_key(raw_pass, utente[3])
        self.set_dati_utente(utente[1], raw_pass)
        self.setup_tabella()
        self.popola_tabella()

    def set_dati_utente(self, utente: str, raw_pass: str):
        self.ui.main_dlbl_utente.setText(utente[1])
        self.ui.main_dlbl_password.setText(raw_pass)

    def setup_tabella(self):
        self.ui.main_tbl_servizi.setColumnCount(4)
        self.ui.main_tbl_servizi.setHorizontalHeaderLabels(
            ["Servizio", "Username", "Password", "Azioni"])
        self.ui.main_tbl_servizi.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

    def popola_tabella(self):
        self.servizi = self.db.get_servizi_per_utente(self.utente_loggato[0])
        for servizio in self.servizi:
            nome = servizio[2]
            username = servizio[3]
            password = decripta(servizio[4], self.key)
