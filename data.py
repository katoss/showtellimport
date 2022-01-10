import pandas as pd
import string

df = pd.read_excel('QSProjects.xlsx', sheet_name='Published Projects')
print(df.columns)

# clean data
# replace ampersands by 'and'
df['Topics'] = df['Topics'].replace('&', 'and', regex=True)
# #capitalize first letter of all topics in topic list
df['Topics'] = df.Topics.apply(lambda x: string.capwords(x, sep=', ') if pd.notnull(x) else x)
# remove empty lines at the end of transcripts
df['Transcription'] = df['Transcription'].str.strip()
# remove 'other' from topic lists
print('Occurences of "Other" in Topics before cleaning: ' + str(df['Topics'].str.count('Other').sum()))
df['Topics'] = df['Topics'].replace(', Other', '', regex=True)
df['Topics'] = df['Topics'].replace('Other, ', '', regex=True)
df['Topics'] = df['Topics'].replace('Other', '', regex=True)
print('Occurences of "Other" in Topics after cleaning: ' + str(df['Topics'].str.count('Other').sum()))
# TODO: unify similar topic names

# Create df with variables needed for wiki import
dfw = df.drop(['Publish Status'], axis=1)
dfw['Vimeo ID'] = df['Vimeo URL'].str.split('/').str[3]

print(dfw.iloc[0])
print(dfw)

# print columns with empty cells
na_values = dfw[dfw.isna().any(axis=1)]
print (na_values)

# write clean df to excel
dfw.to_excel('QSProjects-clean.xlsx')