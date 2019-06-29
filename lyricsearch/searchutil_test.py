# from . import searchutil as su
import searchutil as su


fake_text = "I went to the store the other day."


def test_exact_match_search():
    possible = ([fake_text], 1)
    pattern = "to the store"
    assert su.exact_match_search(possible, pattern)

