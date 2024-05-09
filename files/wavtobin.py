import wave

def audio_to_bin(input_file_path, bin_file_path):
    # Open the WAV file
    with wave.open(input_file_path, 'rb') as wav_file:
        # Read the binary data from the WAV file
        binary_data = wav_file.readframes(wav_file.getnframes())

    # Write the binary data to a .bin file
    with open(bin_file_path, 'wb') as file:
        file.write(binary_data)

# Usage
audio_to_bin('output.wav', 'audio.bin')
