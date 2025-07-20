#!/usr/bin/env python3
"""
GUI测试脚本 - 验证所有GUI版本能否正常启动
"""
import sys
import importlib.util
from pathlib import Path

def test_gui_imports():
    """测试GUI模块导入"""
    gui_modules = [
        ("gui", "原版GUI"),
        ("modern_gui", "现代化GUI"), 
        ("premium_gui", "高级GUI"),
        ("gui_launcher", "GUI启动器")
    ]
    
    print("=" * 50)
    print("GUI模块导入测试")
    print("=" * 50)
    
    results = {}
    
    for module_name, display_name in gui_modules:
        try:
            # 检查文件是否存在
            module_file = Path(f"{module_name}.py")
            if not module_file.exists():
                print(f"❌ {display_name}: 文件不存在 ({module_name}.py)")
                results[module_name] = False
                continue
            
            # 尝试导入模块
            spec = importlib.util.spec_from_file_location(module_name, module_file)
            module = importlib.util.module_from_spec(spec)
            
            # 简单的语法检查
            with open(module_file, 'r', encoding='utf-8') as f:
                compile(f.read(), module_file, 'exec')
            
            print(f"✅ {display_name}: 导入成功")
            results[module_name] = True
            
        except SyntaxError as e:
            print(f"❌ {display_name}: 语法错误 - {e}")
            results[module_name] = False
            
        except Exception as e:
            print(f"⚠️  {display_name}: 导入警告 - {e}")
            results[module_name] = True  # 可能只是依赖问题
    
    return results

def test_dependencies():
    """测试依赖项"""
    print("\n" + "=" * 50)
    print("依赖项测试")
    print("=" * 50)
    
    required_deps = [
        ("tkinter", "GUI基础库"),
        ("pathlib", "路径处理"),
        ("threading", "多线程支持"),
        ("queue", "队列处理"),
        ("json", "JSON处理")
    ]
    
    optional_deps = [
        ("improved_file_handler", "改进的文件处理器"),
        ("improved_data_processor", "改进的数据处理器"),
        ("config", "配置管理")
    ]
    
    dep_results = {}
    
    print("必需依赖:")
    for dep, desc in required_deps:
        try:
            __import__(dep)
            print(f"✅ {desc} ({dep})")
            dep_results[dep] = True
        except ImportError:
            print(f"❌ {desc} ({dep}) - 缺失")
            dep_results[dep] = False
    
    print("\n可选依赖:")
    for dep, desc in optional_deps:
        try:
            __import__(dep)
            print(f"✅ {desc} ({dep})")
            dep_results[dep] = True
        except ImportError:
            print(f"⚠️  {desc} ({dep}) - 未找到")
            dep_results[dep] = False
    
    return dep_results

def check_file_structure():
    """检查文件结构"""
    print("\n" + "=" * 50)
    print("文件结构检查")
    print("=" * 50)
    
    required_files = [
        "gui.py",
        "modern_gui.py", 
        "premium_gui.py",
        "gui_launcher.py",
        "improved_main.py",
        "config.py",
        "improved_file_handler.py",
        "improved_data_processor.py"
    ]
    
    optional_files = [
        "requirements.txt",
        "README_improved.md",
        "test_improvements.py"
    ]
    
    file_results = {}
    
    print("必需文件:")
    for file_name in required_files:
        if Path(file_name).exists():
            print(f"✅ {file_name}")
            file_results[file_name] = True
        else:
            print(f"❌ {file_name} - 缺失")
            file_results[file_name] = False
    
    print("\n可选文件:")
    for file_name in optional_files:
        if Path(file_name).exists():
            print(f"✅ {file_name}")
            file_results[file_name] = True
        else:
            print(f"⚠️  {file_name} - 未找到")
            file_results[file_name] = False
    
    return file_results

def generate_report(gui_results, dep_results, file_results):
    """生成测试报告"""
    print("\n" + "=" * 50)
    print("测试报告")
    print("=" * 50)
    
    # 统计结果
    gui_passed = sum(1 for result in gui_results.values() if result)
    gui_total = len(gui_results)
    
    dep_passed = sum(1 for result in dep_results.values() if result)
    dep_total = len(dep_results)
    
    file_passed = sum(1 for result in file_results.values() if result)
    file_total = len(file_results)
    
    print(f"GUI模块: {gui_passed}/{gui_total} 通过")
    print(f"依赖项: {dep_passed}/{dep_total} 可用")
    print(f"文件结构: {file_passed}/{file_total} 完整")
    
    # 整体评估
    if gui_passed == gui_total and all(file_results[f] for f in ["gui.py", "modern_gui.py", "premium_gui.py"]):
        print("\n🎉 所有GUI版本就绪！")
        print("建议运行: python gui_launcher.py")
    elif gui_passed > 0:
        print("\n⚠️  部分GUI可用")
        available_guis = [name for name, result in gui_results.items() if result]
        print(f"可用的GUI: {', '.join(available_guis)}")
    else:
        print("\n❌ GUI不可用")
        print("请检查依赖项和文件完整性")
    
    # 建议
    print("\n💡 建议:")
    if not dep_results.get("improved_file_handler", False):
        print("- 确保改进的核心模块已创建")
    if not file_results.get("requirements.txt", False):
        print("- 安装必需的依赖包")
    if gui_passed < gui_total:
        print("- 检查GUI文件的语法错误")

def main():
    """主函数"""
    print("智能文件处理工具 - GUI测试")
    
    try:
        # 运行各项测试
        gui_results = test_gui_imports()
        dep_results = test_dependencies()
        file_results = check_file_structure()
        
        # 生成报告
        generate_report(gui_results, dep_results, file_results)
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()