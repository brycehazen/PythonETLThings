import pandas as pd

# Load the new dataset
df_new = pd.read_csv('StFranMissingAddExport.CSV', encoding='ISO-8859-1')

# Identify columns related to DateLastChanged
date_last_changed_columns = [col for col in df_new.columns if "DateLastChanged" in col]

# Extracting the most recent non-blank DateLastChanged for each row along with the corresponding address columns
recent_address_data = []
for index, row in df_new.iterrows():
    # Create a list of tuples (date, column) for each row, ignore invalid or missing dates
    dates_and_columns = [(pd.to_datetime(row[col], errors='coerce'), col) for col in date_last_changed_columns]
    # Sort the list by date, most recent first
    dates_and_columns.sort(key=lambda x: x[0], reverse=True)
    
    recent_date = None
    recent_address = None
    for date, col in dates_and_columns:
        address_prefix = col.rsplit("_", maxsplit=1)[0]
        address = {
            "Addrline1": row[address_prefix + "_Addrline1"],
            "City": row[address_prefix + "_City"],
            "State": row[address_prefix + "_State"],
            "ZIP": row[address_prefix + "_ZIP"]
        }
        # If the address line is not blank, update the recent_date and recent_address and break the loop
        if address["Addrline1"] is not None and not pd.isnull(address["Addrline1"]):
            recent_date = date
            recent_address = address
            break
    recent_address_data.append((row['CnBio_ID'], recent_date, recent_address))

# Create a DataFrame to store the results
recent_address_df = pd.DataFrame(recent_address_data, columns=['ConsID', 'DateLastChanged', 'Address'])

# Convert the 'Address' column from dictionary to string
recent_address_df['Address'] = recent_address_df['Address'].apply(lambda x: str(x) if x is not None else None)

# Replace 'nan' in the 'Address' column with None representation
recent_address_df['Address'] = recent_address_df['Address'].apply(lambda x: x.replace('nan', 'None') if x is not None else None)

# Convert the 'Address' column from string back to dictionary
recent_address_df['Address'] = recent_address_df['Address'].apply(lambda x: eval(x) if x is not None else None)

# Create separate columns for each part of the address
recent_address_df['Addrline1'] = recent_address_df['Address'].apply(lambda x: x.get('Addrline1') if x is not None else None)
recent_address_df['City'] = recent_address_df['Address'].apply(lambda x: x.get('City') if x is not None else None)
recent_address_df['State'] = recent_address_df['Address'].apply(lambda x: x.get('State') if x is not None else None)
recent_address_df['ZIP'] = recent_address_df['Address'].apply(lambda x: x.get('ZIP') if x is not None else None)

# Drop the original 'Address' column
recent_address_df.drop('Address', axis=1, inplace=True)

# Save the adjusted recent address DataFrame to a new CSV file
recent_address_df.to_csv('Recent_Address_Separated.csv', index=False)
