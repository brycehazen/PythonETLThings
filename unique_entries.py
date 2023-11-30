import pandas as pd
import re
import glob
import os

# Get the directory of the current script
script_directory = os.path.dirname(os.path.realpath(__file__))

# Function to compress non-empty cells in a column
def compress_column(series):
    # Filter out empty cells and reset the index without adding a new column
    return series.dropna().reset_index(drop=True)

# Pattern for matching the columns
pattern = re.compile(r'CnCnstncy_1_\d\d_CodeLong')

# Iterate over all Excel files in the script's directory
for file_path in glob.glob(f"{script_directory}/*.xlsx"):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Identify columns that match the pattern
    matching_columns = [col for col in df.columns if pattern.match(col)]

    # Replace NaN values with an empty string in first and last name columns
    df['CnBio_First_Name'] = df['CnBio_First_Name'].fillna('').astype(str)
    df['CnBio_Last_Name'] = df['CnBio_Last_Name'].fillna('').astype(str)

    # Concatenate first and last names
    df['Full_Name'] = df['CnBio_First_Name'] + " " + df['CnBio_Last_Name']

    # Remove leading and trailing spaces
    df['Full_Name'] = df['Full_Name'].str.strip()

    # Combine data from matching columns into a single column using concat
    combined_data = pd.concat([df[col].dropna() for col in matching_columns])
    unique_counts = combined_data.value_counts()
    unique_counts_df = unique_counts.reset_index()
    unique_counts_df.columns = ['Unique Entry', 'Count']

    # Export the count of unique entries to a CSV file
    output_count_file = file_path.replace('.xlsx', '_count_output.csv')
    unique_counts_df.to_csv(output_count_file, index=False, encoding='utf-8')

    # Creating a DataFrame for unique entries as columns
    unique_entries = df[matching_columns].stack().unique()
    unique_entries_df = pd.DataFrame(index=range(len(df)), columns=unique_entries)

    # Fill the unique_entries_df with full names where the unique entry matches
    for entry in unique_entries:
        matched_full_names = df['Full_Name'][df[matching_columns].isin([entry]).any(axis=1)]
        compressed_full_names = compress_column(matched_full_names)
        unique_entries_df[entry][:len(compressed_full_names)] = compressed_full_names

    # Remove rows that are entirely empty across all unique entry columns
    unique_entries_df.dropna(how='all', inplace=True)

    # Export the new DataFrame to a CSV file with UTF-8 encoding
    output_columns_file = file_path.replace('.xlsx', '_compressed_output.csv')
    unique_entries_df.to_csv(output_columns_file, index=False, encoding='utf-8')

print("Processing complete.")
