
# `RETestCases v8.py` README

## Overview

The `RETestCases v8.py` script is a data processing tool designed to cleanse and refine specific CSV files. It mainly adjusts titles and associated gender values, among other modifications.

## Features

- **CSV File Management**: 
  - The script specifies several CSV filenames for different purposes, such as `Failed.csv`, `duplicated.csv`, `RE_Data.csv`, `Passed.csv`, `ImportOmatic.csv`, and `RawParishData.csv`.
  
- **Directory Utility**: 
  - A utility function `get_root()` is defined to get the parent directory of the script.

- **Data Processing**:
  - The `process()` function takes in a CSV file and two directory paths and performs the following tasks:
    * Reads the data from the CSV.
    * Conditionally modifies titles and associated gender values.
    * (Note: Further functionalities might be present but are not captured in the initial segment provided.)

- **Title Corrections**:
  - Adjusts titles like 'Mr', 'Mrs', 'Dr', etc., to their respective standardized forms.
  - Makes corresponding changes to gender based on titles.

## Usage

1. **Dependencies**: 
   - Ensure you have the following Python libraries installed:
     * `pathlib`
     * `pandas`
     * `numpy`

2. **Running the Script**: 
   - To process a specific CSV file, call the `process()` function with the appropriate arguments. Ensure the CSV files specified in the script are present or modify them as per your requirements.

3. **Configuration**: 
   - If you need to adjust the title corrections or add new modifications, you can modify the respective lines within the `process()` function.

## Notes

- This README is based on the initial segment of the script. Further functionalities might be present in the full script.
- Always make backups of your original data before processing to prevent any unintended data loss or changes.

## License

This script is provided as-is without any warranties. Users are advised to review and test the script thoroughly before applying it to crucial datasets.
