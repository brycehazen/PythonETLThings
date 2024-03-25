import tkinter as tk # For GUI
from tkinter import filedialog # For GUI
from pathlib import Path
import pandas as pd 
import numpy as np
import re

failed_csv = 'Failed.csv'
dup_csv = 'duplicated.csv'
renew_csv = 'RE_Data.csv'
passed_csv = 'Passed.csv'
import_csv = 'ImportOmatic.csv'
rawdata_csv = 'RawParishData.csv'

def get_root() -> Path:
    return Path(__file__).resolve().parent


def process(csv_file: Path, out_dir: Path, re_dir: Path) -> None:
    
    data = pd.read_csv(csv_file, encoding='ISO-8859-1')
    
    data.drop(data.columns[[38]], axis=1)
    
    rawdata = pd.read_csv(csv_file, encoding='ISO-8859-1')
    if 'Notes' not in data.columns:
      data["Notes"] = " "
    # Strip leading/trailing spaces from 'ConsCode'
    data['ConsCode'] = data['ConsCode'].str.strip()
    
    def transform_cons_code(data):
        # Strip leading/trailing spaces from 'ConsCode'
        data['ConsCode'] = data['ConsCode'].str.strip()

        # Dictionary mapping of codes to their long format descriptions
        codes_to_descriptions = {
            '1-10': 'St. Hubert of the Forest Mission, Astor',
            '1-11': 'Blessed Sacrament Catholic Church, Clermont',
            '1-22': 'St. John the Baptist Catholic Church, Dunnellon',
            '1-27': 'St. Mary of the Lakes Catholic Church, Eustis',
            '1-30': 'Santo Toribio Romo Mission, Mascotte',
            '1-4': 'St. Theresa Catholic Church, Belleview',
            '1-40': 'St. Timothy Catholic Church, Lady Lake',
            '1-44': 'St. Paul Catholic Church, Leesburg',
            '1-5': 'St. Lawrence Catholic Church, Bushnell',
            '1-51': 'St. Patrick Catholic Church, Mount Dora',
            '1-53': 'St. Joseph of the Forest Mission, Silver Springs',
            '1-56': 'Our Lady of the Springs Catholic Church, Ocala',
            '1-57': 'Blessed Trinity Catholic Church, Ocala',
            '1-65': 'Christ the King Mission, Citra',
            '1-67': 'Queen of Peace Catholic Church, Ocala',
            '1-7': 'St. Jude Catholic Church, Ocala',
            '1-8': 'Immaculate Heart of Mary Catholic Church, Candler',
            '1-84': 'St. Mark the Evangelist Catholic Church, Summerfield',
            '1-85': 'Our Lady of Guadalupe Mission, Ocala',
            '1-89': 'St. Vincent de Paul Catholic Church, Wildwood',
            '1-92': 'San Pedro de Jesus Maldonado Mission, Wildwood',
            '2-1': 'St. Francis of Assisi Catholic Church, Apopka',
            '2-14': 'Corpus Christi Catholic Church, Celebration',
            '2-15': 'St. Maximillian Kolbe Catholic Church, Avalon Park',
            '2-16': 'St. Frances Xavier Cabrini, Orlando',
            '2-2': 'St. Catherine of Siena Catholic Church, Kissimmee',
            '2-29': 'Sts. Peter and Paul Catholic Church, Winter Park',
            '2-33': 'Holy Redeemer Catholic Church, Kissimmee',
            '2-39': 'Church of the Nativity, Longwood',
            '2-45': 'St. Philip Phan Van Minh Catholic Church, Orlando',
            '2-46': 'Annunciation Catholic Church, Longwood',
            '2-47': 'St. Mary Magdalen Catholic Church, Altamonte Springs',
            '2-58': 'St. Isaac Jogues Catholic Church, Orlando',
            '2-59': 'St. Andrew Catholic Church, Orlando',
            '2-6': 'Holy Family Catholic Church, Orlando',
            '2-60': 'Blessed Trinity Catholic Church, Orlando',
            '2-61': 'St. Charles Borromeo Catholic Church, Orlando',
            '2-62': 'Good Shepherd Catholic Church, Orlando',
            '2-63': 'St. James Cathedral, Orlando',
            '2-64': 'St. John Vianney Catholic Church, Orlando',
            '2-66': 'Mary Queen of the Universe Shrine, Orlando',
            '2-68': 'Holy Cross Catholic Church, Orlando',
            '2-78': 'St. Thomas Aquinas Catholic Church, St. Cloud',
            '2-79': 'All Souls Catholic Church, Sanford',
            '2-81': 'St. Ignatius Kim Mission, Orlando',
            '2-82': 'Most Precious Blood Catholic Church, Oviedo',
            '2-9': 'St. Augustine Catholic Church, Casselberry',
            '2-90': 'St. Stephen Catholic Church, Winter Springs',
            '2-91': 'St. Joseph Catholic Church, Orlando',
            '2-95': 'Resurrection Catholic Church, Winter Garden',
            '2-97': 'St. Margaret Mary Catholic Church, Winter Park',
            '3-13': 'St. Faustina Catholic Church, Clermont',
            '3-145': 'Centro Guadalupano Mission, Wahneta',
            '3-28': 'St. John Neumann Catholic Church, Lakeland',
            '3-3': 'St. Thomas Aquinas Catholic Church, Bartow',
            '3-32': 'St. Ann Catholic Church, Haines City',
            '3-34': 'St. Joseph Catholic Church, Lakeland',
            '3-35': 'Church of the Resurrection, Lakeland',
            '3-36': 'St. Anthony Catholic Church, Lakeland',
            '3-41': 'Holy Spirit Catholic Church, Lake Wales',
            '3-42': 'St. Leo the Great Mission, Lake Wales',
            '3-77': 'St. Rose of Lima Catholic Church, Poinciana',
            '3-94': 'St. Matthew Catholic Church, Winter Haven',
            '3-96': 'St. Joseph Catholic Church, Winter Haven',
            '3-98': 'St. Elizabeth Ann Seton Mission, Bartow',
            '4-12': 'Church of Our Saviour, Cocoa Beach',
            '4-26': 'Ascension Catholic Church, Melbourne',
            '4-48': 'Our Lady of Lourdes Catholic Church, Melbourne',
            '4-49': 'Divine Mercy Catholic Church, Merritt Island',
            '4-50': 'Holy Spirit Catholic Church, Mims',
            '4-52': 'Immaculate Conception Catholic Church, Melbourne Beach',
            '4-71': 'St. Joseph Catholic Church, Palm Bay',
            '4-73': 'Our Lady of Grace Catholic Church, Palm Bay',
            '4-75': 'St. Luke Catholic Church, Barefoot Bay',
            '4-76': 'St. Mary Catholic Church, Rockledge',
            '4-80': 'Holy Name of Jesus Catholic Church, Indialantic',
            '4-83': 'Blessed Sacrament Catholic Church, Cocoa',
            '4-87': 'St. John the Evangelist Catholic Church, Viera',
            '4-88': 'St. Teresa Catholic Church, Titusville',
            '5-17': 'Our Lady of Lourdes Catholic Church, Daytona Beach',
            '5-18': 'Basilica of St. Paul Catholic Church, Daytona Beach',
            '5-19': 'St. Ann Catholic Church, DeBary',
            '5-20': 'St. Peter Catholic Church, DeLand',
            '5-21': 'Our Lady of the Lakes Catholic Church, Deltona',
            '5-23': 'San Jose Mission, DeLand',
            '5-24': 'St. Clare Catholic Church, Deltona',
            '5-25': 'St. Gerard Mission, Edgewater',
            '5-54': 'Our Lady Star of the Sea Catholic Church, New Smyrna Beach',
            '5-55': 'Sacred Heart Catholic Church, New Smyrna Beach',
            '5-69': 'St. Brendan Catholic Church, Ormond Beach',
            '5-70': 'Prince of Peace Catholic Church, Ormond Beach',
            '5-72': 'Church of the Epiphany, Port Orange',
            '5-74': 'Our Lady of Hope Catholic Church, Port Orange'
        }

        # Replace ConsCode values based on the mapping
        for code, description in codes_to_descriptions.items():
            data.loc[data['ConsCode'].eq(code), 'ConsCode'] = description

        return data
    
    data = transform_cons_code(data)

    # change MrtlStat based off Gender
    # Create array to track failed cases.
    data['Test Case Failed']= ''
    data = data.replace(np.nan,'')
    data.insert(0, 'ID', range(0, len(data)))


    # Change blank Gender on title
    # AllRETitl1s = ['Dr.', 'The Honorable', 'Col.', 'Cmsgt. Ret.', 'Rev. Mr.', 'Deacon', 'Judge', 
    #             'Lt. Col.', 'Col. Ret.', 'Major', 'Capt.', 'Maj. Gen.', 'Family of', 'Senator', 'Reverend', 
    #             'Lt.', 'Cmdr.', 'Msgt.', 'Sister', 'Drs.', 'Master', 'Sgt. Maj.', 'SMSgt.', 'Prof.', 'Lt. Col. Ret.', 
    #             'Rev. Dr.', 'Father', 'Brother', 'Bishop', 'Gen.', 'Admiral', 'Very Reverend', 'MMC', 'Monsignor', '1st Lt.', 
    #             'Reverend Monsignor', 'Maj.', 'Most Reverend', 'Bishop Emeritus','Mrs.', 'Mr.', 'Ms.', 'Miss','Sr.', 'Family of']

    # strictly_male_titles = ['Rev. Mr.', 'Deacon', 'Father', 'Brother', 'Monsignor', 'Reverend Monsignor', 'Mr.']
    # strictly_female_titles = ['Mrs.', 'Miss', 'Sister', 'Ms.']

    def title_fixer(data):
        """
        Adjusts titles within a dataframe based on various conditions, including gender, marital status, and consistency in title presentation.
        It standardizes titles and updates them based on gender and marital status. Additionally, corrects known title discrepancies.

        Parameters:
        - data: DataFrame containing personal information, including titles, gender, and marital status.

        Returns:
        - DataFrame with updated and standardized titles.
        """

        # Dictionary for correcting common title variations to a standardized form
        title_corrections = {
            'Mr': 'Mr.', 'Mrs': 'Mrs.', 'Ms': 'Ms.', 'Dr': 'Dr.',
            'Rev.': 'Reverend', 'Very Rev.': 'Very Reverend', 'LTC': 'Lt. Col.', 'Cpt.': 'Capt.',
            'Mgen': 'Maj. Gen.', 'Lt Gen': 'Lt. Gen.', 'Maj Gen': 'Maj. Gen.', 'COL': 'Col.'
        }
        
        # Apply corrections to both primary and spouse titles
        data.replace({'Titl1': title_corrections, 'SRTitl1': title_corrections}, inplace=True)

        # Lists of titles strictly associated with a specific gender
        strictly_male_titles = ['Rev. Mr.', 'Deacon', 'Father', 'Brother', 'Monsignor', 'Reverend Monsignor', 'Mr.']
        strictly_female_titles = ['Mrs.', 'Miss', 'Sister', 'Ms.']

        # Update Gender, based on title if Gender is unknown or blank 
        data.loc[(data['Gender'] == '') | (data['Gender'] == 'Unknown'), 'Gender'] = data['Titl1'].map(dict.fromkeys(strictly_male_titles, 'Male')).fillna(data['Gender'])
        data.loc[(data['Gender'] == '') | (data['Gender'] == 'Unknown'), 'Gender'] = data['Titl1'].map(dict.fromkeys(strictly_female_titles, 'Female')).fillna(data['Gender'])

        # Repeat for the SRGender and SRTitl1 columns if needed
        data.loc[(data['SRGender'] == '') | (data['SRGender'] == 'Unknown'), 'SRGender'] = data['SRTitl1'].map(dict.fromkeys(strictly_male_titles, 'Male')).fillna(data['SRGender'])
        data.loc[(data['SRGender'] == '') | (data['SRGender'] == 'Unknown'), 'SRGender'] = data['SRTitl1'].map(dict.fromkeys(strictly_female_titles, 'Female')).fillna(data['SRGender'])

        # Update Title, based on gender if Title is blank but Gender is male or female
        data.loc[(data['Titl1'] == '') & (data['Gender'] == 'Male'), 'Titl1'] = data['Gender'].map({'Male': 'Mr.'})
        data.loc[(data['Titl1'] == '') & (data['Gender'] == 'Female'), 'Titl1'] = data['Gender'].map({'Female': 'Ms.'})

        # Repeat for the SRGender and SRTitl1 columns if needed
        data.loc[(data['SRTitl1'] == '') & (data['SRGender'] == 'Male'), 'SRTitl1'] = data['SRGender'].map({'Male': 'Mr.'})
        data.loc[(data['SRTitl1'] == '') & (data['SRGender'] == 'Female'), 'SRTitl1'] = data['SRGender'].map({'Female': 'Ms.'})
           
        # Change MrtlStat based off Gender or change to one used in RE
        data.loc[(data['MrtlStat'].isnull()) & (data['PrimAddText'].str.contains('&| and ', na=False)) & (data['LastName'] == data['SRLastName']),'MrtlStat'] = 'Married'
        data.loc[(data['MrtlStat'].str.contains('Religion|Civilly|Church Married|Church Marriage|Civil/Other|Marriage|Invalid Marriage|Valid Marriage|Head', na=False)),'MrtlStat'] = 'Married'
        data.loc[(data['MrtlStat'].str.contains('Never|Not Married|Cohabitating|Co-Habitating|Partner|Together', na=False)),'MrtlStat', ] = 'Single'
        data.loc[(data['MrtlStat'].str.contains('Deceased|Widow/Er|Widow', na=False)),'MrtlStat'] = 'Widowed'
        data.loc[(data['MrtlStat'].str.contains('Separated', na=False)),'MrtlStat'] = 'Divorced'

        # Function to update titles based on marital status and last name comparison
        def update_titles_if_married(row):
            """
            Updates the titles to 'Mrs.' for individuals and their spouses if they are married and share the last name,
            provided their current titles are 'Miss' or 'Ms.'.
            
            Parameters:
            - row: A single row from the DataFrame being processed.
            
            Returns:
            - The row with potentially updated titles.
            """
           # Check if the last names match and 'Married'
            if (row['LastName'] == row['SRLastName']) and (row['MrtlStat'] == 'Married') and row['Titl1'] == 'Mr.' and (row['SRTitl1'] == 'Miss'  
            or row['SRTitl1'] == 'Ms.'):
                row['SRTitl1'] = 'Mrs.'
            return row
    
        # Apply the marital status-based title update function across all rows
        data = data.apply(update_titles_if_married, axis=1)

        return data
        
    data = title_fixer(data)


    # Testcase 1 - Both genders are Male but addressee or salutation contains Ms. or Mrs.
    def check_gender_and_salutation(row):
        if (row['Gender'] == 'Male') and (row['SRGender'] == 'Male') and \
          (('Ms' in row['PrimAddText']) or ('Mrs' in row['PrimAddText']) or
            ('Ms' in row['PrimSalText']) or ('Mrs' in row['PrimSalText'])):
            return row['Test Case Failed'] + ', 1'
        else:
            return row['Test Case Failed']

    data['Test Case Failed'] = data.apply(check_gender_and_salutation, axis=1)

    #	Testcase 2 - Both genders are female but addressee or salutation contains Mr. 
    def check_mr(row):
        if (row['Gender'] == 'Female') and (row['SRGender'] == 'Female') and \
          (('Mr.' in row['PrimAddText']) or ('Mr.' in row['PrimSalText'])):
            return row['Test Case Failed'] + ', 2'
        else:
            return row['Test Case Failed']

    data['Test Case Failed'] = data.apply(check_mr, axis=1)

    # Testcase 3 - First name on the record is the same for the spouse.
    def check_first_name(row):
        if row['FirstName'] != '' and row['SRFirstName'] != '' and row['FirstName'] == row['SRFirstName']:
            return row['Test Case Failed'] + ', 3'
        else:
            return row['Test Case Failed']

    data['Test Case Failed'] = data.apply(check_first_name, axis=1)

    # Testcase 4 - Addressee or salutation does not contain the last name of the record
    # Skip test if IsInactive = Yes or SRInactive = Yes
    def check_lastname_in_primadd_sal(row):
        if ((row['IsInactive'] != 'Yes') or (row['SRInactive'] != 'Yes')) and (row['LastName'] not in row['PrimAddText']) and \
          (row['LastName'] not in row['PrimSalText']):
            return row['Test Case Failed'] + ', 4'
        else:
            return row['Test Case Failed']

    data['Test Case Failed'] = data.apply(check_lastname_in_primadd_sal, axis=1)

    # Testcase 5 - Record has Name information, the Spouse has name information, no one is marked deceased,
    def check_addressee_salutation(row):
        if (row['FirstName'] != '') and (row['LastName'] != '') and \
          (row['SRFirstName'] != '') and (row['SRLastName'] != '') and \
          ('Yes' not in row['SRDeceased']) and ('Yes' not in row['Deceased']) and \
          ('Yes' not in row['SRInactive']) and (row['IsInactive'] != 'Yes') and \
          ('&' not in row['PrimAddText']) and ('&' not in row['PrimSalText']) and \
          ('AND' not in row['PrimAddText'].upper()) and ('AND' not in row['PrimSalText'].upper()):
            return row['Test Case Failed'] + ', 5'
        else:
            return row['Test Case Failed']

    data['Test Case Failed'] = data.apply(check_addressee_salutation, axis=1)

    # Testcase 6 - Head of household is not above the age of 18.
    def check_head_of_household_age(row):
        if row['BDay'] >= pd.Timestamp('2004-01-01'):
            return row['Test Case Failed'] + ', 6'
        else:
            return row['Test Case Failed']

    data['BDay'] = pd.to_datetime(data['BDay'], errors="coerce")
    data['Test Case Failed'] = data.apply(check_head_of_household_age, axis=1)

    # Testcase 7 - Addressee or salutation contains "&" or "and" but it shows the Spouse as deceased
    # If SRinactive and inactive is yes skip this test

    def check_addressee_and_spouse_deceased(row):
        if ('Yes' in row['SRDeceased']) and ('Yes' not in row['SRInactive']) and (row['IsInactive'] != 'Yes') and (any(substring in row['PrimAddText'] for substring in [' AND ', '&', ' and ', ' And '])) and (any(substring in row['PrimSalText'] for substring in [' AND ', '&', ' and ', ' And '])):
            return row['Test Case Failed'] + ', 7'
        else:
            return row['Test Case Failed']

    data['Test Case Failed'] = data.apply(check_addressee_and_spouse_deceased, axis=1)

    # Testcase 8 - Addressee or salutation contains & or AND, but spouse's last or first name is empty.
    def check_and_in_addressee_salutation(row):
        if (row['SRLastName'] == '') and (row['SRFirstName'] == '') and \
          ((" AND " in row['PrimAddText']) or ("&" in row['PrimAddText']) or (" and " in row['PrimAddText']) or (" And " in row['PrimAddText']) or \
            (" AND " in row['PrimSalText']) or ("&" in row['PrimSalText']) or (" and " in row['PrimSalText']) or (" And " in row['PrimSalText'])):
            return row['Test Case Failed'] + ', 8'
        else:
            return row['Test Case Failed']

    data['Test Case Failed'] = data.apply(check_and_in_addressee_salutation, axis=1)

    # Testcase 9 -SRDeceasedDate is not empty, MrtlStat is not one of, and IsInactive is not 'Yes'
    def check_deceased_and_status(row):
        if (row['SRDeceasedDate'] != '') and (row['MrtlStat'] not in ['Widowed', 'Widower', 'Widow']) and (row['IsInactive'] != 'Yes'):
            return row['Test Case Failed'] + ', 9'  # Replace X with the appropriate Testcase number
        else:
            return row['Test Case Failed']

    data['Test Case Failed'] = data.apply(check_deceased_and_status, axis=1)

    # # Total cases
    # failed = data[(data['Test Case Failed'] != '')]
    # passed = data[(data['Test Case Failed'] == '') | (data['Notes']=='Passed')]
    # failed.loc[:, 'Test Case Failed'] = failed['Test Case Failed'].str[1:]
    # failed = failed[(failed['Test Case Failed'] != '')]
    # Total cases
    # Testcase 10 - Spouse shows a deceased date, but inactive does not show yes.
    def check_spouse_deceased_and_inactive(row):
        if (row['SRDeceasedDate'] != '') and (row['SRInactive'] != 'Yes'):
            return row['Test Case Failed'] + ', 10'
        else:
            return row['Test Case Failed']

    data['Test Case Failed'] = data.apply(check_spouse_deceased_and_inactive, axis=1)

    # Testcase 11 - Record shows a deceased date, but inactive does not show yes. 
    # Does not equal to yes will pick up Blank and no.
    def check_record_deceased_and_inactive(row):
        if (row['DeceasedDate'] != '') and (row['Inactive'] != 'Yes'):
            return row['Test Case Failed'] + ', 11'
        else:
            return row['Test Case Failed']

    data['Test Case Failed'] = data.apply(check_record_deceased_and_inactive, axis=1)

    # Testcase 12 - There is a deceased date but addressee or salutation contains "&" or "and"
    # If Srinactive and inactive is yes skip this test
    def check_deceased_date_and_addressee(row):
        if (row['SRDeceasedDate'] != '') and ('Yes' not in row['SRInactive']) and (any(substring in row['PrimAddText'] for substring in ['AND', '&', 'and', 'And'])) and (any(substring in row['PrimSalText'] for substring in ['AND', '&', 'and', 'And'])):
            return row['Test Case Failed'] + ', 12'
        else:
            return row['Test Case Failed']

    data['Test Case Failed'] = data.apply(check_deceased_date_and_addressee, axis=1)


    # Testcase 13 - Spouse name information is filled in but marital status shows single.
    def check_spouse_info_and_single(row):
        if (row['SRLastName'] or row['SRFirstName']) and (row['MrtlStat'] == 'single'):
            return row['Test Case Failed'] + ', 13'
        else:
            return row['Test Case Failed']

    data['Test Case Failed'] = data.apply(check_spouse_info_and_single, axis=1)

    # Testcase 14 - Marital status is blank but Addressee or salutation has "&" or "and". 
    # If there is Spouse name information they should be marked as "Partner" 
    # if they are not married but living together.
    def check_marital_status_and_addressee(row):
        if (not row['MrtlStat']) and (any(substring in row['PrimAddText'] for substring in ['AND', '&', 'and', 'And'])) and (any(substring in row['PrimSalText'] for substring in ['AND', '&', 'and', 'And'])):
            return row['Test Case Failed'] + ', 14'
        else:
            return row['Test Case Failed']

    data['Test Case Failed'] = data.apply(check_marital_status_and_addressee, axis=1)

    # Test case 15 - Marital status does not reflect what is in the addressee/salutation 
    # i.e. widowed, but two people are in the add/sal, married but only one person is in add/sal
    # i.e Single will pass if LastName and SRLastNAme are not equal
    def check_marital_status_and_addsal(row):
        # If the marital status is single and the last names are different, pass the test.
        if row['MrtlStat'] == 'Single' and row['LastName'] != row['SRLastName']:
            return row['Test Case Failed']

        # If marital status is widowed, divorced, or single and there are indications of multiple people in add/sal,
        # fail the test unless the account is marked as inactive.
        if ("Widow" in row['MrtlStat'] or "Divorced" in row['MrtlStat'] or "Unknown" in row['MrtlStat'] or "Single" in row['MrtlStat']) and \
                ((any(substring in row['PrimAddText'] for substring in [' AND ', '&', ' and ', ' And ']) or \
                any(substring in row['PrimSalText'] for substring in [' AND ', '&', ' and ', ' And '])) and \
                not any(row[val] == 'Yes' for val in ['IsInactive', 'Inactive', 'SRInactive'])):
            return row['Test Case Failed'] + ', 15'

        return row['Test Case Failed']
    data['Test Case Failed'] = data.apply(check_marital_status_and_addsal, axis=1)
    
    # Test case 16 - Standardize Titles - Titles must be within the table and Gender and Title both cannot be blank
    # AllRETitl1s = ['Dr.', 'The Honorable', 'Col.', 'Cmsgt. Ret.', 'Rev. Mr.', 'Deacon', 'Judge', 
    #             'Lt. Col.', 'Col. Ret.', 'Major', 'Capt.', 'Maj. Gen.', 'Family of', 'Senator', 'Reverend', 
    #             'Lt.', 'Cmdr.', 'Msgt.', 'Sister', 'Drs.', 'Master', 'Sgt. Maj.', 'SMSgt.', 'Prof.', 'Lt. Col. Ret.', 'Rev. Dr.', 
    #             'Father', 'Brother', 'Bishop', 'Gen.', 'Admiral', 'Very Reverend', 'MMC', 'Monsignor', '1st Lt.', 'Reverend Monsignor', 
    #             'Maj.', 'Most Reverend', 'Bishop Emeritus','Mrs.', 'Mr.', 'Ms.', 'Miss','Sr.', 'Family of']

    # def check_Titl1(row):
    #     # Fail when Both SRGender and SRTitl1 are Blank, but if SRLastName is not blank.
    #     if not row['SRGender'] and not row['SRTitl1'] and row['SRLastName']:
    #         return row['Test Case Failed'] + ', 16'
    #     # Fail if Both Gender and Titl1 are Blank.
    #     elif not row['Gender'] and not row['Titl1']:
    #         return row['Test Case Failed'] + ', 16'
    #     # Fail if Titl1 or SRTitl1 are not blank and what they contain is not found in AllRETitl1s.
    #     elif (row['Titl1'] and row['Titl1'] not in AllRETitl1s) or (row['SRTitl1'] and row['SRTitl1'] not in AllRETitl1s):
    #         return row['Test Case Failed'] + ', 16'
    #     else:
    #         return row['Test Case Failed']

    # data['Test Case Failed'] = data.apply(check_Titl1, axis=1)

    if 'NameIsCorrect' in data.columns:
        failed = data[(data['Test Case Failed'] != '') & (data['NameIsCorrect'] != 'Yes')].copy()
        passed = data[(data['Test Case Failed'] == '') | (data['NameIsCorrect'] == 'Yes')].copy()
    else:
        failed = data[data['Test Case Failed'] != ''].copy()
        passed = data[data['Test Case Failed'] == ''].copy()
        
    failed.loc[:, 'Test Case Failed'] = failed['Test Case Failed'].str[1:]
    failed = failed[(failed['Test Case Failed'] != '')]

    # Clean up
    del failed["ID"]
    del passed["ID"]

    # Print results 
    failed['Test Case Failed'].value_counts()
    print("There was a total of",data.shape[0], "rows.", "There were" ,data.shape[0] - failed.shape[0], "rows passed and" ,failed.shape[0], "rows failed at least one test case")

    # remove duplicates
    duplicated = data[data.groupby('ConsID')['ConsID'].transform('size') > 1]
    duplicated = duplicated.drop(columns = ['ID',])
    passed = passed.drop_duplicates(subset=['ConsID'])

    # Dataframe that are new containing *
    new = passed[passed['ConsID'].str.contains ("*", regex = False)]

    # # Drop Columns for importOmatic file 
    # impomatic = new.drop(columns = ['KeyInd', 'ConsCodeImpID', 'Nickname', 'Deceased', 
    # 'DeceasedDate', 'Inactive', 'SRSuff2', 'SRNickname', 'SRDeceased', 'SRDeceasedDate','SRInactive', 
    # 'PrimAddText', 'PrimSalText', 'AddrImpID', 'AddrType', 'AddrRegion', 'AddrSeasonal', 'AddrSeasFrom', 
    # 'AddrSeasTo', 'PhoneAddrImpID','PhoneImpID', 'PhoneType','DateTo', 'NameChanged', 'StreetChanged', 
    # 'MailingChanged', 'AltChanged', 'Test Case Failed', 'Notes']) #, 'AddrImpID.1', 'PhoneAddrImpID.1', 'PhoneImpID.1'])
    columns_to_drop = ['KeyInd', 'ConsCodeImpID', 'Nickname', 'Deceased', 'DeceasedDate', 'Inactive', 'SRSuff2', 'SRNickname', 'SRDeceased', 'SRDeceasedDate','SRInactive', 'PrimAddText', 'PrimSalText', 'AddrImpID', 'AddrType', 'AddrRegion', 'AddrSeasonal', 'AddrSeasFrom', 'AddrSeasTo', 'PhoneAddrImpID','PhoneImpID', 'PhoneType','DateTo', 'NameChanged', 'StreetChanged', 'MailingChanged', 'AltChanged', 'Test Case Failed', 'Notes']
    # Only drop columns that are present in the DataFrame
    columns_to_drop = [col for col in columns_to_drop if col in new.columns]
    impomatic = new.drop(columns=columns_to_drop)
    # Creates spouse column and fills in with Yes if 
    impomatic.insert(loc = 15, column='Spouse', value = '')
    impomatic.loc[(impomatic['SRLastName'] != ''),'Spouse'] = 'Yes'
    
    # creates country column anbd fills in
    impomatic.insert(loc = 17, column='Country', value = '')
    impomatic.loc[(impomatic['AddrCity'] != '') &  impomatic['AddrState'] != '', 'Country'] = 'United States'

    columns_to_drop_redata = ['ImportID', 'ConsCodeImpID', 'Suff1', 'SRSuff2', 'SRInactive', 
                    'AddrRegion', 'AddrImpID', 'AddrImpID', 'PhoneAddrImpID', 
                    'PhoneImpID', 'PhoneAddrImpID', 'PhoneImpID', 'DateTo', 
                    'SecondID', 'Test Case Failed', 'PrimAddText', 'PrimSalText',
                    'NameChanged', 'StreetChanged', 'MailingChanged', 
                    'AltChanged', 'Notes']

    columns_exist = [col for col in columns_to_drop_redata if col in passed.columns]

    if columns_exist:
        redata = passed.drop(columns=columns_exist)
    else:
        redata = passed

    # If ConsID contains *, remove the row - These are new records that are used for importOmatic
    redata = redata[~redata['ConsID'].str.contains("*", regex = False)].reset_index(drop=True)

    # Change Column Spelling to fit Raiser's Edge Import
    redata.rename(columns = {'DeceasedDate':'DecDate', 'SRDeceasedDate':'SRDecDate'}, inplace = True)

    # Change the absolute mess of Titl1 1 being used to fit Raiser's Edge
    redata.loc[redata['Titl1'].eq('MM') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('A') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('B') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('C') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('D') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('E') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('F') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('G') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('H') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('I') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('J') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('J.') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('K') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('L') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('L.') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('M') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('M.') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('N') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('O') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('P') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('Q') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('R') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('S') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('T') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('U') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('V') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('W') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('X') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('Y') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('Z') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('Me') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('Mt') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('Mtr') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('Mtr.') , 'Titl1'] = ''
    redata.loc[redata['Titl1'].eq('Maj') , 'Titl1'] = 'Maj.'
    redata.loc[redata['Titl1'].eq('Maj Gen') , 'Titl1'] = 'Maj. Gen.'
    redata.loc[redata['Titl1'].eq('Mgen') , 'Titl1'] = 'Maj. Gen.'
    redata.loc[redata['Titl1'].eq('Cmdr') , 'Titl1'] = 'Cmdr.'
    redata.loc[redata['Titl1'].eq('Br.') , 'Titl1'] = 'Brother'
    redata.loc[redata['Titl1'].eq('Dn') , 'Titl1'] = 'Deacon'
    redata.loc[redata['Titl1'].eq('Mr'), 'Titl1'] = 'Mr.'
    redata.loc[redata['Titl1'].eq('MR'), 'Titl1'] = 'Mr.'
    redata.loc[redata['Titl1'].eq('Mrs'), 'Titl1'] = 'Mrs.'
    redata.loc[redata['Titl1'].eq('Ms'), 'Titl1'] = 'Miss'
    redata.loc[redata['Titl1'].eq('Rev'), 'Titl1'] = 'Rev.'
    redata.loc[redata['Titl1'].eq('SeÃ±or'), 'Titl1'] = 'Sr.'
    redata.loc[redata['Titl1'].eq('Sen.'), 'Titl1'] = 'Sr.'
    redata.loc[redata['Titl1'].eq('Senor'), 'Titl1'] = 'Sr.'
    redata.loc[redata['Titl1'].eq('Sr'), 'Titl1'] = 'Sr.'
    redata.loc[redata['Titl1'].eq('Sra'), 'Titl1'] = 'Sra.'
    redata.loc[redata['Titl1'].eq('Stra.'), 'Titl1'] = 'Sra.'
    redata.loc[(redata['Titl1'].str.contains('Mr &')),'Titl1'] = 'Mr.'
    redata.loc[(redata['Titl1'].str.contains('Mr. &')),'Titl1'] = 'Mr.'
    redata.loc[(redata['Titl1'].str.contains('Mr/')),'Titl1'] = 'Mr.'
    redata.loc[(redata['Titl1'].str.contains('Mrs')),'Titl1'] = 'Mrs.'
    redata.loc[(redata['Titl1'].str.contains('Mis')),'Titl1'] = 'Miss'
    redata.loc[(redata['Titl1'].str.contains('Ms.')),'Titl1'] = 'Miss'
    redata.loc[(redata['Titl1'].str.contains('Capt')),'Titl1'] = 'Capt.'
    redata.loc[(redata['Titl1'].str.contains('CAPT')),'Titl1'] = 'Capt.'
    redata.loc[(redata['Titl1'].str.contains('Cpt')),'Titl1'] = 'Capt.'
    redata.loc[(redata['Titl1'].str.contains('CPT')),'Titl1'] = 'Capt.'
    redata.loc[(redata['Titl1'].str.contains('Commander')),'Titl1'] = 'Cmdr.'
    redata.loc[(redata['Titl1'].str.contains('COL')),'Titl1'] = 'Col.'
    redata.loc[(redata['Titl1'].str.contains('Col')),'Titl1'] = 'Col.'
    redata.loc[(redata['Titl1'].str.contains('Colonel')),'Titl1'] = 'Col.'
    redata.loc[(redata['Titl1'].str.contains('Dcn')),'Titl1'] = 'Deacon'
    redata.loc[(redata['Titl1'].str.contains('DCN')),'Titl1'] = 'Deacon'
    redata.loc[(redata['Titl1'].str.contains('Dea')),'Titl1'] = 'Deacon'
    redata.loc[(redata['Titl1'].str.contains('Dr')),'Titl1'] = 'Dr.'
    redata.loc[(redata['Titl1'].str.contains('Rev.')),'Titl1'] = 'Rev.'
    redata.loc[(redata['Titl1'].str.contains('Rev. M')),'Titl1'] = 'Rev. Mr.'
    redata.loc[(redata['Titl1'].str.contains('Rev M')),'Titl1'] = 'Rev. Mr.'
    redata.loc[(redata['Titl1'].str.contains('Senor ')),'Titl1'] = 'Sr.'
    redata.loc[(redata['Titl1'].str.contains('Sr ')),'Titl1'] = 'Sr.'
    redata.loc[(redata['SRTitl1'].str.contains('')),'SRTitl1'] = ''
    redata.loc[(redata['SRTitl1'].str.contains('')),'SRTitl1'] = ''
    redata.loc[(redata['SRTitl1'].str.contains('')),'SRTitl1'] = ''
    redata.loc[(redata['SRTitl1'].str.contains('')),'SRTitl1'] = ''

    # Standardize Phone Type and remove these horrific phone types being used. 
    redata.loc[(redata['PhoneType'].str.contains('Her')),'PhoneType'] = 'Cell'
    redata.loc[(redata['PhoneType'].str.contains('His')),'PhoneType'] = 'Cell'
    redata.loc[(redata['PhoneType'].str.contains('Fathers')),'PhoneType'] = 'Cell'
    redata.loc[(redata['PhoneType'].str.contains('Father')),'PhoneType'] = 'Cell'
    redata.loc[(redata['PhoneType'].str.contains('Mother\'s')),'PhoneType'] = 'Cell'
    redata.loc[(redata['PhoneType'].str.contains('Mom')),'PhoneType'] = 'Cell'
    redata.loc[(redata['PhoneType'].str.contains('Dad\'s')),'PhoneType'] = 'Cell'
    redata.loc[(redata['PhoneType'].str.contains('Mobile')),'PhoneType'] = 'Cell'
    redata.loc[(redata['PhoneType'].str.contains('Unknown')),'PhoneType'] = 'Cell'
    redata.loc[(redata['PhoneType'].str.contains('Text-')),'PhoneType'] = 'Cell'
    redata.loc[(redata['PhoneType'].str.contains('Text')),'PhoneType'] = 'Cell'
    redata.loc[(redata['PhoneType'].str.contains('/')),'PhoneType'] = 'Cell'
    redata.loc[(redata['PhoneType'].str.contains('Ms.')),'PhoneType'] = 'Cell'
    redata.loc[(redata['PhoneType'].str.contains('Cel')),'PhoneType'] = 'Cell'
    redata.loc[(redata['PhoneType'].str.contains('Cell')),'PhoneType'] = 'Alternate Home'
    redata.loc[(redata['PhoneType'].str.contains('Grandmother')),'PhoneType'] = 'Cell'
    redata.loc[(redata['PhoneType'].str.contains('Home')),'PhoneType'] = 'Home'
    redata.loc[(redata['PhoneType'].str.contains('ICOE')),'PhoneType'] = 'Cell'
    redata.loc[(redata['PhoneType'].str.contains('wrk|Wrk|Work|work')),'PhoneType'] = 'Work'
    redata.loc[(redata['PhoneType'].str.contains('Alt|alt')),'PhoneType'] = 'Cell 2'

  # Change State column
    redata.loc[(redata['AddrState'].str.contains('Fl.')),'AddrState'] = 'FL'
    redata.loc[(redata['AddrCity'].str.contains(' Fl')),'AddrState'] = 'FL'
    redata.loc[(redata['AddrCity'].str.contains(' FL')),'AddrState'] = 'FL'
    redata.loc[(redata['AddrCity'].str.contains(', Fl')),'AddrState'] = 'FL'
    
     # Splits the 'AddrCity' column of redata into city and state parts, and fills NaN values in the 'AddrState' column with the extracted state.  
    def split_city_state(redata):

        # List of U.S. state abbreviations
        state_abbreviations = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
                "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

        # Convert state abbreviations to a regex pattern that matches them in a case-insensitive way
        state_pattern = '|'.join(state_abbreviations)
        pattern = rf'(?P<City>.*?)(?:,? (?P<State>{state_pattern}))?$'

        # Extract city and state from the AddrCity column, making sure the comparison is case-insensitive
        redata[['ExtractedCity', 'State_Holder']] = redata['AddrCity'].str.extract(pattern, flags=re.IGNORECASE)

        # Fill NaN values in the AddrState column with values from the State_Holder column, and keep original city names
        redata['AddrState'] = np.where(redata['AddrState'].isna(), redata['State_Holder'], redata['AddrState'])
        redata['AddrCity'] = np.where(redata['ExtractedCity'].notna(), redata['ExtractedCity'], redata['AddrCity'])

        # Drop the temporary columns
        redata.drop(columns=['ExtractedCity', 'State_Holder'], inplace=True)

        return redata
        
    redata = split_city_state(redata)

    # Clean addresses in redata
    def normalizeredata(redata):
        redata = redata.copy()
        replacements = {
          r'\bApartment\b': 'Apt',
          r'\bApt\.\b': 'Apt',
          r'\bAPT\b': 'Apt',
          r'\bnApt\b': 'Apt',
          r'\bNApt\b': 'Apt',
          r'\bAvenue\b': 'Ave',
          r'\bAve\.\b': 'Ave',
          r'\bBoulevard\b': 'Blvd',
          r'\bBlvd\.\b': 'Blvd',
          r'\bBuilding\b': 'Bldg',
          r'\bBldg\.\b': 'Bldg',
          r'\bCenter\b': 'Ctr',
          r'\bCtr\.\b': 'Ctr',
          r'\bCircle\b': 'Cir',
          r'\bCir\.\b': 'Cir',
          r'\bCourt\b': 'Ct',
          r'\bCt\.\b': 'Ct',
          r'\bDrive\b': 'Dr',
          r'\bDr\.\b': 'Dr',
          r'\bEast\b': 'E',
          r'\bE\.\b': 'E',
          r'\bExpressway\b': 'Expy',
          r'\bExpy\.\b': 'Expy',
          r'\bExtension\b': 'Ext',
          r'\bExt\.\b': 'Ext',
          r'\bFort\b': 'Ft',
          r'\bFt\.\b': 'Ft',
          r'\bFreeway\b': 'Fwy',
          r'\bFwy\.\b': 'Fwy',
          r'\bHeight\b': 'Hts',
          r'\bHts\.\b': 'Hts',
          r'\bHighway\b': 'Hwy',
          r'\bHwy\.\b': 'Hwy',
          r'\bIsland\b': 'Is',
          r'\bIs\.\b': 'Is',
          r'\bJunction\b': 'Jct',
          r'\bJct\.\b': 'Jct',
          r'\bLane\b': 'Ln',
          r'\bLn\.\b': 'Ln',
          r'\bMount\b': 'Mt',
          r'\bMt\.\b': 'Mt',
          r'\bMountain\b': 'Mt',
          r'\bNorth\b': 'N',
          r'\bN\.\b': 'N',
          r'\bNortheast\b': 'NE',
          r'\bNE\.\b': 'NE',
          r'\bNorthwest\b': 'NW',
          r'\bNW\.\b': 'NW',
          r'\bParkway\b': 'Pky',
          r'\bPky\.\b': 'Pky',
          r'\bPlace\b': 'Pl',
          r'\bPl\.\b': 'Pl',
          r'\bPost Office\b': 'PO',
          r'\bPO\.\b': 'PO',
          r'\bP\.O\b': 'PO',
          r'\bP\.O\.\b': 'PO',
          r'\bRidge\b': 'Rdg',
          r'\bRdg\.\b': 'Rdg',
          r'\bRoad\b': 'Rd',
          r'\bRd\.\b': 'Rd',
          r'\bROAD\b': 'Rd',
          r'\bRural Delivery\b': 'RD',
          r'\bRD\.\b': 'RD',
          r'\bRural Route\b': 'RR',
          r'\bRR\.\b': 'RR',
          r'\bSaint\b': 'St',
          r'\bSt\.\b': 'St',
          r'\bSouth\b': 'S',
          r'\bS\.\b': 'S',
          r'\bSoutheast\b': 'SE',
          r'\bSE\.\b': 'SE',
          r'\bSouthwest\b': 'SW',
          r'\bSW\.\b': 'SW',
          r'\bSpring\b': 'Spg',
          r'\bSpg\.\b': 'Spg',
          r'\bSprings\b': 'Spgs',
          r'\bSpgs\.\b': 'Spgs',
          r'\bSquare\b': 'Sq',
          r'\bSq\.\b': 'Sq',
          r'\bSquares\b': 'Sq',
          r'\bStreet\b': 'St',
          r'\bSuite\b': 'Ste',
          r'\bSte\.\b': 'Ste',
          r'\bTerrace\b': 'Ter',
          r'\bTer\.\b': 'Ter',
          r'\bTurnpike\b': 'Tpke',
          r'\bTpke\.\b': 'Tpke',
          r'\bThroughway\b': 'Trwy',
          r'\bTrwy\.\b': 'Trwy',
          r'\bTunnel\b': 'Tunl',
          r'\bTunl\.\b': 'Tunl',
          r'\bWest\b': 'W',
          r'\bW\.\b': 'W',
          ',': ' ',
          '\.': '',
          '-': ' ',
          '\n': ' '
        }
        for pattern, replacement in replacements.items():
          redata['AddrLines'] = redata['AddrLines'].str.replace(pattern, replacement + ' ', regex=True)

        return redata
    renew = normalizeredata(redata)

    # Clean addresses in impomatic - tried to do this before parsing out ImportOmatic file, but caused more trouble than was worth. 
    def normalizeimpomatic(impomatic):
        impomatic = impomatic.copy()
        replacements = {
          r'\bApartment\b': 'Apt',
          r'\bApt\.\b': 'Apt',
          r'\bAPT\b': 'Apt',
          r'\bnApt\b': 'Apt',
          r'\bNApt\b': 'Apt',
          r'\bAvenue\b': 'Ave',
          r'\bAve\.\b': 'Ave',
          r'\bBoulevard\b': 'Blvd',
          r'\bBlvd\.\b': 'Blvd',
          r'\bBuilding\b': 'Bldg',
          r'\bBldg\.\b': 'Bldg',
          r'\bCenter\b': 'Ctr',
          r'\bCtr\.\b': 'Ctr',
          r'\bCircle\b': 'Cir',
          r'\bCir\.\b': 'Cir',
          r'\bCourt\b': 'Ct',
          r'\bCt\.\b': 'Ct',
          r'\bDrive\b': 'Dr',
          r'\bDr\.\b': 'Dr',
          r'\bEast\b': 'E',
          r'\bE\.\b': 'E',
          r'\bExpressway\b': 'Expy',
          r'\bExpy\.\b': 'Expy',
          r'\bExtension\b': 'Ext',
          r'\bExt\.\b': 'Ext',
          r'\bFort\b': 'Ft',
          r'\bFt\.\b': 'Ft',
          r'\bFreeway\b': 'Fwy',
          r'\bFwy\.\b': 'Fwy',
          r'\bHeight\b': 'Hts',
          r'\bHts\.\b': 'Hts',
          r'\bHighway\b': 'Hwy',
          r'\bHwy\.\b': 'Hwy',
          r'\bIsland\b': 'Is',
          r'\bIs\.\b': 'Is',
          r'\bJunction\b': 'Jct',
          r'\bJct\.\b': 'Jct',
          r'\bLane\b': 'Ln',
          r'\bLn\.\b': 'Ln',
          r'\bMount\b': 'Mt',
          r'\bMt\.\b': 'Mt',
          r'\bMountain\b': 'Mt',
          r'\bNorth\b': 'N',
          r'\bN\.\b': 'N',
          r'\bNortheast\b': 'NE',
          r'\bNE\.\b': 'NE',
          r'\bNorthwest\b': 'NW',
          r'\bNW\.\b': 'NW',
          r'\bParkway\b': 'Pky',
          r'\bPky\.\b': 'Pky',
          r'\bPlace\b': 'Pl',
          r'\bPl\.\b': 'Pl',
          r'\bPost Office\b': 'PO',
          r'\bPO\.\b': 'PO',
          r'\bP\.O\b': 'PO',
          r'\bP\.O\.\b': 'PO',
          r'\bRidge\b': 'Rdg',
          r'\bRdg\.\b': 'Rdg',
          r'\bRoad\b': 'Rd',
          r'\bRd\.\b': 'Rd',
          r'\bROAD\b': 'Rd',
          r'\bRural Delivery\b': 'RD',
          r'\bRD\.\b': 'RD',
          r'\bRural Route\b': 'RR',
          r'\bRR\.\b': 'RR',
          r'\bSaint\b': 'St',
          r'\bSt\.\b': 'St',
          r'\bSouth\b': 'S',
          r'\bS\.\b': 'S',
          r'\bSoutheast\b': 'SE',
          r'\bSE\.\b': 'SE',
          r'\bSouthwest\b': 'SW',
          r'\bSW\.\b': 'SW',
          r'\bSpring\b': 'Spg',
          r'\bSpg\.\b': 'Spg',
          r'\bSprings\b': 'Spgs',
          r'\bSpgs\.\b': 'Spgs',
          r'\bSquare\b': 'Sq',
          r'\bSq\.\b': 'Sq',
          r'\bSquares\b': 'Sq',
          r'\bStreet\b': 'St',
          r'\bSuite\b': 'Ste',
          r'\bSte\.\b': 'Ste',
          r'\bTerrace\b': 'Ter',
          r'\bTer\.\b': 'Ter',
          r'\bTurnpike\b': 'Tpke',
          r'\bTpke\.\b': 'Tpke',
          r'\bThroughway\b': 'Trwy',
          r'\bTrwy\.\b': 'Trwy',
          r'\bTunnel\b': 'Tunl',
          r'\bTunl\.\b': 'Tunl',
          r'\bWest\b': 'W',
          r'\bW\.\b': 'W',
          ',': ' ',
          '\.': '',
          '-': ' ',
          '\n': ' '
        }
        for pattern, replacement in replacements.items():
          impomatic['AddrLines'] = impomatic['AddrLines'].str.replace(pattern, replacement + ' ', regex=True)

        return impomatic

    newimpomatic = normalizeimpomatic(impomatic)
    
    # Reorder columns with 'Test Case Failed' at the start
    cols = ['Test Case Failed'] + [col for col in failed.columns if col != 'Test Case Failed']
    failed = failed[cols]

    # printing files to show output directories
    print(out_dir  / rawdata_csv) # '/users/path/my_file/RawParishData.csv'
    print(out_dir / failed_csv)   # '/users/path/my_file/Failed.csv'
    print(out_dir / dup_csv)      # '/users/path/my_file/duplicated.csv'
    print(re_dir  / renew_csv)    # '/users/path/my_file/RE_Data.csv'
    print(out_dir / passed_csv)   # '/users/path/my_file/Passed.csv'
    print(re_dir  / import_csv)   # '/users/path/my_file/ImportOmatic.csv'

    # sorting files for output directories
    failed.to_csv(out_dir / failed_csv, index=False)
    duplicated.to_csv(out_dir / dup_csv, index=False)
    renew.to_csv(re_dir  / renew_csv, index=False)
    passed.to_csv(out_dir / passed_csv, index=False)
    newimpomatic.to_csv(re_dir  / import_csv, index=False)
    rawdata.to_csv(out_dir / rawdata_csv, index=False)
    
# This names the folder that holds all files after the parish. It will sort files that the parish uses and that Raiser's Edge uses
def main(input_dir: Path, output_dir: Path) -> None: # The input for this function is the input directory and the output directory which changed 
                                                    # to allow the GUI to work was def main(base_dir: Path) -> None:
    print(f'Processing files in {input_dir}: \n')   # Ctrl + H 'base_dir' and change to 'input_dir'

    n_process = 0
    for csv_file in input_dir.glob('*.csv'):
        
        # ex. csv_file = "/users/path/my_file.csv"
        
        name: str = csv_file.stem   # name = "my_file"
        reimportfiles: str = 'REImportFiles'
        
        output_dir: Path = input_dir / name  # output_dir = "/users/path/my_file"
        reout_dir: Path = input_dir / name / output_dir / reimportfiles

        print(f'Creating directory "{output_dir}"')
        Path.mkdir(output_dir, exist_ok=True)

        print(f'Creating directory "{reout_dir}"')
        Path.mkdir(reout_dir, exist_ok=True)

        print(f'Processing "{csv_file}"')
        process(csv_file=csv_file, out_dir=output_dir, re_dir=reout_dir)

        print(f'Completed processing\n')
        n_process += 1

    print(f'\nProcessed {n_process} files')

##################################################
#################For GUI##########################
##################################################

# if __name__ == '__main__':
#     root = get_root()  # root = "users/path"
#     main(input_dir=root)

def select_input_directory():
    input_dir = filedialog.askdirectory()
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_dir)

def select_output_directory():
    output_dir = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_dir)

def start_processing():
    input_dir = Path(input_entry.get())
    output_dir = Path(output_entry.get())
    
    print(f'Starting processing with input directory: {input_dir} and output directory: {output_dir}')
    
    main(input_dir, output_dir)

if __name__ == '__main__':
    root = get_root()
    gui_root = tk.Tk()
    gui_root.geometry("1000x120")  # Adjust window dimensions
    gui_root.title("RE Test Cases v9")

    input_label = tk.Label(gui_root, text="Input Directory:")
    input_label.grid(row=0, column=0, padx = 5, pady = 5, sticky="w")
    
    input_entry = tk.Entry(gui_root, width=80, font=("Helvetica", 12))  # Increase width and adjust font
    input_entry.grid(row=0, column=1, padx=5, pady = 5)
    
    input_button = tk.Button(gui_root, text="Select Input Directory", command=select_input_directory)
    input_button.grid(row=0, column=2, padx = 5, pady = 5)

    output_label = tk.Label(gui_root, text="Output Directory:")
    output_label.grid(row=1, column=0, padx = 5, pady = 5, sticky="w")
    
    output_entry = tk.Entry(gui_root, width=80, font=("Helvetica", 12))  # Increase width and adjust font
    output_entry.grid(row=1, column=1, padx = 5, pady = 5)
    
    output_button = tk.Button(gui_root, text="Select Output Directory", command=select_output_directory)
    output_button.grid(row=1, column=2, padx = 5, pady = 5)

    process_button = tk.Button(gui_root, text="Process CSVs", command=start_processing, font=("Helvetica", 12), width=20)  # Increase font size
    process_button.grid(row=2, column=0, columnspan=3, padx = 5, pady = 10)

    gui_root.mainloop()

##################################################
#################For GUI##########################
##################################################
