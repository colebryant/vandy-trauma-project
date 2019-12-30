import pandas as pd
import math
from scipy.stats import t

df = pd.read_csv('TBIQuestionnaire_DATA_LABELS_2019-11-29_1353.csv')

is_3_month = df['Is this the three month follow-up?'] == 'Yes'

not_3_month = df['Is this the three month follow-up?'] == 'No'

relevant_rows = df[is_3_month]

other_rows = df[not_3_month]

df_columns = relevant_rows['PHQ9 Scores']

df_columns2 = other_rows['PHQ9 Scores']

print(len(df_columns))

print('Average PHQ9 Score for three month follow-up:')
print(df_columns.mean())

# Minimal depression (1-4)

print('Number scoring minimal depression (1-4):')
print(len(df_columns[df_columns <= 4]))

# Mild depression (5-9)

print('Number scoring mild depression (5-9):')
print(len(df_columns[(df_columns >= 5) & (df_columns <= 9)]))

# Moderate depression (10-14)

print('Number scoring moderate depression (10-14):')
print(len(df_columns[(df_columns >= 10) & (df_columns <= 14)]))

# Moderately severe depression (15-19)

print('Number scoring moderately severe depression (15-19):')
print(len(df_columns[(df_columns >= 15) & (df_columns <= 19)]))

# Severe depression (20-27)

print('Number scoring severe depression (20-27):')
print(len(df_columns[(df_columns >= 20) & (df_columns <= 27)]))

# Calculations for t-test
#   Means:
mean1, mean2 = df_columns.mean(), df_columns2.mean()

#   Standard deviation
std1, std2 = df_columns.std(), df_columns2.std()

#   Standard errors
n1, n2 = len(df_columns), len(df_columns2)
se1, se2 = std1/math.sqrt(n1), std2/math.sqrt(n2)

#   Standard error on difference between the samples
sed = math.sqrt(se1**2.0 + se2**2.0)

#   Calculate t-statistic
t_stat = (mean1 - mean2) / sed

def independent_ttest(data1, data2, alpha):
    # calculate means
    mean1, mean2 = data1.mean(), data2.mean()
    #   Standard deviation
    std1, std2 = data1.std(), data2.std()
    # Standard errors
    n1, n2 = len(df_columns), len(df_columns2)
    print('n1: ' + str(n1))
    print('n2: ' + str(n2))
    se1, se2 = std1 / math.sqrt(n1), std2 / math.sqrt(n2)
    # standard error on the difference between the samples
    sed = math.sqrt(se1**2.0 + se2**2.0)
    # calculate the t statistic
    t_stat = (mean1 - mean2) / sed
    # degrees of freedom
    df = len(data1) + len(data2) - 2
    # calculate the critical value
    cv = t.ppf(1.0 - alpha, df)
    # calculate the p-value
    p = (1.0 - t.cdf(abs(t_stat), df)) * 2.0
    # return everything
    return t_stat, df, cv, p

t_stat, df, cv, p = independent_ttest(df_columns, df_columns2, 0.05)

print('t statistic: ' + str(t_stat))
print('degrees of freedom: ' + str(df))
print('critical value: ' + str(cv))
print('p-value: ' + str(p))