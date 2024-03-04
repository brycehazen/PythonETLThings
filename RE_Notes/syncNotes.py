import pandas as pd

# Define the remapping function including the full remap_dict
def remap_fund_id(last_fund_id, last_fund_id_desc):
    # Full mapping of current to remapped Fund ID and descriptions
    remap_dict = {
        10: ("1-10", "St. Hubert of the Forest Mission"),
        15: ("2-15", "St. Maximillian Kolbe Catholic Church"),
        16: ("2-16", "St. Frances Xavier Cabrini"),
        19: ("5-19", "St. Ann Catholic Church"),
        20: ("5-20", "St. Peter Catholic Church"),
        22: ("1-22", "St. John the Baptist Catholic Church"),
        24: ("5-24", "St. Clare Catholic Church"),
        25: ("5-25", "St. Gerard Mission"),
        26: ("4-26", "Ascension Catholic Church"),
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


    # Check if the ID is in the remap dictionary and remap accordingly
    if last_fund_id in remap_dict:
        return remap_dict[last_fund_id]
    # If not in the remap dictionary, return the original values
    return str(last_fund_id), last_fund_id_desc

# Function to apply remapping to each row of the DataFrame
def apply_remap(row):
    # Ensure that LastFundID is an integer before remapping
    try:
        last_fund_id = int(row['LastFundID'])
    except ValueError:
        # If LastFundID cannot be converted to integer, return the original row
        return row

    new_id, new_desc = remap_fund_id(last_fund_id, row['LastFundIDDesc'])
    row['LastFundID'], row['LastFundIDDesc'] = new_id, new_desc
    return row

# Reading the CSV file
filename = 'NotesAllChanges.CSV'
df = pd.read_csv(filename, encoding='ISO-8859-1')

# Apply the remapping to each row
df = df.apply(apply_remap, axis=1)

# Save the updated DataFrame ensuring no NaN values for LastFundID and LastFundIDDesc
updated_filename = 'Updated_NotesAllChanges.CSV'
df.to_csv(updated_filename, index=False, encoding='ISO-8859-1')
