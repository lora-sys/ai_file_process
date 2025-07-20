#!/bin/bash

# 智能文件处理工具 - GUI启动脚本

echo "=========================================="
echo "   智能文件处理工具 - GUI启动器"
echo "=========================================="
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ 错误: 未找到Python"
        echo "请确保已安装Python 3.6或更高版本"
        exit 1
    else
        PYTHON_CMD=python
    fi
else
    PYTHON_CMD=python3
fi

echo "✅ Python已安装"
$PYTHON_CMD --version

echo
echo "🚀 启动GUI界面..."
echo

# 设置工作目录为脚本所在目录
cd "$(dirname "$0")"

# 尝试启动完整版GUI
$PYTHON_CMD run_gui.py
if [ $? -ne 0 ]; then
    echo
    echo "⚠️  完整版启动失败，尝试简化版..."
    echo
    $PYTHON_CMD simple_gui.py
    if [ $? -ne 0 ]; then
        echo
        echo "❌ GUI启动失败"
        echo "请检查依赖包是否已安装:"
        echo "pip install -r requirements.txt"
        echo
        exit 1
    fi
fi

echo
echo "👋 程序已退出"