from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from controller.controller_login import Login
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

    def inizializza_pagine(self):
        self.db = GestoreDatabase()

        self.pag_login = Login(self.db)
        self.pag_login.ui.login_btn_registrati.clicked.connect(
            lambda: self.cambia_pagina(self.pag_registrazione))

        self.pag_registrazione = Registrazione(self.db)
        self.pag_registrazione.ui.reg_btn_annulla.clicked.connect(
            lambda: self.cambia_pagina(self.pag_login))

        self.stack.addWidget(self.pag_login)
        self.stack.addWidget(self.pag_registrazione)

        self.stack.setCurrentIndex(0)

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
