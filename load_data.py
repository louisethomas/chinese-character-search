import pandas as pd



decomp = pd.read_json('DATA_FILES/outlier_decomp.json',orient='index')

# HSK characters 

HSK1 = pd.read_csv('DATA_FILES/HSK1_characters.csv', index_col=0)
HSK2 = pd.read_csv('DATA_FILES/HSK2_characters.csv', index_col=0)
HSK3 = pd.read_csv('DATA_FILES/HSK3_characters.csv', index_col=0)
HSK4 = pd.read_csv('DATA_FILES/HSK4_characters.csv', index_col=0)

HSK1['HSK']=1
HSK2['HSK']=2
HSK3['HSK']=3
HSK4['HSK']=4

all_char = HSK1
all_char = pd.concat([all_char, HSK2])
all_char = pd.concat([all_char, HSK3])
all_char = pd.concat([all_char, HSK4])
all_char = all_char.loc[:,['Pinyin','Definition','HSK']]

char_order = pd.read_json('DATA_FILES/loach_order.json')
char_order['Character order'] = char_order.index
char_order.set_index(0, inplace=True)

all_char = all_char.join(char_order, how='outer')
all_char = all_char.join(decomp)

char_freq = pd.read_json('DATA_FILES/char_freq.json', orient='index')
all_char = all_char.sort_values('Character order')

all_char.rename(columns={0:'Component1'}, inplace=True)
all_char.rename(columns={1:'Component2'}, inplace=True)
all_char.rename(columns={2:'Component3'}, inplace=True)
all_char.rename(columns={3:'Component4'}, inplace=True)
all_char.rename(columns={4:'Component5'}, inplace=True)

# HSK words

HSK1_words = pd.read_csv('DATA_FILES/HSK1_words.csv', sep="\t", index_col=0)
HSK2_words = pd.read_csv('DATA_FILES/HSK2_words.csv', sep="\t", index_col=0)
HSK3_words = pd.read_csv('DATA_FILES/HSK3_words.csv', sep="\t", index_col=0)
HSK4_words = pd.read_csv('DATA_FILES/HSK4_words.csv', sep="\t", index_col=0)
HSK5_words = pd.read_csv('DATA_FILES/HSK5_words.csv', sep="\t", index_col=0)
HSK6_words = pd.read_csv('DATA_FILES/HSK6_words.csv', sep="\t", index_col=0)

HSK1_words['HSK']=1
HSK2_words['HSK']=2
HSK3_words['HSK']=3
HSK4_words['HSK']=4
HSK5_words['HSK']=5
HSK6_words['HSK']=6

all_words = HSK1_words
all_words = pd.concat([all_words, HSK1_words])
all_words = pd.concat([all_words, HSK2_words])
all_words = pd.concat([all_words, HSK3_words])
all_words = pd.concat([all_words, HSK4_words])
all_words = pd.concat([all_words, HSK5_words])
all_words = pd.concat([all_words, HSK6_words])
all_words = all_words.loc[:,['Pinyin','Definition','HSK']]

word_order = pd.read_json('DATA_FILES/loach_word_order.json')
word_order['Word order'] = word_order.index
word_order.set_index(0, inplace=True)
all_words = all_words.join(word_order, how='outer')

word_freq = pd.read_json('DATA_FILES/word_freq.json', orient='index')
all_words = all_words.join(word_freq)
all_words = all_words.sort_values('Word order')



data = pd.read_csv('DATA_FILES/ChineseCharacterMap_Yan2013.csv', index_col=0)
data = data.loc[:,['构件(Decomposition)','拼音(pinyin)']]

# Definitions
definitions = pd.concat([all_words.loc[:,'Definition'],all_char.loc[:,'Definition']]).drop_duplicates()



# Search for similar characters
Char = '孩'
print("{}({}): {}\n".format(Char,all_char.loc[Char,'Pinyin'],all_char.loc[Char,'Definition']))

CharComponent1 = all_char.loc[Char].Component1
print("First component:\n{}({}): {}".format(CharComponent1,all_char.loc[CharComponent1,'Pinyin'],all_char.loc[CharComponent1,'Definition']))
print(all_char.loc[(all_char.Component1 == CharComponent1) | (all_char.Component2 == CharComponent1) | (all_char.Component3 == CharComponent1) |(all_char.Component4 == CharComponent1) |(all_char.Component5 == CharComponent1)][['Pinyin','Definition','HSK']].dropna(thresh=2))

CharComponent2 = all_char.loc[Char].Component2
print("\nSecond component:\n{}({}): {}".format(CharComponent2,all_char.loc[CharComponent2,'Pinyin'],all_char.loc[CharComponent2,'Definition']))
print(all_char.loc[(all_char.Component1 == CharComponent2) | (all_char.Component2 == CharComponent2) | (all_char.Component3 == CharComponent2) |(all_char.Component4 == CharComponent2) |(all_char.Component5 == CharComponent2)][['Pinyin','Definition','HSK']].dropna(thresh=2))

print("\nCompounds:")
print(all_char.loc[(all_char.Component1 == Char) | (all_char.Component2 == Char) | (all_char.Component3 == Char) |(all_char.Component4 == Char) |(all_char.Component5 == Char)][['Pinyin','Definition','HSK']].dropna(thresh=2))

print(all_char.Component4.unique())
