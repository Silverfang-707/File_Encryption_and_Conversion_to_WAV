def binary_converter(file_path):
    # Read the file in binary mode
    with open(file_path, 'rb') as file:
        binary_data = file.read()

    # Write the binary data to a file
    with open('binary_data.bin', 'wb') as file:
        file.write(binary_data)

    print("Binary data has been written to 'binary_data.bin'")

def reconstruct_file(binary_file_path, output_file_path):
    # Read the binary data from the file
    with open(binary_file_path, 'rb') as file:
        binary_data = file.read()

    # Write the binary data back to its original form
    with open(output_file_path, 'wb') as file:
        file.write(binary_data)

    print(f"File has been reconstructed from binary data and saved as '{output_file_path}'")

# Usage
binary_converter('1.png')
reconstruct_file('decrypted_data.bin', 'out.png')
