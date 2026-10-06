@echo off
chcp 65001 >nul
cd /d "%~dp0..\"
set URL=https://api.nuget.org/v3/index.json

echo === 1. Пакет с несколькими зависимостями
py src\main.py --package Microsoft.Extensions.Logging --repo %URL%
echo.

echo === 2. Пакет с зависимостями от старых платформ
py src\main.py --package Newtonsoft.Json --repo %URL%
echo.

echo === 3. Ещё один пакет
py src\main.py --package Serilog.Extensions.Logging --repo %URL%
echo.

echo === 4. Ошибка: пакет не существует
py src\main.py --package NoSuchPackage12345 --repo %URL%
echo.

echo === 5. Ошибка: URL не репозиторий NuGet
py src\main.py --package Serilog --repo https://github.com
echo.

echo === 6. Ошибка: сервер недоступен
py src\main.py --package Serilog --repo https://no-such-host-12345.com/index.json
echo.

pause