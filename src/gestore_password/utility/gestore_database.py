from pathlib import Path
import sqlite3
import sys


# def get_dati_dir():
#     if getattr(sys, 'frozen', False):
#         base_dir =  Path(sys.executable).resolve().parent
#     else:
#         base_dir = Path(__file__).resolve().parent.parent
    
#     return base_dir / "dati"

# dati_dir = get_dati_dir()
# dati_dir.mkdir(exist_ok=True)


# def inserisci_utente(utente, password_hash, salt, dbPath=None):
#     query_create = """CREATE TABLE IF NOT EXISTS Utenti(
#         utente text primary key,
#         hash_password text not null,
#         salt blob not null
#         );"""
#     quey_insert = """INSERT INTO Utenti (utente, hash_password, salt) VALUES(?, ?, ?)"""
    
#     if dbPath is None:
#         dbPath = dati_dir / "utenti.db"
        
#     with sqlite3.connect(dbPath, uri=True) as conn:
#         cursor = conn.cursor()
#         cursor.execute(query_create)
#         cursor.execute(quey_insert, (utente, password_hash, salt))
#         conn.commit()
        
        
# def inserisci_servizio(nome, username, password_cifrata, utente, dbPath = None):
#     query_create = """CREATE TABLE IF NOT EXISTS Servizi(
#         id integer primary key autoincrement,
#         nome text,
#         username text,
#         password_cifrata text not null
#         );"""
#     query_insert = """INSERT INTO Servizi (nome, username, password_cifrata) VALUES (?, ?, ?)"""
    
#     if dbPath is None:
#         dbPath = dati_dir / f"{utente}.db"
    
#     with sqlite3.connect(dbPath, uri=True) as conn:
#         cursor = conn.cursor()
#         cursor.execute(query_create)
#         cursor.execute(query_insert, (nome, username, password_cifrata))
#         conn.commit()
        


# RIVEDERE IL TUTTO PIU' GENERICO (crea tabella, inserisci elemento ecc.)

if getattr(sys, 'frozen', False):
    dati_dir = Path(sys.executable).resolve().parent / "dati"
else:
    dati_dir = Path(__file__).resolve().parent.parent / "dati"  
dati_dir.mkdir(exist_ok=True)
    
def crea_tabella(utente: str, dbPath=None):
    if utente:
        if not dbPath is None:
            dbPath = dati_dir / "utenti.db"
        query_create = """CREATE TABLE IF NOT EXISTS Utenti(
            utente text primary key,
            hash_password text not null,
            salt blob not null
            );"""
    else:
        if not dbPath is None:
            dbPath = dati_dir / f"{utente}.db"
        query_create = """CREATE TABLE IF NOT EXISTS Servizi(
          id integer primary key autoincrement,
          nome text,
          username text,
          password_cifrata text not null
          );"""
        
    with sqlite3.connect(dbPath, uri=True) as conn:
        cur = conn.cursor()
        cur.execute(query_create)
        conn.commit()
    