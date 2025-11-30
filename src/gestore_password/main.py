from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
# from gestore_password.controller.controller_login import Login
from controller.controller_registrati import Registrazione
from utility.gestore_database import GestoreDatabase


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestore Password - Login")

        # Crea uno stacked widget
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Inizializza le varie finestre
        self.inizializza_pagine()

    def apri_registrazione(self):
        self.stack.setCurrentIndex(1)
        self.setWindowTitle("Gestore Password - Registrati")
        self.ridimensiona(self.pag_registrazione)

    def ridimensiona(self, pagina):
        self.resize(pagina)

    def inizializza_pagine(self):
        self.db = GestoreDatabase()
        self.pag_registrazione = Registrazione(self.db)
        self.stack.addWidget(self.pag_registrazione)
        self.stack.setCurrentIndex(1)


if __name__ == "__main__":
    app = QApplication([])
    main_window = MainApp()
    main_window.show()
    app.exec()
