import os
import pandas as pd

def combine_export_csvs(output_file_path):
    """
    Reads all CSV files with '_Export' in the file name in the current directory,
    combines them into one DataFrame, adds a column with part of the file name,
    and saves the combined data into an Excel file.
    """
    current_directory = os.getcwd()
    dataframes = []

    for file in os.listdir(current_directory):
        if file.endswith(".csv") and ' Export' in file:
            file_path = os.path.join(current_directory, file)
            df = pd.read_csv(file_path, encoding='ISO-8859-1', low_memory=False)

            # Extracting ID part from file name (assuming the format 'ID_Export.csv')
            file_id = file.split('_')[0]
            df['FileID'] = file_id

            dataframes.append(df)

    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)

        # Saving combined data to Excel file
        with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
            combined_df.to_excel(writer, index=False, sheet_name='Sheet1')
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            num_cols = combined_df.shape[1]
            text_format = workbook.add_format({'num_format': '@'})

            for col_idx in range(num_cols):
                worksheet.set_column(col_idx, col_idx, None, text_format)
    else:
        print("No matching CSV files found.")

output_file_path = 'combined_data.xlsx'  # Set your desired output file path here
combine_export_csvs(output_file_path)
