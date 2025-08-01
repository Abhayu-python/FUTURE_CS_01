from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

KEY_FILE = 'secret.key'

def generate_key():
    key = get_random_bytes(16)
    with open(KEY_FILE, 'wb') as f:
        f.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, 'rb') as f:
        return f.read()

def pad(data):
    return data + b"\0" * (AES.block_size - len(data) % AES.block_size)

def encrypt_file(input_path, output_path, key):
    cipher = AES.new(key, AES.MODE_ECB)
    with open(input_path, 'rb') as f:
        data = f.read()
    encrypted = cipher.encrypt(pad(data))
    with open(output_path, 'wb') as f:
        f.write(encrypted)

def decrypt_file(input_path, output_path, key):
    cipher = AES.new(key, AES.MODE_ECB)
    with open(input_path, 'rb') as f:
        data = f.read()
    decrypted = cipher.decrypt(data).rstrip(b"\0")
    with open(output_path, 'wb') as f:
        f.write(decrypted)
