from PyQt6.QtWidgets import QDialog, QMessageBox, QDialogButtonBox
from utility.gestore_database import GestoreDatabase
from views.view_modifica_profilo import Ui_Dialog_ModUtente
from utility.criptatore import *

# WORK IN PROGRESS


class Dialog_ModUtente(QDialog):
    def __init__(self, db: GestoreDatabase, utente: tuple, raw_pass: str, parent=None):
        pass
