## Table of Contents for Parish Sync Process - No new records

- [Features](#features)
- [Scripts details](#scripts-details)
- [Overview](#overview)
- [removePhones script](#removephones-script)
- [combineExceptions script](#combineexceptions-script)

## Features
- **Removing Phone Numbers**: 
  - `removePhones.py` will look at `RE_data.csv` and compare `PhoneConsID.csv`.  `PhoneConsID.csv` is a collection pulled from SQL of all Phones in RE. If the Phone is already in RE and found in `RE_Data.csv`, it will get removed and output `updated_RE_Data.csv`. This is will be your import file for Raiser's Edge. With duplicate phone numbers removed from your import file, less exceptions will be created. 
  - If a record and Phone is not found in `PhoneConsID.csv`, but it caused an exception and was put into `RE_DataWithExceptions.csv`, the script will add it to `PhoneConsID.csv`. This will result in the record not causing an exception in the future.
- **Tracking Exceptions**: 
  - After importing records, RE creates a New Import Control-Summary Report - This saved as a csv will be combined with `RE_Data.csv` to output `RE_DataWithExceptions.csv`
  - This will have have the data from `updated_RE_Data.csv` combined with the reason it was not imported. This will make it easier to know what needs to be corrected as well as track what and why records were not Imported.
- **Not Yet added**:
  - Soon I will add an additional part of the script to update constituency codes. This will invlove taking the query created from importing, exporting it back out with all the records ConsCode. Then comparing this ConsCode export to `RE_data.csv`

## Scripts details
- **Summary**:
- This repository contains two Python scripts for data manipulation. For this two work, it is split into two scripts. One is ran before and the other after importing into Rasier's Edge.
- **Scripts used**:
- `removePhones.py`: BEFORE importing into Raiser's Edge, this filters and removes phone-related entries from `RE_Data.csv` based on the data in `PhoneConsID.csv`
- `CombineExceptions.py`: AFTER improting into Raiser's Edge, "New Import Control-Summary Report" is created and needs to be saved as `New Import Control-Summary Report.csv` this then appends them to `updated_RE_Data.csv` outputting `RE_DataWithExceptions.csv`.

## Overview 
- **You will need two csv files to start**:
1. `RE_data.csv` - This comes from [ReTestCases](https://github.com/brycehazen/PythonETLThings/tree/main/ReTestCases)
2. `PhoneConsID.csv` - This comes from SQL and has all Phones/Emails currently in Raiser's Edge.
- **Genral Steps**:
1. Place both csv listed above into the same folder as both scripts, as well as any other csv generated throughout the process. 
2. Run `removePhones.py` - This will output `updated_RE_Data.csv`.
3. Import `updated_RE_Data.csv` into RE ensuring "Import Control-Summary Report" is created and saved as a csv.
4. Run `CombineExceptions.py` - This will output `updated_RE_DataWithExceptions.csv`
5. Run `removePhones.py` once more to update `PhoneConsID.csv` with any new phone numbers that weren't already in `PhoneConsID.csv`
6. Fix exceptions in `updated_RE_DataWithExceptions.csv` and import until all exceptions have cleared
---

## removePhones script
**Description**:
1. This script checks for `updated_RE_DataWithExceptions.csv` and, if found, extracts specific phone-related errors to append them to `PhoneConsID.csv`.
2. It then reads `RE_Data.csv` and removes phone entries that match those in `PhoneConsID.csv`. A match is found if the phone/email + ConsID are matched in `PhoneConsID.csv`
4. The updated data is saved to `updated_RE_Data.csv`.
5. This script should be ran one more time after running `CombineExceptions.py` since this produces `updated_RE_DataWithExceptions.csv` and updates `PhoneConsID.csv` with phone/emails not found the first time. 

**Usage**:
```bash
python CombineExceptions.py
```
**Note:** Ensure `RE_Data.csv`, `PhoneConsID.csv`, and optionally `updated_RE_DataWithExceptions.csv`are present in the working directory before executing the script.

---

## combineExceptions script

**Description**:
1. This script reads data from `New Import Control-Summary Report.csv` and `updated_RE_Data.csv`.
2. Then combines specific exceptions from `New Import Control-Summary Report.csv` with  `updated_RE_Data.csv`. The combined data is saved to `updated_RE_DataWithExceptions.csv`.
3. This script does what the exception file created from the import process should already do. Giving you the record and the reason it was not imported in one file. Rasier's Edge is stupid in a lot of ways. 

**Usage**:
```bash
python CombineExceptions.py
```
**Note:** Ensure both `New Import Control-Summary Report.csv` and `updated_redata.csv` are present in the working directory before executing the script. You should already ran `removePhones.py` and finihsed importing to Raiser's Edge before this is ran

---



## Dependencies

Both scripts require the `pandas` library. Ensure it's installed before executing the scripts.

```bash
pip install pandas
```

---
