@echo off
chcp 65001 >nul
cd /d %~dp0
python -m pip install --upgrade pyinstaller
pyinstaller --noconfirm --clean --onefile --windowed --name OrziceToolbox --add-data "data/features.json;data" main.py
echo.
echo 打包完成：dist\OrziceToolbox.exe
pause
