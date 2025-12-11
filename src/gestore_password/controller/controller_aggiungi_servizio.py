from PyQt6.QtWidgets import QDialog, QMessageBox, QDialogButtonBox
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

        # Scolleghiamo eventuali connessioni "automatiche" al segnale accepted del QDialogButtonBox
        try:
            self.ui.aser_dlg_btns.accepted.disconnect()
        except Exception:
            pass

        # Colleghiamo il nostro handler che validarà, inserirà e chiamerà accept() SOLO se tutto ok
        self.ui.aser_dlg_btns.accepted.connect(self.on_accepted)
        self.ui.aser_dlg_btns.rejected.connect(self.reject)

    def on_accepted(self):
        """Handler chiamato quando viene premuto OK sul QDialogButtonBox."""
        dati_servizio = self.estrai_dati_servizio()
        # validazione locale dei campi (nome, username, password cifrata)
        if not self.valida_campi(dati_servizio[0], dati_servizio[1], dati_servizio[2]):
            return

        # prova a inserire nel DB: se va a buon fine chiudiamo il dialog con accept()
        try:
            self.db.inserisci_servizio(
                self.utente_loggato[0], dati_servizio)

        except Exception as e:
            QMessageBox.critical(
                self, "Errore", f"Impossibile inserire il servizio:\n{e}")
            return

        # tutto ok: chiudi con Accepted
        self.accept()

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

        return True
