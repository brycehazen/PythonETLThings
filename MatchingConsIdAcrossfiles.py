import pandas as pd
import os

# Load the main CSV file
main_df = pd.read_csv('Blanks_created2023.csv', low_memory=False, encoding='ISO-8859-1')
matches = []

# Iterate over all CSV files in the same directory
for file in os.listdir('.'):
    if file.endswith('.csv') and file != 'Blanks_created2023.csv':
        # Read the current CSV file
        current_df = pd.read_csv(file, low_memory=False, encoding='ISO-8859-1')
        
        # Check if 'ConsID' column is in the current CSV
        if 'ConsID' in current_df.columns:
            # Find matches
            matched_rows = current_df[current_df['ConsID'].isin(main_df['CnBio_ID'])]
            
            # If there are matches, add the file name as a new column
            if not matched_rows.empty:
                matched_rows['Matched_File'] = file
                matches.append(matched_rows)

# Concatenate all matches into a single DataFrame and save to a new CSV
if matches:
    result = pd.concat(matches)
    result.to_csv('matched_results.csv', index=False, encoding='ISO-8859-1')
else:
    print("No matches found.")
