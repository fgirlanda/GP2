from PyQt6.QtWidgets import QWidget, QHeaderView, QTableWidgetItem, QGridLayout, QPushButton
from PyQt6 import QtCore, QtGui
from views.view_principale import Ui_Main
from utility.criptatore import *
from utility.gestore_database import GestoreDatabase
from utility.gestore_path import *


class Principale(QWidget):
    def __init__(self, db: GestoreDatabase):
        super().__init__()
        self.ui = Ui_Main()
        self.ui.setupUi(self)
        self.titolo = "Gestore Password"
        self.db = db

    def set_utente_loggato(self, utente: tuple, raw_pass: str):
        self.utente_loggato = utente
        self.key = derive_key(raw_pass, utente[3])
        self.set_dati_utente(utente[1], raw_pass)
        self.setup_tabella()
        self.popola_tabella()

    def set_dati_utente(self, utente: str, raw_pass: str):
        self.ui.main_dlbl_utente.setText(utente[1])
        self.ui.main_dlbl_password.setText(raw_pass)

    def setup_tabella(self):
        self.ui.main_tbl_servizi.setColumnCount(4)
        self.ui.main_tbl_servizi.setHorizontalHeaderLabels(
            ["Servizio", "Username", "Password", "Azioni"])
        self.ui.main_tbl_servizi.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)

    def popola_tabella(self):
        self.servizi = self.db.get_servizi_per_utente(self.utente_loggato[0])
        for servizio in self.servizi:
            row = 0
            self.aggiungi_riga_servizio(servizio, row)
            row += 1

    def aggiungi_riga_servizio(self, servizio: tuple, row: int):
        nome = servizio[2]
        username = servizio[3]
        password = decripta(servizio[4], self.key)

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

    def crea_bottoni_riga(self, servizio_id) -> QWidget:
        widget = QWidget()
        layout = QGridLayout(widget)
        layout.setSpacing(5)

        # Bottone elimina
        btn_elimina = QPushButton()
        icon_del = QtGui.QIcon()
        icon_del.addPixmap(QtGui.QPixmap(get_resource_path("cestino.png")),
                           QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        btn_elimina.setIcon(icon_del)
        btn_elimina.clicked.connect(lambda: self.elimina_servizio(servizio_id))

        # Bottone mostra password
        btn_mostra = QPushButton()
        icon_mostra = QtGui.QIcon()
        icon_mostra.addPixmap(QtGui.QPixmap(get_resource_path("visibile.png")),
                              QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        btn_mostra.setIcon(icon_mostra)
        btn_mostra.clicked.connect(
            lambda: self.mostra_password_servizio(servizio_id))

        # Bottone copia password
        btn_copia = QPushButton()
        icon_copia = QtGui.QIcon()
        icon_copia.addPixmap(QtGui.QPixmap(get_resource_path("copia.png")),
                             QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        btn_copia.setIcon(icon_copia)
        btn_copia.clicked.connect(
            lambda: self.copia_password_servizio(servizio_id))

        # Bottone modifica servizio
        btn_modifica = QPushButton()
        icon_modifica = QtGui.QIcon()
        icon_modifica.addPixmap(QtGui.QPixmap(get_resource_path("modifica.png")),
                                QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        btn_modifica.setIcon(icon_modifica)
        btn_modifica.clicked.connect(
            lambda: self.modifica_password_servizio(servizio_id))

        layout.addWidget(btn_elimina, 0, 0)
        layout.addWidget(btn_mostra, 0, 1)
        layout.addWidget(btn_copia, 1, 0)
        layout.addWidget(btn_modifica, 1, 1)

        return widget

    def elimina_servizio(self, servizio_id):
        pass

    def mostra_password_servizio(self, servizio_id):
        pass

    def copia_password_servizio(self, servizio_id):
        pass

    def modifica_password_servizio(self, servizio_id):
        pass
