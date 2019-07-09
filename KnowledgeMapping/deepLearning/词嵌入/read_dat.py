import pandas as pd

data = pd.read_table('news_sohusite_xml.smarty.dat', sep='::', engine='python')

print(data.shape)
print(data.head())
