"""Конфигурация приложения: параметры запуска и их проверка."""

import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

MIN_ALLOWED_DEPTH = 1
MAX_ALLOWED_DEPTH = 50
PACKAGE_NAME_PATTERN = re.compile(r"[A-Za-z0-9_.-]+")
URL_SCHEMES = ("http", "https")
OUTPUT_SUFFIX = ".png"


@dataclass
class Config:
    """Параметры запуска, заданные пользователем."""

    package: str
    repo: str
    test_mode: bool
    output: str
    max_depth: int


class ConfigError(Exception):
    """Ошибка в параметрах запуска."""


def validate_package(package: str):
    """Проверить имя пакета.

    Имя не должно быть пустым и может содержать только латинские
    буквы, цифры и символы «.», «-», «_».
    """
    if not package.strip():
        raise ConfigError("Имя пакета не должно быть пустым")
    if not PACKAGE_NAME_PATTERN.fullmatch(package):
        raise ConfigError(
            f"Недопустимые символы в имени пакета: {package!r}")


def validate_repo(repo: str, test_mode: bool):
    """Проверить источник данных о пакетах.

    В тестовом режиме repo — путь к существующему файлу,
    в обычном — URL со схемой http или https.
    """
    if not repo.strip():
        raise ConfigError("Адрес репозитория не должен быть пустым")
    if test_mode:
        validate_repo_file(repo)
    else:
        validate_repo_url(repo)


def validate_repo_file(repo: str):
    """Проверить, что путь указывает на существующий файл."""
    repo_file = Path(repo)
    if not repo_file.exists():
        raise ConfigError(
            f"Файл тестового репозитория не найден: {repo_file}")
    if repo_file.is_dir():
        raise ConfigError(
            f"Ожидался файл тестового репозитория, а не папка: {repo_file}")


def validate_repo_url(repo: str):
    """Проверить, что строка — URL со схемой http(s) и адресом сервера."""
    parts = urlsplit(repo)
    if parts.scheme not in URL_SCHEMES or not parts.netloc:
        raise ConfigError(
            f"--repo должен быть URL (http/https), получено: {repo}")


def validate_output(output: str):
    """Проверить имя выходного PNG-файла и наличие папки для него."""
    if not output.strip():
        raise ConfigError("Имя выходного файла не должно быть пустым")

    output_path = Path(output)
    if output_path.suffix.lower() != OUTPUT_SUFFIX:
        raise ConfigError(
            f"Выходной файл должен иметь расширение .png: {output}")
    if not output_path.parent.is_dir():
        raise ConfigError(
            f"Папка для выходного файла не существует: {output_path.parent}")
    if output_path.is_dir():
        raise ConfigError(
            f"Ожидалось имя файла, а не папка: {output_path}")


def validate_depth(max_depth: int):
    """Проверить, что глубина анализа лежит в допустимом диапазоне."""
    if not MIN_ALLOWED_DEPTH <= max_depth <= MAX_ALLOWED_DEPTH:
        raise ConfigError(
            f"max_depth должна быть от {MIN_ALLOWED_DEPTH} "
            f"до {MAX_ALLOWED_DEPTH}, получено: {max_depth}")


def validate_config(conf: Config):
    """Проверить все параметры. При ошибке выбросить ConfigError."""
    validate_package(conf.package)
    validate_repo(conf.repo, conf.test_mode)
    validate_output(conf.output)
    validate_depth(conf.max_depth)