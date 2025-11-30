from PyQt6.QtWidgets import QApplication, QMainWindow
from views.view_registrati import Ui_MainWindow


class Registrazione(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Nota: i widget ora stanno dentro self.ui
        self.ui.reg_btn_crea_utente.clicked.connect(self.registrati)

    def registrati(self):
        utente = self.ui.reg_edit_utente.text()
        raw_password = self.ui.reg_edit_password.text()
        print(utente, raw_password)
