#!/usr/bin/env python3
"""
智能文件处理工具GUI启动脚本
"""
import sys
import os
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

def check_dependencies():
    """检查依赖是否安装"""
    required_packages = [
        'tkinter',
        'nltk', 
        'spacy',
        'langdetect',
        'transformers',
        'PyPDF2',
        'openpyxl',
        'tqdm'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            elif package == 'PyPDF2':
                import PyPDF2
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ 缺少以下依赖包:")
        for pkg in missing_packages:
            print(f"  - {pkg}")
        print("\n请运行以下命令安装依赖:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def check_models():
    """检查NLP模型是否安装"""
    models_to_check = [
        'en_core_web_sm',
        'zh_core_web_sm',
        'xx_ent_wiki_sm'
    ]
    
    missing_models = []
    
    try:
        import spacy
        for model in models_to_check:
            try:
                spacy.load(model)
            except OSError:
                missing_models.append(model)
    except ImportError:
        print("❌ spaCy 未安装")
        return False
    
    if missing_models:
        print("⚠️  缺少以下NLP模型:")
        for model in missing_models:
            print(f"  - {model}")
        print("\n请运行以下命令下载模型:")
        for model in missing_models:
            print(f"python -m spacy download {model}")
        print("\n注意: 缺少模型可能会影响某些功能，但不会阻止程序运行")
    
    return True

def main():
    """主函数"""
    print("🚀 启动智能文件处理工具GUI...")
    
    # 检查依赖
    print("📦 检查依赖包...")
    if not check_dependencies():
        return 1
    
    print("✅ 依赖包检查完成")
    
    # 检查模型
    print("🤖 检查NLP模型...")
    check_models()
    
    print("✅ 模型检查完成")
    
    # 启动GUI
    try:
        print("🎨 启动GUI界面...")
        from improved_gui import SmartFileProcessorGUI
        
        app = SmartFileProcessorGUI()
        app.run()
        
        return 0
        
    except ImportError as e:
        print(f"❌ 导入模块失败: {e}")
        print("请确保所有文件都在正确的位置")
        return 1
    except Exception as e:
        print(f"❌ 启动GUI失败: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())