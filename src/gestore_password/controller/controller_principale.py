from PyQt6.QtWidgets import QWidget, QHeaderView, QTableWidgetItem, QGridLayout, QPushButton, QMessageBox, QHBoxLayout
from PyQt6 import QtCore, QtGui
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
        """Gestisce la chiusura del dialog"""
        if risultato:
            QMessageBox.information(
                self, "Successo", "Il servizio è stato aggiunto")
        self.dialog_aggiungi = None

    def apri_dialog_aggiungi(self):
        self.dialog_aggiungi = Dialog_Aggiungi(
            self.db, self.utente_loggato, self.key)
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
        self.ui.main_tbl_servizi.setRowCount(len(self.servizi))
        self.ui.main_tbl_servizi.setHorizontalHeaderLabels(
            ["Servizio", "Username", "Password", "Azioni"])
        self.ui.main_tbl_servizi.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

    def popola_tabella(self):
        row = 0
        for servizio in self.servizi:
            print(servizio)
            self.aggiungi_riga_servizio(servizio, row)
            row += 1

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

        widget_bottoni = self.crea_bottoni_riga(servizio[0], row)
        self.ui.main_tbl_servizi.setCellWidget(row, 3, widget_bottoni)

    def crea_bottoni_riga(self, servizio_id: int, row: int) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)  # Usa HBoxLayout per bottoni orizzontali
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)

        # Crea bottoni più piccoli
        btn_size = QtCore.QSize(24, 24)

        # Bottone mostra password
        btn_mostra = QPushButton()
        btn_mostra.setFixedSize(btn_size)
        btn_mostra.setIcon(QtGui.QIcon(get_resource_path("visible.png")))
        btn_mostra.setToolTip("Mostra/Nascondi password")
        btn_mostra.clicked.connect(lambda: self.mostra_password_servizio(row))

        # Bottone copia
        btn_copia = QPushButton()
        btn_copia.setFixedSize(btn_size)
        btn_copia.setIcon(QtGui.QIcon(get_resource_path("copia.png")))
        btn_copia.setToolTip("Copia password")
        btn_copia.clicked.connect(lambda: self.copia_password_servizio(row))

        # Bottone modifica
        btn_modifica = QPushButton()
        btn_modifica.setFixedSize(btn_size)
        btn_modifica.setIcon(QtGui.QIcon(get_resource_path("modifica.png")))
        btn_modifica.setToolTip("Modifica servizio")
        btn_modifica.clicked.connect(
            lambda: self.modifica_servizio(servizio_id))

        # Bottone elimina
        btn_elimina = QPushButton()
        btn_elimina.setFixedSize(btn_size)
        btn_elimina.setIcon(QtGui.QIcon(get_resource_path("cestino.png")))
        btn_elimina.setToolTip("Elimina servizio")
        btn_elimina.clicked.connect(lambda: self.elimina_servizio(servizio_id))

        layout.addWidget(btn_mostra)
        layout.addWidget(btn_copia)
        layout.addWidget(btn_modifica)
        layout.addWidget(btn_elimina)

        return widget

    def elimina_servizio(self, servizio_id):
        pass

    def mostra_password_servizio(self, servizio_id):
        pass

    def copia_password_servizio(self, servizio_id):
        pass

    def modifica_servizio(self, servizio_id):
        pass
