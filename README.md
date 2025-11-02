# GP2
Gestore Password v2


# Progettazione (in progress)

## Architettura

### GUI

* Libreria/ambiente: pyqt6, qt designer
* Gestione finestre: QStackedWidget
* Visualizzazione principale: QAbstractModel (tabella + mvc)

### Dati

* Database: sqlite
* Sicurezza: 
    * password master Argon2id (lib argon2-cffi) 
    *  password servizi AES-256 (lib cryptography)
* DB Utenti
* DB Servizi*Utente*

## Design

### GUI

Finestre:
* Log in
    * textfield Utente
    * textfield Password
    * btn Registrati
    * btn Login

* Registrazione
    * textfield Utente
    * textfield Password
    * btn Annulla -> Finestra Log in
    * btn Registrati

* Principale
    * textfield Cerca
    * btn Profilo -> Finestra Profilo
    * btn Esci
    * tab Servizi
        * Servizio
        * Username
        * Password
        * btns
            * btn Modifica -> Finestra Modifica servizio
            * btn Elimina

* Profilo
    * label Username
    * label Password
    * btn Mostra password
    * btn Indietro -> Finestra Principale
    * btn Modifica profilo -> Finestra Modifica profilo

* Aggiungi servizio
    * ...

* Modifica servizio
    * textfield nuovo_nome
    * textfield nuovo_username
    * textfield vecchia_password
    * textfield nuova_password
    * btn Conferma
    * btn Annulla -> Finestra Principale

* Modifica profilo
    * textfield Utente
    * textfield vecchia_password
    * textfield nuova_password
    * btn Conferma
    * btn Annulla -> Finestra Principale


## Requisiti

### Funzionali

* Creare uno/più utente/i (Registrazione)
* Modificare proprio utente (Profilo -> Modifica profilo)
* Recupero password (prossime versioni)
* Visualizzare proprie password
* Modificare servizio (Principale -> Modifica servizio)
* Aggiungere servizi (Principale -> Aggiungi servizio)
* ...

### Non Funzionali

* Criptazione password master
* Criptazione password servizi
* Velocità caricamento
* Semplicità di utilizzo


