import pandas as pd 
import numpy as np

# Import raw data
data = pd.read_csv("C:/Users/file.csv", encoding='latin-1' )

# Create array to track failed cases.
data['Test Case Failed']= ''
data = data.replace(np.nan,'')
data.insert(0, 'ID', range(0, len(data)))

# Testcase 1
data_1 = data[(((data['Gender'] == 'Male') & (data['SRGender'] == 'Male')) & 
              (
                  (data['PrimAddText'].str.contains('Ms')) | (data['PrimAddText'].str.contains('Mrs')) | 
                  (data['PrimSalText'].str.contains('Ms')) | (data['PrimSalText'].str.contains('Mrs'))
                  ))]
ids = data_1.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 1'

# Testcase 2
data_2 = data[(((data['Gender'] == 'Female') & (data['SRGender'] == 'Female')) & 
              (
                  (data['PrimAddText'].str.contains('Ms')) | (data['PrimAddText'].str.contains('Mrs')) | 
                  (data['PrimSalText'].str.contains('Ms')) | (data['PrimSalText'].str.contains('Mrs'))
                  ))]
ids = data_2.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 2'

# Testcase 3
data_3 = data[(data['FirstName'] == data['SRFirstName'])]
ids = data_3.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 3'

# Testcase 4
def find_value_column(row):
    return row.LastName not in row.PrimSalText

data_4 = data[data.apply(find_value_column, axis=1)][['LastName', 'PrimSalText']]
ids = data_4.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 4'

# Testcase  4
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
data['BDay']= pd.to_datetime(data['BDay'], errors="coerce")
data_6 = data.loc[data['BDay'] >= '01/01/2004']
ids = data_6.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 6'

# Testcase  7 
df = data[data['SRDeceased'] == 'Yes']
df = df[df['PrimAddText'].str.contains("AND|&")]
data_7 = df[df['PrimSalText'].str.contains("AND|&")]  
ids = data_7.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 7'

# Testcase  8 
df = data[(data['SRLastName'] == '') | (data['SRFirstName']=='')]
df = df[df['PrimAddText'].str.contains("AND|&", na=False)]
data_8 = df[df['PrimSalText'].str.contains("AND|&", na=False)]  
ids = data_8.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 8'

# Testcase  9
data_9 = data[((data['SRDeceasedDate'] != '') & (data['MrtlStat'] != 'Widowed'))]
ids = data_9.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 9'

# Testcase  10
data_10 = data[(data['SRDeceasedDate']!='') & (df['SRInactive']!='Yes')]
ids = data_10.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 10'

# Testcase  11
data_11 = data[(data['DeceasedDate']!='') & (data['Inactive']!='Yes')]
ids = data_11.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 11'

# Testcase  12
df = data[(data['SRDeceasedDate']!='')]
df = df[df['PrimAddText'].str.contains("AND|&", na=False)]
data_12 = df[df['PrimSalText'].str.contains("AND|&", na=False)]  
ids = data_12.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 12'

# Testcase 13
df = data[((data['SRLastName'] != '') | (data['SRFirstName'] != ''))]
data_13 = df[df['MrtlStat'] == 'single']
ids = data_13.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 13'

# Testcase  14
df = data[data['MrtlStat'] == '']
df = df[df['PrimAddText'].str.contains("AND|&", na=False)]
data_14 = df[df['PrimSalText'].str.contains("AND|&", na=False)]
ids = data_14.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 14'

# Test case  15
df = data[data['MrtlStat'].str.contains("Widow|Divorced|Single")]
data_15_A = df[df['PrimAddText'].str.contains("AND|&", na=False)]
data_15_B = df[df['PrimSalText'].str.contains("AND|&", na=False)]
ids = data_15_A.index.tolist() + data_15_B.index.tolist()
for i in ids:
  data.at[i,'Test Case Failed']+=', 15'


#data.iloc[70:90]
#data.head()
#data['Test Case Failed'].unique()
#(data['Test Case Failed'].values == '').sum()
#failed.head(50)
#failed['Test Case Failed'].unique()
#passed.head()

# Total cases
failed = data[(data['Test Case Failed'] != '')]
passed = data[(data['Test Case Failed'] == '')]
failed['Test Case Failed'] =failed['Test Case Failed'].str[1:]
failed = failed[(failed['Test Case Failed'] != '')]

# Clean up
del failed["ID"]
del passed["ID"]

# Print results 
failed['Test Case Failed'].value_counts()
print("There was a total of",data.shape[0], "rows.", "There was" ,data.shape[0] - failed.shape[0], "rows passed and" ,failed.shape[0], "rows failed at least one test case")

# Drop unwanted columns, this will have to be adjusted if PDS devs help..
redata = passed.drop(columns=['ConsCodeImpID', 'ImportID', 'Suff1', 'SRSuff2', 'Inactive', 
'AddrRegion','AddrImpID', 'AddrImpID', 'AddrImpID.2', 'AddrImpID.1', 'PhoneAddrImpID',
'PhoneAddrImpID.1', 'PhoneImpID', 'PhoneAddrImpID', 'PhoneImpID', 'PhoneType.1', 'DateTo', 
'SecondID', 'Test Case Failed', 'PhoneImpID.1'])

# Clean address  
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

# def selector(x):
#     if 'Street' in x:
#         return 'St'
#     if 'St.' in x:
#         return 'St'
# redata['AddrLines'].apply(selector)

# AddLineNew={1:'St',2:'St'}
# AddLineOld={'Street':1,'St.':2}
# redata.AddrLines.replace(AddLineOld).map(AddLineNew)

# Output edited dropped columns  
redata.to_csv("C:/Users/redata.csv", index = False)
# Output failed rows
failed.to_csv("C:/Users/Failed.csv", index = False)
# Output passed rows 
passed.to_csv("C:/Users/Passed.csv", index = False)

