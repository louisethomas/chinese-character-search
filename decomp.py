import pandas as pd

df = pd.read_csv('DATA_FILES/CharacterDecompositionWiki.csv', sep='\t', index_col='Character')
df = df.loc[:,['Strokes','Composition','Character1','Strokes1','Verification1','Character2','Strokes2','Verification2','Cangjie','Radical']]
df.dropna(how='all', inplace=True)

print(df)
df.to_csv('DATA_FILES/CharacterDecompositionWiki_cleaned.csv')
