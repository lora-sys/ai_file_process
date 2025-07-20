#!/usr/bin/env python3
"""
GUI启动脚本
"""
import sys
import os
from pathlib import Path

def check_dependencies():
    """检查依赖"""
    missing_deps = []
    
    try:
        import tkinter
    except ImportError:
        missing_deps.append("tkinter")
    
    try:
        import spacy
    except ImportError:
        missing_deps.append("spacy")
    
    try:
        import nltk
    except ImportError:
        missing_deps.append("nltk")
    
    try:
        import langdetect
    except ImportError:
        missing_deps.append("langdetect")
    
    return missing_deps

def setup_environment():
    """设置环境"""
    # 添加当前目录到Python路径
    current_dir = Path(__file__).parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))

def main():
    """主函数"""
    print("🚀 启动智能文件处理工具 GUI...")
    
    # 检查依赖
    missing = check_dependencies()
    if missing:
        print(f"❌ 缺少依赖包: {', '.join(missing)}")
        print("请运行: pip install -r requirements.txt")
        input("按Enter键退出...")
        return 1
    
    # 设置环境
    setup_environment()
    
    try:
        # 导入并启动GUI
        from modern_gui import main as gui_main
        gui_main()
        
    except ImportError as e:
        print(f"❌ 导入模块失败: {e}")
        print("请确保所有文件都在正确位置")
        input("按Enter键退出...")
        return 1
        
    except Exception as e:
        print(f"❌ 启动GUI失败: {e}")
        input("按Enter键退出...")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())