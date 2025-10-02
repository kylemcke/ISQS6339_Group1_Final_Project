# Import Libraries
import io
import pandas as pd
import requests as r

#Variables for File Access
# Github Repository
url = "https://raw.githubusercontent.com/kylemcke/ISQS6339_Group1_Final_Project/refs/heads/main/Final_Datasets/"
path = 'C:\\Users\\kylew\\OneDrive\\Documents\\Education\\ISQS 6339 - Business Intelligence\\BI Project\\Output\\'
file_1 = 'sp500_companies.csv'
file_2 = 'sp500_sec_filing_data.csv'
file_3 = 'sp500_stock_data.csv'
file_4 = 'state_census_and_education_data.csv'
file_5 = 'income_by_education_level.csv'
file_6 = 'cpi_by_sector_2023_data.csv'
file_7 = 'macroeconomic_2023_data.csv'

file_out = 'final_combined_dataset.csv'

# Read-in Files
res1 = r.get(url + file_1)
df1 = pd.read_csv(io.StringIO(res1.text))

res2 = r.get(url + file_2)
df2 = pd.read_csv(io.StringIO(res2.text))

res3 = r.get(url + file_3)
df3 = pd.read_csv(io.StringIO(res3.text))

res4 = r.get(url + file_4)
df4 = pd.read_csv(io.StringIO(res4.text))

res5 = r.get(url + file_5)
df5 = pd.read_csv(io.StringIO(res5.text))

res6 = r.get(url + file_6)
df6 = pd.read_csv(io.StringIO(res6.text))

res7 = r.get(url + file_7)
df7 = pd.read_csv(io.StringIO(res7.text))

# Ensuring correct data types & formatting
df1['Date added'] = pd.to_datetime(df1['Date added'])
df1['CIK'] = df1['CIK'].astype(str).str.zfill(10)
print(df1.dtypes)
print('------------------------------')

df2['CIK'] = df2['CIK'].astype(str).str.zfill(10)
df2['filing_date'] = pd.to_datetime(df2['filing_date'])
print(df2.dtypes)
print('------------------------------')
print(df3.dtypes)
print('------------------------------')
print(df4.dtypes)
print('------------------------------')
print(df5.dtypes)
print('------------------------------')
print(df6.dtypes)
print('------------------------------')
print(df7.dtypes)
print('------------------------------')

# Merging Files
df_merge1 = pd.merge(df1, df2, on="Symbol") # Merge df1 and df2 on 'Symbol'
df_merge2 = pd.merge(df_merge1, df3, on="Symbol") # Merge df_merge1 and df3 on 'Symbol'
df_merge3 = pd.merge(df_merge2, df4, on="State") # Merge df_merge2 and df4_styled on 'State'
df_merge4 = pd.merge(df_merge3, df5, on="State") # Merge df_merge3 and df5 on 'State'
df_merge5 = pd.merge(df_merge4, df6, on='GICS Sector') # Merge df_merge4 and df6 on 'GICS Sector'
df_merge6 = pd.merge(df_merge5, df7, on="Fiscal Year") # Merge df_merge5 and df7 on 'Fiscal Year'

# Dropped Unecessary Columns
df_merge6.drop([
    'Security_y',
    'CIK_y',
    'YahooSymbol',
    'Status',
    'Note',
    'Source',
    '2022_Level_Avg',
    '2023_Level_Avg',
    'Proxy_Note',
    'Total_Pop_All_Ages'
],axis=1, inplace=True)

# Renaming Columns for Clarity
df_merge6.rename(columns={
    'US Headquarters City' : 'US HQ City',
    'State' : 'US HQ State',
    'Date added' : 'Date Added S&P500',
    'CIK_x' : 'CIK',
    'filing_accession' : 'Filing Accession No.',
    'filing_date' : 'Filing Date No.',
    'source_form' : 'Source Form',
    'revenue_musd' : 'Revenue (Millions USD)',
    'net_income_musd' : 'Net Income (Millions USD)',
    'total_liabilities_musd' : 'Total Liabilities (Millions USD)',
    'total_shareholders_equity_musd' : 'Total Shareholders Equity (Millions USD)',
    'cfo_musd' : 'Cash Flow from Operating (Millions USD)',
    'liabilities_to_shareholders_equity_ratio' : 'Debt-to-Equity Ratio (%)',
    'LastAdjClose_2023' : 'Last Adjusted Close 2023 (USD)',
    'TotalReturn_2023' : 'Total Return 2023 (USD)',
    'Rolling3Y_Beta_vs_SP500' : 'Rolling 3-Year Beta vs. SP500',
    'AnnualVolatility_2023' : 'Annual Volatility',
    'MeanDailyVolume_2023' : 'Mean Daily Volume',
    'state_fips' : 'State FIPS',
    'population_total' : 'Population Total',
    'median_household_income' : 'Median Household Income',
    'unemployment_rate_percent' : 'Unemployment Rate (%)',
    'educ_25plus_total' : 'Education Age 25+ Total',
    'education_less_than_9th_count' : 'Education Level < 9th Grade',
    'education_less_than_9th_percent' : 'Education Level < 9th Grade (%)',
    'education_ninth_to_twelfth_no_diploma_count' : 'Education Level 9 - 12th Grad No Diploma',
    'education_ninth_to_twelfth_no_diploma_percent' : 'Education Level 9 - 12th Grad No Diploma (%)',
    'education_high_school_grad_count' : 'Education Level High School Graduate',
    'education_high_school_grad_percent' : 'Education Level High School Graduate (%)',
    'education_some_college_no_degree_count' : 'Education Level Some College No Degree',
    'education_some_college_no_degree_percent' : 'Education Level Some College No Degree (%)',
    'education_associates_count' : 'Education Level Associates Degree',
    'education_associates_percent' : 'Education Level Associates Degree (%)',
    'education_bachelors_count' : 'Education Level Bachelors',
    'education_bachelors_percent' : 'Education Level Bachelors (%)',
    'education_grad_professional_count' : 'Education Level Graduate & Professional',
    'education_grad_professional_percent' : 'Education Level Graduate & Professional (%)',
    'Total_Pop_All_Ages' : 'Total Population',
    'STATE' : 'State',
    'MedianEarnings_AllWorkers25plus' : 'Median Earnings All Workers Age 25+ (USD)',
    'MedianEarnings_LessThan_HS' : 'Median Earnings Less Than High School Diploma (USD)',
    'MedianEarnings_HS_Graduate' : 'Median Earnings High School Diploma (USD)',
    'MedianEarnings_SomeCollege_or_Associates' : 'Median Earnings Some College or Associates (USD)',
    'MedianEarnings_Bachelors' : 'Median Earnings Bachelors (USD)',
    'MedianEarnings_Graduate_or_Professional' : 'Median Earnings Graduate & Professional (USD)',
    'SeriesIDs' : 'SeriesID',
    'YoY_%_2023_vs_2022' : 'Sector Inflation Rate (YoY)',
    'Annualized CPI (BLS CPI-U, annual avg YoY, %)' : 'US CPI (Annualized)',
    'PCE Growth (Real, BEA T10101 Line 2, %)' : 'US Consumer Inflation (Mean)',
    'Average VIX (Cboe, 2023)' : 'US Market Volatility (Mean)',
    'Mean Effective Fed Funds Rate (FRED EFFR, %, 2023)' : 'Effective Fed Funds Rate (Mean)'
}, inplace=True)

# Adding in Categorical Data Requirements
## Volatility - Create a new categorical column right next to the numerical one
vol_bins = [0,0.15,0.30,float("inf")]
vol_labels = ['Low', 'Medium', 'High']
volatility_categories = pd.cut(df_merge6["Annual Volatility"], bins=vol_bins, labels=vol_labels, right=False)
vol_col_index = df_merge6.columns.get_loc("Annual Volatility") + 1
df_merge6.insert(vol_col_index, "Annual Volatility Category", volatility_categories)

## Income - Create a new categorical column right next to the numerical one
inc_bins = [0,50000,80000, float("inf")]
inc_labels = ['Low', 'Medium', 'High']
income_categories = pd.cut(df_merge6["Median Household Income"], bins=inc_bins, labels=inc_labels, right=False)
inc_col_index = df_merge6.columns.get_loc("Median Household Income") + 1
df_merge6.insert(inc_col_index, "Median Household Income Category", income_categories)

## Inflation - Create a new categorical column right next to the numerical one
cpi_bins = [-1000, 0, 0.03, 0.1, float("inf")]  
cpi_labels = ['Deflation', 'Low', 'Moderate', 'High']
cpi_categories = pd.cut(df_merge6["Sector Inflation Rate (YoY)"], bins=cpi_bins, labels=cpi_labels, right=False)
cpi_col_index = df_merge6.columns.get_loc("Sector Inflation Rate (YoY)") + 1
df_merge6.insert(cpi_col_index, "Sector Inflation Rate (YoY) Category", cpi_categories)

## Debt-to-Equity Ratio - Create a new categorical column right next to the numerical one
de_ratio_bins = [-float("inf"), 0, 1, 2, float("inf")]
de_ratio_labels = ['Negative', 'Low', 'Moderate', 'High']
de_ratio_categories = pd.cut(df_merge6["Debt-to-Equity Ratio (%)"], bins=de_ratio_bins, labels=de_ratio_labels, right=False)
de_ratio_col_index = df_merge6.columns.get_loc("Debt-to-Equity Ratio (%)") + 1
df_merge6.insert(de_ratio_col_index, "Debt-to-Equity Ratio (%) Category", de_ratio_categories)

df_merge6.to_csv(file_out,index=False)