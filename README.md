# GP2
Gestore Password v2


# Progettazione

## Architettura

### GUI

- Libreria/ambiente: pyqt6, qt designer
- Gestione finestre: QStackedWidget
- Visualizzazione principale: QAbstractModel (tabella + mvc)

### Dati

- Database: sqlite
- Sicurezza: - password master Argon2id (lib argon2-cffi) 
             - password servizi AES-256 (lib cryptography)
- DB Utenti
- DB Servizi*Utente*

## Design

### GUI

Finestre:
- Log in
- Registrazione
- Principale
