@echo off
chcp 65001 >nul
title 智能文件处理工具

echo ==========================================
echo    智能文件处理工具 - GUI启动器
echo ==========================================
echo.

rem 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python
    echo 请确保已安装Python 3.6或更高版本
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Python已安装
python --version

echo.
echo 🚀 启动GUI界面...
echo.

rem 尝试启动完整版GUI
python run_gui.py
if errorlevel 1 (
    echo.
    echo ⚠️  完整版启动失败，尝试简化版...
    echo.
    python simple_gui.py
    if errorlevel 1 (
        echo.
        echo ❌ GUI启动失败
        echo 请检查依赖包是否已安装:
        echo pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

echo.
echo 👋 程序已退出
pause