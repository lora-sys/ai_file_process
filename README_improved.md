# 智能文件处理工具 v2.0

一个功能强大的智能文件处理工具，支持多种文件格式的文本分析、情感识别、实体提取等功能。

## ✨ 主要特性

- 🔍 **智能文本分析**: 自动语言检测、分词、词干化
- 💡 **情感分析**: 使用VADER算法分析文本情感倾向
- 📊 **数据提取**: 自动提取数字、日期、命名实体
- 📁 **多格式支持**: 支持 `.txt`, `.csv`, `.json`, `.pdf`, `.xlsx` 等格式
- ⚡ **并发处理**: 多线程批量处理，提高效率
- 🎯 **多种输出**: 支持摘要、JSON、纯文本等输出格式
- 🛠️ **可配置**: 灵活的配置系统，易于定制

## 🚀 安装

1. 克隆项目:
```bash
git clone <repository-url>
cd file-processing-tool
```

2. 安装依赖:
```bash
pip install -r requirements.txt
```

3. 下载必要的NLP模型:
```bash
python -m spacy download en_core_web_sm
python -m spacy download zh_core_web_sm
python -m spacy download xx_ent_wiki_sm
```

## 📖 使用方法

### 命令行界面

```bash
# 处理单个文件
python improved_main.py document.txt output.txt

# 批量处理文件夹
python improved_main.py input_folder/ output_folder/

# 输出JSON格式
python improved_main.py document.txt result.json --format json

# 查看配置
python improved_main.py --config

# 启用详细日志
python improved_main.py document.txt output.txt --verbose
```

### Python API

```python
from improved_file_handler import file_handler
from improved_data_processor import text_processor, result_formatter

# 读取文件
content = file_handler.read_file("document.txt")

# 处理文本
result = text_processor.process_text(content)

# 格式化结果
summary = result_formatter.to_summary_text(result)
json_output = result_formatter.to_json(result)
```

## 📋 输出格式

### 摘要格式 (默认)
```
语言: en
字符数: 156
词数: 28
情感倾向: 积极 (0.618)
发现数字: 2个
发现日期: 1个
实体类型: PERSON, ORG

处理后文本:
hello world test number date...
```

### JSON格式
```json
{
  "original_text": "原始文本...",
  "processed_text": "处理后文本...",
  "language": "en",
  "sentiment": {
    "compound": 0.618,
    "positive": 0.692,
    "negative": 0.0,
    "neutral": 0.308
  },
  "numbers": [123, 456.78],
  "dates": ["2024-01-01"],
  "entities": [
    {"text": "Apple", "label": "ORG", "start": 10, "end": 15}
  ],
  "statistics": {
    "char_count": 156,
    "word_count": 28,
    "sentence_count": 3
  }
}
```

## ⚙️ 配置

创建 `config.json` 文件来自定义配置:

```json
{
  "processing": {
    "max_file_size_mb": 100,
    "max_workers": 4,
    "supported_formats": [".txt", ".csv", ".json", ".pdf", ".xlsx"]
  },
  "nlp": {
    "detect_language": true,
    "sentiment_analysis": true,
    "models": {
      "en": "en_core_web_sm",
      "zh": "zh_core_web_sm"
    }
  },
  "logging": {
    "level": "INFO",
    "file": "app.log"
  }
}
```

## 🧪 测试

运行测试脚本验证功能:

```bash
python test_improvements.py
```

## 📁 项目结构

```
├── config.py                     # 配置管理
├── improved_file_handler.py      # 文件处理模块
├── improved_data_processor.py    # 数据处理模块
├── improved_main.py              # 主程序
├── test_improvements.py          # 测试脚本
├── requirements.txt              # 依赖列表
└── README_improved.md            # 说明文档
```

## 🔧 主要改进

相比原版本，v2.0 包含以下重要改进:

### 1. 代码质量
- ✅ 修正所有拼写错误
- ✅ 添加类型提示
- ✅ 统一编码规范
- ✅ 优化异常处理

### 2. 功能增强
- ✅ 智能语言检测
- ✅ 实体识别
- ✅ 多种输出格式
- ✅ 详细统计信息
- ✅ 进度条显示

### 3. 性能优化
- ✅ 模型单例模式
- ✅ 并发处理优化
- ✅ 内存使用优化
- ✅ 错误恢复机制

### 4. 架构改进
- ✅ 模块解耦
- ✅ 配置管理系统
- ✅ 可扩展架构
- ✅ 完整测试覆盖

## 🐛 问题修复

- 🔧 修复数字解析错误
- 🔧 改进文件编码检测
- 🔧 优化内存使用
- 🔧 增强错误日志

## 📝 更新日志

### v2.0 (Current)
- 完全重构代码架构
- 添加配置管理系统
- 实现并发处理
- 增加实体识别功能
- 支持多种输出格式

### v1.0 (Original)
- 基础文件处理功能
- 简单文本分析
- 情感分析

## 🤝 贡献

欢迎提交问题和改进建议！

## 📄 许可证

MIT License