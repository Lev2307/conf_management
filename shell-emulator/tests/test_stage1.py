"""Тесты парсера и команд этапа 1."""
import pytest 

from commands import ExitR, ShellError, execute
from shell_parser import parse

def test_parse_splits_by_space():
    """Строка делится на команду и аргументы."""
    assert parse("ls a b c") == ("ls", ["a", "b", "c"])

def test_parse_empty_line():
    """Пустая строка даёт None"""
    assert parse(" ") == (None, [])

def test_stub_prints_name_and_args():
    """Заглушка выводит имя и аргументы"""
    args = ["-l", "/home"]
    assert execute("ls", args) == f"ls: args={args}"

def test_unknown_command():
    """Неизвестная команда вызывает ошибку."""
    with pytest.raises(ShellError):
        execute("find", ["/", "-maxdepth", "1"])

def test_cd_too_many_args():
    """Передача больше одного аргумента команде cd вызывает ошибку."""
    with pytest.raises(ShellError):
        execute("cd", ["a", "b"])

def test_exit():
    """exit завершает работу"""
    with pytest.raises(ExitR):
        execute("exit", [])