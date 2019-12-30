import pandas as pd

# Create dataframe
df = pd.read_csv('CAMICUAssessment.csv')

# Clean up columns in dataframe
df = df.dropna(1, how='all')

# Add DateTime column
df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

# Populate dictionary with keys of patient ids of list of their dates (with positive test results)
patient_dates = {}

for index, row in df.iterrows():
    if row['MedRecNo'] not in patient_dates.keys() and type(row['Overall_CAM-ICU']) == str and row['Overall_CAM-ICU'] == 'Positive':
        patient_dates[row['MedRecNo']] = [[row['DateTime'].strftime('%Y-%m-%d %H:%M:%S'), row['Overall_CAM-ICU']]]
    elif type(row['Overall_CAM-ICU']) == str and row['Overall_CAM-ICU'] == 'Positive':
        patient_dates[row['MedRecNo']].append([row['DateTime'].strftime('%Y-%m-%d %H:%M:%S'), row['Overall_CAM-ICU']])

# Populate dictionary with min datetime for each patient where the CAMICU result is positive
min_datetime_positive = {}

for key in patient_dates.keys():
    patient = patient_dates[key]
    min_date = min(x[0] for x in patient)
    for x in patient:
        if x[0] == min_date:
            min_datetime_positive[key] = [x[0], x[1]]

# Create dataframes to return based on min datetime values found in dictionary
return_list_positive = []

for key in min_datetime_positive.keys():
    list_append = [key, min_datetime_positive[key][0], min_datetime_positive[key][1]]
    return_list_positive.append(list_append)

return_df_positive = pd.DataFrame(return_list_positive, columns=(['MedRecNo', 'DateTime', 'Overall_CAM-ICU']))

df_is_positive = df['MedRecNo'].isin(return_df_positive['MedRecNo'])

return_set_negative = set()

for i, x in df_is_positive.items():
    if not x:
        return_set_negative.add(df.iat[i, 0])

return_df_negative = pd.DataFrame(return_set_negative, columns=(['MedRecNo']))

# Export the return dataframes to excel

return_df_positive.to_excel(r'CAMICUPositive.xlsx')
return_df_negative.to_excel(r'CAMICUNegative.xlsx')

