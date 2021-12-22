import pandas as pd
import string

df = pd.read_excel('QSProjects-mini.xlsx', sheet_name='Published Projects')
print(df.columns)

# Clean data
# Replace ampersands by 'and'
df = df.replace('&', 'and', regex=True)
# #capitalize first letter of all topics in topic list
df['Topics'] = df.Topics.apply(lambda x: string.capwords(x, sep=', ') if pd.notnull(x) else x)
# TODO: remove 'other' from topic lists
# TODO: unify similar topic names

# Create df with variables needed for wiki import
dfw = df.drop(['Publish Status'], axis=1)
dfw['Vimeo ID'] = df['Vimeo URL'].str.split('/').str[3]

print(dfw.iloc[0])
print(dfw)