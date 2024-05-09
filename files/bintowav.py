import wave

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

# Usage
bin_to_audio('encrypted_data.bin', 'output.wav')
