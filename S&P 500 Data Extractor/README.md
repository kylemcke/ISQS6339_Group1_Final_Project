# S&P 500 FY2023 metrics from SEC CompanyFacts

## What this does
- Reads your S&P 500 list from:
  `C:\Users\kylew\OneDrive\Documents\Education\ISQS 6339 - Business Intelligence\BI Project\sp500_companies.csv`
- For each company, fetches FY2023 **annual consolidated** values in USD:
  Revenue, Net Income, Total Equity, Total Debt, CFO.
- Computes **Debt/Equity** (NaN when equity is zero/missing).
- Skips non-USD filers and records them in `excluded_non_usd.csv`.
- Saves:
  - `sp500_fy2023_metrics.csv`
  - `sp500_fy2023_metrics.xlsx` (metrics, provenance, excluded sheets)
  - `run.log`

## Environment (Anaconda)
```bash
conda env create -f environment.yml
conda activate edgar-sp500-fy2023
