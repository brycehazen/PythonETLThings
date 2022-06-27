import pandas as pd 
import numpy as np

# Import raw data
data = pd.read_csv("C:/users/input/file.csv", encoding='latin-1' )

# Create array to track failed cases.
data['Test Case Failed']= ''
data = data.replace(np.nan,'')
data.insert(0, 'ID', range(0, len(data)))

# Testcase 1
# Both genders are Male  but addressee or salutation contains Ms. or Mrs.
data_1 = data[(((data['Gender'] == 'Male') & (data['SRGender'] == 'Male')) & 
              (
                  (data['PrimAddText'].str.contains('Ms')) | (data['PrimAddText'].str.contains('Mrs')) | 
                  (data['PrimSalText'].str.contains('Ms')) | (data['PrimSalText'].str.contains('Mrs'))
                  ))]
ids = data_1.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 1'

# Testcase 2
# Both genders are female but addressee or salutation contains Mr.
data_2 = data[(((data['Gender'] == 'Female') & (data['SRGender'] == 'Female')) & 
              (
                  (data['PrimAddText'].str.contains('Ms')) | (data['PrimAddText'].str.contains('Mrs')) | 
                  (data['PrimSalText'].str.contains('Ms')) | (data['PrimSalText'].str.contains('Mrs'))
                  ))]
ids = data_2.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 2'

# Testcase 3
# First name on the record is the same for the spouse.
data_3 = data[(data['FirstName'] == data['SRFirstName'])]
ids = data_3.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 3'

# Testcase 4
# Addressee or salutation does not contain the last name of the record
def find_value_column(row):
    return row.LastName not in row.PrimSalText

data_4 = data[data.apply(find_value_column, axis=1)][['LastName', 'PrimSalText']]
ids = data_4.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 4'

def find_value_column(row):
    return row.LastName not in row.PrimAddText

data_4 = data[data.apply(find_value_column, axis=1)][['LastName', 'PrimAddText']]
ids = data_4.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 4'

data["Test Case Failed"].replace({", 4, 4": ", 4"}, inplace=True)
data["Test Case Failed"].replace({", 3, 4, 4": ", 4"}, inplace=True)
data["Test Case Failed"].replace({", 2, 4, 4": ", 4"}, inplace=True)
data["Test Case Failed"].replace({", 1, 4, 4": ", 4"}, inplace=True)

# Testcase  5
# Record has Name information, Spouse has name information, no one is marked deceased but Addressee or salutation doesn't have  "&" or "AND"
df = data[((data['FirstName']!='') & (data['LastName']!='')) & 
              ((data['SRFirstName']!='') & (data['SRLastName']!='') &
              (data['SRDeceased'].str.contains('Yes')==False) & (data['Deceased'].str.contains('Yes')==False) 
              )]
df1 = df[df['PrimAddText'].str.contains("AND|&")==False] 
data_5 = df1[df1['PrimSalText'].str.contains("AND|&")==False] 
ids = data_5.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 5'

# Testcase  6
# Head of house hold is not above the age of 18.
data['BDay']= pd.to_datetime(data['BDay'], errors="coerce")
data_6 = data.loc[data['BDay'] >= '01/01/2004']
ids = data_6.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 6'

# Testcase  7 
# Addressee or salutation contains "&" or "and" but  it shows the Spouse as deceased.
df = data[data['SRDeceased'] == 'Yes']
df = df[df['PrimAddText'].str.contains("AND|&")]
data_7 = df[df['PrimSalText'].str.contains("AND|&")]  
ids = data_7.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 7'

# Testcase  8 
# Addressee or salutation contain & or And but  Spouse last or first name is empty.
df = data[(data['SRLastName'] == '') | (data['SRFirstName']=='')]
df = df[df['PrimAddText'].str.contains("AND|&", na=False)]
data_8 = df[df['PrimSalText'].str.contains("AND|&", na=False)]  
ids = data_8.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 8'

# Testcase  9
# The spouse shows a deceased date, but martial status is not marked as widowed. 
data_9 = data[((data['SRDeceasedDate'] != '') & (data['MrtlStat'] != 'Widowed'))]
ids = data_9.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 9'

# Testcase  10
# Spouse shows a deceased date, but inactive does not show yes. 
data_10 = data[(data['SRDeceasedDate']!='') & (df['SRInactive']!='Yes')]
ids = data_10.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 10'

# Testcase  11
# Record shows a deceased date, but inactive does not show yes.
data_11 = data[(data['DeceasedDate']!='') & (data['Inactive']!='Yes')]
ids = data_11.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 11'

# Testcase  12
# There is a deceased date but  addressee or salutation contains "&" or "and".
df = data[(data['SRDeceasedDate']!='')]
df = df[df['PrimAddText'].str.contains("AND|&", na=False)]
data_12 = df[df['PrimSalText'].str.contains("AND|&", na=False)]  
ids = data_12.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 12'

# Testcase 13
# Spouse name information is filled in but marital status shows single.
df = data[((data['SRLastName'] != '') | (data['SRFirstName'] != ''))]
data_13 = df[df['MrtlStat'] == 'single']
ids = data_13.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 13'

# Testcase  14
# Marital status is blank but Addressee or salutation has "&" or "and"
df = data[data['MrtlStat'] == '']
df = df[df['PrimAddText'].str.contains("AND|&", na=False)]
data_14 = df[df['PrimSalText'].str.contains("AND|&", na=False)]
ids = data_14.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 14'

# Test case  15
# Marital status has single, divorced, or some variation of widowed, but primary addressee/salutation has & or AND
df = data[data['MrtlStat'].str.contains("Widow|Divorced|Single")]
data_15_A = df[df['PrimAddText'].str.contains("AND|&", na=False)]
data_15_B = df[df['PrimSalText'].str.contains("AND|&", na=False)]
ids = data_15_A.index.tolist() + data_15_B.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 15'

# Total cases
failed = data[(data['Test Case Failed'] != '')]
passed = data[(data['Test Case Failed'] == '')]
failed['Test Case Failed'] =failed['Test Case Failed'].str[1:]
failed = failed[(failed['Test Case Failed'] != '')]

# Clean up
del failed["ID"]
del passed["ID"]

# Print results of testcases to terminal 
failed['Test Case Failed'].value_counts()
print("There was a total of",data.shape[0], "rows.", "There was" ,data.shape[0] - failed.shape[0], "rows passed and" ,failed.shape[0], "rows failed at least one test case")

#####################################################
############### Creating output Files ############### 
#####################################################

# Drop Columns from ImportOmatic
impomatic = passed.drop(columns = ['KeyInd', 'ConsCodeImpID', 'Nickname', 'Deceased', 'DeceasedDate', 'Inactive', 'SRSuff2', 'SRNickname', 'SRDeceased', 'SRDeceasedDate',
'SRInactive', 'PrimAddText', 'PrimSalText', 'AddrImpID', 'AddrType', 'AddrRegion', 'AddrImpID.1', 'AddrLines.1', 'AddrCity.1', 'AddrState.1', 'AddrZIP.1', 'AddrType.1',
'AddrImpID.2', 'AddrLines.2', 'AddrCity.2', 'AddrState.2', 'AddrZIP.2', 'AddrType.2', 'AddrSeasonal', 'AddrSeasFrom', 'AddrSeasTo', 'PhoneAddrImpID', 'PhoneImpID', 'PhoneType',
'PhoneAddrImpID.1', 'PhoneImpID.1', 'PhoneType.1', 'DateTo', 'NameChanged', 'StreetChanged', 'MailingChanged', 'AltChanged', 'Test Case Failed'])

# Creates spouse column and fills in with Yes if 
impomatic.insert(loc = 15, column='Spouse', value = '')
impomatic.loc[(impomatic['SRLastName'] != ''),'Spouse'] = 'Yes'

# Drop unwanted columns for RE
redata = passed.drop(columns=['ImportID', 'ConsCodeImpID', 'Suff1', 'SRSuff2', 'Inactive', 'SRInactive', 
'AddrRegion','AddrImpID', 'AddrImpID', 'AddrImpID.2', 'AddrImpID.1', 'PhoneAddrImpID', 'PhoneAddrImpID.1',
'PhoneImpID', 'PhoneAddrImpID', 'PhoneImpID', 'PhoneType.1', 'DateTo', 'SecondID', 'Test Case Failed', 
'PhoneImpID.1', 'PrimAddText', 'PrimSalText', 'PhoneNum', 'PhoneType', 'PhoneNum.1', 'PhoneType.1'])

# Change Column Spelling for RE import
redata.rename(columns = {'DeceasedDate':'DecDate', 'SRDeceasedDate':'SRDecDate'}, inplace = True)

# Add These Columns for RE import 
redata.insert(loc = 2, column='ConsCodeImpID', value = '')
redata.insert(loc = 4, column='ConsCodeDateFrom', value = '')
redata.insert(loc = 5, column='ConsCodeDateTo', value = '')

# Fill in  Title column  base on condition
redata.loc[redata['Titl1'].eq('Mr.'), 'Gender'] = 'Male'
redata.loc[redata['Titl1'].eq('Mr'), 'Gender'] = 'Male'
redata.loc[redata['Titl1'].eq('Mrs.'), 'Gender'] = 'Female'
redata.loc[redata['Titl1'].eq('Mrs'), 'Gender'] = 'Female'
redata.loc[redata['Titl1'].eq('Ms.'), 'Gender'] = 'Female'
redata.loc[redata['Titl1'].eq('Ms'), 'Gender'] = 'Female'
redata.loc[redata['Titl1'].eq('Miss'), 'Gender'] = 'Female'
redata.loc[redata['SRTitl1'].eq('Mr.'), 'SRGender'] = 'Male'
redata.loc[redata['SRTitl1'].eq('Mr'), 'SRGender'] = 'Male'
redata.loc[redata['SRTitl1'].eq('Mrs.'), 'SRGender'] = 'Female'
redata.loc[redata['SRTitl1'].eq('Mrs'), 'SRGender'] = 'Female'
redata.loc[redata['SRTitl1'].eq('Ms.'), 'SRGender'] = 'Female'
redata.loc[redata['SRTitl1'].eq('Ms'), 'SRGender'] = 'Female'
redata.loc[redata['SRTitl1'].eq('Miss'), 'SRGender'] = 'Female'

# Changing data to fit what's in RE
redata.loc[(redata['MrtlStat'].str.contains('Civilly')),'MrtlStat'] = 'Married'
redata.loc[(redata['MrtlStat'].str.contains('Never')),'MrtlStat'] = 'Single'
redata.loc[(redata['MrtlStat'].str.contains('Unknown')),'MrtlStat'] = ''

# Standardize addresses 
redata['AddrLines'] = redata['AddrLines'].str.replace('Apartment ','Apt ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Apt\\.','Apt ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('APT','Apt ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('nApt','Apt ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('NApt','Apt ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Avenue','Ave ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Ave\\.','Ave ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Boulevard','Blvd ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Blvd.','Blvd ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Building','Bldg ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Bldg\\.','Bldg ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Center','Ctr ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Ctr\\.','Ctr ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Circle','Cir ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Cir\\.','Cir ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Court','Ct ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Ct\\.','Ct ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Drive','Dr ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Dr\\.','Dr ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('East','E ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('E\\.','E ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Expressway','Expy ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Expy\\.','Expy ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Extension','Ext ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Ext\\.','Ext ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Fort','Ft ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Ft\\.','Ft ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Freeway','Fwy ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Fwy\\.','Fwy ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Height','Hts ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Hts\\.','Hts ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Highway','Hwy ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Hwy\\.','Hwy ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Island','Is ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Is\\.','Is ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Junction','Jct ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Jct\\.','Jct ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Lane','Ln ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Ln\\.','Ln ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Mount','Mt ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Mt\.','Mt ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Mountain','St ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Mt\\.','Mt ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('North','N ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('N\\.','N ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Northeast','NE ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('NE\\.','NE ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Northwest','NW ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('NW\\.','NW',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Parkway','Pky ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Pky\\.','Pky ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Place','Pl ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Pl\\.','Pl ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Post Office','PO ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('PO\\.','PO ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('P\\.O','PO ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('P\\.O\\.','PO ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Ridge','Rdg ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Road','Rd ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Rd\\.','Rd ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('ROAD','Rd ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Rural Delivery','RD ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('RD\\.','RD ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Rural Route','RR ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('RR\\.','RR ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Saint','St ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('St\\.','St ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('South','S ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('S\\.','S ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Southeast','SE ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('SE\\.','SE',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Southwest','SW ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('SW\\.','SW ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Spring','Spg ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Spg\\.','Spg ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Springs','Spgs  ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Spg\\.','Spgs ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Square','Sq ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Sq\\.','Sq ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Squares','Sq ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Sq\\.','Sq ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Street','St ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('St\\.','St ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Suite','Ste ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Ste\\.','Ste ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Terrace','Ter ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Ter\\.','Ter ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Turnpike','Tpke ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('Tpke\\.','Tpke ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('UNIT.','Unit ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('LOT','Tpke ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('West','W ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace(',',' ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('\\.','',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('-',' ',regex=True)
redata['AddrLines'] = redata['AddrLines'].str.replace('\\/n',' ',regex=True)

# Output  for Raiser's Edge
redata.to_csv("C:/users/Output/redata.csv", index = False)

# Output failed rows
failed.to_csv("C:/users/Output/Failed.csv", index = False)

# Output passed rows 
passed.to_csv("C:/users/Output/Passed.csv", index = False)

# Outpt file for ImportOMatic
impomatic.to_csv("C:/users/Output/impomatic.csv", index = False)
