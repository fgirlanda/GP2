from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
# from gestore_password.controller.controller_login import Login
from gestore_password.controller.controller_registrati import Registrazione


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestore Password")

        # Crea uno stacked widget
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Inizializza le varie finestre
        # self.login_page = Login()
        self.registrazione_page = Registrazione()

        # Aggiungile allo stack
        # self.stack.addWidget(self.login_page)          # index 0
        self.stack.addWidget(self.registrazione_page)  # index 1

        # Mostra login di default
        self.stack.setCurrentIndex(1)
        self.resize(self.stack.currentWidget().sizeHint())

        # Collega pulsanti per cambiare finestra
        # self.login_page.ui.reg_btn.goto_registrazione.clicked.connect(
        #     lambda: self.stack.setCurrentWidget(self.registrazione_page)
        # )
        # self.registrazione_page.ui.reg_btn_crea_utente.clicked.connect(
        #     lambda: self.stack.setCurrentWidget(self.login_page)
        # )


if __name__ == "__main__":
    app = QApplication([])
    main_window = MainApp()
    main_window.show()
    app.exec()
