from curtsies import Input


def main():
    with Input(keynames='curses') as input_generator:
        for char in input_generator:
            print(f'Pressed: {char}')

if __name__ == '__main__':
    main()