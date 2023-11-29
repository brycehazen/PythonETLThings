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
