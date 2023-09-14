
import pandas as pd

# Load the data from the CSV file once
data = pd.read_csv("9.7.23-BlankAddressEXPORT.csv", low_memory=False)

# ----- findblank.py -----
# Identify all columns containing the substring `_Addrline1`
addrline1_columns = [col for col in data.columns if '_Addrline1' in col]

# List to store the results of filtering for each address column
filtered_dataframes = []

for addrline1_col in addrline1_columns:
    # Dynamically identify related columns based on the base name (e.g., CnAdrAll_1_XX_)
    col_base = addrline1_col.rsplit('_', 1)[0] + '_'
    
    city_col = col_base + 'City'
    state_col = col_base + 'State'
    zip_col = col_base + 'ZIP'
    type_col = col_base + 'Type'
    preferred_col = col_base + 'Preferred'
    date_added_col = col_base + 'DateAdded'
    date_last_changed_col = col_base + 'DateLastChanged'
    type2_col = col_base + 'Type2'
    indicator_col = col_base + 'Indicator'
    import_id_col = col_base + 'Import_ID'
    
    # Filter data based on criteria for the current address column
    current_filtered_data = data[
        (data[preferred_col] == 'Yes') & 
        (data[addrline1_col].isnull())
    ]
    
    # Extract the required columns
    current_columns_to_extract = [
        'CnBio_ID', 
        'CnBio_No_Valid_Addresses', 
        addrline1_col, 
        city_col, 
        state_col, 
        zip_col, 
        type_col, 
        preferred_col, 
        date_added_col, 
        date_last_changed_col, 
        type2_col, 
        indicator_col, 
        import_id_col
    ]
    
    current_filtered_extracted_data = current_filtered_data[current_columns_to_extract]
    
    # Rename columns for simplification
    current_column_rename_map = {
        addrline1_col: 'Addrline1',
        city_col: 'City',
        state_col: 'State',
        zip_col: 'ZIP',
        type_col: 'Type',
        preferred_col: 'Preferred',
        date_added_col: 'DateAdded',
        date_last_changed_col: 'DateLastChanged',
        type2_col: 'Type2',
        indicator_col: 'Indicator',
        import_id_col: 'Import_ID'
    }

    current_filtered_extracted_data = current_filtered_extracted_data.rename(columns=current_column_rename_map)
    
    # Append the current filtered data to the list of filtered dataframes
    filtered_dataframes.append(current_filtered_extracted_data)

# Concatenate all the filtered dataframes
final_filtered_data = pd.concat(filtered_dataframes, ignore_index=True)
# Save the filtered data to a new CSV file
final_filtered_data.to_csv('final_filtered_data.csv', index=False)

# ----- Transpose.py -----
# List to store transformed data for each address group
transformed_dataframes = []

for i in range(1, 21):  # 1 to 20 inclusive
    # Define the column names for the current address group
    addrline1_col = f'CnAdrAll_1_{i:02}_Addrline1'
    city_col = f'CnAdrAll_1_{i:02}_City'
    state_col = f'CnAdrAll_1_{i:02}_State'
    zip_col = f'CnAdrAll_1_{i:02}_ZIP'
    type_col = f'CnAdrAll_1_{i:02}_Type'
    preferred_col = f'CnAdrAll_1_{i:02}_Preferred'
    date_added_col = f'CnAdrAll_1_{i:02}_DateAdded'
    date_last_changed_col = f'CnAdrAll_1_{i:02}_DateLastChanged'
    type2_col = f'CnAdrAll_1_{i:02}_Type2'
    indicator_col = f'CnAdrAll_1_{i:02}_Indicator'
    import_id_col = f'CnAdrAll_1_{i:02}_Import_ID'
    
    # Extract the relevant columns for the current address group
    current_extracted_data = data[['CnBio_ID', 'CnBio_No_Valid_Addresses', addrline1_col, city_col, state_col, zip_col, type_col, preferred_col, date_added_col, date_last_changed_col, type2_col, indicator_col, import_id_col]]
    
    # Rename the columns
    current_column_rename_map = {
        addrline1_col: 'Addrline1',
        city_col: 'City',
        state_col: 'State',
        zip_col: 'ZIP',
        type_col: 'Type',
        preferred_col: 'Preferred',
        date_added_col: 'DateAdded',
        date_last_changed_col: 'DateLastChanged',
        type2_col: 'Type2',
        indicator_col: 'Indicator',
        import_id_col: 'Import_ID'
    }
    
    current_transformed_data = current_extracted_data.rename(columns=current_column_rename_map)
    
    # Filter out rows where 'Preferred' is 'Yes' or 'Import_ID' is blank
    current_transformed_data = current_transformed_data[~((current_transformed_data['Preferred'] == 'Yes') | (current_transformed_data['Import_ID'].isnull()))]



    # Append the transformed data to the list
    transformed_dataframes.append(current_transformed_data)

# Concatenate all the transformed dataframes vertically
final_transformed_data = pd.concat(transformed_dataframes, ignore_index=True)
# Drop importID column
final_transformed_data.drop('Import_ID', axis=1, inplace=True)
# Output
final_transformed_data.to_csv('final_transformed_data.csv', index=False)

# ----- combine.py -----
# Using data directly without re-loading from CSVs
# Convert 'DateLastChanged' columns to datetime format for sorting
final_transformed_data['DateLastChanged'] = pd.to_datetime(final_transformed_data['DateLastChanged'])

# Function to get the most recent address for a given CnBio_ID
def get_most_recent_address(cnBio_id):
    filtered_data = final_transformed_data[final_transformed_data['CnBio_ID'] == cnBio_id]
    sorted_data = filtered_data.sort_values(by='DateLastChanged', ascending=False).iloc[0]
    return sorted_data[['Addrline1', 'City', 'State', 'ZIP']]

# Filter out rows that don't have a valid address and no matching valid address in final_transformed_data
rows_to_keep = []

for index, row in final_filtered_data.iterrows():
    try:
        recent_address = get_most_recent_address(row['CnBio_ID'])
        if not pd.isna(recent_address['Addrline1']) and recent_address['Addrline1'] != 'nan':
            row['Addrline1'] = recent_address['Addrline1']
            row['City'] = recent_address['City']
            row['State'] = recent_address['State']
            row['ZIP'] = recent_address['ZIP']
            rows_to_keep.append(row)
    except IndexError:
        continue

final_filtered_data_cleaned = pd.DataFrame(rows_to_keep)

# Save the updated dataframe
final_filtered_data_cleaned.to_csv('filled_final_filtered_data.csv', index=False)
