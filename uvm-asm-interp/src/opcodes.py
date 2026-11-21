"""Коды команд и формат команды УВМ (вариант 1).

Команда кодируется 5 байтами (little-endian):
    биты 0-2  — код команды (поле A)
    биты 3-39 — операнд (поле B)
"""

OPCODE_BITS = 3
OPCODE_MASK = (1 << OPCODE_BITS) - 1
COMMAND_SIZE = 5  # размер команды в байтах

LOAD_CONST = 5  # загрузка константы на стек
LOAD_MEM = 0    # чтение значения из памяти
STORE_MEM = 3   # запись значения в память
BSWAP_MEM = 7   # унарная операция bswap()

# Мнемоники языка ассемблера -> код команды
OPCODES = {
    'const': LOAD_CONST,
    'load': LOAD_MEM,
    'store': STORE_MEM,
    'bswap': BSWAP_MEM,
}

# Код команды -> мнемоника (для декодирования)
MNEMONICS = {code: name for name, code in OPCODES.items()}