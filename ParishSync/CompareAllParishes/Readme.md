# CSV Data Processing Script

This Python script is designed to efficiently process multiple CSV files, filter and separate data based on specific criteria, and save the results in Excel format. It is particularly useful for handling large datasets and performing complex data manipulation tasks.

## Features

- **Read Multiple CSV Files**: The script can read all CSV files in a specified directory, excluding any files containing the word 'Realm' in their name.
- **Data Separation**: It separates rows in each CSV file based on the presence of asterisks in the 'ConsID' column.
- **Data Filtering**: The script includes functionality to filter records based on 'Deceased', 'SRDeceased', 'IsInactive', 'Inactive', and 'SRInactive' columns.
- **Excel Output**: Processed data is saved in Excel format with specific formatting and text alignment for better readability.

## Functions

1. `read_csv_files(folder_path)`: Reads all CSV files in the given folder path and returns a list of dataframes.
2. `separate_rows_with_asterisk(dataframes, file_paths)`: Separates rows based on asterisks in the 'ConsID' column.
3. `save_dataframes_to_excel(dataframes, file_path)`: Saves combined DataFrames to an Excel file with formatting.
4. `find_mismatched_consids(dataframes, output_file)`: Identifies and saves mismatches in 'ConsID' and 'ConsCode'.
5. `find_deceased(dataframes)`: Filters and returns DataFrame for records marked as deceased.
6. `find_inactive(dataframes)`: Filters and returns DataFrame for records marked as inactive.
7. `analyze_spouse_consistency(dataframe)`: Analyzes and returns inconsistencies in spouse information.
8. `process_csv_files()`: Main function to execute the script functionalities.

## Usage

1. Place the script in the same directory as your CSV files.
2. Ensure all dependencies are installed (`pandas`, `tqdm`, `xlsxwriter`).
3. Run the script. Processed data will be saved in the same directory as the script.

## Dependencies

- Python 3
- Pandas
- tqdm
- xlsxwriter
