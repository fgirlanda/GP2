from pathlib import Path
import sqlite3
import sys


def get_dati_dir():
    if getattr(sys, 'frozen', False):
        base_dir =  Path(sys.executable).resolve().parent
    base_dir = Path(__file__).resolve().parent.parent
    
    return base_dir / "dati"

dati_dir = get_dati_dir()
database_utenti = dati_dir / "utenti.db"

def inserisci_utente(username, password_hash):
    conn = sqlite3.connect(database_utenti)