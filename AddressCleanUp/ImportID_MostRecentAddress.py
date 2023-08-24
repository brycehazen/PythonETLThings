import os
import pandas as pd

def update_blank_addresses(row):
    updated = False  # Flag to indicate if any address was updated
    
    preferred_cols = [col for col in row.index if 'Preferred' in col and row[col] == 'Yes' and pd.isna(row[col.replace('Preferred', 'Addrline1')])]
    
    for pref_col in preferred_cols:
        # Identify the address column corresponding to the preferred column
        address_col = pref_col.replace('Preferred', 'Addrline1')
        import_id_col = pref_col.replace('Preferred', 'Import_ID')
        
        # Store the original Import_ID
        original_import_id = row[import_id_col]
        
        # Check for spouse address
        if pd.notna(row['CnSpAdrPrf_Addrline1']):
            spouse_cols = [col.replace('CnSpAdrPrf', pref_col.split('_Preferred')[0]) for col in row.filter(like='CnSpAdrPrf').index]
            for col in spouse_cols:
                if 'Import_ID' not in col:
                    row[col] = row[col.replace(pref_col.split('_Preferred')[0], 'CnSpAdrPrf')]
            updated = True
        else:
            # Check other non-blank addresses by recency
            address_dates = row.filter(like='CnAdrAll_1_').filter(like='_DateLastChanged').dropna()
            address_dates = address_dates.apply(pd.to_datetime, errors='coerce').dropna()
            
            if not address_dates.empty:
                most_recent_date_col = address_dates.idxmax()
                most_recent_prefix = most_recent_date_col.split('_DateLastChanged')[0]
                
                for col in row.filter(like=most_recent_prefix).index:
                    if 'Import_ID' not in col:
                        target_col = col.replace(most_recent_prefix, pref_col.split('_Preferred')[0])
                        row[target_col] = row[col]
                updated = True
        
        # Restore the original Import_ID
        row[import_id_col] = original_import_id
    return row, updated

def restructure_updated_rows(row):
    prefixes = [col.split('_Addrline1')[0] for col in row.filter(like='_Addrline1').index]
    for prefix in prefixes:
        if pd.notna(row[f'{prefix}_Addrline1']):
            return {
                'CnBio_ID': row['CnBio_ID'],
                'CnBio_No_Valid_Addresses': row['CnBio_No_Valid_Addresses'],
                'Addrline1': row[f'{prefix}_Addrline1'],
                'City': row[f'{prefix}_City'],
                'State': row[f'{prefix}_State'],
                'ZIP': row[f'{prefix}_ZIP'],
                'Type': row[f'{prefix}_Type'],
                'Preferred': row[f'{prefix}_Preferred'],
                'DateAdded': row[f'{prefix}_DateAdded'],
                'DateLastChanged': row[f'{prefix}_DateLastChanged'],
                'Type2': row[f'{prefix}_Type2'],
                'Indicator': row[f'{prefix}_Indicator'],
                'Add_Import_ID': row[f'{prefix}_Import_ID']
            }
    return {}  # Return an empty dictionary if no valid address was found

# Get the current directory (the location of the script)
folder_path = os.getcwd()

# Identify all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv') and '_output' not in file]

# Iterate over each CSV file and process it
for csv_file in csv_files:
    input_df = pd.read_csv(os.path.join(folder_path, csv_file))
    
    # Update blank addresses and keep only the rows that were updated
    updated_rows = []
    for _, row in input_df.iterrows():
        updated_row, was_updated = update_blank_addresses(row)
        if was_updated:
            updated_rows.append(restructure_updated_rows(updated_row))
    
    # Filter out rows that didn't have their addresses updated before creating the dataframe
    updated_rows = [row for row in updated_rows if row]
    updated_df = pd.DataFrame(updated_rows)
    
    # Save the processed dataframe to a new CSV file
    output_filename = os.path.splitext(csv_file)[0] + "_output.csv"
    updated_df.to_csv(os.path.join(folder_path, output_filename), index=False)
