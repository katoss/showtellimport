import pandas as pd

df = pd.read_excel("QSProjects.xlsx")
print(df)
print(df.columns)

# convert content of column "Topics" to string and split 
df["Topics"] = df["Topics"].astype('str')
df["Topics"] = df["Topics"].str.split(", ")
print(df["Topics"].head())

# count occurences of topics and count number
topic_counts = pd.Series([x for item in df.Topics for x in item]).value_counts()
print(len(topic_counts))
print(topic_counts)
print(topic_counts.sum())

# test if topic counts sums up to same number as length of lists in Topic column
df["Topiclen"] = df["Topics"].str.len()
print(df["Topiclen"])
print(df["Topiclen"].sum())
