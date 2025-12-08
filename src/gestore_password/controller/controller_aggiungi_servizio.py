from PyQt6.QtWidgets import QDialog, QMessageBox
from utility.gestore_database import GestoreDatabase
from views.view_aggiungi_servizio import Ui_Dialog_Aggiungi
from utility.criptatore import *


class Dialog_Aggiungi(QDialog):
    def __init__(self, db: GestoreDatabase, utente: tuple, key: bytes, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog_Aggiungi()
        self.ui.setupUi(self)
        self.titolo = "Gestore Password - Aggiungi Servizio"
        self.db = db
        self.utente_loggato = utente
        self.key = key

        self.ui.aser_dlg_btns.accepted.connect(self.aggiungi_servizio)
        self.ui.aser_dlg_btns.rejected.connect(self.reject)

    def aggiungi_servizio(self):
        dati_servizio = self.estrai_dati_servizio()

        if not self.valida_campi(dati_servizio[0], dati_servizio[1], dati_servizio[2]):
            return
        self.db.inserisci_servizio(self.utente_loggato[0], dati_servizio)

    def estrai_dati_servizio(self):
        nome = self.ui.aser_edit_nome.text().strip()
        username = self.ui.aser_edit_user.text().strip()
        raw_password = self.ui.aser_edit_password.text().strip()
        password_cifrata = cripta(raw_password, self.key)

        return (nome, username, password_cifrata)

    def valida_campi(self, nome, username, password):
        if not nome:
            QMessageBox.warning(self, "Attenzione",
                                "Il nome del servizio è obbligatorio!")
            self.ui.aser_edit_nome.setFocus()
            return False

        if not username:
            QMessageBox.warning(self, "Attenzione",
                                "Lo username è obbligatorio!")
            self.ui.aser_edit_user.setFocus()
            return False

        if not password:
            QMessageBox.warning(self, "Attenzione",
                                "La password è obbligatoria!")
            self.ui.aser_edit_password.setFocus()
            return False

        # opzionale: requisiti password

        # if len(password) < 8:
        #     QMessageBox.warning(
        #         self,
        #         "Password Debole",
        #         "La password deve essere almeno 8 caratteri!"
        #     )
        #     self.ui.aser_edit_password.setFocus()
        #     return False

        return True
