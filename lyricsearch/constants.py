from personal import (
        ARTISTDB,
        DEBUGDIR,
        DEBUGFILE,
        LYRICS,
        RESULTS,
        SETS,
        SOURCETEXT,
        VOCABSETS,
        VOCABRESULTS,
        )

# DEBUG = True
DEBUG = False

if DEBUG:
    ARTISTDB = DEBUGDIR+"artist.db"
    LYRICS = DEBUGDIR+"lyrics/"  # 54 files
    RESULTS = DEBUGDIR+"results/"
    SETS = DEBUGDIR+"sets/"
    SOURCETEXT = DEBUGDIR+"sourcetext/"
    VOCABSETS = DEBUGDIR+"vocabsets/"

# remove?
# NAMEDPATHS = [
#     ("ARTISTDB", ARTISTDB),
#     ("DEBUGDIR", DEBUGDIR),
#     ("LYRICS", LYRICS),
#     ("RESULTS", RESULTS),
#     ("SETS", SETS),
#     ("SOURCETEXT", SOURCETEXT),
#     ("VOCABSETS", VOCABSETS),]

PATHS = [
    ARTISTDB,
    DEBUGDIR,
    DEBUGFILE,
    LYRICS,
    RESULTS,
    SETS,
    SOURCETEXT,
    VOCABSETS,]
