import pandas as pd

data = pd.read_csv("defin10yrnogift.csv")
pd.set_option('display.max_columns', None)
df = pd.DataFrame(data)

# # Transformation and Cleaning.
# If *MrtlStatus* is "Single" and *Addressee* contains "&" or "and". Set *MrtlStatus* to "Widowed".

df.loc[(df['MrtlStatus'] == 'Single') & (df['Addressee'].str.contains('&| and ')),'MrtlStatus'] = 'Widowed'

# If no MrtlStatus and Addressee does not contains "&" or "and". Set MrtlStatus to 'single'.

df.loc[(df['MrtlStatus'].isnull()) & (~df['Addressee'].str.contains('&| and ')),'MrtlStatus'] = 'Single'

# If main person is deceased or inactive, check if spouse is active and not deceased to swap.

# Create a temporary table where main person is deceased or inactive and spouse is not deceased and active.

deceased_table = df.loc[((df['Deceased?'] =='Yes') | (df['Inactive?'] =='Yes')) 
                        & ((df['SpDeceased'] == 'No') & (df['SpInactive?'] == 'No')) 
                        & (df['Addressee'].str.contains('&| and ')),
       ['SpTitle', 'SpFirstName','SpLastName','SpDeceased', 'SpInactive?', 'Title', 'FirstName','LastName','Deceased?', 'Inactive?']]

# Add opposite title if empty. I only did it for Mrs./Mr. because it was the most common. Edge cases can be added if needed.

deceased_table.loc[deceased_table['Title'].eq('Mr.') & deceased_table['SpTitle'].isnull(), 'SpTitle'] = 'Mrs.'
deceased_table.loc[deceased_table['Title'].eq('Mrs.') & deceased_table['SpTitle'].isnull(), 'SpTitle'] = 'Mr.'

# We combine fields to create proper Addressee and Salutation.

deceased_table['Addressee'] = deceased_table['SpTitle'] + ' ' + deceased_table['SpFirstName'] + ' ' + deceased_table['SpLastName']
deceased_table['Salutation'] = deceased_table['SpTitle'] + ' ' + deceased_table['SpLastName']

# Handle null cases for Addressee and Salutation.

deceased_table.loc[deceased_table['SpFirstName'].isnull() & deceased_table['Addressee'].isnull(), 'Addressee'] = deceased_table['SpLastName']
deceased_table.loc[deceased_table['Addressee'].isnull(), 'Addressee'] = deceased_table['SpFirstName'] + ' ' + deceased_table['SpLastName']
deceased_table.loc[deceased_table['Salutation'].isnull(), 'Salutation'] = deceased_table['SpLastName']

# Add values from temporary table to main table.

df.loc[((df['Deceased?'] =='Yes') | (df['Inactive?'] =='Yes')) 
                        & ((df['SpDeceased'] == 'No') & (df['SpInactive?'] == 'No')) 
                        & (df['Addressee'].str.contains('&| and ')),
       ['Title', 'FirstName','LastName','Deceased?', 'Inactive?', 'SpTitle', 'SpFirstName','SpLastName','SpDeceased', 'SpInactive?','Addressee','Salutation']] = deceased_table.values

# If main contact and spouse are deceased both will be inactive.

df.loc[(df['Deceased?'] == 'Yes') & (df['SpDeceased'] == 'Yes'),['Inactive?', 'SpInactive?']] = 'Yes', 'Yes'


redata = df.drop(columns=['SysID', 'SpConsID' , 'SpSysID', 'AddType', 'SpMrtlStatus' , 'SalType', 'Lgdate', 'LGAmount' ])

redata.to_csv('donors_information.csv', index=False,)  


redata.rename(columns = {'oldcolumn1':'newcolumn1', 'oldcolumn2':'newcolumn2'}, inplace = True)
