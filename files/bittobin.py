def bits_to_binary(bits_file_path, output_file_path):
    # Read the bit string from the file
    with open(bits_file_path, 'r') as file:
        bit_string = file.read()

    # Convert the bit string back to binary data
    binary_data = bytes(int(bit_string[i : i + 8], 2) for i in range(0, len(bit_string), 8))

    # Write the binary data to a file
    with open(output_file_path, 'wb') as file:
        file.write(binary_data)

# Usage
bits_to_binary('bit_string.txt', 'reconstructed_data.bin')
