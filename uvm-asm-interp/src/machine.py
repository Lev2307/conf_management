"""Модель УВМ: объединённая память, стек и цикл исполнения."""

from decoder import COMMAND_SIZE, decode_instruction
from opcodes import LOAD_CONST, LOAD_MEM, STORE_MEM

WORD_SIZE = 4       # размер ячейки данных в байтах
MEMORY_SIZE = 4096  # размер объединённой памяти в байтах

class Machine:
    """Учебная вирутальная машина с памятью команд и данных."""

    def __init__(self, memory_size=MEMORY_SIZE):
        """Создает пустую память, пустой стек и указатель команд IP."""
        self.memory = bytearray(memory_size)
        self.stack = []
        self.ip = 0

    def load_program(self, code):
        """Загружает машинный код программы в память с адреса 0."""
        self.memory[:len(code)] = code

    def check_address(self, address):
        """Проверяет, что адрес ячейки целиком попадает в память."""
        if address < 0 or address + WORD_SIZE > len(self.memory):
            raise ValueError(f'Адрес вне памяти: {address}')

    def read_word(self, address):
        """Читает 32-битное слово little-endian из памяти."""
        self.check_address(address)
        end = address + WORD_SIZE
        return int.from_bytes(self.memory[address:end], 'little')

    def write_word(self, address, value):
        """Записывает 32-битное слово little-endian в память."""
        self.check_address(address)
        encoded = value.to_bytes(WORD_SIZE, 'little')
        self.memory[address:address + WORD_SIZE] = encoded

    def run(self, code_size):
        """Выполняет программу длиной code_size байт с адреса 0."""
        self.ip = 0
        while self.ip < code_size:
            instruction = decode_instruction(self.memory, self.ip)
            self.execute(instruction)
            self.ip += COMMAND_SIZE

    def execute(self, instruction):
        """Выполняет одну команду УВМ, снимая операнды со стека."""
        opcode = instruction.opcode
        operand = instruction.operand
        if opcode == LOAD_CONST:
            self.stack.append(operand)
        elif opcode == LOAD_MEM:
            self.stack.append(self.read_word(self.stack.pop() + operand))
        elif opcode == STORE_MEM:
            value = self.stack.pop()
            address = self.stack.pop() + operand
            self.write_word(address, value)
        else:
            raise ValueError(f'Команда не реализована: {opcode}')