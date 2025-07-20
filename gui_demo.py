#!/usr/bin/env python3
"""
GUI演示脚本 - 展示功能特性
"""
import sys
import time
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

def create_demo_files():
    """创建演示文件"""
    demo_dir = Path("demo_files")
    demo_dir.mkdir(exist_ok=True)
    
    # 创建示例文本文件
    demo_files = {
        "sample_english.txt": """Hello world! This is a sample English text for demonstration.
The file contains multiple sentences with different emotions.
I am happy to show you this amazing tool! 
There are some numbers like 123, 456.78, and dates like 2024-01-15.
Apple Inc. is a great technology company founded by Steve Jobs.
The weather today is wonderful and sunny.""",
        
        "sample_chinese.txt": """你好世界！这是一个中文示例文档。
这个工具非常棒，我很高兴能够展示它的功能。
文档中包含一些数字如 100, 3.14，还有日期如2024年1月15日。
腾讯公司是一家优秀的科技企业。
今天天气很好，阳光明媚。""",
        
        "mixed_content.txt": """This is a mixed content file with English and Chinese.
这是一个混合内容的文件，包含英文和中文。
Numbers: 42, 3.14159, 1000
Dates: 2024-12-25, 2023年12月25日
Organizations: Microsoft, 阿里巴巴集团
The sentiment here is very positive and exciting!
这里的情感非常积极和令人兴奋！""",
        
        "data_sample.csv": """Name,Age,City,Score
Alice,25,New York,85.5
Bob,30,Los Angeles,92.3
Charlie,28,Chicago,78.9
Diana,35,Houston,96.2""",
        
        "config_sample.json": """{
    "settings": {
        "theme": "dark",
        "language": "en",
        "auto_save": true,
        "max_items": 100
    },
    "user": {
        "name": "Demo User",
        "email": "demo@example.com",
        "created": "2024-01-01"
    },
    "metrics": {
        "accuracy": 0.95,
        "speed": 1.23,
        "efficiency": 89.7
    }
}"""
    }
    
    # 写入文件
    for filename, content in demo_files.items():
        file_path = demo_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 创建演示文件: {file_path}")
    
    return demo_dir

def demo_command_line():
    """演示命令行功能"""
    print("\n" + "=" * 60)
    print("🖥️  命令行功能演示")
    print("=" * 60)
    
    demo_dir = create_demo_files()
    
    print("\n命令行使用示例:")
    print("# 处理单个文件")
    print(f"python improved_main.py {demo_dir}/sample_english.txt output.txt")
    print("\n# 批量处理")
    print(f"python improved_main.py {demo_dir} output_folder")
    print("\n# 输出JSON格式")
    print(f"python improved_main.py {demo_dir}/sample_english.txt output.json --format json")
    print("\n# 查看配置")
    print("python improved_main.py --config")

def demo_gui_features():
    """演示GUI功能"""
    print("\n" + "=" * 60)
    print("🎨 GUI功能特性")
    print("=" * 60)
    
    features = [
        "📁 拖拽文件支持 - 直接拖拽文件到输入框",
        "🔄 实时进度显示 - 处理进度条和状态更新",
        "📊 多种输出格式 - 摘要、JSON、纯文本",
        "🚀 并发处理 - 多线程批量处理文件",
        "⚙️ 配置管理 - 图形化配置界面",
        "📝 处理日志 - 详细的操作日志记录",
        "👀 结果预览 - 处理前预览功能",
        "💾 结果保存 - 一键保存处理结果",
        "📋 剪贴板支持 - 复制结果到剪贴板",
        "🎯 快捷键支持 - 常用操作快捷键",
        "🔍 帮助系统 - 内置使用说明和快捷键指南",
        "🌐 多语言支持 - 中英文界面和处理"
    ]
    
    for feature in features:
        print(f"  {feature}")
        time.sleep(0.1)

def demo_processing_examples():
    """演示处理示例"""
    print("\n" + "=" * 60)
    print("🔬 处理功能示例")
    print("=" * 60)
    
    try:
        from improved_data_processor import text_processor, result_formatter
        
        # 示例文本
        sample_text = """Hello! I'm excited to demonstrate this amazing text processing tool. 
        The tool can analyze sentiment (this text is positive!), extract numbers like 123 and 456.78, 
        find dates such as 2024-01-15, and identify entities like Apple Inc. and Microsoft Corporation.
        It supports multiple languages and provides detailed statistics."""
        
        print("📝 示例文本:")
        print(f"'{sample_text[:100]}...'\n")
        
        print("🔄 处理中...")
        result = text_processor.process_text(sample_text)
        
        print("📊 处理结果:")
        print(f"  语言: {result.language}")
        print(f"  字符数: {result.statistics.get('char_count', 0)}")
        print(f"  词数: {result.statistics.get('word_count', 0)}")
        print(f"  发现数字: {result.numbers}")
        print(f"  发现日期: {result.dates}")
        print(f"  实体数量: {len(result.entities)}")
        
        if result.sentiment:
            compound = result.sentiment.get('compound', 0)
            sentiment_label = "积极" if compound > 0.05 else "消极" if compound < -0.05 else "中性"
            print(f"  情感倾向: {sentiment_label} ({compound:.3f})")
        
        print("\n✅ 处理完成！")
        
    except ImportError:
        print("⚠️  处理模块未找到，请确保已安装所有依赖")
    except Exception as e:
        print(f"❌ 处理示例失败: {e}")

def launch_gui():
    """启动GUI"""
    print("\n" + "=" * 60)
    print("🚀 启动GUI界面")
    print("=" * 60)
    
    try:
        print("正在启动图形界面...")
        from improved_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"❌ 无法导入GUI模块: {e}")
        print("请确保所有文件都在正确位置")
    except Exception as e:
        print(f"❌ GUI启动失败: {e}")

def main():
    """主演示函数"""
    print("🎉 智能文件处理工具 - GUI演示")
    print("=" * 60)
    print("本演示将展示工具的主要功能和特性")
    
    while True:
        print("\n📋 选择演示内容:")
        print("1. 创建演示文件")
        print("2. 命令行功能演示") 
        print("3. GUI功能特性介绍")
        print("4. 处理功能示例")
        print("5. 启动GUI界面")
        print("0. 退出演示")
        
        try:
            choice = input("\n请选择 (0-5): ").strip()
            
            if choice == "0":
                print("👋 感谢使用演示！")
                break
            elif choice == "1":
                demo_dir = create_demo_files()
                print(f"\n✅ 演示文件已创建在: {demo_dir}")
            elif choice == "2":
                demo_command_line()
            elif choice == "3":
                demo_gui_features()
            elif choice == "4":
                demo_processing_examples()
            elif choice == "5":
                launch_gui()
                break
            else:
                print("❌ 无效选择，请输入 0-5")
                
        except KeyboardInterrupt:
            print("\n\n👋 用户中断，退出演示")
            break
        except Exception as e:
            print(f"❌ 演示出错: {e}")

if __name__ == "__main__":
    main()