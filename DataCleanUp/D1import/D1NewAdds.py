import pandas as pd
import os
import re
import gender_guesser.detector as gender

# Function to split first names that have middle names or initials
def split_first_name(name):
    # Check for format "John D" or "John D."
    match = re.match(r'(\w+)\s([A-Z]\.?)$', name)
    if match:
        return match.group(1), match.group(2)
    
    # Check for format "John David"
    match = re.match(r'(\w+)\s(\w+)$', name)
    if match:
        return match.group(1), match.group(2)

    # Return the original name if no match is found
    return name, None

# Function to guess gender using the gender_guesser library
def guess_gender(name):
    d = gender.Detector()
    g = d.get_gender(name)
    
    # Mapping the gender-guesser outputs to desired values
    gender_map = {
        "male": "Male",
        "mostly_male": "Male",
        "female": "Female",
        "mostly_female": "Female",
        "unknown": "Unknown",
        "andy": "Ambiguous"
    }
    
    # Return the mapped gender or "Unknown" if not in the map
    return gender_map.get(g, "Unknown")

# Get the directory of the current script
directory = os.path.dirname(os.path.realpath(__file__))
# List all CSV files in the directory
csv_files = [f for f in os.listdir(directory) if f.endswith('.CSV') or f.endswith('.csv')]

# Process each CSV file
for file in csv_files:
    file_path = os.path.join(directory, file)
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Clean phone numbers that have no digits
    df['phone'] = df['phone'].apply(lambda x: '' if all(ch not in '0123456789' for ch in str(x)) else x)
    
    # Split first names and update 'first' and 'middle' columns
    df['first'], df['middle'] = zip(*df['first'].apply(split_first_name))
    
    # Guess and assign gender based on first name
    df['gender'] = df['first'].apply(guess_gender)

    # Explicitly fill in titles based on gender
    for idx, row in df.iterrows():
        if pd.isna(row['title']) or row['title'] == '':
            if row['gender'] == 'Male':
                df.at[idx, 'title'] = 'Mr.'
            elif row['gender'] == 'Female':
                df.at[idx, 'title'] = 'Ms.'

    # Reorder columns to place 'gender' after 'title'
    column_order = df.columns.tolist()
    gender_index = column_order.index('title') + 1
    column_order = column_order[:gender_index] + ['gender'] + column_order[gender_index:-1]
    df = df[column_order]
    
    # Construct the output filename with "_clean" appended and save the cleaned dataframe
    output_filename = os.path.splitext(file)[0] + '_clean.CSV'
    output_filepath = os.path.join(directory, output_filename)
    df.to_csv(output_filepath, index=False)
