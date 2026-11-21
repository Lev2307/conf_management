"""Чтение исходного CSV-файла и разбор команд УВМ."""

import csv

from instruction import Instruction
from opcodes import OPCODES

def parse_source(source_path):
    """Читает CSV-файл с программой и возвращает список команд."""
    instructions = []
    with open(source_path, newline='', encoding='utf-8') as source:
        for row in csv.reader(source):
            cells = [cell.strip() for cell in row]
            if not cells or not cells[0] or cells[0].startswith('#'):
                continue
            instructions.append(make_instruction(cells))
    return instructions

def make_instruction(cells):
    """Создает команду из одной строки CSV: мнемоника, операнд."""
    if len(cells) != 2:
        raise ValueError(f'Ожидается "мнемоника, операнд": {cells}')
    mnemonic = cells[0]
    if mnemonic not in OPCODES:
        raise ValueError(f'Неизвестная команда: {mnemonic}')
    return Instruction(mnemonic, OPCODES[mnemonic], int(cells[1]))