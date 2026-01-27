from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

encoded_text = cipher_suite.encrypt(b"This is a really secret message")
print(f"Encoded_text: {encoded_text}")

# use the cryptography library to code and decode a message
decoded_text = cipher_suite.decrypt(encoded_text)
print(f"Decoded_text: {decoded_text.decode('utf-8')}")

