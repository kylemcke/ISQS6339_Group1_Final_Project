# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 14:40:50 2025

@author: mike5
"""

import requests
import pandas as pd
import os

# === Step 1: Query Census API for population + education counts ===
URL = "https://api.census.gov/data/2023/acs/acs1/subject"
params = {
    "get": (
        "NAME,"
        "S0101_C01_001E,"  # Total population (all ages)
        "S1501_C01_009E,"  # <9th
        "S1501_C01_010E,"  # 9–12 no diploma
        "S1501_C01_011E,"  # HS graduate
        "S1501_C01_012E,"  # Some college
        "S1501_C01_013E,"  # Associate's
        "S1501_C01_014E,"  # Bachelor's
        "S1501_C01_015E,"  # Grad/prof
        "STATE,PLACE"
    ),
    "for": "place:*",
    "in": "state:*"
}
resp = requests.get(URL, params=params)
resp.raise_for_status()
rows = resp.json()

df = pd.DataFrame(rows[1:], columns=rows[0])

# === Step 2: Convert numeric columns ===
num_cols = [
    "S0101_C01_001E",
    "S1501_C01_009E","S1501_C01_010E","S1501_C01_011E",
    "S1501_C01_012E","S1501_C01_013E","S1501_C01_014E","S1501_C01_015E"
]
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")

# === Step 3: Sort by population and keep top 250 ===
df = df.sort_values("S0101_C01_001E", ascending=False)
top250 = df.head(250).copy()

# === Step 4: Rename columns for clarity ===
top250 = top250.rename(columns={
    "NAME": "City",
    "S0101_C01_001E": "Total_Pop_All_Ages",
    "S1501_C01_009E": "Count_Less_than_9th",
    "S1501_C01_010E": "Count_9th_to_12th_no_diploma",
    "S1501_C01_011E": "Count_HS_Graduate",
    "S1501_C01_012E": "Count_Some_College_no_degree",
    "S1501_C01_013E": "Count_Associates",
    "S1501_C01_014E": "Count_Bachelors",
    "S1501_C01_015E": "Count_Graduate_or_Professional"
})

# === Step 5: Calculate percentages from counts ===
categories = [
    "Less_than_9th","9th_to_12th_no_diploma","HS_Graduate",
    "Some_College_no_degree","Associates","Bachelors","Graduate_or_Professional"
]

# Denominator = sum of all education counts
top250["Total_Pop_25plus_calc"] = (
    top250[[
        "Count_Less_than_9th",
        "Count_9th_to_12th_no_diploma",
        "Count_HS_Graduate",
        "Count_Some_College_no_degree",
        "Count_Associates",
        "Count_Bachelors",
        "Count_Graduate_or_Professional"
    ]].sum(axis=1)
)

for cat in categories:
    top250[f"Pct_{cat}"] = (
        top250[f"Count_{cat}"] / top250["Total_Pop_25plus_calc"] * 100
    ).round(2)

# Add total % check
pct_cols = [f"Pct_{c}" for c in categories]
top250["Pct_Total_Check"] = top250[pct_cols].sum(axis=1).round(2)

# === Step 6: Save as Excel ===
save_dir = r"C:\Users\mike5\OneDrive\Desktop\ACS Census Data Pulls"
os.makedirs(save_dir, exist_ok=True)
save_path = os.path.join(save_dir, "acs2023_top250_cities.xlsx")

top250.to_excel(save_path, index=False, sheet_name="Top250_Cities")

print(f"\n✅ Saved Excel file to {save_path}")
print(top250.head(10))


