class ParseError(Exception):
    pass


def _str_to_num(num_str):
    if '.' in num_str:
        num = float(num_str)
    else:
        num = int(num_str)

    return num

def get_symbols(in_str):
    assert isinstance(in_str, str)

    symbols = []

    valid_operators = ['+', '-', '/', '*', '^', '(', ')']
    whitespace = [' ', '\t']

    current_num = ''
    for c in in_str:
        if c.isdigit() or c == '.':
            if current_num:
                current_num += c
            else:
                current_num = str(c)
            continue
        elif current_num:
            symbols.append(_str_to_num(current_num))
            current_num = ''

        if c in valid_operators:
            symbols.append(c)
        elif c in whitespace:
            pass
        else:
            raise ParseError('Invalid symbol: "{}"'.format(c))

    if current_num:
        symbols.append(_str_to_num(current_num))

    return symbols
