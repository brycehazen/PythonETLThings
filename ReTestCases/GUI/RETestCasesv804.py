import tkinter as tk
from tkinter import filedialog
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
    # Create array to track failed cases.
    data['Test Case Failed']= ''
    data = data.replace(np.nan,'')
    data.insert(0, 'ID', range(0, len(data)))
    
    # Change blank Gender on title
    AllRETitl1s = ['Dr.', 'The Honorable', 'Col.', 'Cmsgt. Ret.', 'Rev. Mr.', 'Deacon', 'Judge', 
                'Lt. Col.', 'Col. Ret.', 'Major', 'Capt.', 'Maj. Gen.', 'Family of', 'Senator', 'Reverend', 
                'Lt.', 'Cmdr.', 'Msgt.', 'Sister', 'Drs.', 'Master', 'Sgt. Maj.', 'SMSgt.', 'Prof.', 'Lt. Col. Ret.', 'Rev. Dr.', 
                'Father', 'Brother', 'Bishop', 'Gen.', 'Admiral', 'Very Reverend', 'MMC', 'Monsignor', '1st Lt.', 'Reverend Monsignor', 
                'Maj.', 'Most Reverend', 'Bishop Emeritus','Mrs.', 'Mr.', 'Ms.', 'Miss','Sr.', 'Family of']
    # Fixing Titles: 
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

    # Change blank Titles based of Gender
    data.loc[(data['Titl1'] == '') & (data['Gender'] == 'Male'), 'Titl1'] = 'Mr.'
    data.loc[(data['Titl1'] == '') & (data['SRLastName'] == 'LastName') & (data['Gender'] == 'Female'), 'Titl1'] = 'Mrs.'
    data.loc[(data['Titl1'] == '') & (data['SRLastName'] != 'LastName') & (data['Gender'] == 'Female'), 'Titl1'] = 'Ms.'
    # Change blank SRTitles based of Gender
    data.loc[(data['SRTitl1'] == '') & (data['SRGender'] == 'Male'), 'SRTitl1'] = 'Mr.'
    data.loc[(data['SRTitl1'] == '') & (data['SRLastName'] == 'LastName') & (data['SRGender'] == 'Female'), 'SRTitl1'] = 'Mrs.'
    data.loc[(data['SRTitl1'] == '') & (data['SRLastName'] != 'LastName') & (data['SRGender'] == 'Female'), 'SRTitl1'] = 'Ms.'

    strictly_male_titles = ['Rev. Mr.', 'Deacon', 'Father', 'Brother', 'Monsignor', 'Reverend Monsignor', 'Mr.']
    strictly_female_titles = ['Mrs.', 'Miss', 'Sister', 'Ms.']

    data.loc[(data['Gender'] == '') & (data['Titl1'].isin(strictly_male_titles)), 'Gender'] = 'Male'
    data.loc[(data['Gender'] == '') & (data['Titl1'].isin(strictly_female_titles)), 'Gender'] = 'Female'
    data.loc[(data['SRGender'] == '') & (data['SRTitl1'].isin(strictly_male_titles)), 'SRGender'] = 'Male'
    data.loc[(data['SRGender'] == '') & (data['SRTitl1'].isin(strictly_female_titles)), 'SRGender'] = 'Female'

    # SRGender is female, SRTitl1 is one of 'Ms.', 'Miss', 'Mrs.', Gender is unknown, then changed Titl1 and gender to Mr. Male 
    data.loc[(data['SRGender'] == 'Female') & (data['SRTitl1'].isin(['Ms.', 'Miss', 'Mrs.'])) & (data['Gender'] == 'Unknown'), ['Gender', 'Titl1']] = ['Male', 'Mr.']
    # SRGender is unknown, gender is male, Titl1 is Mr., SRlastname is same as Last name, SRTitl1 is blank, then change SRTitl1 and SRGender to Mrs. Female
    data.loc[(data['SRGender'] == 'Unknown') & (data['Gender'] == 'Male') & (data['Titl1'] == 'Mr.') & (data['SRLastName'] == data['LastName']) & (data['SRTitl1'] == ''), ['SRTitl1', 'SRGender']] = ['Mrs.', 'Female']
    # SRGender is unknown, gender is male, Titl1 is Mr., SRlastname is not the as Last name, SRTitl1 is blank, then change SRTitl1 and SRGender to Mrs. Female
    data.loc[(data['SRGender'] == 'Unknown') & (data['Gender'] == 'Male') & (data['Titl1'] == 'Mr.') & (data['SRLastName'] != data['LastName']) & (data['SRTitl1'] == ''), ['SRTitl1', 'SRGender']] = ['Ms.', 'Female']

    # Change MrtlStat based off Gender or change to one used in RE
    data.loc[(data['MrtlStat'].isnull()) & (data['PrimAddText'].str.contains('&| and ', na=False)) & (data['LastName'] == data['SRLastName']),'MrtlStat'] = 'Married'
    data.loc[(data['MrtlStat'].str.contains('Religion|Civilly|Church Married|Church Marriage|Civil/Other', na=False)),'MrtlStat'] = 'Married'
    data.loc[(data['MrtlStat'].str.contains('Never|Not Married|Cohabitating|Co-Habitating|Partner', na=False)),'MrtlStat', ] = 'Single'
    data.loc[(data['MrtlStat'].str.contains('Unknown', na=False)),'MrtlStat'] = ''
    data.loc[(data['MrtlStat'].str.contains('Deceased|Widow/Er|Widow', na=False)),'MrtlStat'] = 'Widowed'
    data.loc[(data['MrtlStat'].str.contains('Separated', na=False)),'MrtlStat'] = 'Divorced'
    data.loc[(data['MrtlStat'].str.contains('Invalid Marriage', na=False)),'MrtlStat'] = 'Married'
    data.loc[(data['MrtlStat'].str.contains('Valid Marriage', na=False)),'MrtlStat'] = 'Married'
    data.loc[(data['MrtlStat'].str.contains('Head', na=False)),'MrtlStat'] = 'Married'

    # Testcase 1 - Both genders are Male but addressee or salutation contains Ms. or Mrs.
    def check_gender_and_salutation(row):
        if (row['Gender'] == 'Male') and (row['SRGender'] == 'Male') and \
        (('Ms' in row['PrimAddText']) or ('Mrs' in row['PrimAddText']) or
            ('Ms' in row['PrimSalText']) or ('Mrs' in row['PrimSalText'])) and \
        (row['SRDeceased'] != 'Yes'):
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
    def check_marital_status_and_addsal(row):
        if ("Widow" in row['MrtlStat'] or "Divorced" in row['MrtlStat'] or "Single" in row['MrtlStat']) and ((any(substring in row['PrimAddText'] for substring in [' AND ', '&', ' and ', ' And ']) or any(substring in row['PrimSalText'] for substring in [' AND ', '&', ' and ', ' And '])) and not any(row[val] == 'Yes' for val in ['IsInactive', 'Inactive', 'SRInactive'])):
            return row['Test Case Failed'] + ', 15'
        else:
            return row['Test Case Failed']

    data['Test Case Failed'] = data.apply(check_marital_status_and_addsal, axis=1)
    
                               ########vvvvvThis is Test case 16 Not in use yetvvvvv########
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
                                ########^^^^^This is Test case 16 Not in use yet^^^^^########

    failed = data[(data['Test Case Failed'] != '') & (data['NameIsCorrect'] != 'Yes')].copy()
    passed = data[(data['Test Case Failed'] == '') | (data['NameIsCorrect'] == 'Yes')].copy()
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

    # Columns to drop from new which becomes importOmatic
    columns_to_drop_impomatic = ['KeyInd', 'ConsCodeImpID', 'Nickname', 'Deceased', 
                    'DeceasedDate', 'Inactive', 'SRSuff2', 'SRNickname', 'SRDeceased', 
                    'SRDeceasedDate', 'SRInactive', 'PrimAddText', 'PrimSalText', 
                    'AddrImpID', 'AddrType', 'AddrRegion', 'AddrSeasonal', 'AddrSeasFrom', 
                    'AddrSeasTo', 'PhoneAddrImpID', 'PhoneImpID', 'PhoneType', 'DateTo', 
                    'NameChanged', 'StreetChanged', 'MailingChanged', 'AltChanged', 
                    'Test Case Failed', 'Notes', 'DateReg']

    # Check if column exists in 'new' dataframe before dropping
    columns_to_drop_impomatic_existing = [col for col in columns_to_drop_impomatic if col in new.columns]

    # Drop the columns from the 'new' dataframe
    impomatic = new.drop(columns=columns_to_drop_impomatic_existing)

    # Columns to drop for the passed dataframe which becomes redata
    columns_to_drop_passed = ['ImportID', 'ConsCodeImpID', 'Suff1', 'SRSuff2', 'SRInactive', 
                            'AddrRegion', 'AddrImpID', 'AddrImpID', 'PhoneAddrImpID', 'PhoneImpID', 
                            'PhoneAddrImpID', 'PhoneImpID', 'DateTo', 'SecondID', 'Test Case Failed', 
                            'PrimAddText', 'PrimSalText', 'NameChanged', 'StreetChanged', 
                            'MailingChanged', 'AltChanged', 'Notes', 'Inactive', 'NameIsCorrect', 
                            'AddrImpID.1', 'AddrImpID.2', 'PhoneAddrImpID.1', 'PhoneImpID.1', 'DateReg']

    # Check if column exists in 'passed' dataframe before dropping
    columns_to_drop_passed_existing = [col for col in columns_to_drop_passed if col in passed.columns]

    # Drop the columns from the 'passed' dataframe
    redata = passed.drop(columns=columns_to_drop_passed_existing)

    # Creates spouse column and fills in with Yes if 
    impomatic.insert(loc = 15, column='Spouse', value = '')
    impomatic.loc[(impomatic['SRLastName'] != ''),'Spouse'] = 'Yes'
    
    # creates country column anbd fills in
    impomatic.insert(loc = 17, column='Country', value = '')
    impomatic.loc[(impomatic['AddrCity'] != '') &  impomatic['AddrState'] != '', 'Country'] = 'United States'

    # Drop unwanted columns from Passed file


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

        # Create a regex pattern to match any state abbreviation from the list
        pattern = r'(?P<City>.*?)(?:,? (?P<State>[A-Z]{2}))?$'
        pattern = pattern.replace('[A-Z]{2}', '|'.join(state_abbreviations))

        # Extract city and state from the AddrCity column
        redata[['AddrCity', 'State_Holder']] = redata['AddrCity'].str.extract(pattern)

        # Fill NaN values in the AddrState column with values from the State_Holder column
        redata['AddrState'] = np.where(redata['AddrState'].isna(), redata['State_Holder'], redata['AddrState'])

        # Drop the temporary State_Holder column
        redata.drop(columns=['State_Holder'], inplace=True)

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

def main(input_dir: Path, output_dir: Path) -> None:
    print(f'Processing files in {input_dir}: \n')

    n_process = 0
    for csv_file in input_dir.glob('*.csv'):
                # ex. csv_file = "/users/path/my_file.csv"
        
        name: str = csv_file.stem   # name = "my_file"
        reimportfiles: str = 'REImportFiles'
        
        output_dir: Path = output_dir / name  # output_dir = "/users/path/my_file"
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
