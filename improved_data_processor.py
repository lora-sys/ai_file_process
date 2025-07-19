"""
改进的数据处理模块
"""
import re
import logging
import json
from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass
from datetime import datetime
import spacy
from langdetect import detect, LangDetectException, DetectorFactory
from transformers import pipeline
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from config import config

# 配置日志
logger = logging.getLogger(__name__)

# 设置随机种子以获得一致的语言检测结果
DetectorFactory.seed = 0

@dataclass
class ProcessingResult:
    """处理结果数据类"""
    original_text: str
    processed_text: str
    language: str
    sentiment: Dict[str, float]
    numbers: List[float]
    dates: List[str]
    entities: List[Dict[str, str]]
    statistics: Dict[str, Any]
    errors: List[str]

class NLPModelManager:
    """NLP模型管理器 - 单例模式"""
    _instance = None
    _models = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self._load_models()
    
    def _load_models(self):
        """加载NLP模型"""
        model_config = config.get('nlp.models', {})
        
        # 加载spaCy模型
        for lang, model_name in model_config.items():
            try:
                self._models[f"spacy_{lang}"] = spacy.load(model_name)
                logger.info(f"已加载 spaCy 模型: {model_name}")
            except OSError:
                logger.warning(f"无法加载 spaCy 模型: {model_name}")
                # 使用备用模型
                if lang == 'en':
                    try:
                        self._models[f"spacy_{lang}"] = spacy.load("en_core_web_sm")
                    except OSError:
                        logger.error("无法加载英文模型")
        
        # 加载情感分析模型
        if config.get('nlp.sentiment_analysis', True):
            try:
                # 下载VADER词典（如果需要）
                nltk.download('vader_lexicon', quiet=True)
                self._models['sentiment'] = SentimentIntensityAnalyzer()
                logger.info("已加载 VADER 情感分析模型")
            except Exception as e:
                logger.error(f"无法加载情感分析模型: {e}")
    
    def get_model(self, model_key: str):
        """获取模型"""
        return self._models.get(model_key)

class AdvancedTextProcessor:
    """高级文本处理器"""
    
    def __init__(self):
        self.model_manager = NLPModelManager()
        self.language_detector_enabled = config.get('nlp.detect_language', True)
    
    def process_text(self, text: str) -> ProcessingResult:
        """处理文本的主方法"""
        if not text or not text.strip():
            return self._create_empty_result(text)
        
        result = ProcessingResult(
            original_text=text,
            processed_text="",
            language="unknown",
            sentiment={},
            numbers=[],
            dates=[],
            entities=[],
            statistics={},
            errors=[]
        )
        
        try:
            # 语言检测
            result.language = self._detect_language(text)
            
            # 文本预处理
            cleaned_text = self._clean_text(text)
            
            # NLP处理
            result.processed_text = self._process_with_nlp(cleaned_text, result.language)
            
            # 提取数字
            result.numbers = self._extract_numbers(text)
            
            # 提取日期
            result.dates = self._extract_dates(text)
            
            # 情感分析
            if config.get('nlp.sentiment_analysis', True):
                result.sentiment = self._analyze_sentiment(cleaned_text)
            
            # 实体识别
            result.entities = self._extract_entities(text, result.language)
            
            # 生成统计信息
            result.statistics = self._generate_statistics(text, result)
            
        except Exception as e:
            logger.error(f"处理文本时发生错误: {e}")
            result.errors.append(str(e))
        
        return result
    
    def _create_empty_result(self, text: str) -> ProcessingResult:
        """创建空结果"""
        return ProcessingResult(
            original_text=text,
            processed_text="",
            language="unknown",
            sentiment={},
            numbers=[],
            dates=[],
            entities=[],
            statistics={"word_count": 0, "char_count": len(text or "")},
            errors=["空文本或无效输入"]
        )
    
    def _detect_language(self, text: str) -> str:
        """检测文本语言"""
        if not self.language_detector_enabled:
            return "en"  # 默认英语
        
        try:
            # 使用前200个字符进行检测，提高准确性
            sample_text = text[:200].strip()
            if not sample_text:
                return "unknown"
            
            detected = detect(sample_text)
            
            # 规范化语言代码
            if detected in ["zh-cn", "zh-tw", "zh"]:
                return "zh"
            elif detected.startswith("en"):
                return "en"
            else:
                return detected
                
        except LangDetectException:
            logger.warning("语言检测失败，使用默认语言")
            return "en"
        except Exception as e:
            logger.error(f"语言检测发生错误: {e}")
            return "unknown"
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        if not text:
            return ""
        
        # 去除多余的空白字符
        cleaned = re.sub(r'\s+', ' ', text).strip()
        
        # 去除特殊字符（可选）
        # cleaned = re.sub(r'[^\w\s\u4e00-\u9fff]', '', cleaned)
        
        return cleaned
    
    def _process_with_nlp(self, text: str, language: str) -> str:
        """使用NLP模型处理文本"""
        try:
            # 选择合适的模型
            model_key = f"spacy_{language}"
            nlp_model = self.model_manager.get_model(model_key)
            
            if nlp_model is None:
                # 使用英文模型作为后备
                nlp_model = self.model_manager.get_model("spacy_en")
                if nlp_model is None:
                    logger.warning("没有可用的NLP模型")
                    return text
            
            # 处理文本
            doc = nlp_model(text)
            
            # 提取词元和词干
            if language == "zh":
                # 中文保留原词
                tokens = [token.text for token in doc 
                         if not token.is_punct and not token.is_space]
            else:
                # 英文使用词干化
                tokens = [token.lemma_.lower() for token in doc 
                         if not token.is_stop and not token.is_punct and not token.is_space]
            
            return " ".join(tokens) if tokens else text
            
        except Exception as e:
            logger.error(f"NLP处理失败: {e}")
            return text
    
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
            logger.error(f"提取数字时发生错误: {e}")
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
            logger.error(f"提取日期时发生错误: {e}")
            return []
    
    def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        """分析情感"""
        try:
            sentiment_analyzer = self.model_manager.get_model('sentiment')
            if sentiment_analyzer is None:
                return {}
            
            scores = sentiment_analyzer.polarity_scores(text)
            return scores
            
        except Exception as e:
            logger.error(f"情感分析失败: {e}")
            return {}
    
    def _extract_entities(self, text: str, language: str) -> List[Dict[str, str]]:
        """提取命名实体"""
        entities = []
        
        try:
            model_key = f"spacy_{language}"
            nlp_model = self.model_manager.get_model(model_key)
            
            if nlp_model is None:
                nlp_model = self.model_manager.get_model("spacy_en")
                if nlp_model is None:
                    return []
            
            doc = nlp_model(text)
            
            for ent in doc.ents:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char
                })
            
            return entities
            
        except Exception as e:
            logger.error(f"实体识别失败: {e}")
            return []
    
    def _generate_statistics(self, original_text: str, result: ProcessingResult) -> Dict[str, Any]:
        """生成统计信息"""
        try:
            words = original_text.split()
            
            stats = {
                "char_count": len(original_text),
                "word_count": len(words),
                "sentence_count": len(re.split(r'[.!?。！？]', original_text)),
                "avg_word_length": sum(len(word) for word in words) / len(words) if words else 0,
                "number_count": len(result.numbers),
                "date_count": len(result.dates),
                "entity_count": len(result.entities),
                "language": result.language,
                "processing_errors": len(result.errors)
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"生成统计信息失败: {e}")
            return {}

class ResultFormatter:
    """结果格式化器"""
    
    @staticmethod
    def to_dict(result: ProcessingResult) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "original_text": result.original_text,
            "processed_text": result.processed_text,
            "language": result.language,
            "sentiment": result.sentiment,
            "numbers": result.numbers,
            "dates": result.dates,
            "entities": result.entities,
            "statistics": result.statistics,
            "errors": result.errors,
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def to_json(result: ProcessingResult, indent: int = 2) -> str:
        """转换为JSON格式"""
        return json.dumps(
            ResultFormatter.to_dict(result),
            ensure_ascii=False,
            indent=indent
        )
    
    @staticmethod
    def to_summary_text(result: ProcessingResult) -> str:
        """转换为摘要文本格式"""
        summary_parts = []
        
        # 基本信息
        summary_parts.append(f"语言: {result.language}")
        summary_parts.append(f"字符数: {result.statistics.get('char_count', 0)}")
        summary_parts.append(f"词数: {result.statistics.get('word_count', 0)}")
        
        # 情感分析
        if result.sentiment:
            compound = result.sentiment.get('compound', 0)
            sentiment_label = "积极" if compound > 0.05 else "消极" if compound < -0.05 else "中性"
            summary_parts.append(f"情感倾向: {sentiment_label} ({compound:.3f})")
        
        # 数字和日期
        if result.numbers:
            summary_parts.append(f"发现数字: {len(result.numbers)}个")
        if result.dates:
            summary_parts.append(f"发现日期: {len(result.dates)}个")
        
        # 实体
        if result.entities:
            entity_types = list(set(ent['label'] for ent in result.entities))
            summary_parts.append(f"实体类型: {', '.join(entity_types)}")
        
        # 错误信息
        if result.errors:
            summary_parts.append(f"处理错误: {len(result.errors)}个")
        
        summary_parts.append("\n处理后文本:")
        summary_parts.append(result.processed_text[:200] + "..." if len(result.processed_text) > 200 else result.processed_text)
        
        return "\n".join(summary_parts)

# 全局处理器实例
text_processor = AdvancedTextProcessor()
result_formatter = ResultFormatter()