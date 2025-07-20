@echo off
echo 🚀 启动智能文件处理工具GUI...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误：Python未安装或未添加到PATH
    echo 请先安装Python：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python已安装

REM 尝试启动完整版GUI
echo 🎨 尝试启动完整版GUI...
python run_gui.py 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  完整版GUI启动失败，尝试简化版...
    echo 🎨 启动简化版GUI...
    python simple_gui.py
    if %errorlevel% neq 0 (
        echo ❌ GUI启动失败
        pause
        exit /b 1
    )
)

echo ✅ GUI已关闭
pause