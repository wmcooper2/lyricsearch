from dividesetsutil import *
import filesanddirs as fad
from constants import DEBUGSONG
from nltk import word_tokenize

simple_sent = "I like birds."

def test_normalized_weird_text():
    assert normalized(DEBUGSONG) == ['nothing', 'good', 'comes', 'easy']

def test_normalized_nonexistent_dir():
    assert normalized("nonexsistent") == []

def test_normalized_simple_pattern():
    assert normalized_pattern(simple_sent) == ["i", "like", "birds"]

def test_normalized_complex_pattern():
    assert normalized_pattern("I LIKe! biRds ~=, 45.") == \
            ["i", "like", "birds"]

def test_normalized_empty_pattern():
    assert normalized_pattern("") == []

def test_read_file():
    assert fad.read_file(DEBUGSONG) == \
            ['*[NoThing', '-good?', '!', 'comeS,', 'easy]', '@`%$#:']

def test_read_file_lines():
    assert fad.read_file_lines(DEBUGSONG) == \
            ['*[NoThing -good? ! comeS, easy] @`%$#:']

def test_remove_empty_elements():
    tokens = word_tokenize(simple_sent+" 0," )
    assert remove_empty_elements(tokens) == \
            ['i', 'like', 'birds']

def test_remove_empty_elements_from_empty_list():
    assert remove_empty_elements([]) == []
