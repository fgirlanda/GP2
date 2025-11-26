from PyQt6.QtWidgets import QMainWindow
from views.view_registrati import Ui_MainWindow
class Registrazione(QMainWindow, Ui_MainWindow):
    query_registrazione = "INSERT INTO Utenti (utente, hash_password, salt) VALUES (?, ?, ?)"
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.reg_btn_crea_utente.clicked.connect(self.registrati)
    
    def registrati(self):
        utente = self.reg_edit_utente.text()
        raw_password = self.reg_edit_password.text()
        
        