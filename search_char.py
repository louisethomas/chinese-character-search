""" Accepts input of Chinese characters or words.
If it is a character, will return hanzi, pinyin and definitions of the
components, compounds, and other characters made from the components.
If it is a word with multiple characters, will return the hanzi, pinyin,
and definitions of each character.
"""

import pandas as pd
import sys

class Hanzi:
    def __init__(self, _character):
        self.hanzi = _character
        self.pinyin = dictionary.loc[_character, 'Pinyin']
        self.definition = dictionary.loc[_character, 'Definition']

    def print_line(self):
        """ Prints character, pinyin, and definition on one line.
        If there is more than one dictionary entry, prints both.
        """
        try:
            # Loop through if multiple matches
            if isinstance(self.pinyin, pd.Series):
                for num in range(self.pinyin.size):
                    print(" {}{}({}): {}".format('  '*num, self.hanzi, self.pinyin[num], self.definition[num]))

            # Print once if only one match
            elif isinstance(self.pinyin, str):
                print(" {}({}): {}".format(self.hanzi, self.pinyin, self.definition))
        except:
            pass


class Character(Hanzi):
    def __init__(self, _character):
        super().__init__(_character)
        self.component1 = decomposition['Character1'][_character]
        self.component2 = decomposition['Character2'][_character]

    def find_compounds(self):
        """ Finds compounds of character """
        # Find all matching compounds
        component_matches = decomposition.loc[(decomposition.Character1 == self.hanzi) | (decomposition.Character2 == self.hanzi)].index

        # Return first 5 matches in order of usage frequency
        matches=[]
        _num_matches=0
        for _char in freq.index:
            if ((_char in component_matches)
                    and (_char != self.hanzi)
                    and (_char != self.component1)
                    and (_char != self.component2)
               ):
                matches.append(_char)
                _num_matches+=1
            if _num_matches == 5:
                break
        self.compounds = matches
        return matches


def character_info(input_text):
    """ Prints information about the character """
    character_input = Character(input_text)
    print('Character matches: ')
    character_input.print_line()
    print('')

    # Search for character components
    for column in ['Character1','Character2']:
        component_str = decomposition[column][character_input.hanzi]

        # Use if statement to check components exist
        if (component_str != character_input.hanzi
                and component_str != '*'
                and component_str in dictionary.Definition
           ):
            # Print hanzi, pinyin and definition of component
            component = Character(decomposition[column][character_input.hanzi])
            print('{}: {}'.format(column, component.hanzi))
            component.print_line()
            print('')

            # Print compounds of component
            print('Most frequent compounds of {}'.format(component.hanzi))
            component.find_compounds()
            for compound in component.compounds:
                Hanzi(compound).print_line()
            print('')

    # Print compounds of character
    character_input.find_compounds()
    if character_input.compounds:
        print('Compounds of {}'.format(character_input.hanzi))
        for compound in character_input.compounds:
            Hanzi(compound).print_line()


def word_info(input_text):
    """ Prints definition and individual characters of word """
    # Check if word exists
    try:
        word_input = Hanzi(input_text)
        print('Word: ')
        word_input.print_line()
        print('')
    except:
        print('Word not found')

    # Print characters in word
    for word in input_text:
        Hanzi(word).print_line()



# load data
decomposition = pd.read_csv('data/character_decomposition.csv', index_col=0)
freq = pd.read_json('data/optimizing_learning_order/char_freq.json', orient='index')
dictionary = pd.read_csv('data/dictionary.csv', index_col=0)


# input character
# input_text = '是可覅'
input_text = str(sys.argv[1])

if len(input_text) == 1:
    character_info(input_text)
elif len(input_text) > 1:
    word_info(input_text)



