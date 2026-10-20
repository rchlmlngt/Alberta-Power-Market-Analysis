import json
import requests
import pandas as pd

url = "https://apimgw.aeso.ca/public/aiesgencapacity-api/v1/AIESGenCapacity"
headers = {"API-KEY": input("Paste your AESO API key: ").strip()}
params = {"startDate": "2023-01-01", "endDate": "2023-01-31"}

r = requests.get(url, headers=headers, params=params, timeout=120)
print("Status:", r.status_code)
raw = r.json()

if r.status_code != 200:
    print("AESO says:", raw.get("message"))
    raise SystemExit()

# Save the full raw response
with open("gen_capacity_jan2023_raw.json", "w") as f:
    json.dump(raw, f, indent=2)

# Show the structure: top-level keys and the first record
body = raw.get("return", raw)
print("Top-level keys:", list(raw.keys()))
print("Type of 'return':", type(body).__name__)
first = body[0] if isinstance(body, list) else body
print(json.dumps(first, indent=2)[:2000])   # first record, cut off at 2000 characters

# Flatten into a CSV (works if records are flat; if nested, we'll adjust after seeing the output)
df = pd.json_normalize(body if isinstance(body, list) else [body])
df.to_csv("gen_capacity_jan2023.csv", index=False)
print("\nShape:", df.shape)
print("Columns:", list(df.columns))
print(df.head(10))