from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from controller.controller_login import Login
from controller.controller_registrati import Registrazione
from controller.controller_principale import Principale
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

    def inizializza_pagine(self):
        self.db = GestoreDatabase()

        self.pag_login = Login(self.db)
        self.pag_login.ui.login_btn_registrati.clicked.connect(
            lambda: self.cambia_pagina(self.pag_registrazione))
        self.pag_login.login_successo.connect(self.login)
        self.pag_login.login_fallito.connect(
            lambda: self.errore("Credenziali errate, riprova."))

        self.pag_registrazione = Registrazione(self.db)
        self.pag_registrazione.ui.reg_btn_annulla.clicked.connect(
            lambda: self.cambia_pagina(self.pag_login))
        self.pag_registrazione.utente_creato.connect(
            lambda: self.cambia_pagina(self.pag_login))

        self.pag_principale = Principale(self.db)

        self.stack.addWidget(self.pag_login)
        self.stack.addWidget(self.pag_registrazione)
        self.stack.addWidget(self.pag_principale)

        self.stack.setCurrentIndex(0)

    def errore(self, messaggio):
        QMessageBox.warning(self, "Errore", messaggio)

    def login(self, utente: tuple):
        self.pag_principale.set_utente_loggato(utente)
        self.cambia_pagina(self.pag_principale)

    def cambia_pagina(self, pagina):
        self.stack.setCurrentWidget(pagina)
        self.ridimensiona(pagina)
        if hasattr(pagina, "titolo"):
            self.setWindowTitle(pagina.titolo)

    def ridimensiona(self, pagina: QMainWindow):
        self.resize(pagina.sizeHint())


if __name__ == "__main__":
    app = QApplication([])
    main_window = MainApp()
    main_window.show()
    app.exec()
