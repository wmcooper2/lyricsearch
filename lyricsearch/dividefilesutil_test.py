import dividesetsutil as du


dict_ = {"I like to": ["eat", "apples and bananas."]}


def test_filepath():
    assert du.filepath("I like to", dict_) == "eat"

def test_lyricset():
    assert du.lyricset("I like to", dict_) == "apples and bananas."

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
