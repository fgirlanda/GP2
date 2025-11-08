from pathlib import Path
import sqlite3
import sys

if getattr(sys, 'frozen', False):
    dati_dir = Path(sys.executable).resolve().parent / "dati"
else:
    dati_dir = Path(__file__).resolve().parent.parent / "dati"  
dati_dir.mkdir(exist_ok=True)


def connetti(utente_loggato: str, dbPath=None):
    global conn
    if dbPath is None:
        if utente_loggato:
            dbPath = dati_dir / f"{utente_loggato}.db"
        else:
            dbPath = dati_dir / "utenti.db"
            
    conn = sqlite3.connect(dbPath, uri=True)

def crea_tabella(query_create):
    global conn
    with conn:
        cur = conn.cursor()
        cur.execute(query_create)
        conn.commit()
    
def inserisci_dati(query_insert, dati):
    global conn
    with conn:
        cur = conn.cursor()
        cur.execute(query_insert, (dati[0], dati[1], dati[2]))
        conn.commit()
    
def rimuovi_dati(query_delete, key):
    global conn
    with conn:
        cur = conn.cursor()
        cur.execute(query_delete, key)
        conn.commit()

def modifica_dati(query_update, dati):
    global conn
    with conn:
        cur = conn.cursor()
        cur.execute(query_update, dati)
        conn.commit()
    
    