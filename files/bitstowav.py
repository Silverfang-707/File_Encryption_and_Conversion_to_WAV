import wave

def bits_to_audio(bits_file_path, output_file_path):
    # Read the bit string from the file
    with open(bits_file_path, 'r') as file:
        bit_string = file.read()

    # Convert the bit string back to binary data
    binary_data = bytes(int(bit_string[i : i + 8], 2) for i in range(0, len(bit_string), 8))

    # Write the binary data to a WAV file
    with wave.open(output_file_path, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(44100)
        wav_file.writeframes(binary_data)

# Usage
bits_to_audio('bit_string.txt', 'output.wav')
