#######################################################################################
#########Use this after running Labels. File must have _clean in the file name#########
#######################################################################################
import os
import pandas as pd

def process_file(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Processing each row
    for index, row in df.iterrows():
        # Skip row if first and last names are blank
        if pd.isna(row['CnBio_First_Name']) and pd.isna(row['CnBio_Last_Name']):
            continue

        # Formulating CnAdrSal_Addressee and CnAdrSal_Salutation
        first_name = row['CnBio_First_Name'] if not pd.isna(row['CnBio_First_Name']) else ''
        last_name = row['CnBio_Last_Name'] if not pd.isna(row['CnBio_Last_Name']) else ''
        spouse_first_name = row['CnSpSpBio_First_Name'] if not pd.isna(row['CnSpSpBio_First_Name']) else ''

        if spouse_first_name:
            df.at[index, 'CnAdrSal_Addressee'] = f"{first_name} and {spouse_first_name} {last_name}"
            df.at[index, 'CnAdrSal_Salutation'] = f"{first_name} and {spouse_first_name}"
        else:
            df.at[index, 'CnAdrSal_Addressee'] = f"{first_name} {last_name}"
            df.at[index, 'CnAdrSal_Salutation'] = first_name

    # Saving the processed file
    new_file_path = os.path.splitext(file_path)[0] + '_BishAddSal.csv'
    df.to_csv(new_file_path, index=False)

def main():
    # Getting the directory where the script is located
    directory = os.path.dirname(os.path.realpath(__file__))

    # Processing each CSV file in the directory
    for file in os.listdir(directory):
        if file.endswith('_clean.csv'):
            process_file(os.path.join(directory, file))

if __name__ == "__main__":
    main()
