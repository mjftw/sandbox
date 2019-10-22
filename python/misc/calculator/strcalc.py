class ParseError(Exception):
    pass


class SymbolTreeNode:
    def __init__(self, symbols):
        self.symbols = symbols
        self.children = []

        self._remove_enclosing_brackets()
        self._find_children()

    def __repr__(self):
        return str(self.symbols)

    def calculate(self):
        num_memory = None
        sym_memory = None
        for i, s in enumerate(self.symbols):
            if isinstance(self.symbols[i], SymbolTreeNode):
                self.symbols[i] = s.calculate()
            if symbol_is_num(self.symbols[i]):
                if num_memory is not None and sym_memory is not None:
                    num_memory = self.do_operation(num_memory, sym_memory, self.symbols[i])
                    sym_memory = None
                elif num_memory is None:
                    num_memory = self.symbols[i]
            elif sym_memory is None:
                sym_memory = self.symbols[i]

        answer = num_memory or 0
        return answer

    def do_operation(self, num1, op, num2):
        answer = None

        if op == '+':
            answer = num1 + num2
        elif op == '-':
            answer = num1 - num2
        elif op == '*':
            answer = num1 * num2
        elif op == '/':
            answer = num1 / num2
        elif op == '^':
            answer = pow(num1, num2)

        return answer

    def _remove_enclosing_brackets(self):
        if self.symbols[0] == '(' and self.symbols[-1] == ')':
            remove_enclosing = True
            bracket_num = 0
            for i, s in enumerate(self.symbols):
                if s == '(':
                    bracket_num += 1
                elif s == ')':
                    bracket_num -= 1
                if bracket_num == 0 and i != (len(self.symbols)-1):
                    remove_enclosing = False
                    break

            if remove_enclosing:
                del(self.symbols[0])
                del(self.symbols[-1])

    def _find_children(self):
        self._find_children_brackets()
        self._consume_extra_pos_neg()
        self._validate_symbols()
        self._find_children_num_op_num('+')
        self._find_children_num_op_num('-')
        self._find_children_num_op_num('*')
        self._find_children_num_op_num('/')
        self._find_children_num_op_num('^')


    def _consume_extra_pos_neg(self):
        new_syms = []
        for s in reversed(self.symbols):
            new_syms.append(s)

            if (len(new_syms) > 2 and
                symbol_is_num(new_syms[-3]) and
                symbol_is_op(new_syms[-1])):
                    if new_syms[-2] == '+':
                        del(new_syms[-2])
                    elif new_syms[-2] == '-':
                        new_syms[-3] = -new_syms[-3]
                        del(new_syms[-2])

        self.symbols = new_syms[::-1]

    def _validate_symbols(self):
        last_s = None
        for s in self.symbols:
            if symbol_is_op(last_s) and symbol_is_op(s):
                raise ParseError(
                    'Invalid syntax at operators {}, {} in {}'.format(
                        last_s, s, self.symbols))
            last_s = s

    def _find_children_brackets(self):
        open_bracket_pos = []
        close_bracket_pos = None
        i = 0
        for s in self.symbols:
            if s == '(':
                open_bracket_pos.append(i)
            elif s ==')':
                if not open_bracket_pos:
                    raise ParseError('Missing opening bracket:  {}[{}]'.format(
                        self.symbols, i))
                close_bracket_pos = i

            if open_bracket_pos and close_bracket_pos is not None:
                len_before = len(self.symbols)
                self._insert_child(open_bracket_pos[-1], close_bracket_pos+1)

                len_change = len_before - len(self.symbols)

                # Alter open positions for new symbols list
                i -= len_change
                for p in open_bracket_pos:
                    p -= len_change

                open_bracket_pos.pop()
                close_bracket_pos = None

            i += 1
        if open_bracket_pos:
            if close_bracket_pos is None:
                raise ParseError('Missing closing bracket: {}[{}]'.format(
                    self.symbols, i))

    def _find_children_num_op_num(self, op):
        try:
            op_pos = self.symbols.index(op)
        except ValueError:
            return

        new_syms = []
        s_before = self.symbols[:op_pos]
        s_after = self.symbols[op_pos+1:]

        if len(s_before) == 1:
            new_syms.append(s_before[0])
        else:
            new_syms.append(SymbolTreeNode(s_before))

        new_syms.append(op)

        if len(s_after) == 1:
            new_syms.append(s_after[0])
        else:
            new_syms.append(SymbolTreeNode(s_after))

        self.symbols = new_syms

    def _insert_child(self, open_idx, close_idx):
        new_syms = self.symbols[:open_idx]
        new_syms.append(SymbolTreeNode(self.symbols[open_idx:close_idx]))
        new_syms.extend(self.symbols[close_idx:])
        self.symbols = new_syms


def calculate(eqation_str):
    return SymbolTreeNode(get_symbols(eqation_str)).calculate()

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

def symbol_is_op(s):
    return (
        s is not None and
        not isinstance(s, int) and
        not isinstance(s, float) and
        not isinstance(s, SymbolTreeNode)
    )

def symbol_is_num(s):
    return (
        isinstance(s, int) or
        isinstance(s, float)
    )