from PyQt6.QtWidgets import QDialog, QMessageBox, QDialogButtonBox
from utility.gestore_database import GestoreDatabase
from views.view_modifica_profilo import Ui_Dialog_ModUtente
from utility.criptatore import *


class Dialog_ModUtente(QDialog):
    def __init__(self, db: GestoreDatabase, utente: tuple, raw_pass: str, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog_ModUtente()
        self.ui.setupUi(self)
        self.titolo = "Gestore Password - Aggiungi Servizio"
        self.db = db
        self.utente_loggato = utente
        self.raw_pass = raw_pass
        self.set_default_text()

        # Scolleghiamo eventuali connessioni "automatiche" al segnale accepted del QDialogButtonBox
        try:
            self.ui.mpro_dlg_btns.accepted.disconnect()
        except Exception:
            pass

        # Colleghiamo il nostro handler che validarà, inserirà e chiamerà accept() SOLO se tutto ok
        self.ui.mpro_dlg_btns.accepted.connect(self.on_accepted)
        self.ui.mpro_dlg_btns.rejected.connect(self.reject)

    def set_default_text(self):
        utente = self.utente_loggato[1]

        self.ui.mpro_edit_nuovo_utente.setText(utente)

    def on_accepted(self):
        """Handler chiamato quando viene premuto OK sul QDialogButtonBox."""
        dati_utente = self.estrai_dati_utente()
        # validazione locale dei campi (utente, vecchia password, nuova password)
        if not self.valida_campi(dati_utente[0], dati_utente[1], dati_utente[2]):
            return

        nuovo_hash = genera_hash(dati_utente[2])
        nuovi_dati = (dati_utente[0], nuovo_hash)
        # prova a inserire nel DB: se va a buon fine chiudiamo il dialog con accept()
        try:
            self.db.aggiorna_dati_utente(self.utente_loggato[0], nuovi_dati)

        except Exception as e:
            QMessageBox.critical(
                self, "Errore", f"Impossibile modificare l'utente:\n{e}")
            return

        # tutto ok: chiudi con Accepted
        self.accept()

    def estrai_dati_utente(self):
        utente = self.ui.mpro_edit_nuovo_utente.text().strip()
        raw_vecchia_password = self.ui.mpro_edit_vecchia_password.text().strip()
        raw_nuova_password = self.ui.mpro_edit_nuova_password.text().strip()

        return (utente, raw_vecchia_password, raw_nuova_password)

    def valida_campi(self, utente, raw_vecchia_password, raw_nuova_password):
        if not utente:
            QMessageBox.warning(self, "Attenzione",
                                "Il nome utente è obbligatorio!")
            self.ui.mpro_edit_nuovo_utente.setFocus()
            return False

        if not raw_vecchia_password or not verifica_password(raw_vecchia_password, self.utente_loggato[2]):
            QMessageBox.warning(self, "Attenzione",
                                "Inserire la password corretta!")
            self.ui.mpro_edit_vecchia_password.setFocus()
            return False

        if not raw_nuova_password:
            QMessageBox.warning(self, "Attenzione",
                                "Inserisci una nuova password!")
            self.ui.mpro_edit_nuova_password.setFocus()
            return False

        return True
