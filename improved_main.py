#!/usr/bin/env python3
"""
智能文件处理工具 - 改进版本
"""
import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from improved_file_handler import file_handler
from improved_data_processor import text_processor, result_formatter
from config import config

# 配置日志
logging.basicConfig(
    level=getattr(logging, config.get('logging.level', 'INFO')),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FileProcessor:
    """文件处理主类"""
    
    def __init__(self):
        self.file_handler = file_handler
        self.text_processor = text_processor
        self.result_formatter = result_formatter
    
    def process_single_file(self, input_path: str, output_path: str, 
                          output_format: str = "summary") -> bool:
        """处理单个文件"""
        try:
            logger.info(f"开始处理文件: {input_path}")
            
            # 读取文件
            content = self.file_handler.read_file(input_path)
            if content is None:
                logger.error(f"无法读取文件: {input_path}")
                return False
            
            # 处理文本
            result = self.text_processor.process_text(content)
            
            # 格式化输出
            if output_format == "json":
                output_content = self.result_formatter.to_json(result)
            elif output_format == "summary":
                output_content = self.result_formatter.to_summary_text(result)
            else:
                output_content = result.processed_text
            
            # 写入结果
            success = self.file_handler.write_file(output_path, output_content)
            
            if success:
                logger.info(f"文件处理完成: {input_path} -> {output_path}")
                self._print_processing_summary(result)
            
            return success
            
        except Exception as e:
            logger.error(f"处理文件时发生错误 {input_path}: {e}")
            return False
    
    def process_batch(self, input_folder: str, output_folder: str,
                     output_format: str = "summary") -> dict:
        """批量处理文件"""
        logger.info(f"开始批量处理: {input_folder} -> {output_folder}")
        
        def process_func(content):
            """文本处理函数"""
            result = self.text_processor.process_text(content)
            
            if output_format == "json":
                return self.result_formatter.to_json(result)
            elif output_format == "summary":
                return self.result_formatter.to_summary_text(result)
            else:
                return result.processed_text
        
        # 使用文件处理器的批量处理功能
        batch_result = self.file_handler.batch_process(
            input_folder, output_folder, process_func
        )
        
        logger.info(f"批量处理完成: 成功 {batch_result.get('processed', 0)} 个文件, "
                   f"失败 {batch_result.get('errors', 0)} 个文件")
        
        return batch_result
    
    def _print_processing_summary(self, result):
        """打印处理摘要"""
        stats = result.statistics
        print(f"\n处理摘要:")
        print(f"- 语言: {result.language}")
        print(f"- 字符数: {stats.get('char_count', 0)}")
        print(f"- 词数: {stats.get('word_count', 0)}")
        print(f"- 发现数字: {stats.get('number_count', 0)} 个")
        print(f"- 发现日期: {stats.get('date_count', 0)} 个")
        print(f"- 发现实体: {stats.get('entity_count', 0)} 个")
        
        if result.sentiment:
            compound = result.sentiment.get('compound', 0)
            sentiment_label = "积极" if compound > 0.05 else "消极" if compound < -0.05 else "中性"
            print(f"- 情感倾向: {sentiment_label} (分数: {compound:.3f})")
        
        if result.errors:
            print(f"- 处理错误: {len(result.errors)} 个")

def create_parser():
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="智能文件处理工具 - 支持文本分析、情感识别、实体提取等功能",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s document.txt output.txt                    # 处理单个文件
  %(prog)s input_folder output_folder                 # 批量处理
  %(prog)s document.txt output.json --format json    # 输出JSON格式
  %(prog)s --config                                   # 查看当前配置
        """
    )
    
    parser.add_argument("input", nargs="?", help="输入文件或文件夹路径")
    parser.add_argument("output", nargs="?", help="输出文件或文件夹路径")
    
    parser.add_argument("--format", "-f", 
                       choices=["summary", "json", "text"],
                       default="summary",
                       help="输出格式 (默认: summary)")
    
    parser.add_argument("--config", "-c", 
                       action="store_true",
                       help="显示当前配置")
    
    parser.add_argument("--verbose", "-v", 
                       action="store_true",
                       help="启用详细日志输出")
    
    parser.add_argument("--version", 
                       action="version", 
                       version="智能文件处理工具 v2.0")
    
    return parser

def main():
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 显示配置
    if args.config:
        print("当前配置:")
        print(f"- 支持的文件格式: {config.get('processing.supported_formats')}")
        print(f"- 最大文件大小: {config.get('processing.max_file_size_mb')} MB")
        print(f"- 并发处理数: {config.get('processing.max_workers')}")
        print(f"- 语言检测: {'启用' if config.get('nlp.detect_language') else '禁用'}")
        print(f"- 情感分析: {'启用' if config.get('nlp.sentiment_analysis') else '禁用'}")
        return 0
    
    # 检查是否启动GUI
    if not args.input and not args.output:
        # 如果没有提供参数，启动GUI
        try:
            from modern_gui import ModernFileProcessorGUI
            print("启动图形用户界面...")
            app = ModernFileProcessorGUI()
            app.run()
            return 0
        except ImportError:
            print("警告: 无法启动GUI，缺少相关模块")
            parser.print_help()
            return 1
        except Exception as e:
            print(f"启动GUI失败: {e}")
            parser.print_help()
            return 1
    
    # 检查参数
    if not args.input or not args.output:
        parser.print_help()
        return 1
    
    # 创建处理器
    processor = FileProcessor()
    
    # 处理文件
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    try:
        if input_path.is_file():
            # 处理单个文件
            success = processor.process_single_file(
                str(input_path), str(output_path), args.format
            )
            return 0 if success else 1
            
        elif input_path.is_dir():
            # 批量处理
            result = processor.process_batch(
                str(input_path), str(output_path), args.format
            )
            return 0 if result.get("success") else 1
            
        else:
            logger.error(f"输入路径无效: {input_path}")
            return 1
            
    except KeyboardInterrupt:
        logger.info("用户中断处理")
        return 1
    except Exception as e:
        logger.error(f"程序执行出错: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())