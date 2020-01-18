import pandas as pd

# Create dataframe
df = pd.read_csv('WorkVocationalDetailsTBIQuestionnaire.csv')

# Clean up columns in dataframe
df = df.dropna(1, how='all')

# Populate dictionary with keys of patient ids and values of first description
vocation_dict = {}

for index, row in df.iterrows():
    if row['MedRecNo'] not in vocation_dict.keys():
        vocation_dict[row['MedRecNo']] = row['Work/Vocational_Details']

# Create dataframes to return
return_list = []

for key in vocation_dict.keys():
    list_append = [key, vocation_dict[key]]
    return_list.append(list_append)

return_df = pd.DataFrame(return_list, columns=(['MedRecNo', 'Work/Vocational_Details']))

# Export the return dataframe to excel

return_df.to_excel(r'WorkVocationalDetailsTBIQuestionnaireFirstInstance.xlsx')


