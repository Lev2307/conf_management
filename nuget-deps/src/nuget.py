"""Получение прямых зависимостей пакета из репозитория NuGet (API v3)."""

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from xml.etree import ElementTree

TIMEOUT_SECONDS = 10
NOT_FOUND_CODE = 404
HEADERS = {"User-Agent": "nuget-deps"}
PACKAGE_BASE_TYPE = "PackageBaseAddress/3.0.0"
PRERELEASE_MARK = "-"


class RepoError(Exception):
    """Ошибка при обращении к репозиторию или разборе его ответа."""


def fetch_text(url: str) -> str:
    """Скачать ресурс по URL и вернуть его как текст.

    При ошибке сети или HTTP выбросить RepoError.
    """
    req = Request(url=url, headers=HEADERS)
    try:
        with urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            return resp.read().decode("utf-8")
    except HTTPError as e:
        if e.code == NOT_FOUND_CODE:
            raise RepoError(f"Не найдено: {url}") from e
        raise RepoError(f"Сервер вернул ошибку {e.code}: {url}") from e
    except URLError as e:
        raise RepoError(
            f"Не удалось подключиться к {url}: {e.reason}") from e
    except TimeoutError as e:
        raise RepoError(f"Превышено время ожидания: {url}") from e


def fetch_json(url: str):
    """Скачать JSON по URL и вернуть разобранный объект.

    Если ответ не является JSON, выбросить RepoError.
    """
    text = fetch_text(url)
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise RepoError(f"Ответ не является JSON: {url}") from e


def find_package_base(index: dict) -> str:
    """Найти в индексе репозитория адрес хранилища пакетов.

    Ищет ресурс с типом PackageBaseAddress/3.0.0 и возвращает его @id.
    Если ресурса нет, выбросить RepoError.
    """
    for resource in index.get("resources", []):
        if resource.get("@type") == PACKAGE_BASE_TYPE:
            return resource["@id"]
    raise RepoError(
        f"Репозиторий не поддерживает {PACKAGE_BASE_TYPE}")


def pick_latest_stable(versions: list) -> str:
    """Вернуть последнюю стабильную версию из списка.

    Список отсортирован по возрастанию; предварительные версии
    (с «-» в номере, например 2.0.0-beta) пропускаются.
    Если стабильных версий нет, выбросить RepoError.
    """
    for version in reversed(versions):
        if PRERELEASE_MARK not in version:
            return version
    raise RepoError("У пакета нет стабильных версий")


def parse_dependencies(nuspec: str) -> dict:
    """Извлечь прямые зависимости из текста .nuspec.

    Возвращает словарь {имя зависимости: диапазон версий}.
    Зависимости из всех групп (целевых платформ) объединяются
    без повторов. Если XML некорректен, выбросить RepoError.
    """
    try:
        root = ElementTree.fromstring(nuspec)
    except ElementTree.ParseError as e:
        raise RepoError("Некорректный XML в описании пакета") from e

    dependencies = {}
    for dep in root.iterfind(".//{*}dependency"):
        dep_id = dep.get("id")
        if dep_id and dep_id not in dependencies:
            dependencies[dep_id] = dep.get("version")
    return dependencies


def get_direct_dependencies(repo_url: str, package: str):
    """Вернуть кортеж (версия, зависимости) для последней стабильной
    версии пакета из репозитория repo_url.
    """
    base = find_package_base(fetch_json(repo_url))
    pkg_id = package.lower()
    try:
        versions = fetch_json(f"{base}{pkg_id}/index.json")
    except RepoError as e:
        raise RepoError(
            f"Пакет {package} не найден в репозитории") from e
    version = pick_latest_stable(versions.get("versions", []))
    nuspec = fetch_text(f"{base}{pkg_id}/{version}/{pkg_id}.nuspec")
    return version, parse_dependencies(nuspec)