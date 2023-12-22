############################################################################################
##### This is testing changeing values like titles and martlstatus but on existing data#####
############################################################################################

import glob
import pandas as pd
import numpy as np
import os

# Any file ending in csv
files = glob.glob('*.CSV')

# List of all RE titles
AllREtitles = ['Dr.', 'The Honorable', 'Col.', 'Cmsgt. Ret.', 'Rev. Mr.', 'Deacon', 'Judge', 
                 'Lt. Col.', 'Col. Ret.', 'Major', 'Capt.', 'Maj. Gen.', 'Family of', 'Senator', 'Reverend', 
                 'Lt.', 'Cmdr.', 'Msgt.', 'Sister', 'Drs.', 'Master', 'Sgt. Maj.', 'SMSgt.', 'Prof.', 'Lt. Col. Ret.', 'Rev. Dr.', 
                 'Father', 'Brother', 'Bishop', 'Gen.', 'Admiral', 'Very Reverend', 'MMC', 'Monsignor', '1st Lt.', 'Reverend Monsignor', 
                  'Maj.', 'Most Reverend', 'Bishop Emeritus','Mrs.', 'Mr.', 'Ms.', 'Sra.', 'Señor', 'Miss','Sr.', 'Family of']

# List of  special  titles
specialTitle = ['Dr.', 'The Honorable', 'Col.', 'Cmsgt. Ret.', 'Rev. Mr.', 'Deacon', 'Judge', 
                 'Lt. Col.', 'Col. Ret.', 'Major', 'Capt.', 'Maj. Gen.', 'Family of', 'Senator', 'Reverend', 
                 'Lt.', 'Cmdr.', 'Msgt.', 'Sister', 'Drs.', 'Master', 'Sgt. Maj.', 'SMSgt.', 'Prof.', 'Lt. Col. Ret.', 'Rev. Dr.', 
                 'Father', 'Brother', 'Bishop', 'Gen.', 'Admiral', 'Very Reverend', 'MMC', 'Monsignor', '1st Lt.', 'Reverend Monsignor', 
                  'Maj.', 'Most Reverend', 'Bishop Emeritus','Family of']

# List of common titles
commonTitles = ['Mrs.', 'Mr.', 'Ms.', 'Miss','Sr.','Sra.', 'Señor']              

for file in files:
    # Skip files with '_clean' in the name
    if '_clean' in file:
        continue

    df = pd.read_csv(file, encoding='ISO-8859-1', low_memory=False)
    df = df.replace([''], np.nan)

    # Add new columns and initialize them with current values
    df.insert(0, 'Etitle', df['CnBio_Title_1'])
    df.insert(1, 'ESptitle', df['CnSpSpBio_Title_1'])
    df.insert(2, 'EMrtst', df['CnBio_Marital_status'])

    # Make a copy to compare original and modified values
    original_df = df.copy()

 # Define a function to remove data based on conditions
    def remove_data_based_on_condition1(row):
        # Check if 'CnBio_First_Name' is equal to 'CnSpSpBio_First_Name' and remove data if True
        if row['CnBio_First_Name'] == row['CnSpSpBio_First_Name']:
            row['CnSpSpBio_Gender'] = None
            row['CnSpSpBio_Title_1'] = None
            row['CnSpSpBio_First_Name'] = None
            row['CnSpSpBio_Last_Name'] = None
            row['CnBio_Marital_status'] = 'WidSinDiv_0'

        return row

    # Apply the function to your DataFrame
    df = df.apply(remove_data_based_on_condition1, axis=1)

    # Define a function to remove data based on conditions
    def remove_data_based_on_condition2(row):
        # Check if 'CnSpSpBio_Inactive' or 'CnSpSpBio_Deceased' is 'Yes' and remove data if True
        if row['CnSpSpBio_Inactive'] == 'Yes' or row['CnSpSpBio_Deceased'] == 'Yes' or row['CnBio_Marital_status'] == 'Widowed' or row['CnBio_Marital_status'] == 'Divorced|Annulled':
            row['CnSpSpBio_Gender'] = None
            row['CnSpSpBio_Title_1'] = None
            row['CnSpSpBio_First_Name'] = None
            row['CnSpSpBio_Last_Name'] = None
            row['CnBio_Marital_status'] = 'WidSinDiv_0'

        return row

    # Apply the function to your DataFrame
    df = df.apply(remove_data_based_on_condition2, axis=1)
  
    def swap_rows_based_on_gender(row):
        if row['CnBio_Gender'] == 'Female' and row['CnSpSpBio_Gender'] == 'Male':
            temp_gender = row['CnBio_Gender']
            temp_first_name = row['CnBio_First_Name']
            temp_last_name = row['CnBio_Last_Name']
            temp_title = row['CnBio_Title_1']

            row['CnBio_Gender'] = row['CnSpSpBio_Gender']
            row['CnBio_First_Name'] = row['CnSpSpBio_First_Name']
            row['CnBio_Last_Name'] = row['CnSpSpBio_Last_Name']
            row['CnBio_Title_1'] = row['CnSpSpBio_Title_1']

            row['CnSpSpBio_Gender'] = temp_gender
            row['CnSpSpBio_First_Name'] = temp_first_name
            row['CnSpSpBio_Last_Name'] = temp_last_name
            row['CnSpSpBio_Title_1'] = temp_title
        return row

    df = df.apply(swap_rows_based_on_gender, axis=1)

    # This function update Ms and Miss to mrs if the last names are the same and marital status is married 2016-8067
    def update_titles_if_married(row):
        if (row['CnBio_Last_Name'] == row['CnSpSpBio_Last_Name']) and (row['CnBio_Marital_status'] == 'Married|Partner' or row['CnSpSpBio_Marital_status'] == 'Married|Partner') and (row['CnBio_Title_1'] != 'Mr.') and (row['CnSpSpBio_Title_1'] == 'Miss' 
           or row['CnSpSpBio_Title_1'] == 'Ms.' or row['CnBio_Title_1'] == 'Miss' or row['CnBio_Title_1'] == 'Ms.'):
            row['CnSpSpBio_Title_1'] = 'Mrs.'
            row['CnBio_Title_1'] = 'Mrs.'
        return row
    df = df.apply(update_titles_if_married, axis=1)

    # This function update blanks titles to mr if gender is male or sptitle is mrs, ms, or miss
    def update_titles_if_blank_mr(row):
        if ((pd.isnull(row['CnBio_Title_1']) and pd.notnull(row['CnBio_Last_Name']) and (row['CnBio_Gender'] == 'Male') and (row['CnSpSpBio_Title_1'] == 'Mrs.' or row['CnSpSpBio_Title_1'] == 'Ms.' or row['CnSpSpBio_Title_1'] == 'Miss'))):
            row['CnBio_Title_1'] = 'Mr.'
        return row
    df = df.apply(update_titles_if_blank_mr, axis=1)

    # This function updates blank titles to ms if gender is female or sptitle Mr.
    def update_titles_if_blank_ms(row):
        if ((pd.isnull(row['CnBio_Title_1']) and pd.notnull(row['CnBio_Last_Name']) and (row['CnBio_Gender'] == 'Female') and (row['CnSpSpBio_Title_1'] == 'Mr.'))):
            row['CnBio_Title_1'] = 'Ms.'
        return row
    df = df.apply(update_titles_if_blank_ms, axis=1)

    # This function updates blank sptitles to mr if gender is male or title is mrs, ms, or miss
    def update_sptitles_if_blank_mr(row):
        if ((pd.isnull(row['CnSpSpBio_Title_1']) and pd.notnull(row['CnSpSpBio_Last_Name']) and (row['CnSpSpBio_Gender'] == 'Male') and (row['CnBio_Title_1'] == 'Mrs.' or row['CnBio_Title_1'] == 'Ms.' or row['CnBio_Title_1'] == 'Miss'))):
            row['CnSpSpBio_Title_1'] = 'Mr.'
        return row
    df = df.apply(update_sptitles_if_blank_mr, axis=1)

    # This function updates blanks sptitles to ms if gender is female or title is mr
    def update_sptitles_if_blank_ms(row):
        if ((pd.isnull(row['CnSpSpBio_Title_1']) and pd.notnull(row['CnSpSpBio_Last_Name']) and (row['CnSpSpBio_Gender'] == 'Female') and (row['CnBio_Title_1'] == 'Mr.'))):
            row['CnSpSpBio_Title_1'] = 'Ms.'
        return row
    df = df.apply(update_sptitles_if_blank_ms, axis=1)
    
    #If marital status is blank and Last names are  equal, fill in with married. They might be brother and sister, but Add/sal will be mostly the same. 
    def update_marital_status_if_blank_married(row):
        if (((pd.isnull(row['CnBio_Marital_status']) or (row['CnBio_Marital_status'] == 'Single')) and (row['CnSpSpBio_Last_Name'] == row['CnBio_Last_Name'])) ):
            row['CnBio_Marital_status'] = 'Married'
        return row
    df = df.apply(update_marital_status_if_blank_married, axis=1)

    # Update the new columns only where changes have occurred
    df['Etitle'] = np.where(df['CnBio_Title_1'] != original_df['CnBio_Title_1'], original_df['CnBio_Title_1'], df['Etitle'])
    df['ESptitle'] = np.where(df['CnSpSpBio_Title_1'] != original_df['CnSpSpBio_Title_1'], original_df['CnSpSpBio_Title_1'], df['ESptitle'])
    df['EMrtst'] = np.where(df['CnBio_Marital_status'] != original_df['CnBio_Marital_status'], original_df['CnBio_Marital_status'], df['EMrtst'])

            # Split the file name and extension
    base, ext = os.path.splitext(file)

    # Insert '_clean' before the extension
    new_file = base + '_clean' + ext
    # Save the DataFrame to the new file name in the current working directory
    df.to_csv(f'{new_file}', index=False, encoding='ISO-8859-1')
