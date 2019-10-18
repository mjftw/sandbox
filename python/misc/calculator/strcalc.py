def _str_to_num(num_str):
    if '.' in num_str:
        num = float(num_str)
    else:
        num = int(num_str)

    return num

def get_symbols(in_str):
    assert isinstance(in_str, str)

    symbols = []

    current_num = ''
    for c in in_str:
        if c.isdigit() or c == '.':
            if current_num:
                current_num += c
            else:
                current_num = str(c)
        elif current_num:
            symbols.append(_str_to_num(current_num))
            current_num = ''

    if current_num:
        symbols.append(_str_to_num(current_num))

    return symbols

