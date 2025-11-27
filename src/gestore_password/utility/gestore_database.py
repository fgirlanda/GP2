from pathlib import Path
import sqlite3
import sys
from contextlib import contextmanager


# ============================
# CLASSE DATABASE MANAGER
# ============================


class GestoreDatabase:

    def __init__(self, in_memory: bool = False):
        """:param in_memory: se True usa database temporaneo in RAM (":memory:")"""
        if in_memory:
            self.conn = sqlite3.connect(":memory:")
        else:
            if getattr(sys, 'frozen', False):
                BASE_DIR = Path(sys.executable).resolve().parent
            else:
                BASE_DIR = Path(__file__).resolve().parent.parent

            DATI_DIR = BASE_DIR / "dati"
            DB_PATH = DATI_DIR / "db_gestore.db"
            DATI_DIR.mkdir(parents=True, exist_ok=True)
            self.conn = sqlite3.connect(DB_PATH)

        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.cur = self.conn.cursor()
        self.crea_tabelle()

    def chiudi(self):

        self.conn.close()

    # ============================
    # CREAZIONE STRUTTURA DB
    # ============================

    def crea_tabelle(self):

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Utenti(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        utente TEXT UNIQUE NOT NULL,
        hash_password TEXT NOT NULL,
        salt BLOB NOT NULL
            )
            ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS Servizi(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_utente INTEGER NOT NULL,
        nome TEXT NOT NULL,
        username TEXT NOT NULL,
        password_cifrata BLOB NOT NULL,
        FOREIGN KEY(id_utente) REFERENCES Utenti(id) ON DELETE CASCADE
            )
            ''')

        self.conn.commit()

    # ============================
    # CRUD UTENTI
    # ============================
    # dati = (utente, hash_password, salt)
    def inserisci_utente(self, dati: tuple):

        self.cur.execute(
            "INSERT INTO Utenti (utente, hash_password, salt) VALUES (?, ?, ?)",
            dati
        )
        self.conn.commit()

    # dati = (utente, hash_password)
    def get_id_utente(self, dati: tuple):
        self.cur.execute(
            "SELECT id FROM Utenti WHERE utente = ? AND hash_password = ?",
            dati
        )
        riga = self.cur.fetchone()
        id_utente = riga[0]
        return id_utente if id_utente else None

    # nuovi_dati = (nuovo_utente, nuovo_hash)
    def aggiorna_dati_utente(self, id_utente: int, nuovi_dati: tuple):
        self.cur.execute(
            "UPDATE Utenti SET utente = ?, hash_password = ? WHERE id = ?",
            (nuovi_dati, id_utente)
        )
        self.conn.commit()

    def elimina_utente(self, id_utente):
        self.cur.execute(
            "DELETE FROM Utenti WHERE id = ?",
            (id_utente,)
        )
        self.conn.commit()

    def get_utente(self, utente, hash_password):
        self.cur.execute(
            "SELECT id, utente, hash_password, salt FROM Utenti WHERE utente = ? AND hash_password = ?",
            (utente, hash_password)
        )
        return self.cur.fetchone()

    # ============================
    # CRUD SERVIZI
    # ============================

    # dati = (nome, username, password_cifrata)
    def inserisci_servizio(self, id_utente, dati: tuple):

        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO Servizi (id_utente, nome, username, password_cifrata) VALUES (?, ?, ?, ?)",
            (id_utente, dati)
        )
        self.conn.commit()

    # nuovi_dati = (nuovo_nome, nuovo_username, nuova_password_cifrata)
    def aggiorna_servizio(self, id_servizio, nuovi_dati):

        cursor = self.conn.cursor()
        cursor.execute(
            """UPDATE Servizi
        SET nome = ?, username = ?, password_cifrata = ?
        WHERE id = ?""",
            (nuovi_dati, id_servizio)
        )
        self.conn.commit()

    def elimina_servizio(self, id_servizio):

        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM Servizi WHERE id = ?",
            (id_servizio,)
        )
        self.conn.commit()

    def get_servizi_per_utente(self, id_utente):

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, nome, username, password_cifrata FROM Servizi WHERE idUtente = ?",
            (id_utente,)
        )
        return cursor.fetchall()

    # def get_servizio_by_id(self, id_servizio):

    #     cursor = self.conn.cursor()
    #     cursor.execute(
    #         "SELECT id, nome, username, password_cifrata FROM Servizi WHERE id = ?",
    #         (id_servizio,)
    #     )
    #     return cursor.fetchone()
