#!/usr/bin/env python3
"""
智能文件处理工具 - 统一启动脚本
"""
import sys
import argparse
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

def check_gui_dependencies():
    """检查GUI依赖"""
    try:
        import tkinter
        return True
    except ImportError:
        return False

def launch_gui():
    """启动GUI"""
    print("🎨 启动图形界面...")
    try:
        from improved_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"❌ 无法导入GUI模块: {e}")
        print("尝试启动启动器...")
        try:
            from gui_launcher import main as launcher_main
            launcher_main()
        except ImportError:
            print("❌ GUI模块不可用")
            return False
    except Exception as e:
        print(f"❌ GUI启动失败: {e}")
        return False
    return True

def launch_cli(args):
    """启动命令行版本"""
    print("🖥️  启动命令行模式...")
    try:
        from improved_main import main as cli_main
        
        # 构建参数
        cli_args = []
        if hasattr(args, 'input') and args.input:
            cli_args.append(args.input)
        if hasattr(args, 'output') and args.output:
            cli_args.append(args.output)
        if hasattr(args, 'format') and args.format:
            cli_args.extend(['--format', args.format])
        if hasattr(args, 'config') and args.config:
            cli_args.append('--config')
        if hasattr(args, 'verbose') and args.verbose:
            cli_args.append('--verbose')
        
        # 临时替换sys.argv
        original_argv = sys.argv
        sys.argv = ['improved_main.py'] + cli_args
        
        try:
            return cli_main()
        finally:
            sys.argv = original_argv
            
    except ImportError as e:
        print(f"❌ 无法导入CLI模块: {e}")
        return 1
    except Exception as e:
        print(f"❌ CLI启动失败: {e}")
        return 1

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="智能文件处理工具 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s                                    # 启动GUI（默认）
  %(prog)s --gui                              # 强制启动GUI
  %(prog)s --cli input.txt output.txt         # 命令行模式
  %(prog)s --demo                             # 启动演示
  %(prog)s --config                           # 查看配置
        """
    )
    
    # 模式选择
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('--gui', action='store_true', 
                           help='启动图形界面（默认）')
    mode_group.add_argument('--cli', action='store_true', 
                           help='启动命令行模式')
    mode_group.add_argument('--demo', action='store_true', 
                           help='启动演示模式')
    
    # CLI参数
    parser.add_argument('input', nargs='?', help='输入文件或文件夹')
    parser.add_argument('output', nargs='?', help='输出文件或文件夹')
    parser.add_argument('--format', choices=['summary', 'json', 'text'], 
                       default='summary', help='输出格式')
    parser.add_argument('--config', action='store_true', help='显示配置')
    parser.add_argument('--verbose', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    print("🚀 智能文件处理工具 v2.0")
    print("=" * 50)
    
    # 处理演示模式
    if args.demo:
        print("🎭 启动演示模式...")
        try:
            from gui_demo import main as demo_main
            demo_main()
            return 0
        except ImportError:
            print("❌ 演示模块不可用")
            return 1
    
    # 处理命令行模式
    if args.cli or args.input or args.output or args.config:
        return launch_cli(args)
    
    # 默认启动GUI
    if not check_gui_dependencies():
        print("⚠️  GUI依赖不可用，切换到命令行模式")
        return launch_cli(args)
    
    if launch_gui():
        return 0
    else:
        print("🔄 GUI启动失败，切换到命令行模式")
        return launch_cli(args)

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ 意外错误: {e}")
        sys.exit(1)