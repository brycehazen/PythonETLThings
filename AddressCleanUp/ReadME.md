# Address Data Processing Script

This script processes CSV files containing address data. It handles various tasks such as merging data from different address types, selecting the best address for each ID based on specific criteria, and identifying rows with blank address fields.

## Features

- **Process Address Types**: Combines data from different address types (`All`, `Sp`, `Prf`) into a single file.
- **Select Best Address**: For each ID, it selects the best address based on recency and type preference.
- **Merge with 'Prf' Type**: Merges the best address data with the 'Prf' type dataset.
- **Identify Blanks**: Outputs rows with all blank address fields to a separate file.

## Usage

1. Place your CSV files in the script's directory.
2. Run the script. It will process all `.csv` files in the directory.
3. The script outputs several files:
   - `Prf_[original_file_name].csv`: Contains processed 'Prf' type data.
   - `Combined_[original_file_name].csv`: Combined data of all types.
   - `BestAddresses_Combined_[original_file_name].csv`: Contains the best address for each ID.
   - `Merged_[original_file_name].csv`: Merged data of 'Prf' type and best addresses.
   - `Blanks_[original_file_name].csv`: Rows with all blank address fields.

## Column Headers

The script processes the following columns in the CSV files:

- `CnBio_ID`
- `Sp_Import_ID`
- `Sp_Addrline1`
- `Sp_City`
- `Sp_State`
- `Sp_ZIP`
- `Sp_Type`
- `Sp_Sndmailtthisaddrss`
- `Sp_DateLastChanged`
- `Sp_DateAdded`
- `Prf_Import_ID`
- `Prf_Addrline1`
- `Prf_City`
- `Prf_State`
- `Prf_ZIP`
- `Prf_Type`
- `Prf_Sndmailtthisaddrss`
- `Prf_DateLastChanged`
- `Prf_DateAdded`
- `All_01_Import_ID`
- `All_01_Addrline1`
- `All_01_City`
- `All_01_State`
- `All_01_ZIP`
- `All_01_Type`
- `All_01_Sndmailtthisaddrss`
- `All_01_DateLastChanged`
- `All_01_DateAdded`
- `All_02_Import_ID`
- `All_02_Addrline1`
- `All_02_City`
- `All_02_State`
- `All_02_ZIP`
- `All_02_Type`
- `All_02_Sndmailtthisaddrss`
- `All_02_DateLastChanged`
- `All_02_DateAdded`
- `All_03_Import_ID`
- `All_03_Addrline1`
- `All_03_City`
- `All_03_State`
- `All_03_ZIP`
- `All_03_Type`
- `All_03_Sndmailtthisaddrss`
- `All_03_DateLastChanged`
- `All_03_DateAdded`
- `All_04_Import_ID`
- `All_04_Addrline1`
- `All_04_City`
- `All_04_State`
- `All_04_ZIP`
- `All_04_Type`
- `All_04_Sndmailtthisaddrss`
- `All_04_DateLastChanged`
- `All_04_DateAdded`
- `All_05_Import_ID`
- `All_05_Addrline1`
- `All_05_City`
- `All_05_State`
- `All_05_ZIP`
- `All_05_Type`
- `All_05_Sndmailtthisaddrss`
- `All_05_DateLastChanged`
- `All_05_DateAdded`
- `All_06_Import_ID`
- `All_06_Addrline1`
- `All_06_City`
- `All_06_State`
- `All_06_ZIP`
- `All_06_Type`
- `All_06_Sndmailtthisaddrss`
- `All_06_DateLastChanged`
- `All_06_DateAdded`
- `All_07_Import_ID`
- `All_07_Addrline1`
- `All_07_City`
- `All_07_State`
- `All_07_ZIP`
- `All_07_Type`
- `All_07_Sndmailtthisaddrss`
- `All_07_DateLastChanged`
- `All_07_DateAdded`
- `All_08_Import_ID`
- `All_08_Addrline1`
- `All_08_City`
- `All_08_State`
- `All_08_ZIP`
- `All_08_Type`
- `All_08_Sndmailtthisaddrss`
- `All_08_DateLastChanged`
- `All_08_DateAdded`


## Script Overview

\```python
import os
import pandas as pd

# Function definitions: process_type, process_all_types, select_best_address...

# Process each .csv file in the directory
for file in csv_files:
    # Processing steps...
    # Read and combine data, process 'Prf' data, merge with best addresses, etc.

    # After processing all files, select the best address for each CnBio_ID
    # ...

    # Output rows with all blank specified headers to a new file
    # ...
\```

## Requirements

- Python 3
- Pandas library

## Notes

- Ensure that your CSV files are correctly formatted and placed in the same directory as the script.
- The script assumes specific column names (`CnBio_ID`, `Addrline1`, `City`, `State`, etc.). Make sure these match your data.
"""
