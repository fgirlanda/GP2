from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QTableWidget, QHeaderView, QTableWidgetItem
from PyQt6 import QtCore, QtGui
from utility.criptatore import decripta
from utility.gestore_path import get_resource_path


class TabellaController(QtCore.QObject):
    elimina_richiesto = QtCore.pyqtSignal(int)
    modifica_richiesta = QtCore.pyqtSignal(int)
    copia_richiesta = QtCore.pyqtSignal(int)
    mostra_richiesta = QtCore.pyqtSignal(int)

    def __init__(self, tabella: QTableWidget):
        super().__init__()
        self.tabella = tabella
        self.setup()

    def setup(self):
        self.tabella.setColumnCount(4)
        self.tabella.setHorizontalHeaderLabels(
            ["Servizio", "Username", "Password", "Azioni"])
        self.tabella.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.tabella.setRowCount(0)

    def aggiorna(self, servizi, key):
        self.tabella.clearContents()
        self.tabella.setRowCount(len(servizi))
        for row, servizio in enumerate(servizi):
            self.aggiungi_riga(servizio, row, key)

    def aggiungi_riga(self, servizio, row, key):
        nome = servizio[1]
        username = servizio[2]
        password = decripta(servizio[3], key)

        item_nome = QTableWidgetItem(nome)
        item_nome.setData(QtCore.Qt.ItemDataRole.UserRole, servizio[0])
        self.tabella.setItem(row, 0, item_nome)

        item_username = QTableWidgetItem(username)
        self.tabella.setItem(row, 1, item_username)

        item_password = QTableWidgetItem("••••••••")
        item_password.setData(QtCore.Qt.ItemDataRole.UserRole, password)
        self.tabella.setItem(row, 2, item_password)

        widget_bottoni = self.crea_bottoni_riga(servizio[0])
        self.tabella.setCellWidget(row, 3, widget_bottoni)

    def crea_bottoni_riga(self, servizio_id: int) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)

        btn_size = QtCore.QSize(24, 24)

        def crea_bottone(icon, tooltip, signal):
            btn = QPushButton()
            btn.setFixedSize(btn_size)
            btn.setIcon(QtGui.QIcon(get_resource_path(icon)))
            btn.setToolTip(tooltip)
            btn.clicked.connect(lambda _, sid=servizio_id: signal.emit(sid))
            return btn

        layout.addWidget(
            crea_bottone("visible.png", "Mostra/Nascondi password",
                         self.mostra_richiesta)
        )
        layout.addWidget(
            crea_bottone("copia.png", "Copia password", self.copia_richiesta)
        )
        layout.addWidget(
            crea_bottone("modifica.png", "Modifica servizio",
                         self.modifica_richiesta)
        )
        layout.addWidget(
            crea_bottone("cestino.png", "Elimina servizio",
                         self.elimina_richiesto)
        )

        return widget

    def find_row_by_id(self, servizio_id: int) -> int:
        for r in range(self.tabella.rowCount()):
            item = self.tabella.item(r, 0)
            if item and item.data(QtCore.Qt.ItemDataRole.UserRole) == servizio_id:
                return r
        return -1

    def elimina_riga(self, servizio_id: int):
        row = self.find_row_by_id(servizio_id)
        if row != -1:
            self.tabella.removeRow(row)

    def toggle_password(self, servizio_id: int):
        row = self.find_row_by_id(servizio_id)
        if row == -1:
            return

        item = self.tabella.item(row, 2)
        real = item.data(QtCore.Qt.ItemDataRole.UserRole)
        item.setText(real if item.text().startswith("•") else "••••••••")

    def copia_password(self, servizio_id: int):
        row = self.find_row_by_id(servizio_id)
        if row == -1:
            return

        pwd = self.tabella.item(row, 2).data(QtCore.Qt.ItemDataRole.UserRole)
        QtGui.QGuiApplication.clipboard().setText(str(pwd))
