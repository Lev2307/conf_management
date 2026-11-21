"""Сохранение дампа памяти УВМ в формате XML."""

import xml.etree.ElementTree as ET
from machine import WORD_SIZE


def read_cell(memory, address):
    """Читает 32-битное слово из ячейки памяти."""
    end = address + WORD_SIZE
    return int.from_bytes(memory[address:end], 'little')

def build_dump(memory, start, end):
    """Создаёт XML-дерево с ячейками памяти из диапазона [start, end)."""
    root = ET.Element('memory')
    for address in range(start, end, WORD_SIZE):
        cell = ET.SubElement(root, 'cell', address=str(address))
        cell.text = str(read_cell(memory, address))
    return root

def save_dump(memory, start, end, path):
    """Сохраняет дамп диапазона памяти в XML-файл."""
    tree = ET.ElementTree(build_dump(memory, start, end))
    ET.indent(tree)
    tree.write(path, encoding='utf-8')