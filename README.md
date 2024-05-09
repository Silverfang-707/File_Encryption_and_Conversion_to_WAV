# File Encryption and Audio Conversion

This script allows you to encrypt any file using AES encryption and then convert it into an audio file (WAV format). It also provides functionality to reverse this process, decrypting the audio file back into its original form.

## Features

- **File Encryption:** Encrypt any file using AES encryption with CBC mode and a user-provided key.
- **Audio Conversion:** Convert encrypted binary files into audio files in WAV format.
- **File Decryption:** Decrypt audio files back into their original binary form.
- **User Interaction:** Simple CLI interface for selecting encryption or decryption and providing necessary inputs.

## Usage

1. **Installation:**

   - Ensure you have Python installed on your system.
   - Install the required packages using `pip install -r requirements.txt`.

2. **Usage:**

   - Run the script using Python: `main.py`.
   - Choose either "File to Audio" or "Audio to File" option.
   - Provide the necessary inputs like the filename, password, and file extension when prompted.

3. **Notes:**

   - Make sure to keep your password secure. Losing it will result in irreversible data loss.
   - The script will overwrite existing files without warning. Exercise caution to avoid accidental data loss.

## Requirements

See `requirements.txt` for the required Python packages and their versions.

