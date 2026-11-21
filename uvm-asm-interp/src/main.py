"""Ассемблер учебной виртуальной машины (УВМ). Вариант 1.

Этап 1: разбор текстового представления программы (CSV)
и трансляция в промежуточное представление.
"""

import argparse

from reader import parse_source

def main():
    """Точка входа: аргументы командной строки и режим тестирования."""
    parser = argparse.ArgumentParser(description='Ассемблер УВМ (вариант 1)')
    parser.add_argument('source', help='путь к исходному CSV-файлу')
    parser.add_argument('output', help='путь к выходному двоичному файлу')
    parser.add_argument('--test', action='store_true',
                        help='вывести промежуточное представление')
    args = parser.parse_args()

    instructions = parse_source(args.source)
    if args.test:
        for instruction in instructions:
            print(instruction.describe())

if __name__ == '__main__':
    main()