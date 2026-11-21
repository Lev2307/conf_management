"""Сборка программы УВМ: CSV-файл -> двоичный файл."""

from encoder import assemble, print_machine_code, write_binary
from reader import parse_source


def assemble_program(source_path, output_path, test_mode):
    """Ассемблирует программу, записывает файл и выводит размер.

    В режиме тестирования печатает промежуточное представление
    и машинный код в байтовом формате, как в спецификации УВМ.
    """
    instructions = parse_source(source_path)
    if test_mode:
        for instruction in instructions:
            print(instruction.describe())
    machine_code = assemble(instructions)
    write_binary(output_path, machine_code)
    print(f'Размер двоичного файла: {len(machine_code)} байт')
    if test_mode:
        print_machine_code(instructions)
