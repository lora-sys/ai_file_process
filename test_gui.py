#!/usr/bin/env python3
"""
GUI功能测试脚本
测试所有GUI版本是否能正常启动
"""
import sys
import subprocess
import time
from pathlib import Path

def test_gui_version(script_name, gui_name):
    """测试特定GUI版本"""
    print(f"\n测试 {gui_name}...")
    
    if not Path(script_name).exists():
        print(f"❌ {script_name} 文件不存在")
        return False
    
    try:
        # 启动GUI（不等待，让它在后台运行）
        process = subprocess.Popen([
            sys.executable, script_name
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待一小段时间看是否有错误
        time.sleep(2)
        
        # 检查进程状态
        poll_result = process.poll()
        
        if poll_result is None:
            # 进程仍在运行，说明启动成功
            print(f"✅ {gui_name} 启动成功")
            
            # 终止进程
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            
            return True
        else:
            # 进程已退出，可能有错误
            stdout, stderr = process.communicate()
            print(f"❌ {gui_name} 启动失败")
            if stderr:
                print(f"   错误信息: {stderr.decode('utf-8').strip()}")
            return False
            
    except Exception as e:
        print(f"❌ {gui_name} 测试异常: {e}")
        return False

def check_dependencies():
    """检查依赖"""
    print("检查依赖...")
    
    required_modules = [
        "tkinter",
        "pathlib",
        "json",
        "threading",
        "queue"
    ]
    
    optional_modules = [
        "tkinterdnd2"  # 高级GUI需要
    ]
    
    missing_required = []
    missing_optional = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            missing_required.append(module)
            print(f"❌ {module} (必需)")
    
    for module in optional_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            missing_optional.append(module)
            print(f"⚠️  {module} (可选，高级GUI需要)")
    
    return missing_required, missing_optional

def main():
    """主函数"""
    print("🧪 GUI功能测试脚本")
    print("=" * 50)
    
    # 检查依赖
    missing_required, missing_optional = check_dependencies()
    
    if missing_required:
        print(f"\n❌ 缺少必需依赖: {', '.join(missing_required)}")
        print("请运行: pip install -r requirements.txt")
        return 1
    
    if missing_optional:
        print(f"\n⚠️  缺少可选依赖: {', '.join(missing_optional)}")
        print("高级GUI功能可能不可用")
    
    print("\n" + "=" * 50)
    print("开始测试GUI版本...")
    
    # 测试各个GUI版本
    test_results = []
    
    # 测试GUI启动器
    result = test_gui_version("gui_launcher.py", "GUI启动器")
    test_results.append(("GUI启动器", result))
    
    # 测试原版GUI
    result = test_gui_version("gui.py", "原版GUI")
    test_results.append(("原版GUI", result))
    
    # 测试现代GUI
    result = test_gui_version("improved_gui.py", "现代GUI")
    test_results.append(("现代GUI", result))
    
    # 测试高级GUI
    if "tkinterdnd2" not in missing_optional:
        result = test_gui_version("advanced_gui.py", "高级GUI")
        test_results.append(("高级GUI", result))
    else:
        print(f"\n⚠️  跳过高级GUI测试（缺少tkinterdnd2）")
        test_results.append(("高级GUI", "跳过"))
    
    # 测试结果汇总
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    print("=" * 50)
    
    for name, result in test_results:
        if result is True:
            print(f"✅ {name}: 通过")
        elif result is False:
            print(f"❌ {name}: 失败")
        else:
            print(f"⚠️  {name}: {result}")
    
    # 统计
    passed = sum(1 for _, result in test_results if result is True)
    total = len([r for _, r in test_results if r is not "跳过"])
    
    print(f"\n📊 测试统计: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有GUI版本测试通过！")
        return 0
    else:
        print("⚠️  部分GUI版本测试失败，请检查错误信息")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n用户中断测试")
        sys.exit(1)
    except Exception as e:
        print(f"\n测试脚本运行异常: {e}")
        sys.exit(1)