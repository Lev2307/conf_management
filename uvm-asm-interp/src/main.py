"""Ассемблер учебной виртуальной машины (УВМ). Вариант 1.

Этап 1: разбор текстового представления программы (CSV)
и трансляция в промежуточное представление.
Этап 2: формирование машинного кода и запись в двоичный файл.
"""

import argparse

from encoder import assemble, print_machine_code, write_binary
from reader import parse_source

def main():
    """Точка входа: аргументы командной строки и режим тестирования."""
    parser = argparse.ArgumentParser(description='Ассемблер УВМ (вариант 1)')
    parser.add_argument('source', help='путь к исходному CSV-файлу')
    parser.add_argument('output', help='путь к выходному двоичному файлу')
    parser.add_argument('--test', action='store_true',
                        help='вывести промежуточное и машинное представление')
    args = parser.parse_args()

    instructions = parse_source(args.source)
    if args.test:
        for instruction in instructions:
            print(instruction.describe())

    machine_code = assemble(instructions)
    write_binary(args.output, machine_code)
    print(f'Размер двоичного файла: {len(machine_code)} байт')
    if args.test:
        print_machine_code(instructions)

if __name__ == '__main__':
    main()