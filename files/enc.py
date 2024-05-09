from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Hash import SHA256

def get_key(user_key):
    # Use SHA-256 hash to ensure the key is 32 bytes long
    return SHA256.new(user_key.encode()).digest()

def encrypt_file(file_path, user_key):
    key = get_key(user_key)
    cipher = AES.new(key, AES.MODE_CBC)

    # Read the file in binary mode
    with open(file_path, 'rb') as file:
        plaintext = file.read()

    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    # Write the binary data to a file
    with open('encrypted_data.bin', 'wb') as file:
        file.write(cipher.iv)
        file.write(ciphertext)

    print("File has been encrypted and saved as 'encrypted_data.bin'")

# Usage
user_key = input("Enter your key: ")
encrypt_file('binary_data.bin', user_key)
