from PyQt6.QtWidgets import QWidget, QHeaderView, QTableWidgetItem, QPushButton, QMessageBox, QHBoxLayout
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QDialog
from views.view_principale import Ui_Main
from utility.criptatore import *
from utility.gestore_database import GestoreDatabase
from utility.gestore_path import *
from controller.controller_aggiungi_servizio import Dialog_Aggiungi


class Principale(QWidget):
    def __init__(self, db: GestoreDatabase):
        super().__init__()
        self.ui = Ui_Main()
        self.ui.setupUi(self)
        self.titolo = "Gestore Password"
        icon_vis = QtGui.QIcon()
        icon_vis.addPixmap(QtGui.QPixmap(get_resource_path("visible.png")),
                           QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.ui.main_btn_visibility_pass.setIcon(icon_vis)

        icon_search = QtGui.QIcon()
        icon_search.addPixmap(QtGui.QPixmap(get_resource_path("cerca.png")),
                              QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.ui.main_btn_cerca.setIcon(icon_search)
        self.db = db
        self.ui.main_btn_aggiungi.clicked.connect(self.apri_dialog_aggiungi)

    def on_dialog_aggiungi_finished(self, risultato):
        """Gestisce la chiusura del dialog."""
        # risultato è QDialog.DialogCode.Accepted o Rejected
        if risultato == QDialog.DialogCode.Accepted:
            # ricarica dal DB e aggiorna la tabella
            try:
                self.servizi = self.db.get_servizi_per_utente(
                    self.utente_loggato[0])
            except Exception as e:
                QMessageBox.critical(
                    self, "Errore", f"Impossibile leggere i servizi dal DB:\n{e}")
                self.dialog_aggiungi = None
                return

            self.popola_tabella()
            QMessageBox.information(
                self, "Successo", "Il servizio è stato aggiunto")
        # se Rejected non facciamo nulla
        self.dialog_aggiungi = None

    def apri_dialog_aggiungi(self):
        self.dialog_aggiungi = Dialog_Aggiungi(
            self.db, self.utente_loggato, self.key)
        # open() mantiene non-modale; exec() sarebbe modale. Open va bene se vuoi non-bloccante.
        self.dialog_aggiungi.open()
        self.dialog_aggiungi.finished.connect(self.on_dialog_aggiungi_finished)

    def set_utente_loggato(self, utente: tuple, raw_pass: str):
        self.utente_loggato = utente
        self.key = derive_key(raw_pass, utente[3])
        self.set_dati_utente(utente[1], raw_pass)
        self.servizi = self.db.get_servizi_per_utente(self.utente_loggato[0])
        self.setup_tabella()
        self.popola_tabella()

    def set_dati_utente(self, utente: str, raw_pass: str):
        self.ui.main_dlbl_utente.setText(utente)
        self.ui.main_dlbl_password.setText(raw_pass)

    def setup_tabella(self):
        self.ui.main_tbl_servizi.setColumnCount(4)
        self.ui.main_tbl_servizi.setHorizontalHeaderLabels(
            ["Servizio", "Username", "Password", "Azioni"])
        self.ui.main_tbl_servizi.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        # inizializza vuota
        self.ui.main_tbl_servizi.setRowCount(0)

    def popola_tabella(self):
        # svuota i contenuti e imposta il numero di righe
        self.ui.main_tbl_servizi.clearContents()
        self.ui.main_tbl_servizi.setRowCount(len(self.servizi))
        for row, servizio in enumerate(self.servizi):
            self.aggiungi_riga_servizio(servizio, row)

    def aggiungi_riga_servizio(self, servizio: tuple, row: int):
        nome = servizio[1]
        username = servizio[2]
        password = decripta(servizio[3], self.key)

        item_nome = QTableWidgetItem(nome)
        item_nome.setData(QtCore.Qt.ItemDataRole.UserRole, servizio[0])
        self.ui.main_tbl_servizi.setItem(row, 0, item_nome)

        item_username = QTableWidgetItem(username)
        self.ui.main_tbl_servizi.setItem(row, 1, item_username)

        item_password = QTableWidgetItem("••••••••")
        item_password.setData(QtCore.Qt.ItemDataRole.UserRole, password)
        self.ui.main_tbl_servizi.setItem(row, 2, item_password)

        widget_bottoni = self.crea_bottoni_riga(servizio[0])
        self.ui.main_tbl_servizi.setCellWidget(row, 3, widget_bottoni)

    def crea_bottoni_riga(self, servizio_id: int) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)
        btn_size = QtCore.QSize(24, 24)

        # Bottone mostra password (passiamo servizio_id, non row)
        btn_mostra = QPushButton()
        btn_mostra.setFixedSize(btn_size)
        btn_mostra.setIcon(QtGui.QIcon(get_resource_path("visible.png")))
        btn_mostra.setToolTip("Mostra/Nascondi password")
        btn_mostra.clicked.connect(
            lambda _, sid=servizio_id: self.mostra_password_servizio(sid))

        # Bottone copia
        btn_copia = QPushButton()
        btn_copia.setFixedSize(btn_size)
        btn_copia.setIcon(QtGui.QIcon(get_resource_path("copia.png")))
        btn_copia.setToolTip("Copia password")
        btn_copia.clicked.connect(
            lambda _, sid=servizio_id: self.copia_password_servizio(sid))

        # Bottone modifica
        btn_modifica = QPushButton()
        btn_modifica.setFixedSize(btn_size)
        btn_modifica.setIcon(QtGui.QIcon(get_resource_path("modifica.png")))
        btn_modifica.setToolTip("Modifica servizio")
        btn_modifica.clicked.connect(
            lambda _, sid=servizio_id: self.modifica_servizio(sid))

        # Bottone elimina
        btn_elimina = QPushButton()
        btn_elimina.setFixedSize(btn_size)
        btn_elimina.setIcon(QtGui.QIcon(get_resource_path("cestino.png")))
        btn_elimina.setToolTip("Elimina servizio")
        btn_elimina.clicked.connect(
            lambda _, sid=servizio_id: self.elimina_servizio(sid))

        layout.addWidget(btn_mostra)
        layout.addWidget(btn_copia)
        layout.addWidget(btn_modifica)
        layout.addWidget(btn_elimina)

        return widget

    def elimina_servizio(self, servizio_id):
        self.db.elimina_servizio(servizio_id)
        self.servizi = [s for s in self.servizi if s[0] != servizio_id]
        self.elimina_riga(servizio_id)

    def elimina_riga(self, servizio_id):
        num = self.ui.main_tbl_servizi.rowCount()
        for r in range(num):
            item = self.ui.main_tbl_servizi.item(r, 0)
            if item is None:
                continue
            if int(item.data(QtCore.Qt.ItemDataRole.UserRole)) == int(servizio_id):
                self.ui.main_tbl_servizi.removeRow(r)
                break

    def mostra_password_servizio(self, servizio_id):
        # esempio: toggle mostra/nascondi usando userRole per recuperare password reale
        row = self.find_row_by_id(servizio_id)
        if row == -1:
            return
        item = self.ui.main_tbl_servizi.item(row, 2)
        if not item:
            return
        current = item.text()
        real_pass = item.data(QtCore.Qt.ItemDataRole.UserRole)
        if current.startswith("•"):
            item.setText(real_pass)
        else:
            item.setText("••••••••")

    def copia_password_servizio(self, servizio_id):
        row = self.find_row_by_id(servizio_id)
        if row == -1:
            return
        item = self.ui.main_tbl_servizi.item(row, 2)
        if not item:
            return
        real_pass = item.data(QtCore.Qt.ItemDataRole.UserRole)
        QtGui.QGuiApplication.clipboard().setText(str(real_pass))
        QMessageBox.information(
            self, "Copia", "Password copiata negli appunti")

    def modifica_servizio(self, servizio_id):
        # implementa secondo necessità
        pass

    def find_row_by_id(self, servizio_id: int) -> int:
        """Ritorna l'indice di riga che contiene servizio_id nella colonna 0, o -1 se non trovato."""
        for r in range(self.ui.main_tbl_servizi.rowCount()):
            item = self.ui.main_tbl_servizi.item(r, 0)
            if item is None:
                continue
            try:
                if int(item.data(QtCore.Qt.ItemDataRole.UserRole)) == int(servizio_id):
                    return r
            except Exception:
                continue
        return -1
