#!/usr/bin/env python3
"""
测试核心功能（不包含GUI）
"""
import sys
from pathlib import Path

def test_imports():
    """测试模块导入"""
    print("测试模块导入...")
    
    try:
        # 测试基本模块
        from pathlib import Path
        import json
        import threading
        import queue
        print("✓ 基本模块导入成功")
        
        # 测试配置模块
        try:
            from config import config
            print("✓ 配置模块导入成功")
        except Exception as e:
            print(f"⚠ 配置模块导入失败: {e}")
            return False
        
        # 测试文件处理模块
        try:
            from improved_file_handler import file_handler
            print("✓ 文件处理模块导入成功")
        except Exception as e:
            print(f"⚠ 文件处理模块导入失败: {e}")
            return False
        
        # 测试数据处理模块  
        try:
            from improved_data_processor import text_processor, result_formatter
            print("✓ 数据处理模块导入成功")
        except Exception as e:
            print(f"⚠ 数据处理模块导入失败: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ 模块导入失败: {e}")
        return False

def test_config():
    """测试配置功能"""
    print("\n测试配置功能...")
    
    try:
        from config import config
        
        # 测试配置读取
        max_size = config.get('processing.max_file_size_mb', 100)
        max_workers = config.get('processing.max_workers', 4)
        print(f"✓ 配置读取成功: 最大文件大小={max_size}MB, 并发数={max_workers}")
        
        # 测试支持的格式
        formats = config.get('processing.supported_formats', [])
        print(f"✓ 支持的文件格式: {', '.join(formats) if formats else '未配置'}")
        
        return True
        
    except Exception as e:
        print(f"✗ 配置测试失败: {e}")
        return False

def test_file_operations():
    """测试文件操作"""
    print("\n测试文件操作...")
    
    try:
        from improved_file_handler import file_handler
        
        # 创建测试文件
        test_content = "Hello world! This is a test. Numbers: 123, 456.78. Date: 2024-01-15."
        test_file = Path("test_sample.txt")
        
        # 写入测试
        success = file_handler.write_file(test_file, test_content)
        if success:
            print("✓ 文件写入成功")
        else:
            print("✗ 文件写入失败")
            return False
        
        # 读取测试
        content = file_handler.read_file(test_file)
        if content and content.strip() == test_content.strip():
            print("✓ 文件读取成功")
        else:
            print("✗ 文件读取失败")
            return False
        
        # 验证测试
        is_valid = file_handler.validate_file(test_file)
        if is_valid:
            print("✓ 文件验证成功")
        else:
            print("✗ 文件验证失败")
        
        # 清理测试文件
        test_file.unlink()
        print("✓ 测试文件已清理")
        
        return True
        
    except Exception as e:
        print(f"✗ 文件操作测试失败: {e}")
        return False

def test_text_processing():
    """测试文本处理"""
    print("\n测试文本处理...")
    
    try:
        from improved_data_processor import text_processor, result_formatter
        
        # 测试文本
        test_text = "Hello world! This is a wonderful day. I feel great! Numbers: 123, 456.78. Date: 2024-01-15."
        
        # 处理文本
        result = text_processor.process_text(test_text)
        
        if result:
            print("✓ 文本处理成功")
            print(f"  - 检测语言: {result.language}")
            print(f"  - 字符数: {len(result.original_text)}")
            print(f"  - 处理后字符数: {len(result.processed_text)}")
            print(f"  - 提取数字: {result.numbers}")
            print(f"  - 提取日期: {result.dates}")
            print(f"  - 情感分析: {result.sentiment}")
            
            # 测试格式化
            summary = result_formatter.to_summary_text(result)
            if summary:
                print("✓ 摘要格式化成功")
            
            json_output = result_formatter.to_json(result)
            if json_output:
                print("✓ JSON格式化成功")
                
            return True
        else:
            print("✗ 文本处理失败")
            return False
        
    except Exception as e:
        print(f"✗ 文本处理测试失败: {e}")
        return False

def test_integration():
    """测试集成功能"""
    print("\n测试集成功能...")
    
    try:
        from improved_main import FileProcessor
        
        processor = FileProcessor()
        print("✓ 文件处理器创建成功")
        
        # 创建测试文件
        test_content = """
        Hello everyone! This is a comprehensive test document.
        
        It contains various types of content:
        - Numbers: 42, 3.14159, 1,234.56
        - Dates: 2024-01-15, 12/25/2023
        - Emotions: I'm very happy and excited about this project!
        - Technical terms: artificial intelligence, machine learning
        
        This document will test our processing capabilities thoroughly.
        """
        
        test_input = Path("integration_test_input.txt")
        test_output = Path("integration_test_output.txt")
        
        # 写入测试文件
        with open(test_input, 'w', encoding='utf-8') as f:
            f.write(test_content.strip())
        
        # 处理文件
        success = processor.process_single_file(
            str(test_input), str(test_output), "summary"
        )
        
        if success and test_output.exists():
            print("✓ 集成处理成功")
            
            # 读取结果
            with open(test_output, 'r', encoding='utf-8') as f:
                result_content = f.read()
                print(f"✓ 结果文件大小: {len(result_content)} 字符")
        else:
            print("✗ 集成处理失败")
            return False
        
        # 清理测试文件
        test_input.unlink()
        test_output.unlink()
        print("✓ 测试文件已清理")
        
        return True
        
    except Exception as e:
        print(f"✗ 集成测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("智能文件处理工具 - 核心功能测试")
    print("=" * 50)
    
    test_functions = [
        test_imports,
        test_config,
        test_file_operations,
        test_text_processing,
        test_integration
    ]
    
    results = []
    
    for test_func in test_functions:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"✗ 测试函数 {test_func.__name__} 执行失败: {e}")
            results.append(False)
    
    # 总结结果
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有核心功能测试通过！")
        print("\n下一步:")
        print("1. 安装tkinter: sudo apt-get install python3-tk (Linux)")
        print("2. 测试GUI: python3 test_gui.py")
        print("3. 启动GUI: python3 start_gui.py")
        return True
    else:
        failed_tests = [name for name, result in zip([f.__name__ for f in test_functions], results) if not result]
        print(f"⚠️ 失败的测试: {', '.join(failed_tests)}")
        print("请检查相关模块和依赖")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)