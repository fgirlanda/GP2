from pathlib import Path
import sqlite3
import sys
from contextlib import contextmanager

# Path dati
if getattr(sys, 'frozen', False):
    DATI_DIR = Path(sys.executable).resolve().parent / "dati"
else:
    DATI_DIR = Path(__file__).resolve().parent.parent / "dati"

DATI_DIR.mkdir(exist_ok=True)


def get_db_path(utente_loggato: str | None = None):
    if utente_loggato:
        return DATI_DIR / f"{utente_loggato}.db"
    return DATI_DIR / "utenti.db"


@contextmanager
def connetti(dbPath=None):
    """Context manager per connessione SQLite"""
    conn = sqlite3.connect(dbPath, uri=True)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def esegui(query: str, dati: tuple | None = None, conn=None, dbPath=None):
    """Query generica (INSERT, UPDATE, DELETE, CREATE)"""
    with conn if conn else connetti(dbPath) as c:
        cur = c.cursor()
        cur.execute(query, dati or ())
        return cur.lastrowid


def fetch(query: str, dati: tuple | None = None, conn=None, dbPath=None):
    """Esegue SELECT e ritorna tutti i risultati"""
    with conn if conn else connetti(dbPath) as c:
        cur = c.cursor()
        cur.execute(query, dati or ())
        return cur.fetchall()
