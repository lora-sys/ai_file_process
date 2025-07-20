#!/usr/bin/env python3
"""
智能文件处理工具演示脚本
"""
import sys
import os
from pathlib import Path
import tempfile
import json

# 添加当前目录到路径
sys.path.append(str(Path(__file__).parent))

def create_demo_files():
    """创建演示文件"""
    print("📁 创建演示文件...")
    
    demo_dir = Path("demo_files")
    demo_dir.mkdir(exist_ok=True)
    
    # 英文文本文件
    with open(demo_dir / "english_sample.txt", "w", encoding="utf-8") as f:
        f.write("""
Hello world! This is a wonderful day with beautiful sunshine.
I am feeling very happy and excited about this amazing project.
There are 123 people attending the conference on 2024-01-15.
The temperature is 25.5 degrees Celsius, perfect for outdoor activities.
Company ABC Inc. and Microsoft Corporation will be participating.
Contact us at support@example.com or call +1-555-0123.
""")
    
    # 中文文本文件
    with open(demo_dir / "chinese_sample.txt", "w", encoding="utf-8") as f:
        f.write("""
你好世界！今天是一个美好的日子。
我感到非常开心和兴奋，这个项目真是太棒了。
会议将在2024年1月15日举行，预计有123人参加。
温度是25.5摄氏度，非常适合户外活动。
阿里巴巴集团和腾讯公司将参与此次活动。
联系我们：support@example.com 或致电 400-123-4567。
""")
    
    # CSV文件
    with open(demo_dir / "sample_data.csv", "w", encoding="utf-8") as f:
        f.write("""Name,Age,City,Score
张三,25,北京,95.5
John,30,New York,88.2
李四,28,上海,92.1
Mary,26,London,89.7
王五,32,深圳,96.3
""")
    
    # JSON文件
    sample_json = {
        "project": "Smart File Processor",
        "version": "2.0",
        "description": "This is an amazing tool for processing files with AI capabilities",
        "features": ["sentiment analysis", "entity recognition", "multilingual support"],
        "statistics": {
            "files_processed": 1250,
            "accuracy": 97.5,
            "languages_supported": 15
        },
        "date_created": "2024-01-01",
        "contact": "info@example.com"
    }
    
    with open(demo_dir / "sample_data.json", "w", encoding="utf-8") as f:
        json.dump(sample_json, f, indent=2, ensure_ascii=False)
    
    print(f"✓ 演示文件已创建在 {demo_dir} 目录中")
    return demo_dir

def demo_cli_processing():
    """演示命令行处理"""
    print("\n🖥️ 命令行处理演示")
    print("=" * 50)
    
    try:
        from improved_main import FileProcessor
        
        demo_dir = create_demo_files()
        output_dir = Path("demo_output")
        output_dir.mkdir(exist_ok=True)
        
        processor = FileProcessor()
        
        # 处理英文文件
        print("\n📝 处理英文文件...")
        success = processor.process_single_file(
            str(demo_dir / "english_sample.txt"),
            str(output_dir / "english_result.txt"),
            "summary"
        )
        
        if success:
            print("✓ 英文文件处理完成")
            # 显示结果
            with open(output_dir / "english_result.txt", "r", encoding="utf-8") as f:
                result = f.read()
                print("结果预览:")
                print("-" * 40)
                print(result[:300] + "..." if len(result) > 300 else result)
                print("-" * 40)
        
        # 处理中文文件
        print("\n📝 处理中文文件...")
        success = processor.process_single_file(
            str(demo_dir / "chinese_sample.txt"),
            str(output_dir / "chinese_result.json"),
            "json"
        )
        
        if success:
            print("✓ 中文文件处理完成")
            # 显示JSON结果片段
            with open(output_dir / "chinese_result.json", "r", encoding="utf-8") as f:
                result_json = json.load(f)
                print("结果信息:")
                print(f"- 语言: {result_json.get('language', 'unknown')}")
                print(f"- 字符数: {result_json.get('statistics', {}).get('char_count', 0)}")
                print(f"- 发现数字: {len(result_json.get('numbers', []))}")
                print(f"- 情感分析: {result_json.get('sentiment', {}).get('compound', 0):.3f}")
        
        return True
        
    except Exception as e:
        print(f"✗ 命令行演示失败: {e}")
        return False

def demo_gui_features():
    """演示GUI功能"""
    print("\n🖥️ GUI功能演示")
    print("=" * 50)
    
    try:
        # 检查GUI模块
        from improved_gui import ModernGUI
        
        print("✓ GUI模块加载成功")
        print("\n🎨 GUI特性:")
        print("- 📁 可视化文件选择")
        print("- 📊 实时进度显示") 
        print("- 📋 多格式输出")
        print("- ⚙️ 配置管理")
        print("- 📈 结果统计")
        print("- 💾 一键导出")
        
        response = input("\n是否启动GUI演示？(y/N): ").strip().lower()
        if response in ['y', 'yes', '是']:
            print("🚀 启动GUI...")
            app = ModernGUI()
            app.run()
        
        return True
        
    except Exception as e:
        print(f"✗ GUI演示失败: {e}")
        return False

def show_config_demo():
    """显示配置演示"""
    print("\n⚙️ 配置系统演示")
    print("=" * 50)
    
    try:
        from config import config
        
        print("当前配置:")
        print(f"- 最大文件大小: {config.get('processing.max_file_size_mb')} MB")
        print(f"- 并发处理数: {config.get('processing.max_workers')}")
        print(f"- 支持格式: {', '.join(config.get('processing.supported_formats', []))}")
        print(f"- 语言检测: {'启用' if config.get('nlp.detect_language') else '禁用'}")
        print(f"- 情感分析: {'启用' if config.get('nlp.sentiment_analysis') else '禁用'}")
        
        return True
        
    except Exception as e:
        print(f"✗ 配置演示失败: {e}")
        return False

def cleanup_demo():
    """清理演示文件"""
    print("\n🧹 清理演示文件...")
    
    import shutil
    
    try:
        # 删除演示目录
        for dir_name in ["demo_files", "demo_output"]:
            if Path(dir_name).exists():
                shutil.rmtree(dir_name)
                print(f"✓ 已删除 {dir_name}")
        
        return True
        
    except Exception as e:
        print(f"⚠️ 清理失败: {e}")
        return False

def main():
    """主演示函数"""
    print("🎭 智能文件处理工具 v2.0 - 功能演示")
    print("=" * 60)
    print()
    
    try:
        # 显示菜单
        while True:
            print("\n📋 演示菜单:")
            print("1. 🖥️  命令行处理演示")
            print("2. 🎨 GUI功能演示") 
            print("3. ⚙️  配置系统演示")
            print("4. 🧹 清理演示文件")
            print("5. ❌ 退出")
            
            choice = input("\n请选择 (1-5): ").strip()
            
            if choice == "1":
                demo_cli_processing()
            elif choice == "2":
                demo_gui_features()
            elif choice == "3":
                show_config_demo()
            elif choice == "4":
                cleanup_demo()
            elif choice == "5":
                print("\n👋 感谢使用演示！")
                break
            else:
                print("❌ 无效选择，请重试")
                
    except KeyboardInterrupt:
        print("\n\n👋 演示已中断")
    except Exception as e:
        print(f"\n❌ 演示出错: {e}")
    finally:
        # 询问是否清理
        try:
            response = input("\n是否清理演示文件？(Y/n): ").strip().lower()
            if response not in ['n', 'no', '否']:
                cleanup_demo()
        except:
            pass

if __name__ == "__main__":
    main()