import pytest
from gestore_password.utility.gestore_database import GestoreDatabase


@pytest.fixture
def db():
    db = GestoreDatabase(in_memory=True)
    yield db
    db.chiudi()


def test_init(db: GestoreDatabase):
    assert db.conn is not None


def test_crea_utente(db: GestoreDatabase):
    utente = "mario"
    hash_password = "prova_hash"
    salt = b"prova_salt"
    prova_dati = (utente, hash_password, salt)
    db.inserisci_utente(prova_dati)

    assert db.get_utente(utente) is not None
