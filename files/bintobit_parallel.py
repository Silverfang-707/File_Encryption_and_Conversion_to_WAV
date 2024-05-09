import concurrent.futures

def binary_to_bits_chunk(chunk):
    # Convert the binary data to bits
    return ''.join(format(byte, '08b') for byte in chunk)

def binary_to_bits_parallel(file_path, bits_file_path):
    # Read the binary data from the file
    with open(file_path, 'rb') as file:
        binary_data = file.read()

    # Split the binary data into chunks
    chunk_size = 1024  # Adjust this value based on your system's capabilities
    chunks = [binary_data[i : i + chunk_size] for i in range(0, len(binary_data), chunk_size)]

    # Process each chunk in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        bit_strings = executor.map(binary_to_bits_chunk, chunks)

    # Combine the bit strings and save them to a file
    with open(bits_file_path, 'w') as file:
        file.write(''.join(bit_strings))

# Usage
binary_to_bits_parallel('encrypted_data.bin', 'bit_string.txt')
