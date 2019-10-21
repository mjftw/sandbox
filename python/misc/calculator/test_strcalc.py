import pytest

from strcalc import get_symbols, symbol_is_num, symbol_is_op,\
    ParseError, SymbolTreeNode

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

#Helpers
def test_symbol_is_num_float():
    assert symbol_is_num(0.1) == True

def test_symbol_is_num_int():
    assert symbol_is_num(1) == True

def test_symbol_is_num_none():
    assert symbol_is_num(None) == False

def test_symbol_is_num_str():
    assert symbol_is_num('h') == False

def test_symbol_is_op_plus():
    assert symbol_is_op('+') == True

def test_symbol_is_op_minus():
    assert symbol_is_op('-') == True

def test_symbol_is_op_misc_other_op():
    assert symbol_is_op('!') == True

def test_symbol_is_op_int():
    assert symbol_is_op(1) == False

def test_symbol_is_op_float():
    assert symbol_is_op(1.1) == False

def test_symbol_is_op_none():
    assert symbol_is_op(None) == False

#SymbolTreeNode
def test_SymbolTreeNode_repr():
    assert str(
        SymbolTreeNode(
            get_symbols(
                '1 + 1'
            )
        )
    ) == "[1, '+', 1]"

def test_SymbolTreeNode_err_missing_open_bracket():
    with pytest.raises(ParseError):
        SymbolTreeNode(
            get_symbols(
                '1)'
            )
        )

def test_SymbolTreeNode_err_missing_close_bracket():
    with pytest.raises(ParseError):
        SymbolTreeNode(
            get_symbols(
                '(1'
            )
        )

def test_SymbolTreeNode_remove_enclosing_brackets():
    assert str(
        SymbolTreeNode(
            get_symbols(
                '(1 1)'
            )
        )
    ) == "[1, 1]"

def test_SymbolTreeNode_nested_brackets_1deep():
    assert str(
        SymbolTreeNode(
            get_symbols(
                '1 3.1 (2 9)'
            )
        )
    ) == "[1, 3.1, [2, 9]]"

def test_SymbolTreeNode_nested_brackets_2deep():
    assert str(
        SymbolTreeNode(
            get_symbols(
                '(1 3.1 (2 9 (1 0)))'
            )
        )
    ) == "[1, 3.1, [2, 9, [1, 0]]]"

def test_SymbolTreeNode_brackets_many_sets():
    assert str(
        SymbolTreeNode(
            get_symbols(
                '(1 3 7) (2 9) 4 (1 0)'
            )
        )
    ) == "[[1, 3, 7], [2, 9], 4, [1, 0]]"

def test_SymbolTreeNode_split_add():
    assert str(
        SymbolTreeNode(
            get_symbols(
                '1 1 + 1 + 1'
            )
        )
    ) == "[[1, 1], '+', [1, '+', 1]]"

def test_SymbolTreeNode_split_subtract():
    assert str(
        SymbolTreeNode(
            get_symbols(
                '1 1 - 1 - 1'
            )
        )
    ) == "[[1, 1], '-', [1, '-', 1]]"

def test_SymbolTreeNode_split_add_subtract():
    assert str(
        SymbolTreeNode(
            get_symbols(
                '1 1 - 1 + 1'
            )
        )
    ) == "[[[1, 1], '-', 1], '+', 1]"

def test_SymbolTreeNode_split_multiply():
    assert str(
        SymbolTreeNode(
            get_symbols(
                '1 1 * 1 * 1'
            )
        )
    ) == "[[1, 1], '*', [1, '*', 1]]"

def test_SymbolTreeNode_split_divide():
    assert str(
        SymbolTreeNode(
            get_symbols(
                '1 1 / 1 / 1'
            )
        )
    ) == "[[1, 1], '/', [1, '/', 1]]"

def test_SymbolTreeNode_split_power():
    assert str(
        SymbolTreeNode(
            get_symbols(
                '1 1 ^ 1 ^ 1'
            )
        )
    ) == "[[1, 1], '^', [1, '^', 1]]"

def test_SymbolTreeNode_all_ops_order():
    assert str(
        SymbolTreeNode(
            get_symbols(
                '(1*2^3+4-5/6)'
            )
        )
    ) == "[[1, '*', [2, '^', 3]], '+', [4, '-', [5, '/', 6]]]"

def test_SymbolTreeNode_err_double_op():
    with pytest.raises(ParseError):
        SymbolTreeNode(
            get_symbols(
                '1 * / 1'
            )
        )

def test_SymbolTreeNode_err_double_op2():
    with pytest.raises(ParseError):
        SymbolTreeNode(
            get_symbols(
                '1 * ^ 1'
            )
        )

def test_SymbolTreeNode_handle_double_plus():
    assert str(
        SymbolTreeNode(
            get_symbols(
                '1 + +1'
            )
        )
    ) == "[1, '+', 1]"

def test_SymbolTreeNode_handle_triple_plus():
    assert str(
        SymbolTreeNode(
            get_symbols(
                '1 + + +1'
            )
        )
    ) == "[1, '+', 1]"

def test_SymbolTreeNode_handle_plus_minus():
    assert str(
        SymbolTreeNode(
            get_symbols(
                '1 + -1'
            )
        )
    ) == "[1, '+', -1]"

def test_SymbolTreeNode_handle_double_minus():
    assert str(
        SymbolTreeNode(
            get_symbols(
                '1 - -1'
            )
        )
    ) == "[1, '-', -1]"

def test_SymbolTreeNode_handle_multiply_minus():
    assert str(
        SymbolTreeNode(
            get_symbols(
                '1 * -1'
            )
        )
    ) == "[1, '*', -1]"

def test_SymbolTreeNode_handle_multiply_plus():
    assert str(
        SymbolTreeNode(
            get_symbols(
                '1 * +1'
            )
        )
    ) == "[1, '*', 1]"

def test_SymbolTreeNode_handle_minus_multiply():
    with pytest.raises(ParseError):
        SymbolTreeNode(
            get_symbols(
                '1 - * 1'
            )
        )


# # calculate
# def test_calculate_handles_empty():
#     assert calculate('') == 0

# def test_calculate_handles_no_op():
#     assert calculate('5') == 5

# def test_calculate_handles_2_num_addition():
#     assert calculate('2 + 2') == 4

# def test_calculate_handles_3_num_addition():
#     assert calculate('2 + 2 + 2') == 6

# def test_calculate_handles_2_num_subtraction():
#     assert calculate('5 - 3') == 2

# def test_calculate_handles_3_num_subtraction():
#     assert calculate('10 - 2 - 1') == 7

# def test_calculate_handles_3_num_addition_subtraction():
#     assert calculate('5 - 3 + 8') == 10

# def test_calculate_handles_plus_plus():
#     assert calculate('5 + +3') == 8

# def test_calculate_handles_plus_minus():
#     assert calculate('5 + -3') == 2

# def test_calculate_handles_minus_plus():
#     assert calculate('5 - +3') == 2

# def test_calculate_handles_minus_minus():
#     assert calculate('5 - -2') == 7

# def test_calculate_handles_leading_plus():
#     assert calculate('+5 - 2') == 3

# def test_calculate_handles_leading_minus():
#     assert calculate('-5 - 2') == -7

# def test_calculate_handles_minus_minus_minus():
#     assert calculate('5 --- 2') == 3

# def test_calculate_handles_plus_plus_plus():
#     assert calculate('5 +++ 2') == 7

# def test_calculate_multiplication():
#     assert calculate('5 * 2') == 10

# def test_calculate_multiplication_addition():
#     assert calculate('1 - 5 * 2') == -9