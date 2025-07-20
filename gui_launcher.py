#!/usr/bin/env python3
"""
GUI启动器 - 简化版本
"""
import sys
import os
from pathlib import Path

# 添加当前目录到路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def check_dependencies():
    """检查依赖是否安装"""
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
    
    return missing_deps

def install_dependencies():
    """安装缺失的依赖"""
    import subprocess
    import sys
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """主函数"""
    print("🚀 智能文件处理工具 GUI 启动器")
    print("=" * 50)
    
    # 检查依赖
    missing_deps = check_dependencies()
    
    if missing_deps:
        print(f"⚠️  缺少依赖: {', '.join(missing_deps)}")
        
        if input("是否自动安装依赖? (y/n): ").lower() in ['y', 'yes']:
            print("正在安装依赖...")
            if install_dependencies():
                print("✅ 依赖安装完成")
            else:
                print("❌ 依赖安装失败，请手动运行: pip install -r requirements.txt")
                return 1
        else:
            print("请先安装依赖后再运行")
            return 1
    
    # 启动GUI
    try:
        print("启动GUI界面...")
        from improved_gui import main as gui_main
        gui_main()
        return 0
        
    except ImportError as e:
        print(f"❌ 导入模块失败: {e}")
        print("请确保所有文件都在同一目录下")
        return 1
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())