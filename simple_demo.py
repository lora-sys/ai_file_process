#!/usr/bin/env python3
"""
智能文件处理工具 - 简单演示版本
"""
import sys
from pathlib import Path

def test_simple_modules():
    """测试简化模块"""
    print("智能文件处理工具 - 简单演示")
    print("=" * 50)
    
    try:
        # 导入简化模块
        from simple_file_handler import simple_file_handler
        from simple_data_processor import simple_text_processor, simple_result_formatter
        from config import config
        
        print("✓ 所有模块导入成功")
        
        # 创建测试文件
        test_content = """
        Hello world! This is a fantastic demonstration.
        
        Our tool can process various types of content:
        - Numbers: 42, 3.14159, 1,234.56
        - Dates: 2024-01-15, 12/25/2023  
        - Emotions: I'm very excited and happy about this project!
        - Mixed content: The temperature is 25.5°C today.
        
        这是一个包含中文的测试文档。
        日期：2024年1月15日
        数字：100, 200.5
        
        This comprehensive test will showcase our processing capabilities.
        """
        
        test_file = Path("demo_input.txt")
        
        # 写入测试文件
        print("\n1. 创建测试文件...")
        success = simple_file_handler.write_file(test_file, test_content.strip())
        if success:
            print("✓ 测试文件创建成功")
        else:
            print("✗ 测试文件创建失败")
            return False
        
        # 读取文件
        print("\n2. 读取文件...")
        content = simple_file_handler.read_file(test_file)
        if content:
            print(f"✓ 文件读取成功 ({len(content)} 字符)")
        else:
            print("✗ 文件读取失败")
            return False
        
        # 处理文本
        print("\n3. 处理文本...")
        result = simple_text_processor.process_text(content)
        if result:
            print("✓ 文本处理成功")
            print(f"  - 语言: {result.language}")
            print(f"  - 字符数: {result.char_count}")
            print(f"  - 词数: {result.word_count}")
            print(f"  - 句子数: {result.sentence_count}")
            print(f"  - 提取数字: {result.numbers}")
            print(f"  - 提取日期: {result.dates}")
        else:
            print("✗ 文本处理失败")
            return False
        
        # 生成摘要
        print("\n4. 生成处理摘要...")
        summary = simple_result_formatter.to_summary_text(result)
        print("✓ 摘要生成成功:")
        print("-" * 30)
        print(summary)
        print("-" * 30)
        
        # 生成JSON
        print("\n5. 生成JSON格式...")
        json_output = simple_result_formatter.to_json(result)
        print("✓ JSON格式生成成功")
        print(f"JSON长度: {len(json_output)} 字符")
        
        # 保存结果
        print("\n6. 保存处理结果...")
        output_file = Path("demo_output.txt")
        success = simple_file_handler.write_file(output_file, summary)
        if success:
            print("✓ 结果文件保存成功")
        else:
            print("✗ 结果文件保存失败")
        
        # 保存JSON结果
        json_file = Path("demo_output.json")
        success = simple_file_handler.write_file(json_file, json_output)
        if success:
            print("✓ JSON文件保存成功")
        else:
            print("✗ JSON文件保存失败")
        
        print("\n" + "=" * 50)
        print("🎉 演示完成！")
        print(f"📁 生成的文件:")
        print(f"  - 输入文件: {test_file}")
        print(f"  - 摘要结果: {output_file}")
        print(f"  - JSON结果: {json_file}")
        
        print(f"\n📊 处理统计:")
        print(f"  - 原始文本: {result.char_count} 字符")
        print(f"  - 处理后文本: {len(result.processed_text)} 字符")
        print(f"  - 提取数字: {len(result.numbers)} 个")
        print(f"  - 提取日期: {len(result.dates)} 个")
        
        return True
        
    except Exception as e:
        print(f"✗ 演示失败: {e}")
        return False

def show_config():
    """显示配置信息"""
    print("\n配置信息:")
    print("=" * 30)
    
    try:
        from config import config
        
        print(f"支持的文件格式: {config.get('processing.supported_formats', ['txt', 'csv', 'json'])}")
        print(f"最大文件大小: {config.get('processing.max_file_size_mb', 100)} MB")
        print(f"并发处理数: {config.get('processing.max_workers', 4)}")
        print(f"语言检测: {'启用' if config.get('nlp.detect_language', True) else '禁用'}")
        
    except Exception as e:
        print(f"配置读取失败: {e}")

def main():
    """主函数"""
    print("欢迎使用智能文件处理工具!")
    print("这是一个简化版演示，展示核心功能")
    
    # 显示配置
    show_config()
    
    # 运行演示
    success = test_simple_modules()
    
    if success:
        print("\n🚀 下一步:")
        print("1. 查看生成的结果文件")
        print("2. 尝试处理自己的文件")
        print("3. 如果需要更多功能，安装完整版依赖:")
        print("   pip install -r requirements.txt")
        print("4. 启动完整版GUI:")
        print("   python start_gui.py")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)