import os
import glob
import pandas as pd

# Define the pattern to search for the CSV files
filename_pattern_to_search = '*RE_DataWithExceptions.csv'

# Get the current directory where the .py script is
current_directory = os.getcwd()

# Construct the full path pattern
full_path_pattern = os.path.join(current_directory, filename_pattern_to_search)

# Find all files that match the pattern
matching_files = glob.glob(full_path_pattern)

# Check if there are any matching files
if matching_files:
    # Read and concatenate all the matching CSV files with specified encoding
    combined_csv = pd.concat([pd.read_csv(f, encoding='ISO-8859-1') for f in matching_files])

    # Optional: Save the combined dataframe to a new CSV file with specified encoding
    combined_csv.to_csv('combined_file.csv', index=False, encoding='ISO-8859-1')

    print("CSV files combined successfully. Saved as 'combined_file.csv'.")
else:
    print("No matching CSV files found.")
