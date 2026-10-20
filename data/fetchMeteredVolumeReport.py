import json, requests
from getpass import getpass

url = "https://apimgw.aeso.ca/public/meteredvolume-api/v1/meteredvolume/details"
headers = {"API-KEY": input("Paste your AESO API key: ").strip()}
params = {"startDate": "2023-01-01", "endDate": "2023-01-17"}

r = requests.get(url, headers=headers, params=params, timeout=120)
print("Status:", r.status_code)

print("Status:", r.status_code)
raw = r.json()

if r.status_code != 200:
    print("AESO says:", raw.get("message"))
    raise SystemExit()

with open("metered_volume_jan2023_raw.json", "w") as f:
    json.dump(raw, f, indent=2)

first = raw["return"][0]
first["asset_list"] = first["asset_list"][:2]
for a in first["asset_list"]:
    a["metered_volume_list"] = a["metered_volume_list"][:3]
print(json.dumps(first, indent=2))
print("Number of participants:", len(raw["return"]))