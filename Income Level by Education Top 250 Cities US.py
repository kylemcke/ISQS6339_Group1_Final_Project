# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 15:20:52 2025

@author: mike5
"""

import requests
import pandas as pd
import os

# === Step 1: Pull population so we can rank top 250 ===
URL_POP = "https://api.census.gov/data/2023/acs/acs1/subject"
params_pop = {
    "get": "NAME,S0101_C01_001E,STATE,PLACE",
    "for": "place:*",
    "in": "state:*"
}
resp_pop = requests.get(URL_POP, params=params_pop)
resp_pop.raise_for_status()
rows_pop = resp_pop.json()
df_pop = pd.DataFrame(rows_pop[1:], columns=rows_pop[0])
df_pop["S0101_C01_001E"] = pd.to_numeric(df_pop["S0101_C01_001E"], errors="coerce")

# Sort by population and keep top 250
df_pop = df_pop.sort_values("S0101_C01_001E", ascending=False)
top250 = df_pop.head(250).copy()
top250["GEOID"] = top250["STATE"] + top250["PLACE"]

# === Step 2: Pull income by education from S2001 ===
URL_INC = "https://api.census.gov/data/2023/acs/acs1/subject"
params_inc = {
    "get": (
        "NAME,"
        "S2001_C01_001E,"  # All workers 25+
        "S2001_C01_002E,"  # <HS graduate
        "S2001_C01_003E,"  # HS graduate (includes equivalency)
        "S2001_C01_004E,"  # Some college or associate's
        "S2001_C01_005E,"  # Bachelor's
        "S2001_C01_006E,"  # Graduate/professional
        "STATE,PLACE"
    ),
    "for": "place:*",
    "in": "state:*"
}
resp_inc = requests.get(URL_INC, params=params_inc)
resp_inc.raise_for_status()
rows_inc = resp_inc.json()
df_inc = pd.DataFrame(rows_inc[1:], columns=rows_inc[0])
df_inc["GEOID"] = df_inc["STATE"] + df_inc["PLACE"]

# === Step 3: Merge population + income, filter to top 250 ===
merged = pd.merge(top250, df_inc, on="GEOID", suffixes=("_pop", "_inc"))

# Convert income columns to numeric
inc_cols = [
    "S2001_C01_001E","S2001_C01_002E","S2001_C01_003E",
    "S2001_C01_004E","S2001_C01_005E","S2001_C01_006E"
]
for c in inc_cols:
    merged[c] = pd.to_numeric(merged[c], errors="coerce")

# === Step 4: Rename for clarity ===
final = merged.rename(columns={
    "NAME_pop": "City",
    "S0101_C01_001E": "Total_Pop_All_Ages",
    "S2001_C01_001E": "MedianEarnings_AllWorkers25plus",
    "S2001_C01_002E": "MedianEarnings_LessThan_HS",
    "S2001_C01_003E": "MedianEarnings_HS_Graduate",
    "S2001_C01_004E": "MedianEarnings_SomeCollege_or_Associates",
    "S2001_C01_005E": "MedianEarnings_Bachelors",
    "S2001_C01_006E": "MedianEarnings_Graduate_or_Professional"
})

# === Step 5: Save to Excel ===
save_dir = r"C:\Users\mike5\OneDrive\Desktop\ACS Census Data Pulls"
os.makedirs(save_dir, exist_ok=True)
save_path = os.path.join(save_dir, "acs2023_top250_income_by_education_level.xlsx")

final.to_excel(save_path, index=False, sheet_name="IncomeByEducation")

print(f"\n✅ Saved Excel file to {save_path}")
print(final.head(10))
