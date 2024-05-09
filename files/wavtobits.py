import wave

def audio_to_bits(input_file_path, bits_file_path):
    # Open the WAV file
    with wave.open(input_file_path, 'rb') as wav_file:
        # Open the output file
        with open(bits_file_path, 'w') as file:
            # Process each frame
            for i in range(wav_file.getnframes()):
                # Read the frame
                frame = wav_file.readframes(1)
                # Convert the frame to bits and write to the file
                file.write(''.join(format(byte, '08b') for byte in frame))

# Usage
audio_to_bits('output.wav', 'reconstructed_bit_string.txt')
