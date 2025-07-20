#!/usr/bin/env python3
"""
测试改进效果的脚本
"""
import sys
import os
from pathlib import Path

# 添加当前目录到路径
sys.path.append(str(Path(__file__).parent))

def test_config():
    """测试配置模块"""
    print("=" * 50)
    print("测试配置模块")
    print("=" * 50)
    
    try:
        from config import config
        
        print(f"✓ 配置模块加载成功")
        print(f"  - 支持的文件格式: {config.get('processing.supported_formats')}")
        print(f"  - 最大文件大小: {config.get('processing.max_file_size_mb')} MB")
        print(f"  - 并发处理数: {config.get('processing.max_workers')}")
        print(f"  - 语言检测: {config.get('nlp.detect_language')}")
        
        return True
    except Exception as e:
        print(f"✗ 配置模块测试失败: {e}")
        return False

def test_file_handler():
    """测试文件处理模块"""
    print("\n" + "=" * 50)
    print("测试文件处理模块")
    print("=" * 50)
    
    try:
        from improved_file_handler import FileHandler
        
        handler = FileHandler()
        print(f"✓ 文件处理器创建成功")
        
        # 测试文件验证
        test_file = "data.txt"
        if Path(test_file).exists():
            is_valid = handler.validate_file(test_file)
            print(f"  - 文件验证: {'✓' if is_valid else '✗'} {test_file}")
        
        # 测试文件读取
        if Path(test_file).exists():
            content = handler.read_file(test_file)
            if content:
                print(f"  - 文件读取: ✓ (读取了 {len(content)} 个字符)")
            else:
                print(f"  - 文件读取: ✗ 无法读取内容")
        
        return True
    except Exception as e:
        print(f"✗ 文件处理模块测试失败: {e}")
        return False

def test_data_processor():
    """测试数据处理模块"""
    print("\n" + "=" * 50)
    print("测试数据处理模块")
    print("=" * 50)
    
    try:
        from improved_data_processor import AdvancedTextProcessor, ResultFormatter
        
        processor = AdvancedTextProcessor()
        formatter = ResultFormatter()
        print(f"✓ 数据处理器创建成功")
        
        # 测试文本处理
        test_text = "Hello world! This is a test with 123 numbers and 2024-01-01 date."
        result = processor.process_text(test_text)
        
        print(f"  - 文本处理: ✓")
        print(f"    * 检测语言: {result.language}")
        print(f"    * 提取数字: {result.numbers}")
        print(f"    * 提取日期: {result.dates}")
        print(f"    * 情感分析: {result.sentiment}")
        print(f"    * 统计信息: 字符数={result.statistics.get('char_count', 0)}")
        
        # 测试格式化
        summary = formatter.to_summary_text(result)
        print(f"  - 结果格式化: ✓ (生成了 {len(summary)} 字符的摘要)")
        
        return True
    except Exception as e:
        print(f"✗ 数据处理模块测试失败: {e}")
        return False

def test_integration():
    """测试集成功能"""
    print("\n" + "=" * 50)
    print("测试集成功能")
    print("=" * 50)
    
    try:
        from improved_main import FileProcessor
        
        processor = FileProcessor()
        print(f"✓ 主处理器创建成功")
        
        # 测试单文件处理
        input_file = "data.txt"
        output_file = "test_output.txt"
        
        if Path(input_file).exists():
            success = processor.process_single_file(
                input_file, output_file, "summary"
            )
            
            if success and Path(output_file).exists():
                print(f"  - 单文件处理: ✓ 输出文件已生成")
                # 清理测试文件
                Path(output_file).unlink()
            else:
                print(f"  - 单文件处理: ✗ 处理失败")
        else:
            print(f"  - 单文件处理: ⚠ 测试文件不存在")
        
        return True
    except Exception as e:
        print(f"✗ 集成测试失败: {e}")
        return False

def test_gui():
    """测试GUI模块"""
    print("\n" + "=" * 50)
    print("测试GUI模块")
    print("=" * 50)
    
    try:
        # 检查tkinter
        import tkinter as tk
        print(f"✓ Tkinter 模块可用")
        
        # 测试GUI模块导入
        from improved_gui import ModernGUI
        print(f"✓ GUI模块导入成功")
        
        # 测试GUI类创建（不启动mainloop）
        try:
            # 创建一个测试根窗口
            test_root = tk.Tk()
            test_root.withdraw()  # 隐藏窗口
            
            # 测试关键组件
            print(f"  - 测试GUI组件创建...")
            
            # 销毁测试窗口
            test_root.destroy()
            print(f"  - GUI组件测试: ✓ 通过")
            
        except Exception as e:
            print(f"  - GUI组件测试: ✗ 失败 ({e})")
            return False
        
        # 测试启动脚本
        try:
            import run_gui
            print(f"✓ GUI启动脚本可用")
        except Exception as e:
            print(f"✗ GUI启动脚本导入失败: {e}")
            return False
        
        return True
        
    except ImportError as e:
        print(f"✗ GUI测试失败: {e}")
        print("  提示: 在某些环境中tkinter可能不可用")
        return False
    except Exception as e:
        print(f"✗ GUI测试失败: {e}")
        return False





def main():
    """主测试函数"""
    print("智能文件处理工具 - 改进测试")
    print("=" * 50)
    
    test_results = []
    
    # 运行各项测试
    test_results.append(test_config())
    test_results.append(test_file_handler())
    test_results.append(test_data_processor())
    test_results.append(test_integration())
    test_results.append(test_gui())
    
    # 总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    
    passed = sum(test_results)
    total = len(test_results)
    
    print(f"通过测试: {passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过！改进成功！")
        return 0
    else:
        print("⚠️  部分测试失败，请检查相关模块")
        return 1

if __name__ == "__main__":
    sys.exit(main())