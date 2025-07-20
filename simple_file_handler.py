#!/usr/bin/env python3
"""
简化的文件处理模块 - 不依赖外部库
"""
import csv
import json
import logging
import os
from pathlib import Path
from typing import Optional, List, Dict, Any, Union

# 基本日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleFileHandler:
    """简化的文件处理类"""
    
    def __init__(self):
        self.supported_formats = {'.txt', '.csv', '.json'}
        self.max_file_size = 100 * 1024 * 1024  # 100MB
    
    def validate_file(self, file_path: Union[str, Path]) -> bool:
        """验证文件是否有效"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            logger.error(f"文件不存在: {file_path}")
            return False
        
        if not file_path.is_file():
            logger.error(f"路径不是文件: {file_path}")
            return False
        
        if file_path.stat().st_size > self.max_file_size:
            logger.error(f"文件太大: {file_path}")
            return False
        
        if file_path.suffix.lower() not in self.supported_formats:
            logger.warning(f"不支持的文件格式: {file_path.suffix}")
            return False
        
        return True
    
    def read_file(self, file_path: Union[str, Path]) -> Optional[str]:
        """读取文件"""
        file_path = Path(file_path)
        
        if not self.validate_file(file_path):
            return None
        
        try:
            suffix = file_path.suffix.lower()
            
            if suffix == '.txt':
                return self._read_text_file(file_path)
            elif suffix == '.csv':
                return self._read_csv_file(file_path)
            elif suffix == '.json':
                return self._read_json_file(file_path)
            else:
                return self._read_text_file(file_path)
                
        except Exception as e:
            logger.error(f"读取文件失败 {file_path}: {e}")
            return None
    
    def _read_text_file(self, file_path: Path) -> Optional[str]:
        """读取文本文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # 尝试其他编码
            for encoding in ['gbk', 'iso-8859-1', 'cp1252']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                        logger.info(f"使用 {encoding} 编码读取文件: {file_path}")
                        return content
                except UnicodeDecodeError:
                    continue
            logger.error(f"无法确定文件编码: {file_path}")
            return None
    
    def _read_csv_file(self, file_path: Path) -> Optional[str]:
        """读取CSV文件"""
        try:
            rows = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    rows.append(' '.join(str(cell) for cell in row))
            return '\n'.join(rows)
        except Exception as e:
            logger.error(f"读取CSV文件失败 {file_path}: {e}")
            return None
    
    def _read_json_file(self, file_path: Path) -> Optional[str]:
        """读取JSON文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return json.dumps(data, ensure_ascii=False, indent=2)
        except json.JSONDecodeError as e:
            logger.error(f"JSON格式错误 {file_path}: {e}")
            return None
    
    def write_file(self, file_path: Union[str, Path], content: str, mode: str = 'w') -> bool:
        """写入文件"""
        file_path = Path(file_path)
        
        try:
            # 确保目录存在
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, mode, encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"文件写入成功: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"写入文件失败 {file_path}: {e}")
            return False

# 创建全局实例
simple_file_handler = SimpleFileHandler()