#!/usr/bin/env python3
"""
创建桌面快捷方式
"""
import os
import sys
from pathlib import Path

def create_windows_shortcut():
    """为Windows创建快捷方式"""
    try:
        import winshell
        from win32com.client import Dispatch
        
        # 获取桌面路径
        desktop = winshell.desktop()
        
        # 快捷方式路径
        shortcut_path = os.path.join(desktop, "智能文件处理工具.lnk")
        
        # 当前脚本目录
        current_dir = Path(__file__).parent.absolute()
        
        # 创建快捷方式
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{current_dir / "run_gui.py"}"'
        shortcut.WorkingDirectory = str(current_dir)
        shortcut.IconLocation = sys.executable
        shortcut.Description = "智能文件处理工具 - 图形界面"
        shortcut.save()
        
        print(f"✅ 已在桌面创建快捷方式: {shortcut_path}")
        return True
        
    except ImportError:
        print("❌ 缺少依赖：pip install winshell pywin32")
        return False
    except Exception as e:
        print(f"❌ 创建快捷方式失败: {e}")
        return False

def create_linux_shortcut():
    """为Linux创建桌面文件"""
    try:
        # 获取桌面路径
        desktop_dir = Path.home() / "Desktop"
        if not desktop_dir.exists():
            desktop_dir = Path.home() / "桌面"
        
        if not desktop_dir.exists():
            print("❌ 未找到桌面目录")
            return False
        
        # 当前脚本目录
        current_dir = Path(__file__).parent.absolute()
        
        # 创建.desktop文件
        desktop_file = desktop_dir / "智能文件处理工具.desktop"
        
        desktop_content = f"""[Desktop Entry]
Name=智能文件处理工具
Comment=智能文件处理工具 - 图形界面
Exec={sys.executable} "{current_dir / "run_gui.py"}"
Icon=application-x-executable
Terminal=false
Type=Application
Categories=Utility;
"""
        
        with open(desktop_file, 'w', encoding='utf-8') as f:
            f.write(desktop_content)
        
        # 设置执行权限
        os.chmod(desktop_file, 0o755)
        
        print(f"✅ 已在桌面创建快捷方式: {desktop_file}")
        return True
        
    except Exception as e:
        print(f"❌ 创建快捷方式失败: {e}")
        return False

def create_macos_shortcut():
    """为macOS创建快捷方式"""
    try:
        # 获取桌面路径
        desktop_dir = Path.home() / "Desktop"
        
        if not desktop_dir.exists():
            print("❌ 未找到桌面目录")
            return False
        
        # 当前脚本目录
        current_dir = Path(__file__).parent.absolute()
        
        # 创建shell脚本
        script_file = desktop_dir / "智能文件处理工具.command"
        
        script_content = f"""#!/bin/bash
cd "{current_dir}"
{sys.executable} run_gui.py
"""
        
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # 设置执行权限
        os.chmod(script_file, 0o755)
        
        print(f"✅ 已在桌面创建快捷方式: {script_file}")
        return True
        
    except Exception as e:
        print(f"❌ 创建快捷方式失败: {e}")
        return False

def main():
    """主函数"""
    print("🔗 创建桌面快捷方式...")
    
    # 检测操作系统
    if sys.platform.startswith('win'):
        print("🖥️ 检测到Windows系统")
        success = create_windows_shortcut()
    elif sys.platform.startswith('linux'):
        print("🐧 检测到Linux系统")
        success = create_linux_shortcut()
    elif sys.platform.startswith('darwin'):
        print("🍎 检测到macOS系统")
        success = create_macos_shortcut()
    else:
        print(f"❌ 不支持的操作系统: {sys.platform}")
        return 1
    
    if success:
        print("\n🎉 快捷方式创建成功！")
        print("📌 你现在可以从桌面启动智能文件处理工具了。")
        return 0
    else:
        print("\n⚠️ 快捷方式创建失败，请手动运行程序:")
        print(f"   python {Path(__file__).parent / 'run_gui.py'}")
        return 1

if __name__ == "__main__":
    sys.exit(main())