from gestore_password.utility.criptatore import derive_key, cripta, decripta
import os

def test_aes():
    pass_utente = "password_utente"
    salt = os.urandom(16)
    pass_servizio = "password_servizio"
    
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
    