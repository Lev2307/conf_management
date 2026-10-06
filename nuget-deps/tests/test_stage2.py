"""Тесты получения прямых зависимостей NuGet (без обращения к сети)."""
import pytest

import main
import nuget
from nuget import (RepoError, find_package_base, get_direct_dependencies,
                   parse_dependencies, pick_latest_stable)

BASE = "https://example.org/flat/"
REPO = "https://example.org/index.json"

NUSPEC_GROUPS = """<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd">
  <metadata>
    <id>Demo</id>
    <dependencies>
      <group targetFramework="net8.0">
        <dependency id="Serilog" version="3.1.1" />
        <dependency id="Microsoft.Extensions.Logging" version="[8.0.0, )" />
      </group>
      <group targetFramework=".NETStandard2.0">
        <dependency id="Serilog" version="3.1.1" />
      </group>
    </dependencies>
  </metadata>
</package>"""

NS_2010 = "http://schemas.microsoft.com/packaging/2010/07/nuspec.xsd"
NUSPEC_FLAT = f"""<package xmlns="{NS_2010}">
  <metadata>
    <dependencies>
      <dependency id="A" version="1.0.0" />
    </dependencies>
  </metadata>
</package>"""

NUSPEC_EMPTY = "<package><metadata><id>Demo</id></metadata></package>"


def test_find_package_base():
    """Из индекса берётся @id ресурса PackageBaseAddress/3.0.0."""
    index = {"resources": [
        {"@id": "https://example.org/search", "@type": "SearchQueryService"},
        {"@id": BASE, "@type": "PackageBaseAddress/3.0.0"},
    ]}
    assert find_package_base(index) == BASE


def test_find_package_base_missing():
    """Нет нужного ресурса — RepoError."""
    with pytest.raises(RepoError):
        find_package_base({"resources": []})


@pytest.mark.parametrize("versions, expected", [
    (["1.0.0", "2.0.0", "3.0.0-beta"], "2.0.0"),
    (["1.0.0"], "1.0.0"),
    (["1.0.0-rc", "1.0.0", "1.1.0-dev.5"], "1.0.0"),
])
def test_pick_latest_stable(versions, expected):
    """Выбирается последняя версия без «-» в номере."""
    assert pick_latest_stable(versions) == expected


@pytest.mark.parametrize("versions", [[], ["1.0.0-beta", "2.0.0-rc"]])
def test_pick_latest_stable_none(versions):
    """Нет стабильных версий — RepoError."""
    with pytest.raises(RepoError):
        pick_latest_stable(versions)


def test_parse_dependencies_groups_without_duplicates():
    """Зависимости всех групп объединяются без повторов."""
    assert parse_dependencies(NUSPEC_GROUPS) == {
        "Serilog": "3.1.1",
        "Microsoft.Extensions.Logging": "[8.0.0, )",
    }


def test_parse_dependencies_without_groups():
    """Зависимости прямо в <dependencies> тоже находятся."""
    assert parse_dependencies(NUSPEC_FLAT) == {"A": "1.0.0"}


def test_parse_dependencies_empty():
    """Пакет без зависимостей — пустой словарь."""
    assert parse_dependencies(NUSPEC_EMPTY) == {}


def test_parse_dependencies_bad_xml():
    """Некорректный XML — RepoError."""
    with pytest.raises(RepoError):
        parse_dependencies("<package><metadata>")


def fake_repo(monkeypatch, versions, nuspec):
    """Подменить сетевые функции ответами тестового репозитория."""
    index = {"resources": [{"@id": BASE,
                            "@type": "PackageBaseAddress/3.0.0"}]}

    def fake_json(url):
        if url == REPO:
            return index
        if url == f"{BASE}demo/index.json":
            return {"versions": versions}
        raise RepoError(f"Не найдено: {url}")

    monkeypatch.setattr(nuget, "fetch_json", fake_json)
    monkeypatch.setattr(nuget, "fetch_text", lambda url: nuspec)


def test_get_direct_dependencies(monkeypatch):
    """Вся цепочка: индекс -> версии -> .nuspec -> словарь."""
    fake_repo(monkeypatch, ["1.0.0", "2.0.0", "3.0.0-beta"], NUSPEC_FLAT)
    assert get_direct_dependencies(REPO, "Demo") == ("2.0.0", {"A": "1.0.0"})


def test_get_direct_dependencies_unknown_package(monkeypatch):
    """Несуществующий пакет — понятная ошибка с его именем."""
    fake_repo(monkeypatch, [], NUSPEC_EMPTY)
    with pytest.raises(RepoError, match="Nope"):
        get_direct_dependencies(REPO, "Nope")


def test_main_prints_dependencies(monkeypatch, capsys):
    """main выводит заголовок и зависимости."""
    fake_repo(monkeypatch, ["2.0.0"], NUSPEC_GROUPS)
    main.main(["--package", "Demo", "--repo", REPO])
    out = capsys.readouterr().out
    assert "Прямые зависимости Demo 2.0.0:" in out
    assert "Serilog 3.1.1" in out


def test_main_repo_error_exits_with_code_1(monkeypatch, capsys):
    """При RepoError main печатает ошибку и выходит с кодом 1."""
    fake_repo(monkeypatch, [], NUSPEC_EMPTY)
    with pytest.raises(SystemExit) as exit_info:
        main.main(["--package", "Nope", "--repo", REPO])
    assert exit_info.value.code == 1
    assert "Nope" in capsys.readouterr().err