#!/usr/bin/env python3
"""
GUI功能测试脚本
"""
import sys
import tkinter as tk
from pathlib import Path

def test_tkinter():
    """测试tkinter是否可用"""
    print("测试tkinter...")
    try:
        root = tk.Tk()
        root.title("tkinter测试")
        root.geometry("300x200")
        
        label = tk.Label(root, text="tkinter工作正常！", font=('Arial', 12))
        label.pack(pady=50)
        
        button = tk.Button(root, text="关闭", command=root.destroy)
        button.pack()
        
        print("✅ tkinter测试窗口已打开")
        print("请关闭测试窗口继续...")
        root.mainloop()
        return True
        
    except Exception as e:
        print(f"❌ tkinter测试失败: {e}")
        return False

def test_simple_gui():
    """测试简化版GUI"""
    print("\n测试简化版GUI...")
    try:
        from simple_gui import SimpleGUI
        print("✅ 简化版GUI模块导入成功")
        
        # 创建但不启动GUI
        app = SimpleGUI()
        print("✅ 简化版GUI创建成功")
        
        # 销毁窗口
        app.root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ 简化版GUI测试失败: {e}")
        return False

def test_improved_gui():
    """测试完整版GUI"""
    print("\n测试完整版GUI...")
    try:
        # 先检查依赖
        import spacy
        import nltk
        from langdetect import detect
        print("✅ 核心依赖检查通过")
        
        from improved_gui import ModernGUI
        print("✅ 完整版GUI模块导入成功")
        
        # 创建但不启动GUI
        app = ModernGUI()
        print("✅ 完整版GUI创建成功")
        
        # 销毁窗口
        app.root.destroy()
        return True
        
    except ImportError as e:
        print(f"⚠️  完整版GUI依赖不足: {e}")
        return False
    except Exception as e:
        print(f"❌ 完整版GUI测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("🧪 GUI功能测试")
    print("=" * 50)
    
    results = []
    
    # 基础tkinter测试
    print("\n1. 基础tkinter测试")
    print("-" * 30)
    results.append(("tkinter", test_tkinter()))
    
    # 简化版GUI测试
    print("\n2. 简化版GUI测试")
    print("-" * 30)
    results.append(("简化版GUI", test_simple_gui()))
    
    # 完整版GUI测试
    print("\n3. 完整版GUI测试")
    print("-" * 30)
    results.append(("完整版GUI", test_improved_gui()))
    
    # 总结
    print("\n" + "=" * 50)
    print("📋 测试总结")
    print("=" * 50)
    
    for name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{name:15} - {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n总体结果: {passed}/{total} 测试通过")
    
    if passed >= 2:  # tkinter + 至少一个GUI版本
        print("🎉 GUI功能基本可用！")
        print("\n💡 建议:")
        if results[2][1]:  # 完整版GUI可用
            print("- 使用 python start_gui.py 启动完整版GUI")
        else:
            print("- 使用 python simple_gui.py 启动简化版GUI")
            print("- 安装缺失依赖以使用完整版GUI")
    else:
        print("⚠️  GUI功能不完整")
        print("\n💡 解决方案:")
        print("- 检查Python安装是否包含tkinter")
        print("- 重新安装Python或tkinter模块")
    
    return 0 if passed >= 2 else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
        sys.exit(0)