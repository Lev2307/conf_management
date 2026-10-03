MAX_CD_ARGS = 1

class ShellError(Exception):
    """Ошибка выполнения команды эмулятора."""

class ExitR(Exception):
    """Принудительный выход из эмулятора."""

def cmd_ls(args):
    """Заглушка ls: вернуть имя команды и аргументы."""
    return f"ls: args={args}"

def cmd_cd(args):
    """Заглушка cd: вернуть имя команды и аргументы."""
    if len(args) > 1:
        raise ShellError("cd: too many arguments")
    return f"cd: args={args}"

def cmd_exit(args):
    raise ExitR()


COMMANDS = {"ls": cmd_ls, "cd": cmd_cd, "exit": cmd_exit}

def execute(name, args):
    handler = COMMANDS.get(name)
    if handler == None:
        raise ShellError(f"{name}: command not found")
    return handler(args)
    