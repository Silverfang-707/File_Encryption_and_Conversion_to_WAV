import wave
import os
import logging
import multiprocessing
import zlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
from tkinter import Tk, filedialog, simpledialog, messagebox, StringVar, OptionMenu, Button

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Progress feedback function
def progress_callback(progress):
    logger.info(f"Progress: {progress}%")

def convert_to_binary(file_path, binary_file_path):
    """Converts a file to binary format."""
    try:
        with open(file_path, 'rb') as file:
            binary_data = file.read()

        with open(binary_file_path, 'wb') as file:
            file.write(binary_data)
    except FileNotFoundError:
        logger.error("File not found: %s", file_path)
        raise
    except Exception as e:
        logger.error("Error converting file to binary: %s", e)
        raise

def reconstruct_from_binary(binary_file_path, output_file_path):
    """Reconstructs a binary file to its original form."""
    try:
        with open(binary_file_path, 'rb') as file:
            binary_data = file.read()

        with open(output_file_path, 'wb') as file:
            file.write(binary_data)
    except Exception as e:
        logger.error("Error reconstructing binary file: %s", e)
        raise

def get_key(user_key):
    """Hashes the user key to ensure it's the required size."""
    try:
        return SHA256.new(user_key.encode()).digest()
    except Exception as e:
        logger.error("Error generating key: %s", e)
        raise

def encrypt_file(file_path, user_key):
    """Encrypts the binary file."""
    try:
        key = get_key(user_key)
        cipher = AES.new(key, AES.MODE_CBC)

        with open(file_path, 'rb') as file:
            plaintext = file.read()

        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

        with open('encrypted_data.bin', 'wb') as file:
            file.write(cipher.iv)
            file.write(ciphertext)
    except Exception as e:
        logger.error("Error encrypting file: %s", e)
        raise

def decrypt_file(file_path, user_key, output_file_path):
    """Decrypts the binary file."""
    try:
        key = get_key(user_key)

        with open(file_path, 'rb') as file:
            iv = file.read(16)
            ciphertext = file.read()

        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

        with open(output_file_path, 'wb') as file:
            file.write(plaintext)
    except Exception as e:
        logger.error("Error decrypting file: %s", e)
        raise

def bin_to_audio(bin_file_path, output_file_path, nchannels=1, sampwidth=2, framerate=44100):
    """Converts the binary file into WAV format."""
    try:
        with open(bin_file_path, 'rb') as file:
            binary_data = file.read()

        with wave.open(output_file_path, 'wb') as wav_file:
            wav_file.setnchannels(nchannels)
            wav_file.setsampwidth(sampwidth)
            wav_file.setframerate(framerate)
            wav_file.writeframes(binary_data)
    except Exception as e:
        logger.error("Error converting binary to audio: %s", e)
        raise

def audio_to_bin(input_file_path, bin_file_path):
    """Converts the audio file back to binary."""
    try:
        with wave.open(input_file_path, 'rb') as wav_file:
            binary_data = wav_file.readframes(wav_file.getnframes())

        with open(bin_file_path, 'wb') as file:
            file.write(binary_data)
    except Exception as e:
        logger.error("Error converting audio to binary: %s", e)
        raise

def compress_file(input_file_path, compressed_file_path):
    """Compresses a file using zlib compression."""
    try:
        with open(input_file_path, 'rb') as file:
            data = file.read()

        compressed_data = zlib.compress(data)

        with open(compressed_file_path, 'wb') as file:
            file.write(compressed_data)
    except Exception as e:
        logger.error("Error compressing file: %s", e)
        raise

def decompress_file(compressed_file_path, output_file_path):
    """Decompresses a zlib-compressed file."""
    try:
        with open(compressed_file_path, 'rb') as file:
            compressed_data = file.read()

        decompressed_data = zlib.decompress(compressed_data)

        with open(output_file_path, 'wb') as file:
            file.write(decompressed_data)
    except Exception as e:
        logger.error("Error decompressing file: %s", e)
        raise

def file_to_wav(filename, user_key):
    """Encrypts a file, compresses it, and converts it to WAV format."""
    try:
        convert_to_binary(filename, 'binary_data.bin')
        encrypt_file('binary_data.bin', user_key)
        compressed_file_path = 'compressed_data.bin'
        compress_file('encrypted_data.bin', compressed_file_path)
        bin_to_audio(compressed_file_path, 'output.wav')
        logger.info('File encrypted, compressed, and saved as output.wav')
        os.remove('binary_data.bin')
        os.remove('encrypted_data.bin')
        os.remove(compressed_file_path)
    except Exception as e:
        logger.error("Error processing file to WAV: %s", e)
        raise

def wav_to_file(filename, user_key):
    """Decrypts a WAV file, decompresses it, and reconstructs the original file."""
    try:
        exten = simpledialog.askstring("Extension", "Enter the extension of the original file (without dot): ")
        if not exten:
            logger.info("No extension provided.")
            return
        output_file_path = f"reconstructed.{exten}"

        if os.path.exists(output_file_path):
            choice = messagebox.askyesno("File Exists", f"Warning! {output_file_path} already exists. Do you want to continue?")
            if not choice:
                logger.info("Operation cancelled by user.")
                return

        audio_to_bin(filename, 'compressed_data.bin')
        decompressed_file_path = 'decrypted_data.bin'
        decompress_file('compressed_data.bin', decompressed_file_path)
        decrypt_file(decompressed_file_path, user_key, 'binary_data.bin')
        reconstruct_from_binary('binary_data.bin', output_file_path)
        logger.info(f'File decrypted, decompressed, and saved as {output_file_path}')
        os.remove('binary_data.bin')
        os.remove('compressed_data.bin')
        os.remove(decompressed_file_path)
    except Exception as e:
        os.remove('decrypted_data.bin')
        logger.error("Error processing WAV to file: %s", e)
        raise

def choose_option_and_convert():
    root = Tk()
    root.title("File Conversion")
    root.geometry("400x150")  # Set the size of the window
    root.configure(bg="#f0f0f0")

    option_var = StringVar(root)
    option_var.set("Choose an option")

    options = ["File to Audio", "Audio to File"]

    option_menu = OptionMenu(root, option_var, *options)
    option_menu.config(bg="#ffffff",width=20)
    option_menu.pack(pady=20)

    def on_convert():
        option = option_var.get()
        if option == "File to Audio":
            filename = filedialog.askopenfilename(title="Select a file to convert", filetypes=[("All files", "*.*")])
            if not filename:
                logger.info("No file selected.")
                return
            user_key = simpledialog.askstring("Password", "Enter password:")
            file_to_wav(filename, user_key)
        elif option == "Audio to File":
            filename = filedialog.askopenfilename(title="Select a WAV file to convert", filetypes=[("WAV files", "*.wav")])
            if not filename:
                logger.info("No file selected.")
                return
            user_key = simpledialog.askstring("Password", "Enter decryption password:")
            wav_to_file(filename, user_key)

    convert_button = Button(root, text="Convert", command=on_convert)
    convert_button.config(bg="#4CAF50", fg="white", width=15, height=1)
    convert_button.pack(pady=10)

    root.mainloop()

def main():
    choose_option_and_convert()

if __name__ == "__main__":
    main()
