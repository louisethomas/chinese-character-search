import re
import pandas as pd

tone_dict = {'a1':'ā','a2':'á','a3':'ǎ','a4':'à','a5':'a',
             'e1':'ē','e2':'é','e3':'ě','e4':'è','e5':'e',
             'i1':'ī','i2':'í','i3':'ǐ','i4':'ì','i5':'i',
             'o1':'ō','o2':'ó','o3':'ǒ','o4':'ò','o5':'o',
             'u1':'ū','u2':'ú','u3':'ǔ','u4':'ù','u5':'u',
             'u:1':'ǖ','u:2':'ǘ','u:3':'ǚ','u:4':'ǜ','u:5':'ü'}

class Dict:

    def __init__(self, text):
        self.traditional = text.partition(' ')[0]
        self.simplified = text.partition(' ')[2].partition(' ')[0]
        self.definition = re.sub('\[((\w|\s|\:)*)\]',lambda x: '[{}]'.format(self.add_tones(x.group(1))) ,text.partition('/')[2].replace('/','; ').strip())     # add tones on definition pinyin, replace '/' with ';'
        self.definition = re.sub(';(?=\W*$)','',self.definition)    # remove final semicolon
        self.pinyin = self.add_tones(text.partition('[')[2].partition(']')[0])

    def add_tones(self, pinyin_num):
        pinyin = ''
        for word in pinyin_num.split():
            if word[-1].isdigit():
                num = word[-1]
                word = word[:-1]    #remove number from word

            # rules for tone position from https://en.wikipedia.org/wiki/Pinyin#Rules_for_placing_the_tone_mark
                if 'a'in word:
                    word = word.replace('a',tone_dict['a'+ num])
                elif 'e' in word:
                    word = word.replace('e',tone_dict['e'+ num])
                elif 'o' in word:
                    word = word.replace('o',tone_dict['o'+ num])
                elif 'u:' in word:
                    word = word.replace('u:',tone_dict['u:'+ num])
                else:
                    for letter in reversed(word):
                        if (letter == 'u') | (letter == 'i'):
                            word = word.replace(letter,tone_dict[letter + num])
                            break
            else:
                word += ' '    #add space after non-pinyin words
            pinyin += word
        return pinyin

dict_dataframe = pd.DataFrame()
with open('cedict_ts.u8') as file:
    line = file.readline()
    while line:
        if (line[0] != '#') and (line.find('surname') == -1):   #skip comment lines and surnames

            l = Dict(line)
            dict_entry = pd.DataFrame({'Traditional':l.traditional, 'Pinyin':l.pinyin, 'Definition':l.definition}, index=[l.simplified])
            dict_dataframe = dict_dataframe.append(dict_entry)

            # print('Simplified: {}'.format(l.simplified))
            # print('Traditional: {}'.format(l.traditional))
            # print('Pinyin: {}'.format(l.pinyin))
            # print('Definition: {}'.format(l.definition + '\n'))

        line = file.readline()

dict_dataframe.to_csv('dictionary.csv')
