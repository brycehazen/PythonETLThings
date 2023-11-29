import os
import pandas as pd

def process_type(data, prefix):
    # Identify columns for the specific prefix
    prefix_columns = [col for col in data.columns if col.startswith(prefix) or col == 'CnBio_ID']
    
    # Extract and process data for this prefix
    type_data = data[prefix_columns].copy()
    type_data.columns = [col.replace(prefix + '_', '') if col != 'CnBio_ID' else col for col in type_data.columns]
    type_data['Type'] = prefix
    
    return type_data

def process_all_types(data, prefix_base):
    # Initialize an empty DataFrame for all 'All' types
    all_data = pd.DataFrame()

    # Identify all unique prefixes that start with 'All'
    all_prefixes = {col.split('_')[0] + '_' + col.split('_')[1] for col in data.columns if col.startswith(prefix_base)}

    # Loop through each unique prefix
    for prefix in all_prefixes:
        # Process and append each 'All' type
        subset_data = process_type(data, prefix)
        all_data = pd.concat([all_data, subset_data], ignore_index=True)

    return all_data

def select_best_address(group):
    # Filter out rows where Addrline1 is blank
    group = group[group['Addrline1'].notna()]

    # Sort by DateLastChanged in descending order to get the most recent date first
    group = group.sort_values(by='DateLastChanged', ascending=False)

    # Try to select an address where Type is 'Sp', otherwise select the topmost row
    best_address = group[group['Type'] == 'Sp'].head(1)
    if best_address.empty:
        best_address = group.head(1)

    return best_address

# Get the directory of the current script
script_directory = os.path.dirname(os.path.realpath(__file__))

# List all .csv files in the directory
csv_files = [f for f in os.listdir(script_directory) if f.endswith('.csv')]

# Process each .csv file
for file in csv_files:
    file_path = os.path.join(script_directory, file)
    
    # Read the .csv file
    data = pd.read_csv(file_path, low_memory=False, encoding='ISO-8859-1')

    # Process 'All' types
    all_types_data = process_all_types(data, 'All')

    # Process 'Sp' type
    sp_data = process_type(data, 'Sp')

    # Process 'Prf' type and save to its own file
    prf_data = process_type(data, 'Prf')
    prf_file_path = os.path.join(script_directory, 'Prf_' + file)
    prf_data.to_csv(prf_file_path, index=False)
    print(f"Processed and saved Prf file: {prf_file_path}")

    # Combine 'All' and 'Sp' types into one DataFrame
    combined_data = pd.concat([all_types_data, sp_data], ignore_index=True)

    # Drop rows where Import_ID is blank and then drop the entire 'Import_ID' column
    combined_data = combined_data.dropna(subset=['Import_ID']).drop(columns=['Import_ID'])

    # Save the combined data to a new file
    combined_file_path = os.path.join(script_directory, 'Combined_' + file)
    combined_data.to_csv(combined_file_path, index=False)
    print(f"Processed and saved combined file: {combined_file_path}")

# After processing all files, select the best address for each CnBio_ID in the combined data
combined_csv_files = [f for f in os.listdir(script_directory) if f.startswith('Combined_') and f.endswith('.csv')]

for file in combined_csv_files:
    combined_file_path = os.path.join(script_directory, file)
    
    # Read the combined .csv file
    combined_data = pd.read_csv(combined_file_path, low_memory=False, encoding='ISO-8859-1')
    combined_data['DateLastChanged'] = pd.to_datetime(combined_data['DateLastChanged'], errors='coerce')

    # Select the best address for each CnBio_ID
    best_addresses = combined_data.groupby('CnBio_ID').apply(select_best_address).reset_index(drop=True)

    # Save the best addresses to a new file
    best_addresses_file_path = os.path.join(script_directory, 'BestAddresses_' + file)
    best_addresses.to_csv(best_addresses_file_path, index=False)
    print(f"Processed and saved best addresses file: {best_addresses_file_path}")

# After selecting the best addresses, join them with the 'Prf' dataset
for file in csv_files:
    prf_file_path = os.path.join(script_directory, 'Prf_' + file)
    best_addresses_file_path = os.path.join(script_directory, 'BestAddresses_Combined_' + file)

    # Check if both files exist before proceeding
    if os.path.exists(prf_file_path) and os.path.exists(best_addresses_file_path):
        # Read the 'Prf' and best addresses data
        prf_data = pd.read_csv(prf_file_path, low_memory=False, encoding='ISO-8859-1')
        best_addresses_data = pd.read_csv(best_addresses_file_path, low_memory=False, encoding='ISO-8859-1')

        # Perform a left join to fill in blanks in 'Prf' data
        merged_data = pd.merge(prf_data, best_addresses_data, on='CnBio_ID', how='left', suffixes=('', '_best'))

        # Fill in the blanks in 'Prf' data with best addresses data
        for column in best_addresses_data.columns:
            if column != 'CnBio_ID':
                merged_data[column] = merged_data[column].fillna(merged_data[column + '_best'])

        # Drop the additional columns from best addresses
        merged_data.drop([col for col in merged_data if col.endswith('_best')], axis=1, inplace=True)

        # Save the merged data to a new file
        merged_file_path = os.path.join(script_directory, 'Merged_' + file)
        merged_data.to_csv(merged_file_path, index=False)
        print(f"Processed and saved merged file: {merged_file_path}")
    else:
        print(f"One or both files do not exist for: {file}")

# if there are still blanks, these blanks are saved to a new csv
for file in csv_files:
    merged_file_path = os.path.join(script_directory, 'Merged_' + file)
    
    if os.path.exists(merged_file_path):
        # Read the merged data
        merged_data = pd.read_csv(merged_file_path, low_memory=False, encoding='ISO-8859-1')

        # Filter rows where all specified headers are blank
        blank_rows = merged_data[merged_data[['Addrline1', 'City', 'State']].isna().all(axis=1)]

        if not blank_rows.empty:
            # Save these rows to a new file
            blanks_file_path = os.path.join(script_directory, 'Blanks_' + file)
            blank_rows.to_csv(blanks_file_path, index=False)
            print(f"Processed and saved blanks file: {blanks_file_path}")
        else:
            print(f"No blank rows found for: {file}")
    else:
        print(f"Merged file does not exist for: {file}")
