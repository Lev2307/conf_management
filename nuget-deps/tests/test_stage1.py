"""Тесты парсера"""
import pytest

from config import ConfigError, validate_config
from main import parse_console_args

URL = "https://api.nuget.org/v3/index.json"

def test_test_mode_off_by_default():
    """Без флага --test-mode режим выключен."""
    conf = parse_console_args(["--package", "A", "--repo", URL])
    assert conf.test_mode is False

def test_test_mode_flag_enables_mode(tmp_path):
    """Флаг --test-mode включает режим."""
    repo_file = tmp_path / "repo.txt"
    repo_file.write_text("A: B\n")
    conf = parse_console_args(
        ["--package", "A", "--repo", str(repo_file), "--test-mode"])
    assert conf.test_mode is True
    validate_config(conf)


@pytest.mark.parametrize("args", [
    ["--package", "", "--repo", URL],
    ["--package", "A", "--repo", "api.nuget.org"],
    ["--package", "A", "--repo", "https://"],
    ["--package", "A", "--repo", URL, "--output", "graph.jpg"],
    ["--package", "A", "--repo", URL, "--output", "nodir/graph.png"],
    ["--package", "A", "--repo", URL, "--max-depth", "0"],
    ["--package", "A", "--repo", URL, "--max-depth", "51"],
])
def test_invalid_config(args):
    """Неверные значения параметров вызывают ConfigError"""
    conf = parse_console_args(args)
    with pytest.raises(ConfigError):
        validate_config(conf)


def test_test_mode_with_missing_file():
    """В тестовом режиме несуществующий файл — ошибка."""
    conf = parse_console_args(
        ["--package", "A", "--repo", "missing.txt", "--test-mode"])
    with pytest.raises(ConfigError):
        validate_config(conf)


def test_unknown_flag_rejected():
    """Несуществующий флаг --no-test-mode argparse отклоняет."""
    with pytest.raises(SystemExit):
        parse_console_args(
            ["--package", "A", "--repo", URL, "--no-test-mode"])