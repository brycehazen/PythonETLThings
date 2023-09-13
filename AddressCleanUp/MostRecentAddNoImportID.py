import pandas as pd
import numpy as np

# Load the CSV
data = pd.read_csv('path_to_input_file.csv')

# Iterate over each row and check for blank preferred address
for index, row in data.iterrows():
    for i in range(1, 8):  # There are 7 address iterations
        prefix = f"CnAdrAll_1_0{i}_"
        if row[prefix + "Preferred"] == "Yes" and pd.isna(row[prefix + "Addrline1"]):
            # If spouse address is not blank, use it
            if not pd.isna(row["CnSpAdrPrf_Addrline1"]):
                for col in ["Addrline1", "City", "State", "ZIP"]:
                    data.at[index, prefix + col] = row["CnSpAdrPrf_" + col]
            else:
                # Find the most recent non-blank address
                most_recent_date = pd.Timestamp('1900-01-01')  # start with a very old date
                most_recent_address = {}
                for j in range(1, 8):
                    address_prefix = f"CnAdrAll_1_0{j}_"
                    if not pd.isna(row[address_prefix + "Addrline1"]):
                        date_added = pd.Timestamp(row[address_prefix + "DateAdded"])
                        if date_added > most_recent_date:
                            most_recent_date = date_added
                            for col in ["Addrline1", "City", "State", "ZIP"]:
                                most_recent_address[col] = row[address_prefix + col]
                # Update blank preferred address with most recent non-blank address
                for col in ["Addrline1", "City", "State", "ZIP"]:
                    data.at[index, prefix + col] = most_recent_address.get(col, np.nan)

# Filter the data for rows where the preferred address was previously blank and has now been filled
filtered_data = data[data['CnBio_No_Valid_Addresses'] == 'Yes']

# Create a simplified dataframe with the required columns
simplified_data = pd.DataFrame({
    'CnBio_ID': filtered_data['CnBio_ID'],
    'CnBio_No_Valid_Addresses': filtered_data['CnBio_No_Valid_Addresses'],
    'CnAdrAllAddrline1': filtered_data['CnAdrAll_1_01_Addrline1'],
    'CnAdrAllCity': filtered_data['CnAdrAll_1_01_City'],
    'CnAdrAllState': filtered_data['CnAdrAll_1_01_State'],
    'CnAdrAllZIP': filtered_data['CnAdrAll_1_01_ZIP'],
    'CnAdrAllType': filtered_data['CnAdrAll_1_01_Type'],
    'CnAdrAllPreferred': filtered_data['CnAdrAll_1_01_Preferred'],
    'CnAdrAllDateAdded': filtered_data['CnAdrAll_1_01_DateAdded'],
    'CnAdrAllDateLastChanged': filtered_data['CnAdrAll_1_01_DateLastChanged'],
    'CnAdrAllType2': filtered_data['CnAdrAll_1_01_Type2'],
    'CnAdrAllIndicator': filtered_data['CnAdrAll_1_01_Indicator'],
    'CnAdrAllImport_ID': filtered_data['CnAdrAll_1_01_Import_ID']
})

# Save the simplified data to a new CSV file
simplified_data.to_csv('path_to_output_file.csv', index=False)
