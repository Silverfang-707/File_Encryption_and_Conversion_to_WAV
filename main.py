import wave
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
import os

#converting the input file to binary
def convert_to_binary(file_path, binary_file_path):
    # Read the file in binary mode
    with open(file_path, 'rb') as file:
        binary_data = file.read()

    # Write the binary data to a file
    with open(binary_file_path, 'wb') as file:
        file.write(binary_data)

#reconstructing the binary file to its original form
def reconstruct_from_binary(binary_file_path, output_file_path):
    # Read the binary data from the file
    with open(binary_file_path, 'rb') as file:
        binary_data = file.read()

    # Write the binary data back to its original form
    with open(output_file_path, 'wb') as file:
        file.write(binary_data)

#hashing user key to make sure it's the required size
def get_key(user_key):
    # Use SHA-256 hash to ensure the key is 32 bytes long
    return SHA256.new(user_key.encode()).digest()

#encrypting the binary file
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

#decrypting the binary file
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

#converting the binary file into wav format
def bin_to_audio(bin_file_path, output_file_path, nchannels=1, sampwidth=2, framerate=44100):
    # Open the binary file
    with open(bin_file_path, 'rb') as file:
        binary_data = file.read()

    # Write the binary data to a WAV file
    with wave.open(output_file_path, 'wb') as wav_file:
        wav_file.setnchannels(nchannels)
        wav_file.setsampwidth(sampwidth)
        wav_file.setframerate(framerate)
        wav_file.writeframes(binary_data)

#converting the audio file back to binary
def audio_to_bin(input_file_path, bin_file_path):
    # Open the WAV file
    with wave.open(input_file_path, 'rb') as wav_file:
        # Read the binary data from the WAV file
        binary_data = wav_file.readframes(wav_file.getnframes())

    # Write the binary data to a .bin file
    with open(bin_file_path, 'wb') as file:
        file.write(binary_data)

def file_to_wav(filename, user_key):
    convert_to_binary(filename, 'binary_data.bin')
    encrypt_file('binary_data.bin', user_key)
    bin_to_audio('encrypted_data.bin', 'output.wav')
    print('File encrypted and saved as output.wav')

def wav_to_file(filename, user_key):
    exten = input("Enter the extension of the original file: ")
    if(exten[0] == '.'):
        exten = exten[1:]
    if(os.path.exists('reconstructed.' + exten)):
        print("Warning! reconstructed. " +exten+" already exists and will be overwritten.")
        remchoice = input("Do you want to continue? (y/n): ")
        if(remchoice == 'n'):
            raise ValueError("Operation Cancelled by User.")
        elif(remchoice != 'y'):
            raise ValueError("Invalid input Cancelling Operation.")
    audio_to_bin(filename, 'decrypted_data.bin')
    decrypt_file('decrypted_data.bin', user_key, 'binary_data.bin')
    reconstruct_from_binary('binary_data.bin', 'reconstructed'+ '.' + exten)
    print('File decrypted and saved as reconstructed.' + exten)

choice=int(input("(1)File to Audio or (2)Audio to File: "))
if choice != 1 and choice != 2:
    raise ValueError("Invalid choice, Choices should be either 1 or 2")

user_key = input("Enter password(in case of (wav to file) input the decryption password): ")

if choice==1:
    filename=input("Enter the name of the file with extension: ")
    if(not os.path.exists(filename)):
        raise FileNotFoundError("Input file does not exist")
    elif(os.stat(filename).st_size==0):
        print("File is empty")
    elif(os.path.exists("output.wav")):
        print("Warning! output.wav already exists and will be overwritten.")
        remchoice = input("Do you want to continue? (y/n): ")
        if(remchoice == 'n'):
            raise ValueError("Operation Cancelled by User.")
        elif remchoice != 'y':
            raise ValueError("Invalid choice Cancelling Operation")
    file_to_wav(filename, user_key)
    os.remove('binary_data.bin')
    os.remove('encrypted_data.bin')

else:
        try:
            filename=input("Enter the name of the audio file: ")
            if(filename == ''):
                filename = 'output.wav'
            if(filename[-4:]!='.wav'):
                filename = filename + '.wav'
            if(not os.path.exists(filename)):
                raise FileNotFoundError("File does not exist")
            elif(os.stat(filename).st_size==0):
                print("File is empty")
            wav_to_file(filename, user_key)
            os.remove('binary_data.bin')
            os.remove('decrypted_data.bin')
        except(ValueError):
            os.remove('decrypted_data.bin')
            print("Invalid Password")