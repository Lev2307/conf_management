"""Трансляция промежуточного представления в машинный код УВМ."""

from opcodes import COMMAND_SIZE, OPCODE_BITS

# Ширина поля A в битах и размер команды в байтах
OPCODE_BITS = 3
COMMAND_SIZE = 5

def encode_instruction(instruction):
    """Кодирует команду: слово = A | (B << 3), 5 байт little-endian."""
    word = instruction.opcode | (instruction.operand << OPCODE_BITS)
    return word.to_bytes(COMMAND_SIZE, byteorder='little')

def assemble(instructions):
    """Возвращает машинный код всей программы в виде байтов."""
    return b''.join(encode_instruction(ins) for ins in instructions)

def write_binary(path, data):
    """Записывает машинный код в двоичный файл."""
    with open(path, 'wb') as target:
        target.write(data)

def print_machine_code(instructions):
    """Печатает команды в байтовом формате, как в тестах спецификации."""
    for instruction in instructions:
        encoded = encode_instruction(instruction)
        print(', '.join(f'0x{byte:02X}' for byte in encoded))