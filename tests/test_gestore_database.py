import pytest
from gestore_password.utility.gestore_database import connetti, esegui, fetch

DB_MEMORY = "file::memory:?cache=shared"  # Database isolato in memoria per ogni test


def test_utente():
    with connetti(DB_MEMORY) as conn:
        # Creazione tabella Utenti
        esegui("""
        CREATE TABLE IF NOT EXISTS Utenti(
            utente TEXT PRIMARY KEY,
            hash_password TEXT NOT NULL,
            salt BLOB NOT NULL
        )
        """, conn=conn)

        # Inserimento utente
        esegui(
            "INSERT INTO Utenti (utente, hash_password, salt) VALUES (?, ?, ?)",
            ("mario", "hash123", b"salt"),
            conn=conn
        )

        # Verifica inserimento
        row = fetch("SELECT * FROM Utenti WHERE utente = ?", ("mario",), conn=conn)[0]
        assert row[0] == "mario"
        assert row[1] == "hash123"
        assert row[2] == b"salt"

        # Modifica utente
        esegui(
            "UPDATE Utenti SET utente=?, hash_password=?, salt=? WHERE utente=?",
            ("luca", "hash456", b"nuovo salt", "mario"),
            conn=conn
        )
        row = fetch("SELECT * FROM Utenti WHERE utente = ?", ("luca",), conn=conn)[0]
        assert row[0] == "luca"
        assert row[1] == "hash456"
        assert row[2] == b"nuovo salt"

        # Cancellazione utente
        esegui("DELETE FROM Utenti WHERE utente=?", ("luca",), conn=conn)
        rows = fetch("SELECT * FROM Utenti WHERE utente = ?", ("luca",), conn=conn)
        assert rows == []


def test_servizio():
    with connetti(DB_MEMORY) as conn:
        # Creazione tabella Servizi
        esegui("""
        CREATE TABLE IF NOT EXISTS Servizi(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            username TEXT,
            password_cifrata TEXT NOT NULL
        )
        """, conn=conn)

        # Inserimento servizio
        esegui(
            "INSERT INTO Servizi (nome, username, password_cifrata) VALUES (?, ?, ?)",
            ("netflix", "mario@mail.it", "cifrata"),
            conn=conn
        )

        # Verifica inserimento
        row = fetch("SELECT * FROM Servizi WHERE username = ?", ("mario@mail.it",), conn=conn)[0]
        assert row[1] == "netflix"
        assert row[2] == "mario@mail.it"
        assert row[3] == "cifrata"

        # Modifica servizio
        esegui(
            "UPDATE Servizi SET nome=?, username=?, password_cifrata=? WHERE id=?",
            ("prime video", "luca@mail.it", "nuova cifrata", row[0]),
            conn=conn
        )
        row = fetch("SELECT * FROM Servizi WHERE username = ?", ("luca@mail.it",), conn=conn)[0]
        assert row[1] == "prime video"
        assert row[2] == "luca@mail.it"
        assert row[3] == "nuova cifrata"

        # Cancellazione servizio
        esegui("DELETE FROM Servizi WHERE id=?", (row[0],), conn=conn)
        rows = fetch("SELECT * FROM Servizi WHERE username = ?", ("luca@mail.it",), conn=conn)
        assert rows == []
