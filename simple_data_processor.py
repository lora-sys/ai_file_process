#!/usr/bin/env python3
"""
简化的数据处理模块 - 不依赖外部NLP库
"""
import re
import json
import logging
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class SimpleProcessingResult:
    """简化的处理结果"""
    original_text: str
    processed_text: str
    language: str
    word_count: int
    char_count: int
    sentence_count: int
    numbers: List[float]
    dates: List[str]
    
class SimpleTextProcessor:
    """简化的文本处理器"""
    
    def __init__(self):
        self.stopwords_en = {
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
            'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
            'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
            'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
            'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
            'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
            'while', 'of', 'at', 'by', 'for', 'with', 'through', 'during', 'before', 'after',
            'above', 'below', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
            'further', 'then', 'once'
        }
    
    def process_text(self, text: str) -> SimpleProcessingResult:
        """处理文本"""
        if not text or not text.strip():
            return self._create_empty_result(text)
        
        try:
            # 基本统计
            char_count = len(text)
            words = self._extract_words(text)
            word_count = len(words)
            sentence_count = len(self._split_sentences(text))
            
            # 语言检测（简单版）
            language = self._detect_language_simple(text)
            
            # 处理文本
            processed_text = self._process_words(words, language)
            
            # 提取数据
            numbers = self._extract_numbers(text)
            dates = self._extract_dates(text)
            
            return SimpleProcessingResult(
                original_text=text,
                processed_text=processed_text,
                language=language,
                word_count=word_count,
                char_count=char_count,
                sentence_count=sentence_count,
                numbers=numbers,
                dates=dates
            )
            
        except Exception as e:
            logger.error(f"文本处理失败: {e}")
            return self._create_empty_result(text)
    
    def _create_empty_result(self, text: str) -> SimpleProcessingResult:
        """创建空结果"""
        return SimpleProcessingResult(
            original_text=text or "",
            processed_text="",
            language="unknown",
            word_count=0,
            char_count=len(text) if text else 0,
            sentence_count=0,
            numbers=[],
            dates=[]
        )
    
    def _detect_language_simple(self, text: str) -> str:
        """简单的语言检测"""
        # 检测中文字符
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
        if len(chinese_chars) > len(text) * 0.1:  # 如果中文字符超过10%
            return "zh"
        return "en"
    
    def _extract_words(self, text: str) -> List[str]:
        """提取单词"""
        # 移除标点符号，保留字母数字和中文
        cleaned = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
        words = cleaned.split()
        return [word.lower() for word in words if word.strip()]
    
    def _split_sentences(self, text: str) -> List[str]:
        """分割句子"""
        sentences = re.split(r'[.!?。！？]', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _process_words(self, words: List[str], language: str) -> str:
        """处理单词"""
        if language == "en":
            # 移除英文停用词
            filtered_words = [word for word in words if word not in self.stopwords_en]
        else:
            # 中文或其他语言，保留所有词
            filtered_words = words
        
        return " ".join(filtered_words)
    
    def _extract_numbers(self, text: str) -> List[float]:
        """提取数字"""
        numbers = []
        
        try:
            # 匹配各种数字格式
            patterns = [
                r'\b\d+\.\d+\b',      # 小数
                r'\b\d+\b',           # 整数
                r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b',  # 带逗号的数字
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    try:
                        # 去除逗号
                        cleaned_number = match.replace(',', '')
                        numbers.append(float(cleaned_number))
                    except ValueError:
                        continue
            
            # 去重并排序
            return sorted(list(set(numbers)))
            
        except Exception as e:
            logger.error(f"提取数字失败: {e}")
            return []
    
    def _extract_dates(self, text: str) -> List[str]:
        """提取日期"""
        dates = []
        
        try:
            # 各种日期格式
            date_patterns = [
                r'\b\d{4}-\d{1,2}-\d{1,2}\b',           # YYYY-MM-DD
                r'\b\d{1,2}/\d{1,2}/\d{4}\b',           # MM/DD/YYYY
                r'\b\d{1,2}-\d{1,2}-\d{4}\b',           # MM-DD-YYYY
                r'\b\d{4}年\d{1,2}月\d{1,2}日\b',        # 中文日期
            ]
            
            for pattern in date_patterns:
                matches = re.findall(pattern, text)
                dates.extend(matches)
            
            return list(set(dates))  # 去重
            
        except Exception as e:
            logger.error(f"提取日期失败: {e}")
            return []

class SimpleResultFormatter:
    """简化的结果格式化器"""
    
    @staticmethod
    def to_summary_text(result: SimpleProcessingResult) -> str:
        """转换为摘要文本"""
        summary_parts = []
        
        summary_parts.append(f"语言: {result.language}")
        summary_parts.append(f"字符数: {result.char_count}")
        summary_parts.append(f"词数: {result.word_count}")
        summary_parts.append(f"句子数: {result.sentence_count}")
        
        if result.numbers:
            summary_parts.append(f"发现数字: {len(result.numbers)}个 {result.numbers}")
        
        if result.dates:
            summary_parts.append(f"发现日期: {len(result.dates)}个 {result.dates}")
        
        summary_parts.append("\n处理后文本:")
        processed_preview = result.processed_text[:200] + "..." if len(result.processed_text) > 200 else result.processed_text
        summary_parts.append(processed_preview)
        
        return "\n".join(summary_parts)
    
    @staticmethod
    def to_json(result: SimpleProcessingResult, indent: int = 2) -> str:
        """转换为JSON格式"""
        data = {
            "original_text": result.original_text,
            "processed_text": result.processed_text,
            "language": result.language,
            "statistics": {
                "char_count": result.char_count,
                "word_count": result.word_count,
                "sentence_count": result.sentence_count
            },
            "extracted_data": {
                "numbers": result.numbers,
                "dates": result.dates
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return json.dumps(data, ensure_ascii=False, indent=indent)

# 创建全局实例
simple_text_processor = SimpleTextProcessor()
simple_result_formatter = SimpleResultFormatter()