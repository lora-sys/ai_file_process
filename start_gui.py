#!/usr/bin/env python3
"""
智能文件处理工具 GUI 启动脚本
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
    print("🚀 智能文件处理工具 GUI")
    print("=" * 40)
    
    # 检查依赖
    print("检查依赖...")
    missing_deps = check_dependencies()
    
    if missing_deps:
        print(f"❌ 缺少依赖: {', '.join(missing_deps)}")
        print("\n请运行以下命令安装依赖:")
        print("pip install -r requirements.txt")
        
        # 检查是否有GUI环境
        try:
            import tkinter as tk
            root = tk.Tk()
            from tkinter import messagebox
            root.withdraw()
            
            messagebox.showerror(
                "缺少依赖",
                f"缺少以下依赖包:\n{chr(10).join(missing_deps)}\n\n"
                "请运行: pip install -r requirements.txt"
            )
            root.destroy()
        except:
            pass
        
        return 1
    
    print("✅ 依赖检查通过")
    
    # 设置环境
    setup_environment()
    
    # 启动GUI
    try:
        print("启动图形界面...")
        from improved_gui import main as gui_main
        gui_main()
        return 0
        
    except ImportError as e:
        print(f"❌ 导入GUI模块失败: {e}")
        print("请确保所有文件都在正确位置")
        return 1
        
    except Exception as e:
        print(f"❌ 启动GUI失败: {e}")
        print("\n可能的解决方案:")
        print("1. 确保系统支持图形界面")
        print("2. 检查tkinter是否正确安装")
        print("3. 尝试运行命令行版本: python improved_main.py --help")
        
        # 尝试提供备用方案
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            
            result = messagebox.askyesno(
                "GUI启动失败",
                f"GUI启动失败: {e}\n\n是否查看命令行帮助?"
            )
            
            if result:
                os.system("python improved_main.py --help")
            
            root.destroy()
        except:
            pass
            
        return 1

if __name__ == "__main__":
    sys.exit(main())