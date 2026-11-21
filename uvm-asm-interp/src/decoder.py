"""Декорирование машинного кода УВМ в промежуточное представление."""

from instruction import Instruction
from opcodes import COMMAND_SIZE, MNEMONICS, OPCODE_BITS, OPCODE_MASK


def decode_instruction(data, offset):
    """Читает команду из bytes по смещению и возвращает Instruction."""
    chunk = data[offset:offset + COMMAND_SIZE]
    word = int.from_bytes(chunk, byteorder='little')
    opcode = word & OPCODE_MASK
    if opcode not in MNEMONICS:
        raise ValueError(f'Неизвестный код команды: {opcode}')
    operand = word >> OPCODE_BITS
    return Instruction(MNEMONICS[opcode], opcode, operand)