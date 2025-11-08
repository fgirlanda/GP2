import sqlite3
from gestore_password.utility.gestore_database import connetti, crea_tabella, inserisci_dati, rimuovi_dati, modifica_dati
DB_MEMORY = "file::memory:?cache=shared"
def test_utente():
    # Connessione + creazione tabella
    connetti(None, DB_MEMORY)
    query_create_utenti = """CREATE TABLE IF NOT EXISTS Utenti(
            utente text primary key,
            hash_password text not null,
            salt blob not null
            );"""
    crea_tabella(query_create_utenti)
    
    # Inserimento
    query_insert_utente = "INSERT INTO Utenti (utente, hash_password, salt) VALUES(?, ?, ?)"
    dati_utente = ["mario", "hash123", b"salt"]
    inserisci_dati(query_insert_utente, dati_utente)
    conn = sqlite3.connect(DB_MEMORY, uri=True)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Utenti WHERE utente = 'mario'")
    row = cur.fetchone()
    assert row[0] == "mario"
    assert row[1] == "hash123"
    
    # Modifica
    query_update_utente = "UPDATE Utenti SET utente=?, hash_password=?, salt=? WHERE utente='mario'"
    dati_update_utente = ["luca", "hash456", b"nuovo salt"]
    modifica_dati(query_update_utente, dati_update_utente)
    cur.execute("SELECT * FROM Utenti WHERE utente = 'luca'")
    row = cur.fetchone()

    assert row[0] == "luca"
    assert row[1] == "hash456"
    
    # Cancellazione
    query_delete_utente = "DELETE FROM Utenti WHERE utente=?"
    key_utente=("mario",)
    rimuovi_dati(query_delete_utente, key_utente)
    cur.execute("SELECT * FROM Utenti WHERE utente = 'mario'")
    row = cur.fetchone()
    assert row == None
    
    conn.close()

    
def test_servizio():
    # Connessione + creazione tabella
    connetti("mario", DB_MEMORY)
    query_create_servizi = """CREATE TABLE IF NOT EXISTS Servizi(
            id integer primary key autoincrement,
            nome text,
            username text,
            password_cifrata text not null
            );"""
    crea_tabella(query_create_servizi)
    
    # Inserimento
    query_insert_servizio = "INSERT INTO Servizi (nome, username, password_cifrata) VALUES(?, ?, ?)"
    dati_servizio = ["netflix", "mario@mail.it", "cifrata"]
    inserisci_dati(query_insert_servizio, dati_servizio)
    
    conn = sqlite3.connect(DB_MEMORY, uri=True)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Servizi WHERE username = 'mario@mail.it'")
    row = cur.fetchone()

    assert row[1] == "netflix"
    assert row[2] == "mario@mail.it"
    assert row[3] == "cifrata"
    
    # Modifica
    
    query_update_servizio = "UPDATE Servizi SET nome=?, username=?, password_cifrata=? WHERE id=?"
    dati_update_servizio = ["prime video", "luca@mail.it", "nuova cifrata", 1]
    modifica_dati(query_update_servizio, dati_update_servizio)
    cur.execute("SELECT * FROM Servizi WHERE username = 'luca@mail.it'")
    row = cur.fetchone()

    assert row[1] == "prime video"
    assert row[2] == "luca@mail.it"
    assert row[3] == "nuova cifrata"
    
    # Cancellazione
    query_delete_servizio = "DELETE FROM Servizi WHERE id=?"
    key_servizio = (1,)
    rimuovi_dati(query_delete_servizio, key_servizio)
    cur.execute("SELECT * FROM Servizi WHERE username='mario@mail.it'")
    row = cur.fetchone()
    assert row == None
    
    conn.close()