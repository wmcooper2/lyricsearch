# import dividesetsutil as du
import filesanddirs as fad


dict_ = {"I like to": ["eat", "apples and bananas."]}


def test_file_path():
    assert fad.file_path("I like to", dict_) == "eat"

# def test_lyricset():
#     assert du.lyric_set("I like to", dict_) == "apples and bananas."

def test_make_mega_set():
    pass

def test_make_set():
    pass

def test_pi_set_from_dir():
    pass

def test_read_file():
    pass

def test_read_file_lines():
    pass

def test_save_error():
    pass
