import pandas as pd
import glob
import os

# Get the directory where the script is located
script_dir = os.path.dirname(__file__)

# Find all CSV files in the directory
csv_files = glob.glob(os.path.join(script_dir, '*.csv'))

for file in csv_files:
    # Read the CSV file
    df = pd.read_csv(file, encoding='ISO-8859-1', low_memory=False)

    # Drop duplicates
    df_new = df.drop_duplicates(subset=['Constituent ID'])

    # Define the output file name
    output_file_name = os.path.splitext(os.path.basename(file))[0] + '_PROCESSED.csv'
    output_file = os.path.join(script_dir, output_file_name)

    # Save to CSV
    df_new.to_csv(output_file, index=False, encoding='ISO-8859-1')
