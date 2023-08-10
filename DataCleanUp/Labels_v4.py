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
                  'Maj.', 'Most Reverend', 'Bishop Emeritus','Mrs.', 'Mr.', 'Ms.', 'Miss','Sr.', 'Family of']

# List of  special  titles
specialTitle = ['Dr.', 'The Honorable', 'Col.', 'Cmsgt. Ret.', 'Rev. Mr.', 'Deacon', 'Judge', 
                 'Lt. Col.', 'Col. Ret.', 'Major', 'Capt.', 'Maj. Gen.', 'Family of', 'Senator', 'Reverend', 
                 'Lt.', 'Cmdr.', 'Msgt.', 'Sister', 'Drs.', 'Master', 'Sgt. Maj.', 'SMSgt.', 'Prof.', 'Lt. Col. Ret.', 'Rev. Dr.', 
                 'Father', 'Brother', 'Bishop', 'Gen.', 'Admiral', 'Very Reverend', 'MMC', 'Monsignor', '1st Lt.', 'Reverend Monsignor', 
                  'Maj.', 'Most Reverend', 'Bishop Emeritus','Family of']

# List of common titles
commonTitles = ['Mrs.', 'Mr.', 'Ms.', 'Miss','Sr.']              

# Loop through all files in directory
for file in files:
    df = pd.read_csv(file, encoding='latin-1', low_memory=False)
    # Replaces all spaces with nan
    df = df.replace([''], np.nan)

    # drops row if address is blank
    # df = df.dropna(subset=['CnAdrPrf_Addrline1'])
    # drop row if all name information are blank - estates and orgs
    # df = df.dropna(subset=['CnBio_First_Name', 'CnBio_Last_Name', 'CnSpSpBio_First_Name', 'CnSpSpBio_Last_Name'], how='all')
    # drops duplicate ConsID
    df = df.drop_duplicates(subset=['CnBio_ID'])

    
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
        if (row['CnBio_Last_Name'] == row['CnSpSpBio_Last_Name']) and (row['CnBio_Marital_status'] == 'Married' or row['CnSpSpBio_Marital_status'] == 'Married') and (row['CnBio_Title_1'] != 'Mr.') and (row['CnSpSpBio_Title_1'] == 'Miss' 
           or row['CnSpSpBio_Title_1'] == 'Ms.' or row['CnBio_Title_1'] == 'Miss' or row['CnBio_Title_1'] == 'Ms.'):
            row['CnSpSpBio_Title_1'] = 'Mrs.'
            row['CnBio_Title_1'] = 'Mrs.'
        return row
    df = df.apply(update_titles_if_married, axis=1)

    # This function update blanks titles to mr if gender is male or sptitle is mrs, ms, or miss
    def update_titles_if_blank_mr(row):
        if (pd.isnull(row['CnBio_Title_1']) and pd.notnull(row['CnBio_Last_Name']) and (row['CnBio_Gender'] == 'Male' or row['CnSpSpBio_Title_1'] == 'Mrs.' or row['CnSpSpBio_Title_1'] == 'Ms.' or row['CnSpSpBio_Title_1'] == 'Miss')):
            row['CnBio_Title_1'] = 'Mr.'
        return row
    df = df.apply(update_titles_if_blank_mr, axis=1)

    # This function updates blank titles to ms if gender is female or sptitle Mr.
    def update_titles_if_blank_ms(row):
        if (pd.isnull(row['CnBio_Title_1']) and pd.notnull(row['CnBio_Last_Name']) and (row['CnBio_Gender'] == 'Female' or row['CnSpSpBio_Title_1'] == 'Mr.')):
            row['CnBio_Title_1'] = 'Ms.'
        return row
    df = df.apply(update_titles_if_blank_ms, axis=1)

    # This function updates blank sptitles to mr if gender is male or title is mrs, ms, or miss
    def update_sptitles_if_blank_mr(row):
        if (pd.isnull(row['CnSpSpBio_Title_1']) and pd.notnull(row['CnSpSpBio_Last_Name']) and (row['CnSpSpBio_Gender'] == 'Male' or row['CnBio_Title_1'] == 'Mrs.' or row['CnBio_Title_1'] == 'Ms.' or row['CnBio_Title_1'] == 'Miss')):
            row['CnSpSpBio_Title_1'] = 'Mr.'
        return row
    df = df.apply(update_sptitles_if_blank_mr, axis=1)

    # This function updates blanks sptitles to ms if gender is female or title is mr
    def update_sptitles_if_blank_ms(row):
        if (pd.isnull(row['CnSpSpBio_Title_1']) and pd.notnull(row['CnSpSpBio_Last_Name']) and (row['CnSpSpBio_Gender'] == 'Female' or row['CnBio_Title_1'] == 'Mr.')):
            row['CnSpSpBio_Title_1'] = 'Ms.'
        return row
    df = df.apply(update_sptitles_if_blank_ms, axis=1)
    
    #If marital status is blank and Last names are  equal, fill in with married. They might be brother and sister, but Add/sal will be mostly the same. 
    def update_marital_status_if_blank_married(row):
        if (((pd.isnull(row['CnBio_Marital_status']) or (row['CnBio_Marital_status'] == 'Single')) and (row['CnSpSpBio_Last_Name'] == row['CnBio_Last_Name'])) or ((row['CnSpSpBio_Last_Name'] != row['CnBio_Last_Name']) and pd.notnull(row['CnSpSpBio_Last_Name']) )):
            row['CnBio_Marital_status'] = 'Married'
        return row
    df = df.apply(update_marital_status_if_blank_married, axis=1)

    # updates marital status to Widowed if Deceased or Inactive = yes, but avoids changing divorced. it will also change instnaces where person is married to themselves (wrong status but avoids bad add/sal) 
    def update_marital_status_Widowed(row):
        if (((row['CnSpSpBio_Deceased'] == 'Yes') or (row['CnSpSpBio_Inactive'] == 'Yes')) or ((row['CnBio_Marital_status'] == 'Divorced')) or ((row['CnSpSpBio_First_Name'] == row['CnBio_First_Name'])) or (((row['CnBio_Marital_status'] == 'Single') 
        or (pd.isnull(row['CnBio_Marital_status']))) or (pd.isnull(row['CnSpSpBio_First_Name']))) ):
            row['CnBio_Marital_status'] = 'Widowed'
        return row
    df = df.apply(update_marital_status_Widowed, axis=1)

    # If last names are different
    def Different_Last_Name_1(row):
         if ( (row['CnBio_Last_Name'] != row['CnSpSpBio_Last_Name']) and (row['CnBio_Marital_status'] == 'Married') and (pd.notnull(row['CnSpSpBio_First_Name']) or pd.notnull(row['CnSpSpBio_Last_Name'])) ):
             row['CnBio_Marital_status'] = 'DifferentLastName_1'
         return row
    df = df.apply(Different_Last_Name_1, axis=1)
    
    # If last names are different but titles are the same and neither are special
    def Same_Last_Name_Same_Title_NonSpecial_2(row):
        global specialTitle # uses list of titles, global is used so that it can be accessed inside the functions
        if ((row['CnBio_Last_Name'] == row['CnSpSpBio_Last_Name']) and (row['CnBio_Title_1'] == row['CnSpSpBio_Title_1']) and (row['CnBio_Marital_status'] == 'Married') and (row['CnBio_Title_1'] not in specialTitle) ): # 
             row['CnBio_Marital_status'] = 'SameLastNameSameTitleNonSpecial_2'
        return row
    df = df.apply(Same_Last_Name_Same_Title_NonSpecial_2, axis=1)

    # If Last names are the same and the title is the same 
    def Same_Last_Name_Same_Title_Special_3(row):
        global specialTitle
        if ((row['CnBio_Last_Name'] == row['CnSpSpBio_Last_Name']) and (row['CnBio_Marital_status'] == 'Married') and (row['CnBio_Title_1'] == row['CnSpSpBio_Title_1']) and (row['CnBio_Title_1'] in specialTitle) ):
            row['CnBio_Marital_status'] = 'SameLastNameSameTitleSpecial_3'
        return row
    df = df.apply(Same_Last_Name_Same_Title_Special_3, axis=1)
    
    # If Last names are the same and both have a special title
    def Same_Last_Name_Both_Specical_Title_4(row):
        global specialTitle
        if ((row['CnBio_Last_Name'] == row['CnSpSpBio_Last_Name']) and (row['CnBio_Marital_status'] == 'Married') and (row['CnBio_Title_1'] in specialTitle and row['CnSpSpBio_Title_1'] in specialTitle) ):
            row['CnBio_Marital_status'] = 'SameLastNameBothSpecicalTitle_4'
        return row
    df = df.apply(Same_Last_Name_Both_Specical_Title_4, axis=1)
    
    # If Last names are the same only main has special title
    def Same_Last_Name_Main_Specical_Title_5(row):
        global specialTitle
        if ((row['CnBio_Last_Name'] == row['CnSpSpBio_Last_Name']) and (row['CnBio_Marital_status'] == 'Married') and (row['CnBio_Title_1'] in specialTitle) ):
            row['CnBio_Marital_status'] = 'SameLastNameMainSpecicalTitle_5'
        return row
    df = df.apply(Same_Last_Name_Main_Specical_Title_5, axis=1) 
    
    # If Last names are the same only spouse has special title
    def Same_Last_Name_Sp_Specical_Title_6(row): 
        global specialTitle
        if ((row['CnBio_Last_Name'] == row['CnSpSpBio_Last_Name']) and (row['CnBio_Marital_status'] == 'Married') and (row['CnSpSpBio_Title_1'] in specialTitle) ):
            row['CnBio_Marital_status'] = 'SameLastNameSpSpecicalTitle_6'
        return row
    df = df.apply(Same_Last_Name_Sp_Specical_Title_6, axis=1)

    # Standard Add/sal for married couple
    def Standard_Add_Sal_7(row): 
        global commonTitles
        if ((row['CnBio_Last_Name'] == row['CnSpSpBio_Last_Name']) and (row['CnBio_Marital_status'] != 'Widowed') and 
            (row['CnBio_Marital_status'] == 'Married') and ((row['CnBio_Title_1'] in commonTitles) or (row['CnSpSpBio_Title_1'] in commonTitles)  ) ):
            row['CnBio_Marital_status'] = 'StandardAddSal_7'
        return row
    df = df.apply(Standard_Add_Sal_7, axis=1) 
    
    def Standard_Add_Sal_MaleSp_8(row):
        global commonTitles
        if (row['CnBio_Last_Name'] == row['CnSpSpBio_Last_Name']
            and row['CnBio_Marital_status'] != 'Widowed'
            and row['CnBio_Marital_status'] == 'Married'
            and (row['CnBio_Title_1'] in commonTitles or row['CnSpSpBio_Title_1'] in commonTitles)
            and row['CnSpSpBio_Gender'] == 'Male'
        ):
            row['CnBio_Marital_status'] = 'StandardAddSal_MaleSp_8'
        return row

    df = df.apply(Standard_Add_Sal_MaleSp_8, axis=1)

    

    # fills First and last name with a blank space otherwise it would fill cell with 'nan'
    df['CnBio_First_Name'] = df['CnBio_First_Name'].loc[:].fillna('')
    df['CnBio_Last_Name'] = df['CnBio_Last_Name'].loc[:].fillna('')

    # Add/sal  
    def concate_add_sal(row):

        # Widowed
        # Mr. Bryce Howard 
        # Mr. Howard
        if (row['CnBio_Marital_status'] == 'Widowed' ): # and pd.notnull(row['CnBio_First_Name']) 
            addressee = str(row['CnBio_Title_1']) + ' ' + str(row['CnBio_First_Name']) + ' ' + str(row['CnBio_Last_Name'])
            salutation = str(row['CnBio_Title_1']) + ' ' + str(row['CnBio_Last_Name'])
     
        # Different_Last_Name_1
        # Mr. Bryce Howard and Mrs. Jennifer Ha 
        # Mr. Howard and Mrs. Ha
        elif (row['CnBio_Marital_status'] == 'DifferentLastName_1'):
            addressee = str(row['CnBio_Title_1']) + ' ' + str(row['CnBio_First_Name']) + ' ' + str(row['CnBio_Last_Name']) +' and ' + str(row['CnSpSpBio_Title_1']) + ' ' + str(row['CnSpSpBio_First_Name']) + ' ' +  str( row['CnSpSpBio_Last_Name'])
            salutation = str(row['CnBio_Title_1']) + ' ' + str(row['CnBio_Last_Name']) + ' and ' + str(row['CnSpSpBio_Title_1']) + ' ' + str(row['CnSpSpBio_Last_Name'])

        # Same_Last_Name_Same_Title_NonSpecial_2
        # Mr. Bryce Howard and Mr. Branden Howard
        # Mr Howard and Mr. Howard
        elif (row['CnBio_Marital_status'] == 'SameLastNameSameTitleNonSpecial_2'):
            addressee = str(row['CnBio_Title_1']) + ' ' + str(row['CnBio_First_Name']) + ' ' + str(row['CnBio_Last_Name']) +' and ' + str(row['CnSpSpBio_Title_1']) + ' ' + str(row['CnSpSpBio_First_Name']) + ' ' +  str( row['CnSpSpBio_Last_Name'])
            salutation = str(row['CnBio_Title_1']) + ' and ' + str(row['CnSpSpBio_Title_1']) + ' ' + str(row['CnBio_Last_Name'])

        # Gives: Same_Last_Name_Same_Title_Special_3
        # Dr. Bryce Howard and Dr. Jen Howard
        # Dr. Howard and Dr. Howard
        elif (row['CnBio_Marital_status'] == 'SameLastNameSameTitleSpecial_3'):
            addressee = str(row['CnBio_Title_1']) + ' ' + str(row['CnBio_First_Name']) + ' ' + str(row['CnBio_Last_Name']) + ' and ' + str(row['CnSpSpBio_Title_1']) + ' ' + str(row['CnSpSpBio_First_Name']) + ' ' +  str( row['CnSpSpBio_Last_Name'])
            salutation = str(row['CnBio_Title_1']) + ' ' + str(row['CnBio_Last_Name']) + ' and ' + str(row['CnSpSpBio_Title_1']) + ' ' + str(row['CnSpSpBio_Last_Name'])

        # Same_Last_Name_Both_Specical_Title_4 
        # Senator Bryce Howard and Dr. Jen Howard
        # Senator Howard and Dr. Howard
        elif (row['CnBio_Marital_status'] == 'SameLastNameBothSpecicalTitle_4'):
            addressee = str(row['CnBio_Title_1']) + ' ' + str(row['CnBio_First_Name']) + ' ' + str(row['CnBio_Last_Name']) + ' and ' + str(row['CnSpSpBio_Title_1']) + ' ' + str(row['CnSpSpBio_First_Name']) + ' ' +  str( row['CnSpSpBio_Last_Name'])
            salutation = str(row['CnBio_Title_1']) + ' ' + str(row['CnBio_Last_Name']) + ' and ' + str(row['CnSpSpBio_Title_1']) + ' ' + str(row['CnSpSpBio_Last_Name'])

        # Same_Last_Name_Main_Specical_Title_5 
        # Dr. Bryce Howard and Mrs. Howard
        # Dr. Howard and Mrs. Howard
        elif (row['CnBio_Marital_status'] == 'SameLastNameMainSpecicalTitle_5'):
            addressee = str(row['CnBio_Title_1']) + ' ' + str(row['CnBio_First_Name']) + ' ' + str(row['CnBio_Last_Name']) + ' and ' + str(row['CnSpSpBio_Title_1']) + ' ' +  str( row['CnSpSpBio_Last_Name'])
            salutation = str(row['CnBio_Title_1']) + ' ' + str(row['CnBio_Last_Name']) + ' and ' + str(row['CnSpSpBio_Title_1']) + ' ' + str(row['CnSpSpBio_Last_Name'])       
        
        # Same_Last_Name_Sp_Specical_Title_6 
        # Dr. Jennifer Howard and Mr. Bryce Howard
        # Dr. Howard and Mr. Howard
        elif (row['CnBio_Marital_status'] == 'SameLastNameSpSpecicalTitle_6'):
            addressee = str(row['CnSpSpBio_Title_1']) + ' ' + str(row['CnSpSpBio_First_Name']) + ' ' + str(row['CnSpSpBio_Last_Name']) + ' and ' + str(row['CnBio_Title_1']) + ' ' +  str( row['CnBio_Last_Name'])
            salutation = str(row['CnSpSpBio_Title_1']) + ' ' + str(row['CnSpSpBio_Last_Name']) + ' and ' + str(row['CnBio_Title_1']) + ' ' + str(row['CnBio_Last_Name'])      
        
        # Standard_Add_Sal_7
        # Mr. and Mrs. Bryce Howard
        # Mr. and Mrs. Howard
        elif (row['CnBio_Marital_status'] == 'StandardAddSal_7'):
            addressee = str(row['CnBio_Title_1']) + ' and ' + str(row['CnSpSpBio_Title_1']) + ' ' + str(row['CnBio_First_Name']) + ' ' + str(row['CnBio_Last_Name'])
            salutation = str(row['CnBio_Title_1']) + ' and ' + str(row['CnSpSpBio_Title_1']) + ' ' + str(row['CnBio_Last_Name'])

        elif (row['CnBio_Marital_status'] == 'Standard_Add_Sal_MaleSp_8'):
            addressee = str(row['CnSpSpBio_Title_1']) + ' and ' + str(row['CnBio_Title_1']) + ' ' + str(row['CnSpSpBio_First_Name']) + ' ' + str(row['CnSpSpBio_Last_Name'])
            salutation = str(row['CnSpSpBio_Title_1']) + ' and ' + str(row['CnBio_Title_1']) + ' ' + str(row['CnSpSpBio_Last_Name'])

        # This will make the add/sal blank, which will help find edge cases. Any add/sal that did not fit the criteria above, will come out blank.   
        else:
            addressee = ''
            salutation = ''
        return pd.Series({'CnAdrSal_Addressee': addressee, 'CnAdrSal_Salutation': salutation})
    
    # applies the function to the Add/sal field
    df[['CnAdrSal_Addressee', 'CnAdrSal_Salutation']] = df.apply(concate_add_sal, axis=1)


    # list of columns_to_drop I stopped droppping columns and decided to do that manually after this runs to better trouble shoot any issues.
    #columns_to_drop = ['CnAdrPrf_Type', 'CnAdrPrf_Sndmailtthisaddrss', 'CnSpSpBio_Anonymous', 'CnBio_Gender', 'CnSpSpBio_Gender', 
                       #'CnSpSpBio_Inactive', 'CnSpSpBio_Deceased',   'CnSpSpBio_Marital_status', 'CnBio_Marital_status']
    
#'CnBio_Inactive','CnSpSpBio_ID', 'CnBio_Deceased', 'CnBio_Anonymous', 'CnBio_Title_1', 'CnSpSpBio_Title_1', 'CnSpSpBio_First_Name', 'CnSpSpBio_Last_Name','CnBio_Org_Name',,'CnBio_Org_ID', 

    # drops columns in list
    #df = df.drop(columns=columns_to_drop)
    # Sort the DataFrame by 'CnBio_Last_Name' and 'CnBio_First_Name'
    
    # Split the file name and extension
    base, ext = os.path.splitext(file)

    # Insert '_clean' before the extension
    new_file = base + '_clean' + ext
    # Save the DataFrame to the new file name in the current working directory
    df.to_csv(f'{new_file}', index=False)
