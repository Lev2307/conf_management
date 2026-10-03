"""Простой парсер командной строки эмулятора."""

def parse(line):
    """Разбить строку по пробелам на команду и список аргументов.

    Возвращает кортеж (command, args). Для пустой строки
    command равен None.
    """
    parts = line.split()
    return (None, []) if not parts else (parts[0], parts[1:])