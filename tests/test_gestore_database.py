import sqlite3
from gestore_password.utility.gestore_database import inserisci_utente, inserisci_servizio

DB_MEMORY = "file::memory:?cache=shared"
def test_inserisci_utente():
    inserisci_utente("mario", "hash123", b"salt123", DB_MEMORY)
    conn = sqlite3.connect(DB_MEMORY, uri=True)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Utenti WHERE utente = 'mario'")
    row = cur.fetchone()
    conn.close()

    assert row[0] == "mario"
    assert row[1] == "hash123"

def test_inserisci_servizio():
    inserisci_servizio("netflix", "mario@mail.it", "cifrata", "mario", DB_MEMORY)
    conn = sqlite3.connect(DB_MEMORY, uri=True)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Servizi WHERE nome = 'netflix'")
    row = cur.fetchone()
    conn.close
    
    assert row[1] == 'netflix'
    assert row[2] == 'mario@mail.it'
    assert row[3] == 'cifrata'