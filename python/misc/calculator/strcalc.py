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

def compute_symbols(num1, sym, num2):
    answer = None#

    if sym == '+':
        answer = num1 + num2
    elif sym == '-':
        answer = num1 - num2

    return answer

def calculate(in_str):
    answer = None

    symbols = get_symbols(in_str)

    num_memory = None
    sym_memory = None
    for s in symbols:
        if isinstance(s, int) or isinstance(s, float):
            if sym_memory == '-':
                sym_memory = '+'
                s = -s
            if num_memory is not None and sym_memory:
                num_memory = compute_symbols(num_memory, sym_memory, s)
                sym_memory = None
            elif num_memory is None:
                num_memory = s
            else:
                raise ParseError(
                    'Cannot have two numbers in a row: {}, {}'.format(
                        num_memory, s))
        elif sym_memory is None:
            sym_memory = s
        else:
            if sym_memory == '+' and s == '+':
                sym_memory = '+'
            elif sym_memory == '+' and s == '-':
                sym_memory = '-'
            elif sym_memory == '-' and s == '+':
                sym_memory = '-'
            elif sym_memory == '-' and s == '-':
                sym_memory = '+'

    answer = num_memory

    return answer