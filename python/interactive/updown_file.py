import argparse
from ast import literal_eval
from curtsies import Input
import shutil
import re


def main(filename):
    print('\n')
    with Input(keynames='curses') as input_generator:
        for char in (c for c in input_generator
                if c in ['KEY_UP', 'KEY_DOWN']):
            value = read_value(filename)
            if char == 'KEY_UP':
                value += 1
                bar_char = '>'
            elif char == 'KEY_DOWN':
                value -= 1
                bar_char = '<'

            write_value(value, filename)
            reprint(f'{value}\n{bar_char * int(value)}')

def read_value(filename):
    try:
        with open(filename, 'r')as f:
            str_value = f.read()
    except FileNotFoundError:
        return 0

    if not str_value:
        return 0
    else:
        try:
            value = literal_eval(str_value)
        except SyntaxError:
           return 0

    try:
        float(value)
    except ValueError:
        return 0

    return value

def write_value(value, filename):
    with open(filename, 'w') as f:
        f.write(str(value))

def reprint(string):
    # Pad rows with spaces
    rows, cols = shutil.get_terminal_size()
    lines = re.split('\n', string)
    string = '\n'.join(f'{l}{" " * cols}' for l in lines)

    # Move cursor up
    print('\033[F' * len(lines), end='')

    # Print string where old string was
    print(f'{string}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')

    args = parser.parse_args()
    main(args.filename)
