#!/usr/bin/env python3
"""
GUI功能测试脚本
"""
import sys
import tkinter as tk
from pathlib import Path

def test_tkinter():
    """测试tkinter是否可用"""
    try:
        root = tk.Tk()
        root.title("GUI测试")
        root.geometry("400x300")
        
        # 创建测试界面
        frame = tk.Frame(root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="🎉 GUI测试成功!", 
                font=('Arial', 16, 'bold')).pack(pady=20)
        
        tk.Label(frame, text="tkinter界面工作正常", 
                font=('Arial', 12)).pack(pady=10)
        
        # 测试按钮
        def test_function():
            tk.messagebox.showinfo("测试", "按钮功能正常!")
        
        tk.Button(frame, text="测试按钮", 
                 command=test_function).pack(pady=10)
        
        tk.Button(frame, text="关闭", 
                 command=root.quit).pack(pady=10)
        
        # 显示系统信息
        info_text = f"Python版本: {sys.version.split()[0]}\n"
        info_text += f"tkinter版本: {tk.TkVersion}\n"
        info_text += f"系统平台: {sys.platform}"
        
        tk.Label(frame, text=info_text, 
                font=('Arial', 10), justify=tk.LEFT).pack(pady=20)
        
        print("✅ tkinter测试窗口已打开")
        print("如果看到测试窗口，说明GUI功能正常")
        
        root.mainloop()
        return True
        
    except ImportError:
        print("❌ tkinter未安装或不可用")
        return False
    except Exception as e:
        print(f"❌ tkinter测试失败: {e}")
        return False

def test_dependencies():
    """测试其他依赖"""
    results = []
    
    # 测试基础模块
    try:
        import threading
        results.append(("threading", True, "✅"))
    except ImportError:
        results.append(("threading", False, "❌"))
    
    try:
        import queue
        results.append(("queue", True, "✅"))
    except ImportError:
        results.append(("queue", False, "❌"))
    
    # 测试项目模块
    try:
        from config import config
        results.append(("config", True, "✅"))
    except ImportError:
        results.append(("config", False, "❌"))
    
    try:
        from simple_gui import SimpleFileProcessorGUI
        results.append(("simple_gui", True, "✅"))
    except ImportError:
        results.append(("simple_gui", False, "❌"))
    
    # 测试可选模块
    try:
        import spacy
        results.append(("spacy", True, "✅ (NLP功能可用)"))
    except ImportError:
        results.append(("spacy", False, "⚠️ (NLP功能受限)"))
    
    try:
        import nltk
        results.append(("nltk", True, "✅ (情感分析可用)"))
    except ImportError:
        results.append(("nltk", False, "⚠️ (情感分析受限)"))
    
    return results

def main():
    """主测试函数"""
    print("=" * 50)
    print("智能文件处理工具 - GUI测试")
    print("=" * 50)
    
    # 检查Python版本
    print(f"Python版本: {sys.version}")
    if sys.version_info < (3, 6):
        print("❌ 需要Python 3.6或更高版本")
        return False
    
    print("✅ Python版本符合要求")
    print()
    
    # 测试依赖
    print("检查依赖模块:")
    print("-" * 30)
    
    deps = test_dependencies()
    for name, available, status in deps:
        print(f"{status} {name}")
    
    print()
    
    # 检查必需的依赖
    required_deps = ["threading", "queue", "simple_gui"]
    missing_required = [name for name, available, _ in deps 
                       if name in required_deps and not available]
    
    if missing_required:
        print(f"❌ 缺少必需的依赖: {', '.join(missing_required)}")
        print("请检查文件是否完整")
        return False
    
    print("✅ 基础依赖检查通过")
    print()
    
    # 测试tkinter
    print("测试图形界面:")
    print("-" * 30)
    
    if not test_tkinter():
        print("❌ GUI测试失败")
        return False
    
    print("✅ GUI测试通过")
    print()
    
    # 总结
    print("=" * 50)
    print("测试完成!")
    
    optional_missing = [name for name, available, _ in deps 
                       if name in ["spacy", "nltk"] and not available]
    
    if optional_missing:
        print("⚠️  可选功能:")
        for name in optional_missing:
            if name == "spacy":
                print("   - NLP功能受限（可安装spacy获得完整功能）")
            elif name == "nltk":
                print("   - 情感分析受限（可安装nltk获得完整功能）")
        print("   但基础GUI功能仍可正常使用")
    else:
        print("🎉 所有功能都可用!")
    
    print()
    print("建议:")
    print("1. 运行 'python simple_gui.py' 启动简化版GUI")
    print("2. 运行 'python run_gui.py' 启动完整版GUI")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            input("按Enter键退出...")
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"\n测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        input("按Enter键退出...")