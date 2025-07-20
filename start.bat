@echo off
chcp 65001 >nul
title 智能文件处理工具 v2.0

echo.
echo =========================================
echo    智能文件处理工具 v2.0 - GUI启动器
echo =========================================
echo.

echo [INFO] 正在启动GUI界面...
python run_gui.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] GUI启动失败，尝试命令行版本...
    echo.
    python improved_main.py --help
    echo.
    echo 请检查Python环境和依赖包是否正确安装
    echo 运行: pip install -r requirements.txt
)

echo.
pause