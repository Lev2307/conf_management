"""Точка входа: разбор параметров и вывод прямых зависимостей пакета."""

import argparse
import sys

from config import Config, ConfigError, validate_config
from nuget import RepoError, get_direct_dependencies


def parse_console_args(argv=None) -> Config:
    """Разобрать аргументы командной строки.

    Возвращает объект Config. Проверку значений не выполняет,
    для неё есть validate_config.
    """
    parser = argparse.ArgumentParser(
        description="Визуализация графа зависимостей пакетов NuGet")
    parser.add_argument(
        "--package", required=True,
        help="имя анализируемого пакета NuGet, например Newtonsoft.Json")
    parser.add_argument(
        "--repo", required=True,
        help="URL репозитория NuGet (https://...) или, при --test-mode, "
             "путь к файлу тестового репозитория")
    parser.add_argument(
        "--test-mode", action="store_true",
        help="режим тестового репозитория: --repo трактуется как путь "
             "к локальному файлу с описанием графа")
    parser.add_argument(
        "--output", default="graph.png",
        help="имя PNG-файла с изображением графа (по умолчанию graph.png)")
    parser.add_argument(
        "--max-depth", type=int, default=3,
        help="максимальная глубина анализа зависимостей, целое число > 0 "
             "(по умолчанию 3)")
    args = parser.parse_args(argv)
    return Config(args.package, args.repo, args.test_mode,
                  args.output, args.max_depth)


def print_dependencies(package: str, version: str, deps: dict):
    """Вывести прямые зависимости пакета, по одной в строке."""
    print(f"Прямые зависимости {package} {version}:")
    if not deps:
        print("  (нет)")
    for name, version_range in deps.items():
        print(f"  {name} {version_range or 'любая версия'}")


def fail(message: str):
    """Вывести сообщение об ошибке и завершить программу с кодом 1."""
    print(f"Ошибка: {message}", file=sys.stderr)
    sys.exit(1)


def main(argv=None):
    """Проверить параметры и вывести прямые зависимости пакета."""
    conf = parse_console_args(argv)
    try:
        validate_config(conf)
    except ConfigError as error:
        fail(str(error))

    if conf.test_mode:
        fail("тестовый режим будет реализован на этапе 3")

    try:
        version, deps = get_direct_dependencies(conf.repo, conf.package)
    except RepoError as error:
        fail(str(error))
    print_dependencies(conf.package, version, deps)


if __name__ == "__main__":
    main()