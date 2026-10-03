import argparse
from gui import ShellApp


def parse_args(argv=None):
    """Разобрать аргументы командной строки.
    
    Возвращает кортеж (vfs_path, script_path). 
    Незаданный параметр равен None.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--vfs")
    parser.add_argument("--script")
    args = parser.parse_args(argv)
    return args.vfs, args.script


def main():
    """Основная функция программы."""
    vfs, script = parse_args()
    ShellApp(vfs, script).run()


if __name__ == "__main__":
    main()