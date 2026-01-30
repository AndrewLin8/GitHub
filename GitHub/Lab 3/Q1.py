from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

meessage = b"Hello, cryptography!"

encrypted = cipher.encrypt(meessage)
print("Encrypted message:", encrypted)
decrypted = cipher.decrypt(encrypted)
print("Decrypted message:", decrypted.decode('utf-8'))