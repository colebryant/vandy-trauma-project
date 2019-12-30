import pandas as pd

# Create dataframes
df_right = pd.read_csv('RightEyePupilReaction.csv')
df_left = pd.read_csv('LeftEyePupilReaction.csv')

# Clean up columns in dataframes
df_right = df_right.dropna(1, how='all')
df_left = df_left.dropna(1, how='all')

# Add DateTime column
df_right['DateTime'] = pd.to_datetime(df_right['Date'] + ' ' + df_right['Time'])
df_left['DateTime'] = pd.to_datetime(df_left['Date'] + ' ' + df_left['Time'])

# Populate dictionary with keys of patient ids and values of list of their dates
right_patient_dates = {}

for index, row in df_right.iterrows():
    if row['MedRecNo'] not in right_patient_dates.keys() and type(row['Pupil_reaction_(right_eye)_']) == str and row['Pupil_reaction_(right_eye)_'] != '' and row['Pupil_reaction_(right_eye)_'] is not None:
        right_patient_dates[row['MedRecNo']] = [[row['DateTime'].strftime('%Y-%m-%d %H:%M:%S'), row['Pupil_reaction_(right_eye)_']]]
    elif type(row['Pupil_reaction_(right_eye)_']) == str and row['Pupil_reaction_(right_eye)_'] != '' and row['Pupil_reaction_(right_eye)_'] is not None:
        right_patient_dates[row['MedRecNo']].append([row['DateTime'].strftime('%Y-%m-%d %H:%M:%S'), row['Pupil_reaction_(right_eye)_']])

left_patient_dates = {}

for index, row in df_left.iterrows():
    if row['MedRecNo'] not in left_patient_dates.keys() and type(row['Pupil_reaction_(left_eye)']) == str and row['Pupil_reaction_(left_eye)'] != '' and row['Pupil_reaction_(left_eye)'] is not None:
        left_patient_dates[row['MedRecNo']] = [[row['DateTime'].strftime('%Y-%m-%d %H:%M:%S'), row['Pupil_reaction_(left_eye)']]]
    elif type(row['Pupil_reaction_(left_eye)']) == str and row['Pupil_reaction_(left_eye)'] != '' and row['Pupil_reaction_(left_eye)'] is not None:
        left_patient_dates[row['MedRecNo']].append([row['DateTime'].strftime('%Y-%m-%d %H:%M:%S'), row['Pupil_reaction_(left_eye)']])

# Populate dictionary with min datetime for each patient
right_min_datetime = {}

for key in right_patient_dates.keys():
    patient = right_patient_dates[key]
    min_date = min(x[0] for x in patient)
    for x in patient:
        if x[0] == min_date:
            right_min_datetime[key] = [x[0], x[1]]

left_min_datetime = {}

for key in left_patient_dates.keys():
    patient = left_patient_dates[key]
    min_date = min(x[0] for x in patient)
    for x in patient:
        if x[0] == min_date:
            left_min_datetime[key] = [x[0], x[1]]

# Create dataframes to return based on min datetime values found in dictionary
right_return_list = []

for key in right_min_datetime.keys():
    list_append = [key, right_min_datetime[key][0], right_min_datetime[key][1]]
    right_return_list.append(list_append)

right_return_df = pd.DataFrame(right_return_list, columns=(['MedRecNo', 'DateTime', 'Pupil_reaction_(right_eye)_']))

left_return_list = []

for key in left_min_datetime.keys():
    list_append = [key, left_min_datetime[key][0], left_min_datetime[key][1]]
    left_return_list.append(list_append)

left_return_df = pd.DataFrame(left_return_list, columns=(['MedRecNo', 'DateTime', 'Pupil_reaction_(left_eye)']))

# Export the return dataframes to excel

right_return_df.to_excel(r'RightEyeFirstReaction.xlsx')

left_return_df.to_excel(r'LeftEyeFirstReaction.xlsx')
