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
        self.setup_tabella()

    def set_utente_loggato(self, utente: tuple, raw_pass: str):
        self.utente_loggato = utente
        self.set_dati_utente(utente[1], raw_pass)
        self.mostra_servizi(utente[0])

    def set_dati_utente(self, utente: str, raw_pass: str):
        self.ui.main_dlbl_utente.setText(utente[1])
        self.ui.main_dlbl_password.setText(raw_pass)

    def mostra_servizi(self, id_utente: int):
        self.servizi = self.db.get_servizi_per_utente(id_utente)

    def setup_tabella(self):
        self.ui.main_tbl_servizi.setColumnCount(4)
        self.ui.main_tbl_servizi.setHorizontalHeaderLabels(
            ["Servizio", "Username", "Password", "Azioni"])
        self.ui.main_tbl_servizi.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
