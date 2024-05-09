def reconstruct_from_binary(binary_file_path, output_file_path):
    # Read the binary data from the file
    with open(binary_file_path, 'rb') as file:
        binary_data = file.read()

    # Write the binary data back to its original form
    with open(output_file_path, 'wb') as file:
        file.write(binary_data)

    print(f"File has been reconstructed from binary data and saved as '{output_file_path}'")

# Usage
extension = input("Enter the extension of the original file: ")
reconstruct_from_binary('decrypted_data.bin', 'reconstructed.'+extension)
