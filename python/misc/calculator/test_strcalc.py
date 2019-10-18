from strcalc import get_symbols

### TESTS ###
def test_get_symbols_can_parse_ints():
    assert get_symbols('1984') == [1984]

def test_get_symbols_can_parse_floats():
    assert get_symbols('12.34') == [12.34]
