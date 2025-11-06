from gestore_password.utility.criptatore import derive_key, cripta, decripta, genera_hash, verifica_password
import os

pass_utente = "password_utente"
pass_servizio = "password_servizio"

def test_aes():
    salt = os.urandom(16)
    
    key = derive_key(pass_utente, salt)
    test_cifra = cripta(pass_servizio, key)
    test_decifra = decripta(test_cifra, key)
    
    print("== TEST ALGORITMO AES-256 ==\n\n",
          "Originale utente = ", pass_utente, "\n",
          "Originale servizio = ", pass_servizio, "\n\n",
          "Key = ", key, "\n",
          "Salt = ", salt, "\n\n",
          "Criptata = ", test_cifra, "\n",
          "Decriptata = ", test_decifra)
    
def test_hash():
    hash_corretto = genera_hash(pass_utente)
    risultato_corretto = verifica_password(pass_utente, hash_corretto)
    
    hash_errato = "errore"
    risultato_errato = verifica_password(pass_utente, hash_errato)
    print("\n== TEST ALGORITMO HASHING ==\n\n", 
          "Output corretto = ",risultato_corretto, "\n",
          "Output errato = ", risultato_errato)
    