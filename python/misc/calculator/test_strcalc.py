from strcalc import get_symbols

### TESTS ###
def test_get_symbols_can_parse_ints():
    assert get_symbols('1984') == [1984]

def test_get_symbols_can_parse_floats():
    assert get_symbols('12.34') == [12.34]

def test_get_symbols_can_parse_plus():
    assert get_symbols('+') == ['+']

def test_get_symbols_can_parse_minus():
    assert get_symbols('-') == ['-']

def test_get_symbols_can_parse_divde():
    assert get_symbols('/') == ['/']

def test_get_symbols_can_parse_multiply():
    assert get_symbols('*') == ['*']

def test_get_symbols_can_parse_power():
    assert get_symbols('^') == ['^']

def test_get_symbols_can_parse_open_parenthesis():
    assert get_symbols('(') == ['(']

def test_get_symbols_can_parse_close_parenthesis():
    assert get_symbols(')') == [')']

def test_get_symbols_can_parse_multiple():
    assert get_symbols('2.1+5') == [2.1, '+', 5]

def test_get_symbols_can_parse_multiple_all_symbols():
    assert get_symbols('2.1*3+5/2-(2^4)') == [2.1, '*', 3, '+', 5, '/', 2, '-', '(', 2, '^', 4, ')']

def test_get_symbols_ignores_whitespace():
    assert get_symbols('2.1 + 5') == [2.1, '+', 5]