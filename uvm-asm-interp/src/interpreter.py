"""Исполнение программы УВМ: бинарный файл -> дамп памяти XML."""

from dump import save_dump
from machine import Machine


def read_binary(path):
    """Читает бинарный файл программы и возвращает байты."""
    with open(path, 'rb') as source:
        return source.read()


def interpret(binary_path, dump_path, start, end):
    """Исполняет программу и сохраняет дамп памяти в XML-файл."""
    code = read_binary(binary_path)
    machine = Machine()
    machine.load_program(code)
    machine.run(len(code))
    save_dump(machine.memory, start, end, dump_path)
