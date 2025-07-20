#!/bin/bash

# 智能文件处理工具 GUI 启动脚本

echo "🚀 智能文件处理工具 GUI"
echo "====================================="
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ 错误: 未找到Python"
        echo "请先安装Python 3.7或更高版本"
        echo "Ubuntu/Debian: sudo apt install python3"
        echo "macOS: brew install python3"
        echo
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "✅ Python环境检测通过"

# 检查Python版本
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
MAJOR_VERSION=$(echo $PYTHON_VERSION | cut -d'.' -f1)
MINOR_VERSION=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$MAJOR_VERSION" -lt 3 ] || ([ "$MAJOR_VERSION" -eq 3 ] && [ "$MINOR_VERSION" -lt 7 ]); then
    echo "❌ 错误: Python版本过低 ($PYTHON_VERSION)"
    echo "需要Python 3.7或更高版本"
    echo
    exit 1
fi

echo "✅ Python版本检测通过 ($PYTHON_VERSION)"

# 检查是否存在主要文件
if [ ! -f "start_gui.py" ]; then
    echo "❌ 错误: 找不到start_gui.py文件"
    echo "请确保所有文件都在正确位置"
    echo
    exit 1
fi

echo "✅ 文件检测通过"

# 检查显示环境（仅Linux）
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if [ -z "$DISPLAY" ] && [ -z "$WAYLAND_DISPLAY" ]; then
        echo "⚠️  警告: 未检测到图形环境"
        echo "如果您在远程服务器上，请使用命令行版本:"
        echo "$PYTHON_CMD improved_main.py --help"
        echo
        read -p "继续启动GUI? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 0
        fi
    fi
fi

# 尝试启动GUI
echo "启动图形界面..."
echo
$PYTHON_CMD start_gui.py

if [ $? -ne 0 ]; then
    echo
    echo "❌ GUI启动失败"
    echo
    echo "可能的解决方案:"
    echo "1. 安装依赖: pip3 install -r requirements.txt"
    echo "2. 使用命令行版本: $PYTHON_CMD improved_main.py --help"
    echo "3. 检查图形环境是否可用"
    echo
    exit 1
fi