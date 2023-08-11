from pathlib import Path
import pandas as pd 
import numpy as np

failed_csv = 'Failed.csv'
dup_csv = 'duplicated.csv'
renew_csv = 'RE_Data.csv'
passed_csv = 'Passed.csv'
import_csv = 'ImportOmatic.csv'
rawdata_csv = 'RawParishData.csv'

def get_root() -> Path:
    return Path(__file__).resolve().parent


def process(csv_file: Path, out_dir: Path, re_dir: Path) -> None:
    
    data = pd.read_csv(csv_file, encoding='latin-1')
    
    data.drop(data.columns[[38]], axis=1)
    
    rawdata = pd.read_csv(csv_file, encoding='latin-1')
    if 'Notes' not in data.columns:
      data["Notes"] = " "

    # Fixing titles- 
    data.loc[data['Titl1'].eq('Mr'), 'Titl1'] = 'Mr.'
    data.loc[data['Titl1'].eq('Mrs'), 'Titl1'] = 'Mrs.'
    data.loc[data['Titl1'].eq('Ms'), 'Titl1'] = 'Ms.'
    data.loc[data['Titl1'].eq('Dr'), 'Titl1'] = 'Dr.'
    data.loc[data['SRTitl1'].eq('Mr'), 'SRTitl1'] = 'Mr.'
    data.loc[data['SRTitl1'].eq('Mrs'), 'SRTitl1'] = 'Mrs.'
    data.loc[data['SRTitl1'].eq('Ms'), 'SRTitl1'] = 'Ms.'
    data.loc[data['SRTitl1'].eq('Dr'), 'SRTitl1'] = 'Dr.'
    data.loc[data['Titl1'].eq('Rev.') , 'Titl1'] = 'Reverend'
    data.loc[data['Titl1'].eq('Very Rev.') , 'Titl1'] = 'Very Reverend'
    data.loc[data['Titl1'].eq('LTC') , 'Titl1'] = 'Lt. Col.'
    data.loc[data['Titl1'].eq('Cpt.') , 'Titl1'] = 'Capt.'
    data.loc[data['Titl1'].eq('Mgen') , 'Titl1'] = 'Maj. Gen.'
    data.loc[data['Titl1'].eq('Lt Gen') , 'Titl1'] = 'Lt. Gen.'
    data.loc[data['Titl1'].eq('Mr. & Mrs.') , 'Titl1'] = 'Mr.'
    data.loc[data['SRTitl1'].eq('Mr. & Mrs.'), 'SRTitl1'] = 'Mrs.'
    data.loc[data['SRTitl1'].eq('Maj Gen'), 'SRTitl1'] = 'Maj. Gen.'
    data.loc[data['SRTitl1'].eq('COL'), 'SRTitl1'] = 'Col.'


    # change title based off Gender This has been approved by the dioIT despite not knowing if it's title or gender that's correct. 
    data.loc[data['Titl1'].eq('Mr.'), 'Gender'] = 'Male'
    data.loc[data['Titl1'].eq('Mrs.'), 'Gender'] = 'Female'
    data.loc[data['Titl1'].eq('Ms.'), 'Gender'] = 'Female'
    data.loc[data['Titl1'].eq('Miss'), 'Gender'] = 'Female'
    data.loc[data['SRTitl1'].eq('Mr.'), 'SRGender'] = 'Male'
    data.loc[data['SRTitl1'].eq('Mrs.'), 'SRGender'] = 'Female'
    data.loc[data['SRTitl1'].eq('Ms.'), 'SRGender'] = 'Female'
    data.loc[data['SRTitl1'].eq('Miss'), 'SRGender'] = 'Female'

    # change Gender bases off title
    #Gender is male, title is blank, then change title to Mr.
    data.loc[(data['Gender'].eq('Male')) & (data['Titl1'] == ''), 'Titl1'] = 'Mr.'
    # Gender is Female, title blank, SRlast name is not the same as Last name, then changed title = Ms.
    data.loc[(data['Gender'].eq('Female')) & (data['Titl1'] == '') & (data['SRLastName'] != data['LastName']), 'Titl1'] = 'Ms.'
    # Gender is Female, title blank, SRlastname and last name are the same, then changed title = Mrs.
    data.loc[(data['Gender'].eq('Female')) & (data['Titl1'] == '') & (data['SRLastName'] == data['LastName']), 'Titl1'] = 'Mrs.'
    # SRGender is female, SRtitle is one of 'Ms.', 'Miss', 'Mrs.', Gender is unknown, then changed title and gender to Mr. Male 
    data.loc[(data['SRGender'] == 'Female') & (data['SRtitl1'].isin(['Ms.', 'Miss', 'Mrs.'])) & (data['Gender'] == 'Unknown'), ['Gender', 'Titl1']] = ['Male', 'Mr.']
    # SRGender is unknown, gender is male, title is Mr., SRlastname is same as Last name, SRtitle is blank, then change SRtitle and SRGender to Mrs. Female
    data.loc[(data['SRGender'] == 'Unknown') & (data['Gender'] == 'Male') & (data['titl1'] == 'Mr.') & (data['SRLastName'] == data['LastName']) & (data['SRtitl1'] == ''), ['SRtitl1', 'SRGender']] = ['Mrs.', 'Female']


    # Change ConsCode to long format to fit Raiser's Edge Import
    data.loc[data['ConsCode'].eq('1-10'), 'ConsCode'] = 'St. Hubert of the Forest Mission, Astor'
    data.loc[data['ConsCode'].eq(' 1-10'), 'ConsCode'] = 'St. Hubert of the Forest Mission, Astor'
    data.loc[data['ConsCode'].eq('1-11'), 'ConsCode'] = 'Blessed Sacrament Catholic Church, Clermont'
    data.loc[data['ConsCode'].eq(' 1-11'), 'ConsCode'] = 'Blessed Sacrament Catholic Church, Clermont'
    data.loc[data['ConsCode'].eq('1-22'), 'ConsCode'] = 'St. John the Baptist Catholic Church, Dunnellon'
    data.loc[data['ConsCode'].eq(' 1-22'), 'ConsCode'] = 'St. John the Baptist Catholic Church, Dunnellon'
    data.loc[data['ConsCode'].eq('1-27'), 'ConsCode'] = 'St. Mary of the Lakes Catholic Church, Eustis'
    data.loc[data['ConsCode'].eq(' 1-27'), 'ConsCode'] = 'St. Mary of the Lakes Catholic Church, Eustis'
    data.loc[data['ConsCode'].eq('1-30'), 'ConsCode'] = 'Santo Toribio Romo Mission, Mascotte'
    data.loc[data['ConsCode'].eq(' 1-30'), 'ConsCode'] = 'Santo Toribio Romo Mission, Mascotte'
    data.loc[data['ConsCode'].eq('1-4'), 'ConsCode'] = 'St. Theresa Catholic Church, Belleview'
    data.loc[data['ConsCode'].eq(' 1-4'), 'ConsCode'] = 'St. Theresa Catholic Church, Belleview'
    data.loc[data['ConsCode'].eq('1-40'), 'ConsCode'] = 'St. Timothy Catholic Church, Lady Lake'
    data.loc[data['ConsCode'].eq(' 1-40'), 'ConsCode'] = 'St. Timothy Catholic Church, Lady Lake'
    data.loc[data['ConsCode'].eq('1-44'), 'ConsCode'] = 'St. Paul Catholic Church, Leesburg'
    data.loc[data['ConsCode'].eq(' 1-44'), 'ConsCode'] = 'St. Paul Catholic Church, Leesburg'
    data.loc[data['ConsCode'].eq('1-5'), 'ConsCode'] = 'St. Lawrence Catholic Church, Bushnell'
    data.loc[data['ConsCode'].eq(' 1-5'), 'ConsCode'] = 'St. Lawrence Catholic Church, Bushnell'
    data.loc[data['ConsCode'].eq('1-51'), 'ConsCode'] = 'St. Patrick Catholic Church, Mount Dora'
    data.loc[data['ConsCode'].eq(' 1-51'), 'ConsCode'] = 'St. Patrick Catholic Church, Mount Dora'
    data.loc[data['ConsCode'].eq('1-53'), 'ConsCode'] = 'St. Joseph of the Forest Mission, Silver Springs'
    data.loc[data['ConsCode'].eq(' 1-53'), 'ConsCode'] = 'St. Joseph of the Forest Mission, Silver Springs'
    data.loc[data['ConsCode'].eq('1-56'), 'ConsCode'] = 'Our Lady of the Springs Catholic Church, Ocala'
    data.loc[data['ConsCode'].eq(' 1-56'), 'ConsCode'] = 'Our Lady of the Springs Catholic Church, Ocala'
    data.loc[data['ConsCode'].eq('1-57'), 'ConsCode'] = 'Blessed Trinity Catholic Church, Ocala'
    data.loc[data['ConsCode'].eq(' 1-57'), 'ConsCode'] = 'Blessed Trinity Catholic Church, Ocala'
    data.loc[data['ConsCode'].eq('1-65'), 'ConsCode'] = 'Christ the King Mission, Citra'
    data.loc[data['ConsCode'].eq(' 1-65'), 'ConsCode'] = 'Christ the King Mission, Citra'
    data.loc[data['ConsCode'].eq('1-67'), 'ConsCode'] = 'Queen of Peace Catholic Church, Ocala'
    data.loc[data['ConsCode'].eq(' 1-67'), 'ConsCode'] = 'Queen of Peace Catholic Church, Ocala'
    data.loc[data['ConsCode'].eq('1-7'), 'ConsCode'] = 'St. Jude Catholic Church, Ocala'
    data.loc[data['ConsCode'].eq(' 1-7'), 'ConsCode'] = 'St. Jude Catholic Church, Ocala'
    data.loc[data['ConsCode'].eq('1-8'), 'ConsCode'] = 'Immaculate Heart of Mary Catholic Church, Candler'
    data.loc[data['ConsCode'].eq(' 1-8'), 'ConsCode'] = 'Immaculate Heart of Mary Catholic Church, Candler'
    data.loc[data['ConsCode'].eq('1-84'), 'ConsCode'] = 'St. Mark the Evangelist Catholic Church, Summerfield'
    data.loc[data['ConsCode'].eq(' 1-84'), 'ConsCode'] = 'St. Mark the Evangelist Catholic Church, Summerfield'
    data.loc[data['ConsCode'].eq('1-85'), 'ConsCode'] = 'Our Lady of Guadalupe Mission, Ocala'
    data.loc[data['ConsCode'].eq(' 1-85'), 'ConsCode'] = 'Our Lady of Guadalupe Mission, Ocala'
    data.loc[data['ConsCode'].eq('1-89'), 'ConsCode'] = 'St. Vincent de Paul Catholic Church, Wildwood'
    data.loc[data['ConsCode'].eq(' 1-89'), 'ConsCode'] = 'St. Vincent de Paul Catholic Church, Wildwood'
    data.loc[data['ConsCode'].eq('1-92'), 'ConsCode'] = 'San Pedro de Jesus Maldonado Mission, Wildwood'
    data.loc[data['ConsCode'].eq(' 1-92'), 'ConsCode'] = 'San Pedro de Jesus Maldonado Mission, Wildwood'
    data.loc[data['ConsCode'].eq('2-1'), 'ConsCode'] = 'St. Francis of Assisi Catholic Church, Apopka'
    data.loc[data['ConsCode'].eq(' 2-1'), 'ConsCode'] = 'St. Francis of Assisi Catholic Church, Apopka'
    data.loc[data['ConsCode'].eq('2-14'), 'ConsCode'] = 'Corpus Christi Catholic Church, Celebration'
    data.loc[data['ConsCode'].eq(' 2-14'), 'ConsCode'] = 'Corpus Christi Catholic Church, Celebration'
    data.loc[data['ConsCode'].eq('2-15'), 'ConsCode'] = 'St. Maximillian Kolbe Catholic Church, Avalon Park'
    data.loc[data['ConsCode'].eq(' 2-15'), 'ConsCode'] = 'St. Maximillian Kolbe Catholic Church, Avalon Park'
    data.loc[data['ConsCode'].eq('2-16'), 'ConsCode'] = 'St. Frances Xavier Cabrini, Orlando'
    data.loc[data['ConsCode'].eq(' 2-16'), 'ConsCode'] = 'St. Frances Xavier Cabrini, Orlando'
    data.loc[data['ConsCode'].eq('2-2'), 'ConsCode'] = 'St. Catherine of Siena Catholic Church, Kissimmee'
    data.loc[data['ConsCode'].eq(' 2-2'), 'ConsCode'] = 'St. Catherine of Siena Catholic Church, Kissimmee'
    data.loc[data['ConsCode'].eq('2-29'), 'ConsCode'] = 'Sts. Peter and Paul Catholic Church, Winter Park'
    data.loc[data['ConsCode'].eq(' 2-29'), 'ConsCode'] = 'Sts. Peter and Paul Catholic Church, Winter Park'
    data.loc[data['ConsCode'].eq('2-33'), 'ConsCode'] = 'Holy Redeemer Catholic Church, Kissimmee'
    data.loc[data['ConsCode'].eq(' 2-33'), 'ConsCode'] = 'Holy Redeemer Catholic Church, Kissimmee'
    data.loc[data['ConsCode'].eq('2-39'), 'ConsCode'] = 'Church of the Nativity, Longwood'
    data.loc[data['ConsCode'].eq(' 2-39'), 'ConsCode'] = 'Church of the Nativity, Longwood'
    data.loc[data['ConsCode'].eq('2-45'), 'ConsCode'] = 'St. Philip Phan Van Minh Catholic Church, Orlando'
    data.loc[data['ConsCode'].eq(' 2-45'), 'ConsCode'] = 'St. Philip Phan Van Minh Catholic Church, Orlando'
    data.loc[data['ConsCode'].eq('2-46'), 'ConsCode'] = 'Annunciation Catholic Church, Longwood'
    data.loc[data['ConsCode'].eq(' 2-46'), 'ConsCode'] = 'Annunciation Catholic Church, Longwood'
    data.loc[data['ConsCode'].eq('2-47'), 'ConsCode'] = 'St. Mary Magdalen Catholic Church, Altamonte Springs'
    data.loc[data['ConsCode'].eq(' 2-47'), 'ConsCode'] = 'St. Mary Magdalen Catholic Church, Altamonte Springs'
    data.loc[data['ConsCode'].eq('2-58'), 'ConsCode'] = 'St. Isaac Jogues Catholic Church, Orlando'
    data.loc[data['ConsCode'].eq(' 2-58'), 'ConsCode'] = 'St. Isaac Jogues Catholic Church, Orlando'
    data.loc[data['ConsCode'].eq('2-59'), 'ConsCode'] = 'St. Andrew Catholic Church, Orlando'
    data.loc[data['ConsCode'].eq(' 2-59'), 'ConsCode'] = 'St. Andrew Catholic Church, Orlando'
    data.loc[data['ConsCode'].eq('2-6'), 'ConsCode'] = 'Holy Family Catholic Church, Orlando'
    data.loc[data['ConsCode'].eq(' 2-6'), 'ConsCode'] = 'Holy Family Catholic Church, Orlando'
    data.loc[data['ConsCode'].eq('2-60'), 'ConsCode'] = 'Blessed Trinity Catholic Church, Orlando'
    data.loc[data['ConsCode'].eq(' 2-60'), 'ConsCode'] = 'Blessed Trinity Catholic Church, Orlando'
    data.loc[data['ConsCode'].eq('2-61'), 'ConsCode'] = 'St. Charles Borromeo Catholic Church, Orlando'
    data.loc[data['ConsCode'].eq(' 2-61'), 'ConsCode'] = 'St. Charles Borromeo Catholic Church, Orlando'
    data.loc[data['ConsCode'].eq('2-62'), 'ConsCode'] = 'Good Shepherd Catholic Church, Orlando'
    data.loc[data['ConsCode'].eq(' 2-62'), 'ConsCode'] = 'Good Shepherd Catholic Church, Orlando'
    data.loc[data['ConsCode'].eq('2-63'), 'ConsCode'] = 'St. James Cathedral, Orlando'
    data.loc[data['ConsCode'].eq(' 2-63'), 'ConsCode'] = 'St. James Cathedral, Orlando'
    data.loc[data['ConsCode'].eq('2-64'), 'ConsCode'] = 'St. John Vianney Catholic Church, Orlando'
    data.loc[data['ConsCode'].eq(' 2-64'), 'ConsCode'] = 'St. John Vianney Catholic Church, Orlando'
    data.loc[data['ConsCode'].eq('2-66'), 'ConsCode'] = 'Mary Queen of the Universe Shrine, Orlando'
    data.loc[data['ConsCode'].eq(' 2-66'), 'ConsCode'] = 'Mary Queen of the Universe Shrine, Orlando'
    data.loc[data['ConsCode'].eq('2-68'), 'ConsCode'] = 'Holy Cross Catholic Church, Orlando'
    data.loc[data['ConsCode'].eq(' 2-68'), 'ConsCode'] = 'Holy Cross Catholic Church, Orlando'
    data.loc[data['ConsCode'].eq('2-78'), 'ConsCode'] = 'St. Thomas Aquinas Catholic Church, St. Cloud'
    data.loc[data['ConsCode'].eq(' 2-78'), 'ConsCode'] = 'St. Thomas Aquinas Catholic Church, St. Cloud'
    data.loc[data['ConsCode'].eq('2-79'), 'ConsCode'] = 'All Souls Catholic Church, Sanford'
    data.loc[data['ConsCode'].eq(' 2-79'), 'ConsCode'] = 'All Souls Catholic Church, Sanford'
    data.loc[data['ConsCode'].eq('2-81'), 'ConsCode'] = 'St. Ignatius Kim Mission, Orlando'
    data.loc[data['ConsCode'].eq(' 2-81'), 'ConsCode'] = 'St. Ignatius Kim Mission, Orlando'
    data.loc[data['ConsCode'].eq('2-82'), 'ConsCode'] = 'Most Precious Blood Catholic Church, Oviedo'
    data.loc[data['ConsCode'].eq(' 2-82'), 'ConsCode'] = 'Most Precious Blood Catholic Church, Oviedo'
    data.loc[data['ConsCode'].eq('2-9'), 'ConsCode'] = 'St. Augustine Catholic Church, Casselberry'
    data.loc[data['ConsCode'].eq(' 2-9'), 'ConsCode'] = 'St. Augustine Catholic Church, Casselberry'
    data.loc[data['ConsCode'].eq('2-90'), 'ConsCode'] = 'St. Stephen Catholic Church, Winter Springs'
    data.loc[data['ConsCode'].eq(' 2-90'), 'ConsCode'] = 'St. Stephen Catholic Church, Winter Springs'
    data.loc[data['ConsCode'].eq('2-91'), 'ConsCode'] = 'St. Joseph Catholic Church, Orlando'
    data.loc[data['ConsCode'].eq(' 2-91'), 'ConsCode'] = 'St. Joseph Catholic Church, Orlando'
    data.loc[data['ConsCode'].eq('2-95'), 'ConsCode'] = 'Resurrection Catholic Church, Winter Garden'
    data.loc[data['ConsCode'].eq(' 2-95'), 'ConsCode'] = 'Resurrection Catholic Church, Winter Garden'
    data.loc[data['ConsCode'].eq('2-97'), 'ConsCode'] = 'St. Margaret Mary Catholic Church, Winter Park'
    data.loc[data['ConsCode'].eq(' 2-97'), 'ConsCode'] = 'St. Margaret Mary Catholic Church, Winter Park'
    data.loc[data['ConsCode'].eq('3-13'), 'ConsCode'] = 'St. Faustina Catholic Church, Clermont'
    data.loc[data['ConsCode'].eq(' 3-13'), 'ConsCode'] = 'St. Faustina Catholic Church, Clermont'
    data.loc[data['ConsCode'].eq('3-145'), 'ConsCode'] = 'Centro Guadalupano Mission, Wahneta'
    data.loc[data['ConsCode'].eq(' 3-145'), 'ConsCode'] = 'Centro Guadalupano Mission, Wahneta'
    data.loc[data['ConsCode'].eq('3-28'), 'ConsCode'] = 'St. John Neumann Catholic Church, Lakeland'
    data.loc[data['ConsCode'].eq(' 3-28'), 'ConsCode'] = 'St. John Neumann Catholic Church, Lakeland'
    data.loc[data['ConsCode'].eq('3-3'), 'ConsCode'] = 'St. Thomas Aquinas Catholic Church, Bartow'
    data.loc[data['ConsCode'].eq(' 3-3'), 'ConsCode'] = 'St. Thomas Aquinas Catholic Church, Bartow'
    data.loc[data['ConsCode'].eq('3-32'), 'ConsCode'] = 'St. Ann Catholic Church, Haines City'
    data.loc[data['ConsCode'].eq(' 3-32'), 'ConsCode'] = 'St. Ann Catholic Church, Haines City'
    data.loc[data['ConsCode'].eq('3-34'), 'ConsCode'] = 'St. Joseph Catholic Church, Lakeland'
    data.loc[data['ConsCode'].eq(' 3-34'), 'ConsCode'] = 'St. Joseph Catholic Church, Lakeland'
    data.loc[data['ConsCode'].eq('3-35'), 'ConsCode'] = 'Church of the Resurrection, Lakeland'
    data.loc[data['ConsCode'].eq(' 3-35'), 'ConsCode'] = 'Church of the Resurrection, Lakeland'
    data.loc[data['ConsCode'].eq('3-36'), 'ConsCode'] = 'St. Anthony Catholic Church, Lakeland'
    data.loc[data['ConsCode'].eq(' 3-36'), 'ConsCode'] = 'St. Anthony Catholic Church, Lakeland'
    data.loc[data['ConsCode'].eq('3-41'), 'ConsCode'] = 'Holy Spirit Catholic Church, Lake Wales'
    data.loc[data['ConsCode'].eq(' 3-41'), 'ConsCode'] = 'Holy Spirit Catholic Church, Lake Wales'
    data.loc[data['ConsCode'].eq('3-42'), 'ConsCode'] = 'St. Leo the Great Mission, Lake Wales'
    data.loc[data['ConsCode'].eq(' 3-42'), 'ConsCode'] = 'St. Leo the Great Mission, Lake Wales'
    data.loc[data['ConsCode'].eq('3-77'), 'ConsCode'] = 'St. Rose of Lima Catholic Church, Poinciana'
    data.loc[data['ConsCode'].eq(' 3-77'), 'ConsCode'] = 'St. Rose of Lima Catholic Church, Poinciana'
    data.loc[data['ConsCode'].eq('3-94'), 'ConsCode'] = 'St. Matthew Catholic Church, Winter Haven'
    data.loc[data['ConsCode'].eq(' 3-94'), 'ConsCode'] = 'St. Matthew Catholic Church, Winter Haven'
    data.loc[data['ConsCode'].eq('3-96'), 'ConsCode'] = 'St. Joseph Catholic Church, Winter Haven'
    data.loc[data['ConsCode'].eq(' 3-96'), 'ConsCode'] = 'St. Joseph Catholic Church, Winter Haven'
    data.loc[data['ConsCode'].eq('3-98'), 'ConsCode'] = 'St. Elizabeth Ann Seton Mission, Bartow'
    data.loc[data['ConsCode'].eq(' 3-98'), 'ConsCode'] = 'St. Elizabeth Ann Seton Mission, Bartow'
    data.loc[data['ConsCode'].eq('4-12'), 'ConsCode'] = 'Church of Our Saviour, Cocoa Beach'
    data.loc[data['ConsCode'].eq(' 4-12'), 'ConsCode'] = 'Church of Our Saviour, Cocoa Beach'
    data.loc[data['ConsCode'].eq('4-26'), 'ConsCode'] = 'Ascension Catholic Church, Melbourne'
    data.loc[data['ConsCode'].eq(' 4-26'), 'ConsCode'] = 'Ascension Catholic Church, Melbourne'
    data.loc[data['ConsCode'].eq('4-48'), 'ConsCode'] = 'Our Lady of Lourdes Catholic Church, Melbourne'
    data.loc[data['ConsCode'].eq(' 4-48'), 'ConsCode'] = 'Our Lady of Lourdes Catholic Church, Melbourne'
    data.loc[data['ConsCode'].eq('4-49'), 'ConsCode'] = 'Divine Mercy Catholic Church, Merritt Island'
    data.loc[data['ConsCode'].eq(' 4-49'), 'ConsCode'] = 'Divine Mercy Catholic Church, Merritt Island'
    data.loc[data['ConsCode'].eq('4-50'), 'ConsCode'] = 'Holy Spirit Catholic Church, Mims'
    data.loc[data['ConsCode'].eq(' 4-50'), 'ConsCode'] = 'Holy Spirit Catholic Church, Mims'
    data.loc[data['ConsCode'].eq('4-52'), 'ConsCode'] = 'Immaculate Conception Catholic Church, Melbourne Beach'
    data.loc[data['ConsCode'].eq(' 4-52'), 'ConsCode'] = 'Immaculate Conception Catholic Church, Melbourne Beach'
    data.loc[data['ConsCode'].eq('4-71'), 'ConsCode'] = 'St. Joseph Catholic Church, Palm Bay'
    data.loc[data['ConsCode'].eq(' 4-71'), 'ConsCode'] = 'St. Joseph Catholic Church, Palm Bay'
    data.loc[data['ConsCode'].eq('4-73'), 'ConsCode'] = 'Our Lady of Grace Catholic Church, Palm Bay'
    data.loc[data['ConsCode'].eq(' 4-73'), 'ConsCode'] = 'Our Lady of Grace Catholic Church, Palm Bay'
    data.loc[data['ConsCode'].eq('4-75'), 'ConsCode'] = 'St. Luke Catholic Church, Barefoot Bay'
    data.loc[data['ConsCode'].eq(' 4-75'), 'ConsCode'] = 'St. Luke Catholic Church, Barefoot Bay'
    data.loc[data['ConsCode'].eq('4-76'), 'ConsCode'] = 'St. Mary Catholic Church, Rockledge'
    data.loc[data['ConsCode'].eq(' 4-76'), 'ConsCode'] = 'St. Mary Catholic Church, Rockledge'
    data.loc[data['ConsCode'].eq('4-80'), 'ConsCode'] = 'Holy Name of Jesus Catholic Church, Indialantic'
    data.loc[data['ConsCode'].eq(' 4-80'), 'ConsCode'] = 'Holy Name of Jesus Catholic Church, Indialantic'
    data.loc[data['ConsCode'].eq('4-83'), 'ConsCode'] = 'Blessed Sacrament Catholic Church, Cocoa'
    data.loc[data['ConsCode'].eq(' 4-83'), 'ConsCode'] = 'Blessed Sacrament Catholic Church, Cocoa'
    data.loc[data['ConsCode'].eq('4-87'), 'ConsCode'] = 'St. John the Evangelist Catholic Church, Viera'
    data.loc[data['ConsCode'].eq(' 4-87'), 'ConsCode'] = 'St. John the Evangelist Catholic Church, Viera'
    data.loc[data['ConsCode'].eq('4-88'), 'ConsCode'] = 'St. Teresa Catholic Church, Titusville'
    data.loc[data['ConsCode'].eq(' 4-88'), 'ConsCode'] = 'St. Teresa Catholic Church, Titusville'
    data.loc[data['ConsCode'].eq('5-17'), 'ConsCode'] = 'Our Lady of Lourdes Catholic Church, Daytona Beach'
    data.loc[data['ConsCode'].eq(' 5-17'), 'ConsCode'] = 'Our Lady of Lourdes Catholic Church, Daytona Beach'
    data.loc[data['ConsCode'].eq('5-18'), 'ConsCode'] = 'Basilica of St. Paul Catholic Church, Daytona Beach'
    data.loc[data['ConsCode'].eq(' 5-18'), 'ConsCode'] = 'Basilica of St. Paul Catholic Church, Daytona Beach'
    data.loc[data['ConsCode'].eq('5-19'), 'ConsCode'] = 'St. Ann Catholic Church, DeBary'
    data.loc[data['ConsCode'].eq(' 5-19'), 'ConsCode'] = 'St. Ann Catholic Church, DeBary'
    data.loc[data['ConsCode'].eq('5-20'), 'ConsCode'] = 'St. Peter Catholic Church, DeLand'
    data.loc[data['ConsCode'].eq(' 5-20'), 'ConsCode'] = 'St. Peter Catholic Church, DeLand'
    data.loc[data['ConsCode'].eq('5-21'), 'ConsCode'] = 'Our Lady of the Lakes Catholic Church, Deltona'
    data.loc[data['ConsCode'].eq(' 5-21'), 'ConsCode'] = 'Our Lady of the Lakes Catholic Church, Deltona'
    data.loc[data['ConsCode'].eq('5-23'), 'ConsCode'] = 'San Jose Mission, DeLand'
    data.loc[data['ConsCode'].eq(' 5-23'), 'ConsCode'] = 'San Jose Mission, DeLand'
    data.loc[data['ConsCode'].eq('5-24'), 'ConsCode'] = 'St. Clare Catholic Church, Deltona'
    data.loc[data['ConsCode'].eq(' 5-24'), 'ConsCode'] = 'St. Clare Catholic Church, Deltona'
    data.loc[data['ConsCode'].eq('5-25'), 'ConsCode'] = 'St. Gerard Mission, Edgewater'
    data.loc[data['ConsCode'].eq(' 5-25'), 'ConsCode'] = 'St. Gerard Mission, Edgewater'
    data.loc[data['ConsCode'].eq('5-54'), 'ConsCode'] = 'Our Lady Star of the Sea Catholic Church, New Smyrna Beach'
    data.loc[data['ConsCode'].eq(' 5-54'), 'ConsCode'] = 'Our Lady Star of the Sea Catholic Church, New Smyrna Beach'
    data.loc[data['ConsCode'].eq('5-55'), 'ConsCode'] = 'Sacred Heart Catholic Church, New Smyrna Beach'
    data.loc[data['ConsCode'].eq(' 5-55'), 'ConsCode'] = 'Sacred Heart Catholic Church, New Smyrna Beach'
    data.loc[data['ConsCode'].eq('5-69'), 'ConsCode'] = 'St. Brendan Catholic Church, Ormond Beach'
    data.loc[data['ConsCode'].eq(' 5-69'), 'ConsCode'] = 'St. Brendan Catholic Church, Ormond Beach'
    data.loc[data['ConsCode'].eq('5-70'), 'ConsCode'] = 'Prince of Peace Catholic Church, Ormond Beach'
    data.loc[data['ConsCode'].eq(' 5-70'), 'ConsCode'] = 'Prince of Peace Catholic Church, Ormond Beach'
    data.loc[data['ConsCode'].eq('5-72'), 'ConsCode'] = 'Church of the Epiphany, Port Orange'
    data.loc[data['ConsCode'].eq(' 5-72'), 'ConsCode'] = 'Church of the Epiphany, Port Orange'
    data.loc[data['ConsCode'].eq('5-74'), 'ConsCode'] = 'Our Lady of Hope Catholic Church, Port Orange'
    data.loc[data['ConsCode'].eq(' 5-74'), 'ConsCode'] = 'Our Lady of Hope Catholic Church, Port Orange'

    # change MrtlStat based off Gender
    data.loc[(data['MrtlStat'].isnull()) & (data['PrimAddText'].str.contains('&| and ', na=False)) & (data['LastName'] == data['SRLastName']),'MrtlStat'] = 'Married'
    data.loc[(data['MrtlStat'].str.contains('Religion|Civilly', na=False)),'MrtlStat'] = 'Married'
    data.loc[(data['MrtlStat'].str.contains('Never', na=False)),'MrtlStat', ] = 'Single'
    data.loc[(data['MrtlStat'].str.contains('Unknown', na=False)),'MrtlStat'] = ''
    data.loc[(data['MrtlStat'].isnull()) & (data['PrimAddText'].str.contains('&| and ')),'MrtlStat'] = 'Married'

    # Create array to track failed cases.
    data['Test Case Failed']= ''
    data = data.replace(np.nan,'')
    data.insert(0, 'ID', range(0, len(data)))

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

    # Testcase  6 -	Head of house hold is not above the age of 18.
    data['BDay']= pd.to_datetime(data['BDay'], errors="coerce")
    data_6 = data.loc[data['BDay'] >= '01/01/2004']
    ids = data_6.index.tolist()
    for i in ids:
      data.at[i,'Test Case Failed']+=', 6'

    # Testcase 7 - Addressee or salutation contains "&" or "and" but it shows the Spouse as deceased
    # If SRinactive and inactive is yes skip this test
    df = data[(data['SRDeceased'].str.contains('Yes') == True) &
              (data['SRInactive'].str.contains('Yes') == True) &
              (data['IsInactive'] != 'Yes')]

    df = df[df['PrimAddText'].str.contains(" AND |&| and | And ")]
    data_7 = df[df['PrimSalText'].str.contains(" AND |&| and | And ")]
    ids = data_7.index.tolist()
    for i in ids:
        data.at[i, 'Test Case Failed'] += ', 7'

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


    # Testcase  10 - Spouse shows a deceased date, but inactive does not show yes. Does not equal to yes will pick up Blank and no.
    data_10 = data[(data['SRDeceasedDate']!='') & (df['SRInactive']!='Yes')]
    ids = data_10.index.tolist()
    for i in ids:
      data.at[i,'Test Case Failed']+=', 10'

    # Testcase  11 - Record shows a deceased date, but inactive does not show yes. Does not equal to yes will pick up Blank and no.
    data_11 = data[(data['DeceasedDate']!='') & (data['Inactive']!='Yes')]
    ids = data_11.index.tolist()
    for i in ids:
      data.at[i,'Test Case Failed']+=', 11'

    # Testcase  12 - There is a deceased date but  addressee or salutation contains "&" or "and" If Srinactive and inactive is yes skip this test
    df = data[(data['SRDeceasedDate']!='') & (data['SRInactive'].str.contains('Yes')==False)]
    df = df[df['PrimAddText'].str.contains("AND|&|and|And", na=False)]
    data_12 = df[df['PrimSalText'].str.contains("AND|&|and|And", na=False)]  
    ids = data_12.index.tolist()
    for i in ids:
      data.at[i,'Test Case Failed']+=', 12'

    # Testcase 13 - Spouse name information is filled in but marital status shows single. 
    df = data[((data['SRLastName'] != '') | (data['SRFirstName'] != ''))]
    data_13 = df[df['MrtlStat'] == 'single']
    ids = data_13.index.tolist()
    for i in ids:
      data.at[i,'Test Case Failed']+=', 13'

    # Testcase  14 -Marital status is blank but Addressee or salutation has "&" or "and". If there is Spouse name 
    # informationn they should be marked as "Partner" if they are not married but living together. 
    df = data[data['MrtlStat'] == '']
    df = df[df['PrimAddText'].str.contains("AND|&|and|And", na=False)]
    data_14 = df[df['PrimSalText'].str.contains("AND|&|and|And", na=False)]
    ids = data_14.index.tolist()
    for i in ids:
      data.at[i,'Test Case Failed']+=', 14'
    
    # Test case  15  Marital status does not reflect what is in the addressee/salutation i.e. widowed, but two people are in the add/sal, married but only one perosn is in add/sal
    df = data[data['MrtlStat'].str.contains("Widow|Divorced|Single")]
    data_15 = df[((df['PrimAddText'].str.contains(" AND |&| and | And ", na=False)) | (df['PrimSalText'].str.contains(" AND |&| and | And ", na=False))) & ~((df['IsInactive'] == 'Yes') | (df['Inactive'] == 'Yes') | (df['SRInactive'] == 'Yes'))]
    ids = data_15.index.tolist()
    for i in ids:
        data.at[i, 'Test Case Failed'] += ', 15'

    # # Total cases
    # failed = data[(data['Test Case Failed'] != '')]
    # passed = data[(data['Test Case Failed'] == '') | (data['Notes']=='Passed')]
    # failed.loc[:, 'Test Case Failed'] = failed['Test Case Failed'].str[1:]
    # failed = failed[(failed['Test Case Failed'] != '')]
    # Total cases

    failed = data[(data['Test Case Failed'] != '') & (data['Notes'] != 'Passed')].copy()
    passed = data[(data['Test Case Failed'] == '') | (data['Notes'] == 'Passed')].copy()
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

    # Drop Columns for importOmatic file
    impomatic = new.drop(columns = ['KeyInd', 'ConsCodeImpID', 'Nickname', 'Deceased', 
    'DeceasedDate', 'Inactive', 'SRSuff2', 'SRNickname', 'SRDeceased', 'SRDeceasedDate','SRInactive', 
    'PrimAddText', 'PrimSalText', 'AddrImpID', 'AddrType', 'AddrRegion', 'AddrSeasonal', 'AddrSeasFrom', 
    'AddrSeasTo', 'PhoneAddrImpID','PhoneImpID', 'PhoneType','DateTo', 'NameChanged', 'StreetChanged', 
    'MailingChanged', 'AltChanged', 'Test Case Failed', 'Notes']) #, 'AddrImpID.1', 'PhoneAddrImpID.1', 'PhoneImpID.1'])

    # Creates spouse column and fills in with Yes if 
    impomatic.insert(loc = 15, column='Spouse', value = '')
    impomatic.loc[(impomatic['SRLastName'] != ''),'Spouse'] = 'Yes'
    
    # creates country column anbd fills in
    impomatic.insert(loc = 17, column='Country', value = '')
    impomatic.loc[(impomatic['AddrCity'] != '') &  impomatic['AddrState'] != '', 'Country'] = 'United States'

    # Drop unwanted columns from Passed file
    redata = passed.drop(columns=['ImportID', 'ConsCodeImpID', 'Suff1', 'SRSuff2', 'SRInactive', 
    'AddrRegion','AddrImpID', 'AddrImpID', 'PhoneAddrImpID', 'PhoneImpID', 'PhoneAddrImpID', 
    'PhoneImpID', 'DateTo', 'SecondID', 'Test Case Failed', 'PrimAddText', 'PrimSalText',
    'NameChanged', 'StreetChanged', 'MailingChanged', 'AltChanged', 'Notes' ])

    # If ConsID contains *, remove the row - These are new records that are used for importOmatic
    redata = redata[~redata['ConsID'].str.contains("*", regex = False)].reset_index(drop=True)

    # Change Column Spelling to fit Raiser's Edge Import
    redata.rename(columns = {'DeceasedDate':'DecDate', 'SRDeceasedDate':'SRDecDate'}, inplace = True)

    # Add These Columns to a specific location
    # redata.insert(loc = 2, column='ConsCodeImpID', value = '')
    # redata.insert(loc = 4, column='ConsCodeDateFrom', value = '')
    # redata.insert(loc = 5, column='ConsCodeDateTo', value = '')

    # Change the absolute mess of Title 1 being used to fit Raiser's Edge
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

    # Fill in Gender based on title - I think this can be removed given Lines 27 - 45
    redata.loc[redata['Titl1'].eq('Mr.'), 'Gender'] = 'Male'
    redata.loc[redata['Titl1'].eq('Mrs.'), 'Gender'] = 'Female'
    redata.loc[redata['Titl1'].eq('Ms.'), 'Gender'] = 'Female'
    redata.loc[redata['Titl1'].eq('Miss'), 'Gender'] = 'Female'
    redata.loc[redata['SRTitl1'].eq('Mr.'), 'SRGender'] = 'Male'
    redata.loc[redata['SRTitl1'].eq('Mrs.'), 'SRGender'] = 'Female'
    redata.loc[redata['SRTitl1'].eq('Ms.'), 'SRGender'] = 'Female'
    redata.loc[redata['SRTitl1'].eq('Miss'), 'SRGender'] = 'Female'

    # Check Gender Change Gender Based on Title
    redata.loc[redata['Titl1'].eq('Mr.') & (redata['Gender'].str.contains('Unknown|Home ')), 'Gender'] = 'Male'
    redata.loc[redata['Titl1'].eq('Mrs.') & (redata['Gender'].str.contains('Unknown|Home ')), 'Gender'] = 'Female'
    redata.loc[redata['Titl1'].eq('Ms.') & (redata['Gender'].str.contains('Unknown|Home ')), 'Gender'] = 'Female'
    redata.loc[redata['Titl1'].eq('Miss') & (redata['Gender'].str.contains('Unknown|Home ')), 'Gender'] = 'Female'
    redata.loc[redata['SRTitl1'].eq('Mr.') & (redata['SRGender'].str.contains('Unknown|Home ')), 'SRGender'] = 'Male'
    redata.loc[redata['SRTitl1'].eq('Mrs.') & (redata['SRGender'].str.contains('Unknown|Home ')), 'SRGender'] = 'Female'
    redata.loc[redata['SRTitl1'].eq('Ms.') & (redata['SRGender'].str.contains('Unknown|Home ')), 'SRGender'] = 'Female'
    redata.loc[redata['SRTitl1'].eq('Miss') & (redata['SRGender'].str.contains('Unknown|Home ')), 'SRGender'] = 'Female'


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
    
    # Replaces instacnes where state is in the same cell as city. 
    redata[['AddrCity', 'State_Holder']] = redata['AddrCity'].str.replace(', ', ' ').str.replace(' ', ', ').str.split(', ', 1, expand = True)
    redata['AddrState'] = np.where(redata['AddrState'].isna(), redata['State_Holder'], redata['AddrState'])
    redata = redata.drop(columns = ['State_Holder'])

    # Clean addresses in redata
    def normalizeredata(redata):
        redata = redata.copy()
        redata['AddrLines'] = redata['AddrLines'].str.replace('Apartment ','Apt ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Apt\\.','Apt ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('APT','Apt ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('nApt','Apt ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('NApt','Apt ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Avenue','Ave ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Ave\\.','Ave ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Boulevard','Blvd ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Blvd.','Blvd ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Building','Bldg ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Bldg\\.','Bldg ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Center','Ctr ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Ctr\\.','Ctr ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Circle','Cir ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Cir\\.','Cir ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Court','Ct ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Ct\\.','Ct ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Drive','Dr ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Dr\\.','Dr ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('East','E ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('E\\.','E ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Expressway','Expy ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Expy\\.','Expy ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Extension','Ext ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Ext\\.','Ext ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Fort','Ft ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Ft\\.','Ft ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Freeway','Fwy ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Fwy\\.','Fwy ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Height','Hts ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Hts\\.','Hts ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Highway','Hwy ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Hwy\\.','Hwy ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Island','Is ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Is\\.','Is ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Junction','Jct ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Jct\\.','Jct ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Lane','Ln ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Ln\\.','Ln ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Mount','Mt ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Mt\.','Mt ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Mountain','St ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Mt\\.','Mt ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('North','N ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('N\\.','N ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Northeast','NE ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('NE\\.','NE ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Northwest','NW ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('NW\\.','NW',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Parkway','Pky ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Pky\\.','Pky ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Place','Pl ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Pl\\.','Pl ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Post Office','PO ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('PO\\.','PO ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('P\\.O','PO ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('P\\.O\\.','PO ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Ridge','Rdg ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Road','Rd ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Rd\\.','Rd ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('ROAD','Rd ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Rural Delivery','RD ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('RD\\.','RD ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Rural Route','RR ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('RR\\.','RR ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Saint','St ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('St\\.','St ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('South','S ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('S\\.','S ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Southeast','SE ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('SE\\.','SE',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Southwest','SW ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('SW\\.','SW ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Spring','Spg ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Spg\\.','Spg ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Springs','Spgs  ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Spg\\.','Spgs ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Square','Sq ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Sq\\.','Sq ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Squares','Sq ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Sq\\.','Sq ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Street','St ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('St\\.','St ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Suite','Ste ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Ste\\.','Ste ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Terrace','Ter ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Ter\\.','Ter ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Turnpike','Tpke ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('Tpke\\.','Tpke ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('UNIT.','Unit ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('LOT','Tpke ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('West','W ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('west','W ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace(',',' ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('\\.','',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('-',' ',regex=True)
        redata['AddrLines'] = redata['AddrLines'].str.replace('\\/n',' ',regex=True)
        return redata
    renew = normalizeredata(redata)

    # Clean addresses in impomatic - tried to do this before parsing out ImportOmatic file, but caused more trouble than was worth. 
    def normalizeimpomatic(impomatic):
        impomatic = impomatic.copy()
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Apartment ','Apt ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Apt\\.','Apt ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('APT','Apt ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('nApt','Apt ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('NApt','Apt ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Avenue','Ave ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Ave\\.','Ave ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Boulevard','Blvd ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Blvd.','Blvd ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Building','Bldg ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Bldg\\.','Bldg ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Center','Ctr ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Ctr\\.','Ctr ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Circle','Cir ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Cir\\.','Cir ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Court','Ct ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Ct\\.','Ct ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Drive','Dr ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Dr\\.','Dr ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('East','E ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('E\\.','E ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Expressway','Expy ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Expy\\.','Expy ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Extension','Ext ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Ext\\.','Ext ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Fort','Ft ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Ft\\.','Ft ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Freeway','Fwy ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Fwy\\.','Fwy ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Height','Hts ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Hts\\.','Hts ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Highway','Hwy ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Hwy\\.','Hwy ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Island','Is ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Is\\.','Is ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Junction','Jct ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Jct\\.','Jct ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Lane','Ln ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Ln\\.','Ln ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Mount','Mt ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Mt\.','Mt ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Mountain','St ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Mt\\.','Mt ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('North','N ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('N\\.','N ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Northeast','NE ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('NE\\.','NE ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Northwest','NW ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('NW\\.','NW',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Parkway','Pky ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Pky\\.','Pky ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Place','Pl ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Pl\\.','Pl ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Post Office','PO ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('PO\\.','PO ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('P\\.O','PO ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('P\\.O\\.','PO ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Ridge','Rdg ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Road','Rd ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Rd\\.','Rd ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('ROAD','Rd ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Rural Delivery','RD ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('RD\\.','RD ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Rural Route','RR ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('RR\\.','RR ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Saint','St ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('St\\.','St ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('South','S ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('S\\.','S ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Southeast','SE ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('SE\\.','SE',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Southwest','SW ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('SW\\.','SW ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Spring','Spg ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Spg\\.','Spg ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Springs','Spgs  ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Spg\\.','Spgs ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Square','Sq ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Sq\\.','Sq ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Squares','Sq ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Sq\\.','Sq ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Street','St ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('St\\.','St ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Suite','Ste ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Ste\\.','Ste ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Terrace','Ter ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Ter\\.','Ter ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Turnpike','Tpke ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('Tpke\\.','Tpke ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('UNIT.','Unit ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('LOT','Tpke ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('West','W ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('west','W ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace(',',' ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('\\.','',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('-',' ',regex=True)
        impomatic['AddrLines'] = impomatic['AddrLines'].str.replace('\\/n',' ',regex=True)
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
def main(base_dir: Path) -> None:

    print(f'Processing files in {base_dir}: \n')

    n_process = 0
    for csv_file in base_dir.glob('*.csv'):
        
        # ex. csv_file = "/users/path/my_file.csv"
        
        name: str = csv_file.stem   # name = "my_file"
        reimportfiles: str = 'REImportFiles'
        
        output_dir: Path = base_dir / name  # output_dir = "/users/path/my_file"
        reout_dir: Path = base_dir / name / output_dir / reimportfiles

        print(f'Creating directory "{output_dir}"')
        Path.mkdir(output_dir, exist_ok=True)

        print(f'Creating directory "{reout_dir}"')
        Path.mkdir(reout_dir, exist_ok=True)

        print(f'Processing "{csv_file}"')
        process(csv_file=csv_file, out_dir=output_dir, re_dir=reout_dir)

        print(f'Completed processing\n')
        n_process += 1

    print(f'\nProcessed {n_process} files')

if __name__ == '__main__':
    root = get_root()  # root = "users/path"
    main(base_dir=root)
