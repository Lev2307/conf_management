@echo off
cd /d "%~dp0..\"

set URL=https://api.nuget.org/v3/index.json
set FILEPATH=scripts\test_repo.txt

echo == Default mode with url
py src\main.py --package A --repo %URL% --output graph.png --max-depth 2

echo == Test mode with file
py src\main.py --package A --repo %FILEPATH% --test-mode --output graph.png --max-depth 1

echo == Default mode with only required args
py src\main.py --package A --repo %URL%