import pandas as pd
import os

# Initialize phone_cons_id outside of the conditional check to avoid NameError later
phone_cons_id = pd.DataFrame()

# Check if RE_DataWithExceptions.csv exists
if os.path.exists("updated_RE_DataWithExceptions.csv"):
    exceptions = pd.read_csv("updated_RE_DataWithExceptions.csv", encoding='ISO-8859-1')
    
    # Filter rows based on conditions
    condition = (exceptions['Column'] == 'PhoneType') & (exceptions['Reason'].str.contains('Error saving record: A duplicate phone number and phone type exists.'))
    filtered_rows = exceptions[condition]
    
    # Add rows to PhoneConsID.csv
    new_rows = []
    for _, row in filtered_rows.iterrows():
        phone = row['PhoneNum'] if pd.notnull(row['PhoneNum']) else row['PhoneNum.1']
        new_rows.append({'ConsID': row['ConsID'], 'Phone': phone})
    
    # Read the phone_cons_id data
    if os.path.exists("PhoneConsID.csv"):
        phone_cons_id = pd.read_csv("PhoneConsID.csv", encoding='ISO-8859-1')
    phone_cons_id = pd.concat([phone_cons_id, pd.DataFrame(new_rows)], ignore_index=True)
    phone_cons_id.drop_duplicates(inplace=True)
    phone_cons_id.to_csv("PhoneConsID.csv", index=False)

# Make sure PhoneConsID.csv exists
if os.path.exists("PhoneConsID.csv"):
    phone_cons_id = pd.read_csv("PhoneConsID.csv", encoding='ISO-8859-1')

# Read RE_Data.csv
redata = pd.read_csv("RE_Data.csv", encoding='ISO-8859-1')
phone_cons_id['Phone'] = phone_cons_id['Phone'].astype(str)

# Removing entries from 'PhoneNum' and 'PhoneType' in redata based on phone_cons_id matches
mask_phone = redata.set_index(['ConsID', 'PhoneNum']).index.isin(phone_cons_id.set_index(['ConsID', 'Phone']).index)
redata.loc[mask_phone, ['PhoneNum', 'PhoneType']] = ''

# Removing entries from 'PhoneNum.1' and 'PhoneType.1' in redata based on phone_cons_id matches
mask_phone_1 = redata.set_index(['ConsID', 'PhoneNum.1']).index.isin(phone_cons_id.set_index(['ConsID', 'Phone']).index)
redata.loc[mask_phone_1, ['PhoneNum.1', 'PhoneType.1']] = ''

# Save the updated data to a new CSV file
redata.to_csv("updated_RE_Data.csv", encoding='ISO-8859-1')
