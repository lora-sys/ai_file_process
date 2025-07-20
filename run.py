#!/usr/bin/env python3
"""
智能文件处理工具 - 统一启动脚本
支持GUI和命令行两种模式
"""
import sys
import argparse
from pathlib import Path

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="智能文件处理工具 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用模式:
  python run.py                              # 启动GUI模式
  python run.py --cli                        # 使用命令行模式
  python run.py --cli input.txt output.txt  # 直接处理文件
  python run.py --gui                        # 强制启动GUI模式

示例:
  python run.py                              # 图形界面
  python run.py --cli document.txt result.txt --format json
  python run.py --cli input_folder/ output_folder/
        """
    )
    
    # 模式选择
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--gui", action="store_true", 
                           help="启动图形界面模式（默认）")
    mode_group.add_argument("--cli", action="store_true", 
                           help="使用命令行模式")
    
    # 命令行参数（仅在CLI模式下使用）
    parser.add_argument("input", nargs="?", help="输入文件或文件夹路径")
    parser.add_argument("output", nargs="?", help="输出文件或文件夹路径")
    
    parser.add_argument("--format", "-f", 
                       choices=["summary", "json", "text"],
                       default="summary",
                       help="输出格式（仅CLI模式）")
    
    parser.add_argument("--config", "-c", 
                       action="store_true",
                       help="显示配置信息（仅CLI模式）")
    
    parser.add_argument("--verbose", "-v", 
                       action="store_true",
                       help="启用详细输出（仅CLI模式）")
    
    parser.add_argument("--test", action="store_true",
                       help="运行功能测试")
    
    args = parser.parse_args()
    
    # 运行测试
    if args.test:
        print("正在运行功能测试...")
        try:
            from test_improvements import main as test_main
            return test_main()
        except ImportError:
            print("错误: 无法导入测试模块")
            return 1
    
    # 确定运行模式
    if args.cli or (args.input and args.output):
        # 命令行模式
        return run_cli_mode(args)
    else:
        # GUI模式（默认）
        return run_gui_mode()

def run_gui_mode():
    """运行GUI模式"""
    print("启动图形界面...")
    
    try:
        # 检查GUI依赖
        import tkinter as tk
        from tkinter import ttk
        
        # 导入GUI模块
        from improved_gui import ModernGUI
        
        # 创建并运行GUI
        app = ModernGUI()
        app.run()
        return 0
        
    except ImportError as e:
        print(f"GUI依赖缺失: {e}")
        print("正在回退到命令行模式...")
        return run_cli_fallback()
        
    except Exception as e:
        print(f"GUI启动失败: {e}")
        print("正在回退到命令行模式...")
        return run_cli_fallback()

def run_cli_mode(args):
    """运行命令行模式"""
    try:
        from improved_main import main as cli_main
        
        # 构建CLI参数
        cli_args = []
        
        if args.input:
            cli_args.append(args.input)
        if args.output:
            cli_args.append(args.output)
            
        if args.format:
            cli_args.extend(["--format", args.format])
        if args.config:
            cli_args.append("--config")
        if args.verbose:
            cli_args.append("--verbose")
        
        # 备份原始参数
        original_argv = sys.argv
        try:
            # 设置CLI参数
            sys.argv = ["improved_main.py"] + cli_args
            return cli_main()
        finally:
            # 恢复原始参数
            sys.argv = original_argv
            
    except ImportError:
        print("错误: 无法导入CLI模块")
        return 1
    except Exception as e:
        print(f"CLI运行失败: {e}")
        return 1

def run_cli_fallback():
    """CLI回退模式"""
    print("\n" + "="*50)
    print("智能文件处理工具 v2.0 - 简化CLI模式")
    print("="*50)
    
    try:
        # 简单的交互式处理
        input_path = input("请输入文件或文件夹路径: ").strip()
        if not input_path:
            print("未提供输入路径，退出")
            return 1
            
        if not Path(input_path).exists():
            print(f"路径不存在: {input_path}")
            return 1
            
        output_path = input("请输入输出路径: ").strip()
        if not output_path:
            print("未提供输出路径，退出")
            return 1
            
        format_choice = input("选择输出格式 (1=摘要, 2=JSON, 3=纯文本) [1]: ").strip() or "1"
        format_map = {"1": "summary", "2": "json", "3": "text"}
        output_format = format_map.get(format_choice, "summary")
        
        print(f"\n开始处理...")
        print(f"输入: {input_path}")
        print(f"输出: {output_path}")
        print(f"格式: {output_format}")
        
        # 导入处理模块
        from improved_main import FileProcessor
        
        processor = FileProcessor()
        
        if Path(input_path).is_file():
            success = processor.process_single_file(input_path, output_path, output_format)
        else:
            result = processor.process_batch(input_path, output_path, output_format)
            success = result.get("success", False)
        
        if success:
            print("\n✅ 处理完成！")
            return 0
        else:
            print("\n❌ 处理失败！")
            return 1
            
    except KeyboardInterrupt:
        print("\n用户中断处理")
        return 1
    except Exception as e:
        print(f"\n处理失败: {e}")
        return 1

def check_dependencies():
    """检查依赖"""
    missing_deps = []
    
    # 基础依赖
    try:
        import pathlib
        import json
        import re
        import logging
    except ImportError as e:
        missing_deps.append(f"基础模块: {e}")
    
    # NLP依赖
    try:
        import spacy
        import langdetect
        import nltk
    except ImportError as e:
        missing_deps.append(f"NLP模块: {e}")
    
    # 文件处理依赖
    try:
        import PyPDF2
        import openpyxl
    except ImportError as e:
        missing_deps.append(f"文件处理模块: {e}")
    
    # GUI依赖（可选）
    try:
        import tkinter
        from tkinter import ttk
    except ImportError:
        print("注意: GUI依赖缺失，将只能使用命令行模式")
    
    if missing_deps:
        print("缺少以下依赖:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\n请运行: pip install -r requirements.txt")
        return False
    
    return True

if __name__ == "__main__":
    # 检查依赖
    if not check_dependencies():
        print("依赖检查失败，请先安装必要的依赖包")
        sys.exit(1)
    
    # 运行主程序
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"程序运行时发生未知错误: {e}")
        sys.exit(1)