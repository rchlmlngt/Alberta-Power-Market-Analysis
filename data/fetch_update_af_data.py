#%%
import requests
from io import StringIO
import pandas as pd
from datetime import datetime, timedelta

# Note: this report returns at most 31 days per request
file = 'ActualForecastData.csv'
url = "http://ets.aeso.ca/ets_web/ip/Market/Reports/ActualForecastWMRQHReportServlet"
headers = {"User-Agent": "Mozilla/5.0"}

def fetch(begin, end):
    '''
    Fetch data from AESO website and return a clean dataframe
    :param begin: start date MMDDYYYY
    :param end: end date MMDDYYYY
    :return: cleaned dataFrame
    '''
    params = {
            "beginDate"  : begin,
            "endDate"    : end,
            "contentType": "html"}
    r = requests.get(url, params=params, headers=headers)
    r.raise_for_status()
    tables = pd.read_html(StringIO(r.text))
    df = tables[1] # This table contains the actual data

    # Rename to clean, code-friendly column names
    df = df.rename(columns={
        "Date (HE)": "date_he",
        "Forecast Pool Price": "forecast_price",
        "Actual Posted Pool Price": "actual_price",
        "Forecast AIL": "forecast_ail",
        "Actual AIL": "actual_ail",
        "Forecast AIL & Actual AIL Difference": "ail_diff",
        })

    ########################### Clean Data ##################################
    parts = df["date_he"].str.strip().str.split(" ", expand=True) # Split "05/21/2026 21" into date and hour parts
    date = pd.to_datetime(parts[0], format="%m/%d/%Y") # Convert each part to its proper type
    he   = pd.to_numeric(parts[1], errors="coerce")
    # Note: hour-ending 24 rolls over to 00:00 of the next day (MM/DD becomes MM/DD+1)
    df["date_he"] = date + pd.to_timedelta(he, unit="h") # Recombine into one datetime

    return df

def update(file):
    '''
    Fetch recent data and merge it into existing CSV
    :param file: 'ActualForecastData.csv'
    '''
    existing = pd.read_csv(file, parse_dates=["date_he"])
    # Fetch from a few days before the last saved date (overlap for safety) up to now
    last_day = existing["date_he"].max()
    begin = (last_day - pd.Timedelta(days=3)).strftime("%m%d%Y")
    end = datetime.now().strftime("%m%d%Y")
    new = fetch(begin, end)

    # Combine old + new, then clean
    ActualForecastData = pd.concat([existing, new], ignore_index=True)
    ActualForecastData = ActualForecastData.sort_values("date_he").reset_index(
        drop=True)  # Sort chronologically by date
    ActualForecastData = ActualForecastData.drop_duplicates(subset=["date_he"],
                                                            keep="last")  # Keep only unique rows, drop duplicated rows
    ActualForecastData = ActualForecastData.dropna(subset=['date_he']).reset_index(
        drop=True)  # Re-index after dropping duplicated rows and NaT rows

    # Save back to the same CSV
    ActualForecastData.to_csv(file, index=False)

    # Report what happened
    added = len(ActualForecastData) - len(existing)
    print(ActualForecastData.info())
    print(f"Updated from {begin}. Added {added} new rows. Total now {len(ActualForecastData)}.")

if __name__ == "__main__":
    update(file)
