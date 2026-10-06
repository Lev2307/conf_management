@echo off
cd /d "%~dp0..\"
set URL=https://api.nuget.org/v3/index.json

echo === There is no required parameter --package
py src\main.py --repo %URL%

echo === Empty package name
py src\main.py --package "" --repo %URL%

echo === Invalid characters in the package name
py src\main.py --package "my pkg!" --repo %URL%

echo === repo is not URL
py src\main.py --package A --repo api.nuget.org

echo === Test mode: File not found
py src\main.py --package A --repo missing.txt --test-mode

echo === Output file not PNG
py src\main.py --package A --repo %URL% --output graph.jpg

echo === The output file folder does not exist
py src\main.py --package A --repo %URL% --output nodir\graph.png

echo === Max depth not int
py src\main.py --package A --repo %URL% --max-depth abc

echo === Max depth out of range
py src\main.py --package A --repo %URL% --max-depth 0