from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import pyqtSignal
from views.view_aggiungi_servizio import Ui_Dialog_Aggiungi
from utility.criptatore import *
from utility.gestore_database import GestoreDatabase


class Dialog_Aggiungi(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog_Aggiungi()
        self.ui.setupUi(self)
        self.titolo = "Gestore Password - Aggiungi Servizio"
