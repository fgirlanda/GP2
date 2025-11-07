import sqlite3
from gestore_password.utility.gestore_database import connetti, crea_tabella, inserisci_dati
DB_MEMORY = "file::memory:?cache=shared"
def test_utente():
    connetti(None, DB_MEMORY)
    query_create_utenti = """CREATE TABLE IF NOT EXISTS Utenti(
            utente text primary key,
            hash_password text not null,
            salt blob not null
            );"""
    crea_tabella(query_create_utenti)
    query_insert_utente = "INSERT INTO Utenti (utente, hash_password, salt) VALUES(?, ?, ?)"
    dati_utente = ["mario", "hash123", b"salt"]
    inserisci_dati(query_insert_utente, dati_utente)
    
    conn = sqlite3.connect(DB_MEMORY, uri=True)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Utenti WHERE utente = 'mario'")
    row = cur.fetchone()
    conn.close()

    assert row[0] == "mario"
    assert row[1] == "hash123"
    
def test_servizio():
    connetti("mario", DB_MEMORY)
    query_create_servizi = """CREATE TABLE IF NOT EXISTS Servizi(
            id integer primary key autoincrement,
            nome text,
            username text,
            password_cifrata text not null
            );"""
    crea_tabella(query_create_servizi)
    query_insert_servizio = "INSERT INTO Servizi (nome, username, password_cifrata) VALUES(?, ?, ?)"
    dati_servizio = ["netflix", "mario@mail.it", "cifrata"]
    inserisci_dati(query_insert_servizio, dati_servizio)
    
    conn = sqlite3.connect(DB_MEMORY, uri=True)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Servizi WHERE username = 'mario@mail.it'")
    row = cur.fetchone()
    conn.close()

    assert row[1] == "netflix"
    assert row[2] == "mario@mail.it"
    assert row[3] == "cifrata"