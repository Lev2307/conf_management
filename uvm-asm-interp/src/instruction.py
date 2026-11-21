"""Промежуточное представление команды УВМ."""

class Instruction:
    """Команда УВМ в промежуточном представлении."""

    def __init__(self, mnemonic, opcode, operand):
        """Сохраняет мнемонику, код команды (A) и операнд (B)."""
        self.mnemonic = mnemonic
        self.opcode = opcode
        self.operand = operand

    def describe(self):
        """Возвращает строку 'A=<код>, B=<операнд>' как в спецификации."""
        return f'A={self.opcode}, B={self.operand}'