import pandas as pd
from datetime import datetime
import os

# Define the function to get the best address details for a single record
def get_best_address_details(record):
    # Initialize variables to store best address details
    best_address_details = {
        'Best_Address': None,
        'Best_City': None,
        'Best_State': None,
        'Best_ZIP': None
    }
    
    # Check if there is a spouse's address
    if pd.notna(record['CnSpAdrPrf_Addrline1']):
        best_address_details['Best_Address'] = record['CnSpAdrPrf_Addrline1']
        best_address_details['Best_City'] = record['CnSpAdrPrf_City']
        best_address_details['Best_State'] = record['CnSpAdrPrf_State']
        best_address_details['Best_ZIP'] = record['CnSpAdrPrf_ZIP']
        return best_address_details
    
    # Find the most recently changed non-blank address
    most_recent_date = datetime.min
    for i in range(1, 8):
        address = record[f'CnAdrAll_1_0{i}_Addrline1']
        city = record[f'CnAdrAll_1_0{i}_City']
        state = record[f'CnAdrAll_1_0{i}_State']
        zip_code = record[f'CnAdrAll_1_0{i}_ZIP']
        date_last_changed = record[f'CnAdrAll_1_0{i}_DateLastChanged']
        
        if pd.notna(address) and pd.notna(date_last_changed):
            date_last_changed = datetime.strptime(date_last_changed, '%m/%d/%Y')
            if date_last_changed > most_recent_date:
                most_recent_date = date_last_changed
                best_address_details['Best_Address'] = address
                best_address_details['Best_City'] = city
                best_address_details['Best_State'] = state
                best_address_details['Best_ZIP'] = zip_code
                
    return best_address_details

# Get list of all CSV files in the current directory
csv_files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.csv')]

# Process each CSV file
for csv_file in csv_files:
    # Load the full dataset
    full_data = pd.read_csv(csv_file)

    # Create a dataframe 'blank_addresses' with only the rows where the address is blank and 'Preferred' is 'Yes'
    blank_addresses = full_data[full_data['CnAdrAll_1_01_Addrline1'].isna() & (full_data['CnAdrAll_1_01_Preferred'] == 'Yes')].copy()

    # For each row in 'blank_addresses', find the best address to fill in the blank from the corresponding record in 'full_data'
    for index, row in blank_addresses.iterrows():
        best_address_details = get_best_address_details(full_data.loc[index])
        blank_addresses.loc[index, 'CnAdrAll_1_01_Addrline1'] = best_address_details['Best_Address']
        blank_addresses.loc[index, 'CnAdrAll_1_01_City'] = best_address_details['Best_City']
        blank_addresses.loc[index, 'CnAdrAll_1_01_State'] = best_address_details['Best_State']
        blank_addresses.loc[index, 'CnAdrAll_1_01_ZIP'] = best_address_details['Best_ZIP']

    # Create a new CSV file with only 'CnBio_ID', 'ImportID', and the filled-in address details
    filled_addresses_final = blank_addresses[['CnBio_ID', 'CnAdrAll_1_01_Import_ID', 'CnAdrAll_1_01_Addrline1', 'CnAdrAll_1_01_City', 'CnAdrAll_1_01_State', 'CnAdrAll_1_01_ZIP']]
    filled_addresses_final.columns = ['CnBio_ID', 'ImportID', 'Filled_Address', 'Filled_City', 'Filled_State', 'Filled_ZIP']
    filled_addresses_final = filled_addresses_final.dropna(subset=['Filled_Address'])

    # Save to CSV
    output_file = os.path.splitext(csv_file)[0] + '_output.csv'
    filled_addresses_final.to_csv(output_file, index=False)

    print(f'Processed {csv_file} and saved output to {output_file}')
