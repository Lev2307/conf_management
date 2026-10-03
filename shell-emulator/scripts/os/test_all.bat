@echo off
cd /d "%~dp0..\.."
py src\main.py --vfs scripts\emulator\empty_vfs.csv --script scripts\emulator\ok.txt