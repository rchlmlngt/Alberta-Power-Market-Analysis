
import pandas as pd

data20230106 = pd.read_csv('CSD_Generation_(Hourly)202301_to_202306.csv')
data20230712 = pd.read_csv('CSD_Generation_(Hourly)202307_to_202312.csv')
data20240106 = pd.read_csv('CSD_Generation_(Hourly)202401_to_202406.csv')
data20240712 = pd.read_csv('CSD_Generation_(Hourly)202407_to_202412.csv')
data20250106 = pd.read_csv('CSD_Generation_(Hourly)202501_to_202506.csv')
data20250712 = pd.read_csv('CSD_Generation_(Hourly)202507_to_202512.csv')
data20260106 = pd.read_csv('CSD_Generation_(Hourly)202601_to_202606.csv')

cols = ['Date (MPT)', 'Asset Short Name', 'Volume', 'Maximum Capability', 'Fuel Type', 'Sub Fuel Type']

supply_Data = pd.concat([data20230106[cols], data20230712[cols], data20240106[cols], data20240712[cols],
                         data20250106[cols], data20250712[cols],data20260106[cols]],ignore_index=True)
# 1. Clean and rename columns to be SQL-friendly
rename_map = {
    'Date (MPT)': 'date_mpt_he',
    'Asset Short Name': 'asset_short_name',
    'Volume': 'volume',
    'Maximum Capability': 'max_capability',
    'Fuel Type': 'fuel_type',
    'Sub Fuel Type': 'sub_fuel_type'
}
supply_Data = supply_Data.rename(columns=rename_map)

# 2. Ensure the date column is a real datetime object for SQL
# Convert hours to follow hour ending convention, so 00 stands in for 24
dateTime = pd.to_datetime(supply_Data['date_mpt_he'])
supply_Data['date_mpt_he'] = dateTime + pd.Timedelta(hours=1)

supply_Data.to_csv('supply_data.csv', index=False)
