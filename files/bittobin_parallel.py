import concurrent.futures

def bits_to_binary_chunk(bit_string):
    # Convert the bit string back to binary data
    return bytes(int(bit_string[i : i + 8], 2) for i in range(0, len(bit_string), 8))

def bits_to_binary_parallel(bits_file_path, output_file_path):
    # Read the bit string from the file
    with open(bits_file_path, 'r') as file:
        bit_string = file.read()

    # Split the bit string into chunks
    chunk_size = 1024  # Adjust this value based on your system's capabilities
    chunks = [bit_string[i : i + chunk_size] for i in range(0, len(bit_string), chunk_size)]

    # Process each chunk in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        binary_chunks = executor.map(bits_to_binary_chunk, chunks)

    # Combine the binary chunks and write them to a file
    with open(output_file_path, 'wb') as file:
        for binary_data in binary_chunks:
            file.write(binary_data)

# Usage
bits_to_binary_parallel('reconstructed_bit_string.txt', 'reconstructed_data.bin')
