import pandas as pd
import os
import re
import gender_guesser.detector as gender

def split_first_name(name):
    """
    Split a name of the form 'John D' or 'John D.' or 'John David' into first and middle components.
    Returns a tuple (first, middle).
    """
    match = re.match(r'(\w+)\s([A-Z]\.?)$', name)
    if match:
        return match.group(1), match.group(2)
    
    match = re.match(r'(\w+)\s(\w+)$', name)
    if match:
        return match.group(1), match.group(2)

    return name, None

def guess_gender(name):
    d = gender.Detector()
    return d.get_gender(name)

# Get the current directory where the script is located
directory = os.path.dirname(os.path.realpath(__file__))

# List all CSV files in the directory
csv_files = [f for f in os.listdir(directory) if f.endswith('.CSV') or f.endswith('.csv')]

for file in csv_files:
    # Construct the full file path
    file_path = os.path.join(directory, file)
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Clean phone column
    df['phone'] = df['phone'].apply(lambda x: '' if all(ch not in '0123456789' for ch in str(x)) else x)
    
    # Split first names and update 'first' and 'middle' columns
    df['first'], df['middle'] = zip(*df['first'].apply(split_first_name))
    
    # Guess gender for each first name and insert it after 'title' column
    df['gender'] = df['first'].apply(guess_gender)
    column_order = df.columns.tolist()
    gender_index = column_order.index('title') + 1
    column_order = column_order[:gender_index] + ['gender'] + column_order[gender_index:-1]
    df = df[column_order]
    
    # fill in empty titles based on gender
    df.loc[(df['title'] == '') & (df['gender'] == 'Male'), 'title'] = 'Mr.'
    df.loc[(df['title'] == '') & (df['gender'] == 'Female'), 'title'] = 'Ms.'

    # Construct the output filename with "_clean" appended
    output_filename = os.path.splitext(file)[0] + '_clean.CSV'
    output_filepath = os.path.join(directory, output_filename)
    
    # Save the cleaned dataframe back to a CSV
    df.to_csv(output_filepath, index=False)
