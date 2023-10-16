import pandas as pd
from bs4 import BeautifulSoup

# Read the HTML file
file_name = 'Blackbaud.html'
with open(file_name, 'r', encoding='utf-8') as f:
    content = f.read()

# Parse the HTML content
soup = BeautifulSoup(content, 'html.parser')

# Extract email addresses and names
data = []
for row in soup.find_all('tr', {'class': 'sky-grid-row'}):
    email_cell = row.find('sky-grid-cell', {'sky-cmp-id': 'emailAddress'})
    name_cell = row.find('sky-grid-cell', {'sky-cmp-id': 'displayName'})
    
    if email_cell and name_cell:
        email = email_cell.text.strip()
        name = name_cell.text.strip()
        data.append({'Email': email, 'Name': name})

# Save the data to a CSV file
emails_and_names_df = pd.DataFrame(data)
emails_and_names_df.to_csv('emails_and_names.csv', index=False)

# Read the Emailbounces.csv file
email_bounces_df = pd.read_csv('EmailBounces.csv')

# Create a new dataframe to store the matched email addresses and their corresponding Import_IDs
bounce_email_import_df = pd.DataFrame(columns=['importID', 'PhoneImpID', 'PhoneNum', 'PhoneIsInactive'])

# Iterate over the email columns and their corresponding Import_ID columns
for i in range(1, 11):
    email_col = f'CnPh_1_{i:02d}_Phone_number'
    import_id_col = f'CnPh_1_{i:02d}_Import_ID'
    
    # Convert the email column to string (object) data type
    email_bounces_df[email_col] = email_bounces_df[email_col].astype(str)
    
    # Merge the current email column with the emails_and_names_df dataframe based on the email addresses
    merged_df = emails_and_names_df.merge(email_bounces_df[['CnBio_Import_ID', email_col, import_id_col]], left_on='Email', right_on=email_col)
    
    # If there are any matches, append them to the bounce_email_import_df dataframe
    if not merged_df.empty:
        matched_data = merged_df[['CnBio_Import_ID', import_id_col, 'Email']].assign(PhoneIsInactive='Yes')
        matched_data.columns = ['importID', 'PhoneImpID', 'PhoneNum', 'PhoneIsInactive']
        bounce_email_import_df = pd.concat([bounce_email_import_df, matched_data], ignore_index=True)

# Save the bounceEmailImport.csv file
bounce_email_import_df.to_csv('BouncedEmailsImport.csv', index=False)
