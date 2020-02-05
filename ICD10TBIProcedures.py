import pandas as pd
import numpy as np

df = pd.read_csv('ICD10TBIProcedures.csv')

# Create DataFrame of code + procedures
df_procedures = df.iloc[:, 0:57]

# Melt above DataFrame, order and clean
df_procedures_melted = pd.melt(df_procedures, id_vars=['Code'], value_vars=list(df_procedures.columns[1:]), var_name='Procedure_Number', value_name='Procedure_Code')

df_procedures_melted['Procedure_Number'] = df_procedures_melted['Procedure_Number'].astype(str)
df_procedures_melted['Procedure_Number'] = df_procedures_melted['Procedure_Number'].str.slice(10).astype(int)

df_procedures_ms = df_procedures_melted.sort_values(by=['Code', 'Procedure_Number'])

df_procedures_ms['Procedure_Code'] = df_procedures_ms['Procedure_Code'].str.strip()

df_procedures_ms['Procedure_Code'].replace('', np.nan, inplace=True)
df_procedures_ms['Procedure_Code'].replace('n/a', np.nan, inplace=True)

df_procedures_ms.dropna(subset=['Procedure_Code'], inplace=True)

# Create DataFrame of code + dates of procedures
df_dates = df.iloc[:, [0, 57]]

# Melt above DataFrame, order and clean
df_dates['PR_STR_EVENTS_L'] = df_dates['PR_STR_EVENTS_L'].str.rstrip()

df_dates_spread = pd.concat([df_dates[['Code']], df_dates['PR_STR_EVENTS_L'].str.split(', ', expand=True)], axis=1)

df_dates_melted = pd.melt(df_dates_spread, id_vars=['Code'], value_vars=list(df_dates_spread.columns[1:]), var_name='Procedure_Number', value_name='Date')

df_dates_melted['Procedure_Number'] = df_procedures_melted['Procedure_Number'].astype(int)

df_dates_ms = df_dates_melted.sort_values(by=['Code', 'Procedure_Number'])

# df_dates_ms.fillna(value=pd.np.nan, inplace=True)

# df_dates_ms.dropna(subset=['Date'], inplace=True)

df_merged = pd.merge(df_procedures_ms, df_dates_ms, on=['Code', 'Procedure_Number'])

# Read in new DataFrame of procedure definitions

df_TQIP = pd.read_csv('TQIPCodes.csv', encoding='ISO-8859-1')
df_TQIP_adjusted = df_TQIP.rename(columns={'Code': 'Procedure_Code'})

# Create new merge (inner join) on procedures from procedure definition DataFrame
df_merged_TQIP = pd.merge(df_merged, df_TQIP_adjusted, on='Procedure_Code').sort_values(by=['Code', 'Procedure_Number'])

# Output result sets to excel
df_merged.to_excel(r'ICD10TBIProceduresResults.xlsx')
df_merged_TQIP.to_excel(r'ICD10TBIProceduresResultsFiltered.xlsx')