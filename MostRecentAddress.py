import pandas as pd
import os

# Define the CSV filename (assuming it has the same name as the script but with a .csv extension)
file_name = os.path.splitext(os.path.basename(__file__))[0] + '.csv'

# Load the data
df = pd.read_csv(file_name, encoding='latin-1', low_memory=False)

# Filter out rows where CnAdrAll_1_01_Addrline1 is blank or NaN
filtered_df = df[df['CnAdrAll_1_01_Addrline1'].notna() & (df['CnAdrAll_1_01_Addrline1'] != "")]

# Create dataframe for individual's address and add a Source column
individual_df = filtered_df[['CnBio_ID', 'CnBio_No_Valid_Addresses', ...]]
individual_df['Source'] = 'Individual'

# Create dataframe for spouse's address, rename columns to match individual_df, and add a Source column
spouse_df = filtered_df[['CnBio_ID', 'CnBio_No_Valid_Addresses', ...]]
spouse_df.columns = individual_df.columns
spouse_df['Source'] = 'Spouse'

# Concatenate the two dataframes
combined_df = pd.concat([individual_df, spouse_df])

# Convert the CnAdrAll_1_01_DateLastChanged column to datetime format for proper sorting
combined_df['CnAdrAll_1_01_DateLastChanged'] = pd.to_datetime(combined_df['CnAdrAll_1_01_DateLastChanged'])

# Sort the dataframe by CnBio_ID and CnAdrAll_1_01_DateLastChanged in descending order
sorted_combined_df = combined_df.sort_values(by=['CnBio_ID', 'CnAdrAll_1_01_DateLastChanged'], ascending=[True, False])

# Group by CnBio_ID and pick the first row for each group (i.e., the most recent address change)
final_output_df = sorted_combined_df.groupby('CnBio_ID').first().reset_index()

# Save the final output dataframe to a CSV file (with a '_output' suffix)
output_file_path = os.path.splitext(file_name)[0] + '_output.csv'
final_output_df.to_csv(output_file_path, index=False)
