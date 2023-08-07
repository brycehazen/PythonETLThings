# Most Recent Address Extractor - ImportID_MostRecentAddress.py

This script processes a CSV file to extract the most recent address for each individual, considering both their own and their spouse's address records. 
The script expects a CSV file in the same directory with the same name as the script.

## Features

- **Handles both individual and spouse address details**: Extracts information from separate columns dedicated to individual and spouse addresses.
- **Date-based extraction**: Extracts the most recent address based on the date of the last change.
- **Outputs a new CSV file**: The processed data is saved with an `_output` suffix.

## How to Use

1. Place the desired CSV file in the same directory as the script.
2. Ensure the CSV file has the same name as the `.py` script (without the `.py` extension).
3. Run the script using Python.
4. The processed data will be saved in the same directory with an `_output` suffix (e.g., `process_data_output.csv`).

## Columns Expected in Input CSV

### Individual's Address Details:

- `CnBio_ID`
- `CnBio_No_Valid_Addresses`
- `CnAdrAll_1_01_Addrline1`
- ... (and other relevant columns)

### Spouse's Address Details:

- `CnSpAdrPrf_Addrline1`
- `CnSpAdrPrf_City`
- ... (and other relevant columns)

## Dependencies

- **pandas**: Used for data processing.
- **os**: Used for file and directory operations.

## Known Issues

- Ensure that the input CSV file is encoded in 'latin-1'.

## Steps
- Query on blank prefered addresses
- In Export select query
- Use All adresses and export several addresses
- Include spouse's perfered address.
- Put csv from Export in directory with this .py
- take output file from .py and reimport back in. 
