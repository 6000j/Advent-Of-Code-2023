import re
import coreUtils.CleaningTools

# A bunch of misc useful wordcount-related functions

def words_list(inp):
    '''Takes a string and splits it into words using regex (vs using spaces). This is preferred to splitting at spaces.'''
    return re.findall(r'\w+', inp)


def simplified_word_count(inp):
    '''Returns the word count of the input string, assuming it has already been correctly cleaned'''
    return len(words_list(inp))


def cleaned_word_count(inp):
    '''Returns the word count of the input string, along with cleaning it first'''
    return simplified_word_count(coreUtils.CleaningTools.clean_html(inp))