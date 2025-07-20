#!/usr/bin/env python3
"""
智能文件处理工具 - GUI启动脚本
"""
import sys
import os
from pathlib import Path

# 添加当前目录到Python路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def check_dependencies():
    """检查必要的依赖是否已安装"""
    missing_packages = []
    
    try:
        import tkinter
    except ImportError:
        missing_packages.append('tkinter')
    
    try:
        import spacy
    except ImportError:
        missing_packages.append('spacy')
    
    try:
        import nltk
    except ImportError:
        missing_packages.append('nltk')
    
    try:
        import langdetect
    except ImportError:
        missing_packages.append('langdetect')
    
    try:
        import PyPDF2
    except ImportError:
        missing_packages.append('PyPDF2')
    
    try:
        import openpyxl
    except ImportError:
        missing_packages.append('openpyxl')
    
    try:
        import tqdm
    except ImportError:
        missing_packages.append('tqdm')
    
    if missing_packages:
        print("❌ 缺少以下依赖包:")
        for package in missing_packages:
            print(f"   • {package}")
        print("\n📦 请运行以下命令安装依赖:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def check_nlp_models():
    """检查NLP模型是否已下载"""
    print("🔍 检查NLP模型...")
    
    try:
        import spacy
        
        models_to_check = [
            ("en_core_web_sm", "英文模型"),
            ("zh_core_web_sm", "中文模型")
        ]
        
        missing_models = []
        for model_name, description in models_to_check:
            try:
                spacy.load(model_name)
                print(f"   ✅ {description} ({model_name}) - 已安装")
            except OSError:
                missing_models.append((model_name, description))
                print(f"   ❌ {description} ({model_name}) - 未安装")
        
        if missing_models:
            print("\n📥 请下载缺少的模型:")
            for model_name, description in missing_models:
                print(f"   python -m spacy download {model_name}")
            print("\n⚠️  注意: 没有模型也可以运行，但功能会受限")
            
            # 询问用户是否继续
            response = input("\n是否继续启动GUI? (y/n): ").lower().strip()
            if response not in ['y', 'yes', '是']:
                return False
    
    except Exception as e:
        print(f"⚠️  检查模型时出错: {e}")
        print("⚠️  将使用基础功能启动")
    
    return True

def main():
    """主函数"""
    print("🚀 启动智能文件处理工具...")
    print("=" * 50)
    
    # 检查依赖
    print("📋 检查依赖包...")
    if not check_dependencies():
        sys.exit(1)
    print("   ✅ 所有依赖包已安装")
    
    # 检查NLP模型
    if not check_nlp_models():
        sys.exit(1)
    
    print("\n🎉 所有检查通过，正在启动GUI...")
    print("=" * 50)
    
    try:
        # 导入并启动GUI
        from modern_gui import main as gui_main
        gui_main()
        
    except ImportError as e:
        print(f"❌ 导入GUI模块失败: {e}")
        print("💡 请确保所有文件都在正确位置")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ 启动GUI失败: {e}")
        print("💡 请检查错误信息并重试")
        sys.exit(1)

if __name__ == "__main__":
    main()