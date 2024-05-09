from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Hash import SHA256

def get_key(user_key):
    # Use SHA-256 hash to ensure the key is 32 bytes long
    return SHA256.new(user_key.encode()).digest()

def decrypt_file(file_path, user_key, output_file_path):
    key = get_key(user_key)

    # Read the binary data from the file
    with open(file_path, 'rb') as file:
        iv = file.read(16)
        ciphertext = file.read()

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    # Write the binary data back to its original form
    with open(output_file_path, 'wb') as file:
        file.write(plaintext)

    print(f"File has been decrypted and saved as '{output_file_path}'")

# Usage
user_key = input("Enter your key: ")
decrypt_file('reconstructed_data.bin', user_key, 'decrypted_data.bin')
