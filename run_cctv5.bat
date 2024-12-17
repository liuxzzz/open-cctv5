@echo off
title CCTV5

:: 检查 Python 是否已安装
python --version >nul 2>&1
if errorlevel 1 (
    echo Python未安装，请先安装Python
    pause
    exit /b
)

:: 检查 selenium 是否已安装
python -c "import selenium" >nul 2>&1
if errorlevel 1 (
    echo 正在安装 selenium...
    pip install selenium
)

:: 运行脚本
echo open cctv5 ing...
cd /d "%~dp0"
python -c "import sys; sys.path.append('.'); from open_cctv5 import open_cctv5; open_cctv5()"

pause