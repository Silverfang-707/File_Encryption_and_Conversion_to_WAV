def binary_to_bits(file_path, bits_file_path):
    # Read the binary data from the file
    with open(file_path, 'rb') as file:
        binary_data = file.read()

    # Convert the binary data to bits
    bit_string = ''.join(format(byte, '08b') for byte in binary_data)

    # Save the bit string to a file
    with open(bits_file_path, 'w') as file:
        file.write(bit_string)

# Usage
binary_to_bits('encrypted_data.bin', 'bit_string.txt')
