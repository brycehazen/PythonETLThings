import os
import chardet
import glob

# Use glob to match all CSV files in the current directory
for file_path in glob.glob('*.csv'):
    # Open the file in binary mode and read a sample of the file
    with open(file_path, 'rb') as f:
        raw_data = f.read(100000)  # Read a sample of the file, adjust size as needed

    # Detect the character encoding
    result = chardet.detect(raw_data)

    # Print the filename and the detected encoding
    print(f"File: {file_path}, Encoding: {result['encoding']}")
