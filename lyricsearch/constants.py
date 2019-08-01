from personal import (
        ARTISTDB,
        BIGRAMSETS,
        DEBUGDIR,
        DEBUGFILE,
        DEBUGSONG,
        LYRICS,
        RESULTS,
        SOURCETEXT,
        VOCABSETS,
        VOCABRESULTS,
        )

DEBUG = True
# DEBUG = False

if DEBUG:
    ARTISTDB = DEBUGDIR+"artist.db"
    BIGRAMSETS = DEBUGDIR+"bigramsets/"
    LYRICS = DEBUGDIR+"lyrics/"  # 54 files
    RESULTS = DEBUGDIR+"results/"
    SOURCETEXT = DEBUGDIR+"sourcetext/"
    VOCABSETS = DEBUGDIR+"vocabsets/"

PATHS = [
    ARTISTDB,
    BIGRAMSETS,
    DEBUGDIR,
    DEBUGFILE,
    DEBUGSONG,
    LYRICS,
    RESULTS,
    SOURCETEXT,
    VOCABSETS,]
