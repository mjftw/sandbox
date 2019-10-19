import pytest

from strcalc import get_symbols, calculate, ParseError

### TESTS ###
# get_symbols()
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

def test_get_symbols_ignores_spaces():
    assert get_symbols('2.1 + 5') == [2.1, '+', 5]

def test_get_symbols_ignores_tabs():
    assert get_symbols('2.1\t+\t5') == [2.1, '+', 5]

def test_get_symbols_float_with_trailing_dot_okay():
    assert get_symbols('2. +') == [2.0, '+']

def test_get_symbols_float_with_leading_dot_okay():
    assert get_symbols('.2 +') == [0.2, '+']

def test_get_symbols_catches_invalid_symbols():
    with pytest.raises(ParseError):
        get_symbols('#')

# calculate
def test_calculate_handles_2_num_addition():
    assert calculate('2 + 2') == 4

def test_calculate_handles_3_num_addition():
    assert calculate('2 + 2 + 2') == 6

def test_calculate_handles_2_num_subtraction():
    assert calculate('5 - 3') == 2

def test_calculate_handles_3_num_subtraction():
    assert calculate('10 - 2 - 1') == 7

def test_calculate_handles_3_num_addition_subtraction():
    assert calculate('5 - 3 + 8') == 10

def test_calculate_handles_plus_plus():
    assert calculate('5 + +3') == 8

def test_calculate_handles_plus_minus():
    assert calculate('5 + -3') == 2

def test_calculate_handles_minus_plus():
    assert calculate('5 - +3') == 2

def test_calculate_handles_minus_minus():
    assert calculate('5 - -2') == 7

def test_calculate_handles_leading_plus():
    assert calculate('+5 - 2') == 3

def test_calculate_handles_leading_minus():
    assert calculate('-5 - 2') == -7