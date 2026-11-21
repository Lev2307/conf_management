"""УВМ (вариант 1): единая точка входа ассемблера и интерпретатора.

Подкоманды:
    assemble <исходник.csv> <результат.bin> [--test]
    run <программа.bin> <дамп.xml> <начало> <конец>
"""

import argparse

from assembler import assemble_program
from interpreter import interpret


def build_parser():
    """Создаёт парсер аргументов с подкомандами assemble и run."""
    parser = argparse.ArgumentParser(
        description='Ассемблер и интерпретатор УВМ (вариант 1)')
    subparsers = parser.add_subparsers(dest='command', required=True)

    asm = subparsers.add_parser('assemble', help='ассемблировать программу')
    asm.add_argument('source', help='путь к исходному CSV-файлу')
    asm.add_argument('output', help='путь к выходному двоичному файлу')
    asm.add_argument('--test', action='store_true',
                     help='вывести промежуточное и машинное представление')

    run = subparsers.add_parser('run', help='исполнить программу')
    run.add_argument('binary', help='путь к бинарному файлу программы')
    run.add_argument('dump', help='путь к файлу дампа памяти (XML)')
    run.add_argument('start', type=int, help='начальный адрес дампа')
    run.add_argument('end', type=int,
                     help='конечный адрес дампа, не включая')
    return parser


def main():
    """Разбирает аргументы и запускает нужную подкоманду."""
    args = build_parser().parse_args()
    if args.command == 'assemble':
        assemble_program(args.source, args.output, args.test)
    elif args.command == 'run':
        interpret(args.binary, args.dump, args.start, args.end)


if __name__ == '__main__':
    main()
