@echo off
chcp 65001 > nul
title 智能文件处理工具 GUI

echo.
echo =====================================
echo    智能文件处理工具 v2.0 GUI
echo =====================================
echo.

REM 检查Python是否安装
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.8或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python 已安装
echo.

REM 尝试启动GUI
echo 🚀 正在启动GUI界面...
python launch_gui.py

if errorlevel 1 (
    echo.
    echo ❌ GUI启动失败，请检查错误信息
    echo 💡 常见解决方案:
    echo    1. 运行: pip install -r requirements.txt
    echo    2. 确保所有文件都在同一目录下
    echo    3. 检查Python版本是否为3.8+
    echo.
    pause
)