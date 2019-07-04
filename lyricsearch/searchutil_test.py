import searchutil as su


fake_text = "I went to the store the other day."


def test_exact_search():
    possible = ([fake_text], 1)
    pattern = "to the store"
    assert su.exact_search(possible, pattern)

def test_exact_search():
    pass

def test_lyric_set():
    pass

def test_save():
    # save data to file
    # reload data 
    # compare saved to loaded
    pass

def test_search_db():
    pass

def subset_match():
    pass

def subset_search():
    pass
