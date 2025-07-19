"""
配置管理模块
"""
from typing import Dict, Any
import json
import os
from pathlib import Path

class Config:
    """配置管理类"""
    
    DEFAULT_CONFIG = {
        "processing": {
            "max_file_size_mb": 100,
            "chunk_size": 1024,
            "max_workers": 4,
            "supported_formats": [".txt", ".csv", ".json", ".pdf", ".xlsx", ".docx"]
        },
        "nlp": {
            "models": {
                "en": "en_core_web_sm",
                "zh": "zh_core_web_sm", 
                "multi": "xx_ent_wiki_sm"
            },
            "detect_language": True,
            "sentiment_analysis": True
        },
        "logging": {
            "level": "INFO",
            "file": "app.log",
            "max_file_size_mb": 10,
            "backup_count": 3
        },
        "output": {
            "format": "txt",
            "encoding": "utf-8",
            "generate_summary": True,
            "include_statistics": True
        }
    }
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # 合并默认配置
                return self._merge_config(self.DEFAULT_CONFIG, config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"配置文件加载失败，使用默认配置: {e}")
        
        return self.DEFAULT_CONFIG.copy()
    
    def _merge_config(self, default: Dict, custom: Dict) -> Dict:
        """递归合并配置"""
        result = default.copy()
        for key, value in custom.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        return result
    
    def get(self, key: str, default=None):
        """获取配置值，支持点号分割的路径"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def save(self):
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"配置文件保存失败: {e}")

# 全局配置实例
config = Config()