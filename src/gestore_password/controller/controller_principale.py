from PyQt6.QtWidgets import QWidget, QHeaderView, QTableWidgetItem, QPushButton, QMessageBox, QHBoxLayout, QDialog
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import pyqtSignal
from controller.controller_modifica_servizio import Dialog_Modifica
from views.view_principale import Ui_Main
from utility.criptatore import *
from utility.gestore_database import GestoreDatabase
from utility.gestore_path import *
from utility.controllo_tabella import TabellaController
from controller.controller_aggiungi_servizio import Dialog_Aggiungi


class Principale(QWidget):
    dialog_aggiungi_signal = pyqtSignal()

    def __init__(self, db: GestoreDatabase):
        super().__init__()
        self.ui = Ui_Main()
        self.ui.setupUi(self)
        self.titolo = "Gestore Password"

        # Tabella
        self.tabella_ctrl = TabellaController(self.ui.main_tbl_servizi)
        self.tabella_ctrl.elimina_richiesto.connect(self.elimina_servizio)
        self.tabella_ctrl.modifica_richiesta.connect(self.modifica_servizio)
        self.tabella_ctrl.copia_richiesta.connect(self.copia_password_servizio)
        self.tabella_ctrl.mostra_richiesta.connect(
            self.toggle_password_servizio)

        self.db = db

        # ===== PRINCIPALE =====

        # ricerca
        icon_search = QtGui.QIcon()
        icon_search.addPixmap(QtGui.QPixmap(get_resource_path("cerca.png")),
                              QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.ui.main_btn_cerca.setIcon(icon_search)

        # aggiungi servizio
        self.ui.main_btn_aggiungi.clicked.connect(self.apri_dialog_aggiungi)

        # ===== PROFILO =====

        # visibilità password utente
        icon_vis = QtGui.QIcon()
        icon_vis.addPixmap(QtGui.QPixmap(get_resource_path("visible.png")),
                           QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.ui.main_btn_visibility_pass.setIcon(icon_vis)
        self.ui.main_btn_visibility_pass.clicked.connect(
            self.mostra_pass_utente)

        # modifica utente (in progress)
        self.ui.main_btn_modutente.clicked.connect(self.in_progress)

    ####################################################################################

    # SETUP PAGINA

    def set_utente_loggato(self, utente: tuple, raw_pass: str):
        self.utente_loggato = utente
        self.key = derive_key(raw_pass, utente[3])
        self.set_dati_utente(utente[1], raw_pass)
        self.servizi = self.db.get_servizi_per_utente(self.utente_loggato[0])
        self.tabella_ctrl.aggiorna(self.servizi, self.key)

    def set_dati_utente(self, utente: str, raw_pass: str):
        self.ui.main_dlbl_utente.setText(utente)
        label = self.ui.main_dlbl_password
        label.setProperty("password", raw_pass)
        label.setProperty("hidden", True)

        label.setText("••••••••")

    ####################################################################################

    # MODIFICA UTENTE

    def in_progress(self):
        QMessageBox.information(
            self, "Attenzione", "Funzionalità non ancora implementata.")

    ####################################################################################

    # MOSTRA/NASCONDI PASSWORD UTENTE

    def mostra_pass_utente(self):
        label = self.ui.main_dlbl_password
        pwd = label.property("password")

        if not pwd:
            return
        hidden = label.property("hidden")
        if hidden:
            label.setText(pwd)
        else:
            label.setText("••••••••")
        label.setProperty("hidden", not hidden)

    ####################################################################################

    # AGGIUNGI SERVIZIO

    def apri_dialog_aggiungi(self):
        self.dialog_aggiungi = Dialog_Aggiungi(
            self.db, self.utente_loggato, self.key)
        self.dialog_aggiungi.open()
        self.dialog_aggiungi.finished.connect(self.on_dialog_aggiungi_finished)

    def on_dialog_aggiungi_finished(self, risultato):
        """Gestisce la chiusura del dialog."""
        if risultato == QDialog.DialogCode.Accepted:
            try:
                self.servizi = self.db.get_servizi_per_utente(
                    self.utente_loggato[0])
            except Exception as e:
                QMessageBox.critical(
                    self, "Errore", f"Impossibile leggere i servizi dal DB:\n{e}")
                self.dialog_aggiungi = None
                return

            self.tabella_ctrl.aggiorna(self.servizi, self.key)
            QMessageBox.information(
                self, "Successo", "Il servizio è stato aggiunto")
        self.dialog_aggiungi = None

    ####################################################################################

    # TABELLA SERVIZI
    def elimina_servizio(self, servizio_id):
        self.db.elimina_servizio(servizio_id)
        self.servizi = [s for s in self.servizi if s[0] != servizio_id]
        self.tabella_ctrl.elimina_riga(servizio_id)

    def toggle_password_servizio(self, servizio_id):
        self.tabella_ctrl.toggle_password(servizio_id)

    def copia_password_servizio(self, servizio_id):
        self.tabella_ctrl.copia_password(servizio_id)
        QMessageBox.information(
            self, "Copia", "Password copiata negli appunti")

    def modifica_servizio(self, servizio_id):
        servizio = self.db.get_servizio_by_id(servizio_id)
        self.dialog_modifica = Dialog_Modifica(
            self.db, self.utente_loggato, servizio, self.key)
        self.dialog_modifica.open()
        self.dialog_modifica.finished.connect(self.on_dialog_modifica_finished)

    def on_dialog_modifica_finished(self, risultato):
        """Gestisce la chiusura del dialog."""
        if risultato == QDialog.DialogCode.Accepted:
            try:
                self.servizi = self.db.get_servizi_per_utente(
                    self.utente_loggato[0])
            except Exception as e:
                QMessageBox.critical(
                    self, "Errore", f"Impossibile leggere i servizi dal DB:\n{e}")
                self.dialog_aggiungi = None
                return

            self.tabella_ctrl.aggiorna(self.servizi, self.key)
            QMessageBox.information(
                self, "Successo", "Il servizio è stato modificato")
        self.dialog_aggiungi = None
