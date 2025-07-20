@echo off
chcp 65001 >nul
title 智能文件处理工具

echo 🚀 智能文件处理工具 GUI
echo =====================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到Python
    echo 请先安装Python 3.7或更高版本
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python环境检测通过

REM 检查是否存在主要文件
if not exist "start_gui.py" (
    echo ❌ 错误: 找不到start_gui.py文件
    echo 请确保所有文件都在正确位置
    echo.
    pause
    exit /b 1
)

echo ✅ 文件检测通过

REM 尝试启动GUI
echo 启动图形界面...
echo.
python start_gui.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ GUI启动失败
    echo.
    echo 可能的解决方案:
    echo 1. 运行: pip install -r requirements.txt
    echo 2. 使用命令行版本: python improved_main.py --help
    echo.
    pause
)

exit /b %errorlevel%