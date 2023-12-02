import re
import coreUtils.CleaningTools as ct

# Used for detecting multi-chapters, and splitting them up

# Detecting things
# Detects if a fic is multi-chapter
def is_multichapter(inp):
    '''Checks if the fic represented by the string "inp" is multi-chapter or not. Returns a boolean'''
    return inp.find("<!--chapter content-->") != -1


# Detects if a fic is single-chapter (note that multi-chapter fics with only one chapter will be caught here)
def is_singlechapter(inp):
    '''Checks if the fic represented by the string "inp" is single-chapter or not. Returns a boolean'''
    return not is_multichapter(inp)

# Want to also have a function for the number of chapters



# Splitting up into chapters. Does not error if not multichapter! Does not do any cleaning of text.
def split_chapters(inp):
    '''Split up a fic string into a list of chapter strings'''

    chapters = []
    if is_singlechapter(inp):
        # Cleaning up the string to only include the chapter
        chapter = inp.split("<div id=\"chapters\" class=\"userstuff\">", 1)[1]
        chapter = chapter.rsplit("<div id=\"afterword\">", 1)[0]
        chapter = chapter.strip()
        chapter = re.sub("<h2 class=\"toc-heading\">(.+?)</h2>", "", chapter)
        chapters.append(chapter)
    else:
        # If we're multi-chapter we do this!
        chapters = inp.split("<!--chapter content-->")[1:]
        for k in range(len(chapters)):
            chapter = chapters[k]
            chapter = chapter.strip()
            chapter = chapter.split("<!--/chapter content-->")[0]
            chapters[k] = chapter

    return chapters


def split_and_clean_chapters(inp):
    '''Takes a fic as input, returns a list of the chapters with all html and non-alphanumeric characters removed'''
    return map(ct.clean_html, split_chapters(inp))