"""Тесты парсера консольных аргументов"""
from main import parse_args


def test_parse_args_no_args():
    """Парсинг значений без аргументов."""
    assert parse_args([]) == (None, None)


def test_parse_args_only_vfs():
    """Задан только --vfs."""
    assert parse_args(["--vfs", "vfs_empty.csv"]) == ("vfs_empty.csv", None)


def test_parse_args_only_script():
    """Парсинг значений: только script."""
    assert parse_args(["--script", "script.txt"]) == (None, "script.txt")


def test_parse_args_all():
    """Парсинг значений всех аргументов"""
    assert parse_args(["--vfs", "vfs_empty.csv", "--script", "script.txt"]) == ("vfs_empty.csv", "script.txt")