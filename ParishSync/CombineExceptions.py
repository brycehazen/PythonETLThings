import pandas as pd

# Read both CSV files
summary_data = pd.read_csv("New Import Control-Summary Report.csv", header=None, encoding='ISO-8859-1')
redata_exceptions = pd.read_csv("updated_RE_Data.csv", encoding='ISO-8859-1')

# Create a placeholder DataFrame with the same number of rows as redata_exceptions 
# and the columns: 'Column', 'ColumnValue', 'Reason'
placeholders = pd.DataFrame(columns=['Column', 'ColumnValue', 'Reason'], index=redata_exceptions.index)

for idx, row in summary_data.iterrows():
    target_index = int(row[43].replace(',', '')) - 1  # Remove commas and subtract 1 because index starts from 0
     #target_index = str(int(row[43]).replace(',', '')) - 1
    placeholders.at[target_index, 'Column'] = row[44]
    placeholders.at[target_index, 'ColumnValue'] = row[45]
    placeholders.at[target_index, 'Reason'] = row[46]

# Concatenate the placeholders dataframe at the start of redata_exceptions
result = pd.concat([placeholders, redata_exceptions], axis=1)

# Drop rows where all values in the specified columns are blank
result = result.dropna(how='all', subset=['Column', 'ColumnValue', 'Reason'])

# Save the result to a new CSV file
result.to_csv("updated_RE_DataWithExceptions.csv", index=False, encoding='ISO-8859-1')
