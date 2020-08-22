import pandas as pd

all_words = pd.DataFrame()

for num in range(1,7):
    filename = 'HSK' + str(num) + '_words.csv'
    HSK_words = pd.read_csv(filename, sep="\t", index_col=0)
    HSK_words['HSK'] = num
    all_words = pd.concat([all_words, HSK_words])

all_words = all_words.loc[:,['Pinyin','Definition','HSK']]
all_words.to_csv('HSK_all_words.csv')
