import pandas as pd
import os
from datetime import datetime

# Function to remap fund IDs based on a dictionary
def remap_fund_id(last_fund_id, last_fund_id_desc):
    # Dictionary mapping original fund IDs to their corresponding IDs and descriptions
    # Original ID: (New ID, Description)
    remap_dict = {
        1: ("2-1", "St. Francis of Assisi Catholic Church"),
        2: ("2-2", "St. Catherine of Siena Catholic Church"),
        3: ("3-3", "St. Thomas Aquinas Catholic Church"),
        4: ("1-4", "St. Theresa Catholic Church"),
        5: ("1-5", "St. Lawrence Catholic Church"),
        6: ("2-6", "Holy Family Catholic Church"),
        7: ("1-7", "St. Jude Catholic Church"),
        8: ("1-8", "Immaculate Heart of Mary Catholic Church"),
        9: ("2-9", "St. Augustine Catholic Church"),
        10: ("1-10", "St. Hubert of the Forest Mission"),
        11: ("1-11", "Blessed Sacrament Catholic Church"),
        12: ("4-12", "Church of Our Saviour"),
        13: ("3-13", "St. Faustina Catholic Church"),
        14: ("2-14", "Corpus Christi Catholic Churchh"),
        15: ("2-15", "St. Maximillian Kolbe Catholic Church"),
        16: ("2-16", "St. Frances Xavier Cabrini"),
        17: ("5-17", "Our Lady of Lourdes Catholic Church,"),
        18: ("5-18", "Basilica of St. Paulh"),
        19: ("5-19", "St. Ann Catholic Church"),
        20: ("5-20", "St. Peter Catholic Church"),
        21: ("5-21", "Our Lady of the Lakes Catholic Church"),
        22: ("1-22", "St. John the Baptist Catholic Church"),
        23: ("5-23", "San Jose Mission"),
        24: ("5-24", "St. Clare Catholic Church"),
        25: ("5-25", "St. Gerard Mission"),
        26: ("4-26", "Ascension Catholic Church"),
        27: ("1-27", "St. Mary of the Lakes Catholic Church"),
        28: ("3-28", "St. John Neumann Catholic Church"),
        29: ("2-29", "Sts. Peter and Paul Catholic Church"),
        30: ("1-30", "Santo Toribio Romo Mission"),
        32: ("3-32", "St. Ann Catholic Church"),
        33: ("2-33", "Holy Redeemer Catholic Church"),
        34: ("3-34", "St. Joseph Catholic Church"),
        35: ("3-35", "Church of the Resurrection"),
        36: ("3-36", "St. Anthony Catholic Church"),
        39: ("2-39", "Church of the Nativity"),
        40: ("1-40", "St. Timothy Catholic Church"),
        41: ("3-41", "Holy Spirit Catholic Church"),
        42: ("3-42", "St. Leo the Great Mission"),
        44: ("1-44", "St. Paul Catholic Church"),
        45: ("2-45", "St. Philip Phan Van Minh Catholic Church"),
        46: ("2-46", "Annunciation Catholic Church"),
        47: ("2-47", "St. Mary Magdalen Catholic Church"),
        48: ("4-48", "Our Lady of Lourdes Catholic Church"),
        49: ("4-49", "Divine Mercy Catholic Church"),
        50: ("4-50", "Holy Spirit Catholic Church"),
        51: ("1-51", "St. Patrick Catholic Church"),
        52: ("4-52", "Immaculate Conception Catholic Church"),
        53: ("1-53", "St. Joseph of the Forest Mission"),
        54: ("5-54", "Our Lady Star of the Sea Catholic Church"),
        55: ("5-55", "Sacred Heart Catholic Church"),
        56: ("1-56", "Our Lady of the Springs Catholic Church"),
        57: ("1-57", "Blessed Trinity Catholic Church"),
        58: ("2-58", "St. Isaac Jogues Catholic Church"),
        59: ("2-59", "St. Andrew Catholic Church"),
        60: ("2-60", "Blessed Trinity Catholic Church"),
        61: ("2-61", "St. Charles Borromeo Catholic Church"),
        62: ("2-62", "Good Shepherd Catholic Church"),
        63: ("2-63", "St. James Cathedral"),
        64: ("2-64", "St. John Vianney Catholic Church"),
        65: ("1-65", "Christ the King Mission"),
        66: ("2-66", "Mary Queen of the Universe Shrine"),
        67: ("1-67", "Queen of Peace Catholic Church"),
        68: ("2-68", "Holy Cross Catholic Church"),
        69: ("5-69", "St. Brendan Catholic Church"),
        70: ("5-70", "Prince of Peace Catholic Church"),
        71: ("4-71", "St. Joseph Catholic Church"),
        72: ("5-72", "Church of the Epiphany"),
        73: ("4-73", "Our Lady of Grace Catholic Church"),
        74: ("5-74", "Our Lady of Hope Catholic Church"),
        75: ("4-75", "St. Luke Catholic Church"),
        76: ("4-76", "St. Mary Catholic Church"),
        77: ("3-77", "St. Rose of Lima Catholic Church"),
        78: ("2-78", "St. Thomas Aquinas Catholic Church"),
        79: ("2-79", "All Souls Catholic Church"),
        80: ("4-80", "Holy Name of Jesus Catholic Church"),
        81: ("2-81", "St. Ignatius Kim Mission"),
        82: ("2-82", "Most Precious Blood Catholic Church"),
        83: ("4-83", "Blessed Sacrament Catholic Church"),
        84: ("1-84", "St. Mark the Evangelist Catholic Church"),
        85: ("1-85", "Our Lady of Guadalupe Mission"),
        87: ("4-87", "St. John the Evangelist Catholic Church"),
        88: ("4-88", "St. Teresa Catholic Church"),
        89: ("1-89", "St. Vincent de Paul Catholic Church"),
        90: ("2-90", "St. Stephen Catholic Church"),
        91: ("2-91", "St. Joseph Catholic Church"),
        92: ("1-92", "San Pedro de Jesus Maldonado Mission"),
        94: ("3-94", "St. Matthew Catholic Church"),
        95: ("2-95", "Resurrection Catholic Church"),
        96: ("3-96", "St. Joseph Catholic Church"),
        97: ("2-97", "St. Margaret Mary Catholic Church"),
        98: ("3-98", "St. Elizabeth Ann Seton Mission"),
        145: ("3-145", "Centro Guadalupano Mission"),
    }
    # Return the new ID and description for the given fund ID, or the original ID and description if not found in the dictionary
    return remap_dict.get(last_fund_id, (str(last_fund_id), last_fund_id_desc))

# Function to apply remapping to each row of the DataFrame
def apply_remap(row):
    # Get the new ID and description using remap_fund_id function
    new_id, new_desc = remap_fund_id(row['LastFundID'], row['LastFundIDDesc'])
    # Update the row with the new ID and description
    row['LastFundID'], row['LastFundIDDesc'] = new_id, new_desc
    return row

# Function to concatenate columns and generate actual notes and description
def concatenate_columns(row, columns_to_concatenate, conscode_groups):
    # Concatenate non-null values from specified columns into actual notes
    actual_notes = '\n'.join([f"{col}: {row[col]}" for col in columns_to_concatenate if pd.notnull(row[col])])
    row['CnNote_1_01_Actual_Notes'] = actual_notes

    # Extract cons codes from the row based on provided groups
    cons_codes_short = []
    for short_col, end_date_col in conscode_groups:
        if pd.isnull(row[end_date_col]) and pd.notnull(row[short_col]):
            cons_codes_short.append(str(row[short_col])
                                    )
    # If no cons codes found and LastFundID is not null, add LastFundID to cons codes            
    if not cons_codes_short and pd.notnull(row['LastFundID']):
        cons_codes_short.append(str(row['LastFundID']))
    # Join and sort the unique cons codes to generate the description
    row['CnNote_1_01_Description'] = '; '.join(sorted(set(cons_codes_short)))
    return row

# Function to process the DataFrame applying concatenation and remapping
def process_dataframe(df, columns_to_concatenate, conscode_groups):
    # Apply concatenation and remapping functions to each row of the DataFrame    
    return df.apply(concatenate_columns, args=(columns_to_concatenate, conscode_groups), axis=1)

# Function to create individual files for each unique description in a directory
def parish_files(df, dir_name):
    # Create the directory if it doesn't exist
    os.makedirs(dir_name, exist_ok=True)
    # Get unique descriptions from the DataFrame
    descriptions = df['CnNote_1_01_Description'].dropna().unique()
    # Iterate through each description
    for desc in descriptions:
        # Split the description if there are multiple codes separated by ';'
        for single_desc in desc.split('; '):
            # Filter DataFrame rows containing the current description
            desc_df = df[df['CnNote_1_01_Description'].str.contains(f"\\b{single_desc}\\b", na=False, regex=True)]
            # Generate file name based on the description and save filtered DataFrame to Excel file
            file_name = f"{single_desc.replace('/', '_').replace(' ', '_')}.xlsx"
            desc_df.to_excel(os.path.join(dir_name, file_name), index=False)

# Function to prepare DataFrame for re-importing     
def creating_Import_files(df):
    # Create a new dataframe for reimporting
    reimport_df = df.copy()
    # Fill in column 'CnNote_1_01_Title' with 'Synced'
    reimport_df['CnNote_1_01_Title'] = 'Synced'
    # Drop the specified columns
    columns_to_drop = [
        'CnAls_1_01_Alias', 'CnAls_1_01_Alias_Type',
        'CnAls_1_02_Alias', 'CnAls_1_02_Alias_Type',
        'CnAls_1_03_Alias', 'CnAls_1_03_Alias_Type',
        'CnAls_1_04_Alias', 'CnAls_1_04_Alias_Type',
        'CnAls_1_05_Alias', 'CnAls_1_05_Alias_Type',
        'CnAls_1_06_Alias', 'CnAls_1_06_Alias_Type',
        'LastChangedBy', 'DateLastChange', 'PrimAddText', 'PrimSalText','SRConsID', 'SRInactive', 'SRMrtlStat',
        'CnNote_1_01_Description', 'ConsCode_Long', 'ConsCode_Short', 'ConsCode_StartDate', 'ConsCode_EndDate',
        'ConsCode_Long_1', 'ConsCode_Short_1', 'ConsCode_StartDate_1', 'ConsCode_EndDate_1',  'ConsCode_Long_2',
        'ConsCode_Short_2', 'ConsCode_StartDate_2', 'ConsCode_EndDate_2', 'LastFundIDDesc', 'LastFundID',
    ]
    # Drop specified columns from the DataFrame
    reimport_df.drop(columns=columns_to_drop, inplace=True, errors='ignore')
    # Output a new csv called 'NotesAllChanges_ImportReady.csv'
    reimport_df.to_csv('NotesAllChanges_ImportReady.csv', index=False)

    return reimport_df

# Function to clean up files in a directory
def file_clean_up(dir_name):
    # List of columns to be removed from each file
    columns_to_remove = [
        'CnNote_1_01_Type', 'CnNote_1_01_Title', 'CnNote_1_01_Description',
        'CnNote_1_01_Import_ID', 'ConsCode_Long', 'ConsCode_Short',
        'ConsCode_StartDate', 'ConsCode_EndDate', 'ConsCode_Long_1',
        'ConsCode_Short_1', 'ConsCode_StartDate_1', 'ConsCode_EndDate_1',
        'ConsCode_Long_2', 'ConsCode_Short_2', 'ConsCode_StartDate_2',
        'ConsCode_EndDate_2', 'LastFundIDDesc', 'LastFundID', 'CnNote_1_01_Actual_Notes', 'LastChangedBy', 'DateLastChange',
    ]
    total_counts = {}

    # Iterate through each file in the directory
    for file in os.listdir(dir_name):
        # Check if the file is an Excel file and not one of the special files
        if file.endswith('.xlsx') and file not in ['TotalCount.xlsx', 'Rows Without File.xlsx']:
            file_path = os.path.join(dir_name, file)
            # Read the Excel file into a DataFrame
            df = pd.read_excel(file_path)
            # Remove specified columns if they exist in the DataFrame
            df.drop(columns=[col for col in columns_to_remove if col in df.columns], inplace=True, errors='ignore')
            # Save the modified DataFrame back to the file
            df.to_excel(file_path, index=False)
            # Update total_counts after cleanup
            total_counts[file] = len(df)

    # Create "TotalCount.xlsx" containing the row count of each file
    total_count_df = pd.DataFrame(list(total_counts.items()), columns=['FileName', 'RowCount'])
    total_count_path = os.path.join(dir_name, "TotalCount.xlsx")
    total_count_df.to_excel(total_count_path, index=False)

    # Rename 'nan.xlsx' to 'Rows Without File.xlsx' if present
    nan_path = os.path.join(dir_name, 'nan.xlsx')
    rows_without_file_path = os.path.join(dir_name, 'Rows Without File.xlsx')

    # Check if 'nan.xlsx' exists in the directory
    if os.path.exists(nan_path):
        # Check if 'Rows Without File.xlsx' already exists
        if os.path.exists(rows_without_file_path):
            # Remove 'Rows Without File.xlsx' to avoid conflict before renaming
            os.remove(rows_without_file_path)
        # Rename 'nan.xlsx' to 'Rows Without File.xlsx'
        os.rename(nan_path, rows_without_file_path)


# Get today's date
today = datetime.today().strftime('%Y-%m-%d')
# Create directory name with today's date
dir_name = f"Parish Updates {today}"
# Input filename containing the original data
filename = 'NotesAllChanges.XLS'
# Read data from Excel file into a DataFrame
df = pd.read_excel(filename)
# Apply remapping function to each row of the DataFrame
df = df.apply(apply_remap, axis=1)

# Columns to concatenate
columns_to_concatenate = [
        'LastChangedBy', 'DateLastChange', 'ConsID', 'IsInactive', 'Deceased', 'DeceasedDate', 'Gender',
        'Titl1', 'FirstName', 'LastName', 'Suffix', 'MrtlStat', 'MaidenName', 'Bday', 'PrimAddText',
        'PrimSalText', 'SRConsID', 'SRInactive', 'SRDeceased', 'SRDeceasedDate', 'SRGender',
        'SRTitl1', 'SRFirstName', 'SRLastName', 'SRSuffix', 'SRMrtlStat', 'SRMaidenName', 'AddrLines',
        'AddrCity', 'AddrState', 'AddrZIP'
    ]
# Cons code groups with their criteria
conscode_groups = [
            ('ConsCode_Short', 'ConsCode_EndDate'),
            ('ConsCode_Short_1', 'ConsCode_EndDate_1'),
            ('ConsCode_Short_2', 'ConsCode_EndDate_2'),
        ]

# Process the DataFrame by applying concatenation and remapping
df = process_dataframe(df, columns_to_concatenate, conscode_groups)
# Save the processed DataFrame to an Excel file
df.to_excel('Updated_NotesAllChanges.xlsx', index=False)
# Prepare DataFrame for re-importing
reimport_df = creating_Import_files(df)
# Generate individual files for each unique description in the directory
parish_files(df, dir_name)
# Clean up files in the directory
file_clean_up(dir_name)
