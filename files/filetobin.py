def convert_to_binary(file_path, binary_file_path):
    # Read the file in binary mode
    with open(file_path, 'rb') as file:
        binary_data = file.read()

    # Write the binary data to a file
    with open(binary_file_path, 'wb') as file:
        file.write(binary_data)

    print(f"Binary data has been written to '{binary_file_path}'")

# Usage
convert_to_binary('1.png', 'binary_data.bin')
