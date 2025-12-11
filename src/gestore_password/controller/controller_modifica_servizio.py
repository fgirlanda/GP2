from PyQt6.QtWidgets import QDialog, QMessageBox, QDialogButtonBox
from utility.gestore_database import GestoreDatabase
from views.view_modifica_servizio import Ui_Dialog_Modifica
from utility.criptatore import *


class Dialog_Modifica(QDialog):
    def __init__(self, db: GestoreDatabase, utente: tuple, servizio: tuple, key: bytes, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog_Modifica()
        self.ui.setupUi(self)
        self.titolo = "Gestore Password - Aggiungi Servizio"
        self.db = db
        self.utente_loggato = utente
        self.servizio = servizio
        self.key = key
        self.set_default_text()

        # Scolleghiamo eventuali connessioni "automatiche" al segnale accepted del QDialogButtonBox
        try:
            self.ui.mser_dlg_btns.accepted.disconnect()
        except Exception:
            pass

        # Colleghiamo il nostro handler che validarà, inserirà e chiamerà accept() SOLO se tutto ok
        self.ui.mser_dlg_btns.accepted.connect(self.on_accepted)
        self.ui.mser_dlg_btns.rejected.connect(self.reject)

    def set_default_text(self):
        nome = self.servizio[1]
        username = self.servizio[2]
        password_cifrata = self.servizio[3]
        real_pass = decripta(password_cifrata, self.key)

        self.ui.mser_edit_nuovo_nome.setText(nome)
        self.ui.mser_edit_nuovo_user.setText(username)
        self.ui.mser_edit_nuova_password.setText(real_pass)

    def on_accepted(self):
        """Handler chiamato quando viene premuto OK sul QDialogButtonBox."""
        dati_servizio = self.estrai_dati_servizio()
        # validazione locale dei campi (nome, username, password cifrata)
        if not self.valida_campi(dati_servizio[0], dati_servizio[1], dati_servizio[2]):
            return

        # prova a inserire nel DB: se va a buon fine chiudiamo il dialog con accept()
        try:
            self.db.aggiorna_servizio(self.servizio[0], dati_servizio)

        except Exception as e:
            QMessageBox.critical(
                self, "Errore", f"Impossibile inserire il servizio:\n{e}")
            return

        # tutto ok: chiudi con Accepted
        self.accept()

    def estrai_dati_servizio(self):
        nome = self.ui.mser_edit_nuovo_nome.text().strip()
        username = self.ui.mser_edit_nuovo_user.text().strip()
        raw_password = self.ui.mser_edit_nuova_password.text().strip()
        password_cifrata = cripta(raw_password, self.key)

        return (nome, username, password_cifrata)

    def valida_campi(self, nome, username, password):
        if not nome:
            QMessageBox.warning(self, "Attenzione",
                                "Il nome del servizio è obbligatorio!")
            self.ui.mser_edit_nuovo_nome.setFocus()
            return False

        if not username:
            QMessageBox.warning(self, "Attenzione",
                                "Lo username è obbligatorio!")
            self.ui.mser_edit_nuovo_user.setFocus()
            return False

        if not password:
            QMessageBox.warning(self, "Attenzione",
                                "La password è obbligatoria!")
            self.ui.mser_edit_nuova_password.setFocus()
            return False

        if nome == self.servizio[2] and username == self.servizio[3] and password == decripta(self.servizio[3], self.key):
            QMessageBox.warning(self, "Attenzione",
                                "Nessun dato modificato!")
            return False
        return True
