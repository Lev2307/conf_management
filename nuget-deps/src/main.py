import argparse
import sys
from dataclasses import asdict
from config import Config, ConfigError, validate_config

def parse_console_args(argv=None) -> Config:
    """Разобрать аргументы консольной строки.

        Возвращает объект Config
    """
    parser = argparse.ArgumentParser()
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
    config = Config(args.package, args.repo, args.test_mode, args.output, args.max_depth)
    return config

def print_config(conf: Config):
    """Вывести все параметры в формате ключ = значение."""
    for key, value in asdict(conf).items():
        print(f"{key} = {value}")
 

def main():
    """
        Основная функция программы.
    """
    conf = parse_console_args()
    try:
        validate_config(conf)
    except ConfigError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        sys.exit(1)
    print_config(conf)

if __name__ == "__main__":
    main()