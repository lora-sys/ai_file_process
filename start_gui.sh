#!/bin/bash

echo "🚀 启动智能文件处理工具GUI..."
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ 错误：Python未安装"
        echo "请先安装Python 3.8+"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "✅ Python已安装"

# 尝试启动完整版GUI
echo "🎨 尝试启动完整版GUI..."
$PYTHON_CMD run_gui.py 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  完整版GUI启动失败，尝试简化版..."
    echo "🎨 启动简化版GUI..."
    $PYTHON_CMD simple_gui.py
    if [ $? -ne 0 ]; then
        echo "❌ GUI启动失败"
        exit 1
    fi
fi

echo "✅ GUI已关闭"