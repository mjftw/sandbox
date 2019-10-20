class ParseError(Exception):
    pass


class SymbolTreeNode:
    def __init__(self, symbols):
        self.symbols = symbols
        self.children = []

        self.remove_enclosing_brackets()
        self.find_children()

    def __repr__(self):
        return str(self.symbols)

    def remove_enclosing_brackets(self):
        if self.symbols[0] == '(' and self.symbols[-1] == ')':
            del(self.symbols[0])
            del(self.symbols[-1])

    def find_children(self):
        # Brackets search
        open_bracket_pos = []
        close_bracket_pos = None
        for i, s in enumerate(self.symbols):
            if s == '(':
                open_bracket_pos.append(i)
            elif s ==')':
                if not open_bracket_pos:
                    raise ParseError('Missing opening bracket:  {}[{}]'.format(
                        self.symbols, i))
                close_bracket_pos = i

            if open_bracket_pos and close_bracket_pos is not None:
                self.insert_child(open_bracket_pos[-1], close_bracket_pos+1)
                open_bracket_pos.pop()

        if open_bracket_pos:
            if close_bracket_pos is None:
                raise ParseError('Missing closing bracket: {}[{}]'.format(
                    self.symbols, i))

    def insert_child(self, open_idx, close_idx):
        new_syms = self.symbols[:open_idx]
        new_syms.append(SymbolTreeNode(self.symbols[open_idx:close_idx]))
        new_syms.extend(self.symbols[close_idx:])
        self.symbols = new_syms


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

# def do_operation(num1, op, num2):
#     answer = None

#     if op == '+':
#         answer = num1 + num2
#     elif op == '-':
#         answer = num1 - num2
#     elif op == '*':
#         answer = num1 * num2
#     else:
#         raise ParseError('Unsupported operator: {}'.format(op))

#     return answer

# def calculate(in_str):
#     symbols = get_symbols(in_str)
#     answer = calculate_symbols(symbols)

#     return answer

# def calculate_symbols(symbols):
#     answer = None

#     num_memory = None
#     sym_memory = None
#     for s in symbols:
#         if isinstance(s, int) or isinstance(s, float):
#             if sym_memory == '-':
#                 sym_memory = '+'
#                 s = -s
#             if num_memory is not None and sym_memory:
#                 num_memory = do_operation(num_memory, sym_memory, s)
#                 sym_memory = None
#             elif num_memory is None:
#                 num_memory = s
#             else:
#                 raise ParseError(
#                     'Cannot have two numbers in a row: {}, {}'.format(
#                         num_memory, s))
#         elif sym_memory is None:
#             sym_memory = s
#         else:
#             if sym_memory == '+' and s == '+':
#                 sym_memory = '+'
#             elif sym_memory == '+' and s == '-':
#                 sym_memory = '-'
#             elif sym_memory == '-' and s == '+':
#                 sym_memory = '-'
#             elif sym_memory == '-' and s == '-':
#                 sym_memory = '+'

#     answer = num_memory or 0

#     return answer