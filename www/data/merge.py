import pandas as pd

# Read the files into two dataframes.
df1 = pd.read_csv('data.csv')
df2 = pd.read_csv('ncbi.csv')
df3 = pd.merge(df1, df2, on = 'Assembly')
df3.set_index('Name', inplace = True)
df3.to_csv('output.csv')