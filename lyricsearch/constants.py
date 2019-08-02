from personal import (
        ARTISTDB,
        BIGRAMSETS,
        DEBUGDIR,
        DEBUGFILE,
        DEBUGSONG,
        LISTS,
        LYRICS,
        RESULTS,
        SOURCETEXT,
        VOCABRESULTS,
        VOCABSETS,
        )

DEBUG = True
# DEBUG = False

if DEBUG:
    ARTISTDB = DEBUGDIR+"artist.db"
    BIGRAMSETS = DEBUGDIR+"bigramsets/"
    LISTS = DEBUGDIR+"lists/"
    LYRICS = DEBUGDIR+"lyrics/"  # 33900 lyrics files
    RESULTS = DEBUGDIR+"results/"
    SOURCETEXT = DEBUGDIR+"sourcetext/"
    VOCABRESULTS = DEBUGDIR+"vocabresults/"
    VOCABSETS = DEBUGDIR+"vocabsets/"

PATHS = [
    ARTISTDB,
    BIGRAMSETS,
    DEBUGDIR,
    DEBUGFILE,
    DEBUGSONG,
    LISTS,
    LYRICS,
    RESULTS,
    SOURCETEXT,
    VOCABRESULTS,
    VOCABSETS,
    ]
