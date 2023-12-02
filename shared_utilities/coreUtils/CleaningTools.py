# Cleans up stuff

import re

# Cleans up all the formatting in the input, and just returns a string of words
def clean_html(inu):
    '''Cleans up all html formatting in the input string, returns only words with no punctuation'''
    chapter = inu
    # Cleaning up html tags
    chapter = re.sub("<(.*?)>", " ", chapter)
    # Cleaning up HTML Entities
    chapter = re.sub("&(.+?);", " ", chapter)
    # This part is an approximation of the Ao3 word counter, which can be found here
    # https://github.com/otwcode/otwarchive/blob/master/lib/word_counter.rb 
    chapter = re.sub("--", "—", chapter)
    chapter = re.sub("['’‘-]", "", chapter)

    return chapter