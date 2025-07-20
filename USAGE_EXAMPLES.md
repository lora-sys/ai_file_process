# 使用示例和演示

本文档提供智能文件处理工具的详细使用示例和演示。

## 🚀 快速开始

### 1. 启动图形界面（最简单）

```bash
# 一键启动GUI
python run.py
```

这是最推荐的使用方式。程序会自动：
- 检测依赖环境
- 选择最适合的GUI版本
- 启动图形界面

### 2. 演示版本（无依赖）

如果你的环境缺少某些依赖，可以使用演示版本：

```bash
python demo_gui.py
```

演示版本特点：
- 仅需Python标准库
- 提供基本的文件处理功能
- 模拟高级NLP功能（用于演示）

## 📖 详细使用示例

### GUI模式示例

#### 示例1：处理单个文档

**目标**: 分析一篇文章的情感和提取关键信息

1. **启动程序**
   ```bash
   python run.py
   ```

2. **选择文件**
   - 点击"选择文件"按钮
   - 选择 `documents/article.txt`

3. **设置输出**
   - 输出路径自动设置为 `documents/article_processed.txt`
   - 选择"摘要"格式

4. **开始处理**
   - 点击"开始处理"
   - 观察进度条和状态显示

5. **查看结果**
   - 在"摘要"标签页查看处理结果
   - 切换到"详细结果"查看JSON格式数据
   - "处理日志"标签页显示处理过程

**预期结果**:
```
文件处理摘要报告
====================

文件统计:
- 字符数: 2,456
- 词数: 487
- 句子数: 23

情感分析:
- 情感倾向: 积极 (0.642)
- 置信度: 85.3%

数据提取:
- 发现数字: 12个 [2023, 100, 25.5, ...]
- 发现日期: 3个 [2023-12-01, 2024年1月]
- 实体识别: 8个 [OpenAI, Python, 北京, ...]

处理信息:
- 语言: en (91.2%), zh (8.8%)
- 处理时间: 3.2秒
- 输出格式: 摘要
```

#### 示例2：批量处理报告文件夹

**目标**: 批量分析多个报告文件

1. **选择文件夹**
   - 点击"选择文件夹"
   - 选择包含多个文档的文件夹

2. **设置输出**
   - 选择输出文件夹
   - 选择"JSON"格式以便后续分析

3. **查看批量处理结果**
   - 统计信息显示处理进度
   - 查看成功/失败文件数量

### 命令行模式示例

#### 示例1：单文件处理

```bash
# 基本处理
python run.py --cli report.pdf output.txt

# 指定JSON格式输出
python run.py --cli report.pdf analysis.json --format json

# 启用详细日志
python run.py --cli report.pdf output.txt --verbose
```

#### 示例2：批量处理

```bash
# 批量处理文件夹
python run.py --cli documents/ processed_documents/

# 批量处理并输出JSON格式
python run.py --cli input_folder/ output_folder/ --format json
```

#### 示例3：查看配置和测试

```bash
# 查看当前配置
python run.py --cli --config

# 运行功能测试
python run.py --test
```

## 🎯 不同文件格式处理示例

### 文本文件 (.txt)

**输入文件**: `sample.txt`
```
Hello world! This is a test document.
It contains some positive words like "excellent" and "amazing".
The date is 2024-01-15 and the temperature is 23.5 degrees.
```

**处理命令**:
```bash
python run.py --cli sample.txt result.json --format json
```

**输出结果**:
```json
{
  "original_text": "Hello world! This is a test document...",
  "processed_text": "hello world test document contain positive word like excellent amazing date temperature degree",
  "language": "en",
  "sentiment": {
    "compound": 0.7269,
    "positive": 0.358,
    "negative": 0.0,
    "neutral": 0.642
  },
  "numbers": [2024, 1, 15, 23.5],
  "dates": ["2024-01-15"],
  "entities": [
    {"text": "2024-01-15", "label": "DATE", "start": 89, "end": 99}
  ],
  "statistics": {
    "char_count": 156,
    "word_count": 28,
    "sentence_count": 3
  }
}
```

### CSV文件 (.csv)

**输入文件**: `data.csv`
```csv
Name,Comment,Rating
Alice,This product is amazing!,5
Bob,Not very good quality,2
Carol,Excellent service and support,5
```

**处理结果**:
- 自动识别表格结构
- 分析每行评论的情感
- 提取评分数字
- 生成整体情感趋势

### PDF文件 (.pdf)

**处理特点**:
- 自动提取文本内容
- 处理多页文档
- 保留文档结构信息
- 支持图表中的文字识别

## 📊 输出格式详解

### 摘要格式 (summary)

适合快速查看处理结果：
- 文件基本统计
- 情感分析结果
- 关键数据提取
- 处理信息概览

### JSON格式 (json)

适合程序进一步处理：
- 结构化数据格式
- 包含所有分析结果
- 便于数据库存储
- 支持API集成

### 纯文本格式 (text)

适合文本清理和标准化：
- 去除格式和特殊字符
- 标准化空格和换行
- 统一编码格式
- 便于后续处理

## 🔧 高级配置示例

### 创建自定义配置

创建 `config.json` 文件：

```json
{
  "processing": {
    "max_file_size_mb": 200,
    "max_workers": 8,
    "supported_formats": [".txt", ".csv", ".json", ".pdf", ".xlsx", ".docx"]
  },
  "nlp": {
    "detect_language": true,
    "sentiment_analysis": true,
    "models": {
      "en": "en_core_web_lg",
      "zh": "zh_core_web_lg"
    }
  },
  "output": {
    "format": "json",
    "encoding": "utf-8",
    "generate_summary": true,
    "include_statistics": true
  }
}
```

### 使用自定义配置

```bash
# GUI会自动加载config.json
python run.py

# CLI模式查看配置
python run.py --cli --config
```

## 🚨 常见问题和解决方案

### 问题1：GUI启动失败

**错误信息**: `GUI依赖缺失`

**解决方案**:
```bash
# 方案1：使用演示版本
python demo_gui.py

# 方案2：安装完整依赖
pip install -r requirements.txt

# 方案3：使用CLI模式
python run.py --cli
```

### 问题2：NLP模型未找到

**错误信息**: `无法加载 spaCy 模型`

**解决方案**:
```bash
# 下载英文模型
python -m spacy download en_core_web_sm

# 下载中文模型
python -m spacy download zh_core_web_sm

# 下载多语言模型
python -m spacy download xx_ent_wiki_sm
```

### 问题3：大文件处理缓慢

**解决方案**:
- 调整配置中的 `max_workers` 参数
- 增加 `max_file_size_mb` 限制
- 使用批量处理模式
- 选择合适的输出格式

### 问题4：中文处理结果不理想

**解决方案**:
- 确保安装了中文NLP模型
- 检查文件编码格式
- 在配置中启用语言检测
- 尝试不同的输出格式

## 📈 性能优化建议

### 1. 批量处理优化

```bash
# 调整并发数（根据CPU核心数）
python run.py --cli large_folder/ output/ --workers 8

# 使用简化输出格式提高速度
python run.py --cli folder/ output/ --format text
```

### 2. 内存使用优化

- 处理大文件时选择"纯文本"格式
- 避免同时处理过多文件
- 定期清理处理历史

### 3. 准确性优化

- 根据文档语言选择合适的NLP模型
- 启用所有分析功能（情感、实体等）
- 使用"JSON"格式获取最详细结果

## 🎓 进阶使用技巧

### 1. 与其他工具集成

```python
# Python脚本中使用API
from improved_data_processor import text_processor
from improved_file_handler import file_handler

# 处理文件
content = file_handler.read_file("document.pdf")
result = text_processor.process_text(content)

# 获取特定信息
sentiment_score = result.sentiment.get('compound', 0)
extracted_numbers = result.numbers
detected_language = result.language
```

### 2. 自动化批处理

```bash
#!/bin/bash
# 自动处理脚本
for folder in input_*; do
    python run.py --cli "$folder" "processed_$folder" --format json
done
```

### 3. 结果分析和可视化

```python
# 分析批处理结果
import json
import glob

results = []
for file in glob.glob("output/*.json"):
    with open(file) as f:
        results.append(json.load(f))

# 统计情感分布
positive_count = sum(1 for r in results if r['sentiment']['compound'] > 0.1)
print(f"积极文档比例: {positive_count/len(results)*100:.1f}%")
```

## 🎉 结语

智能文件处理工具提供了强大而灵活的文本分析功能。无论是简单的文件格式转换，还是复杂的情感分析和实体识别，都能通过直观的GUI或简洁的命令行完成。

如有问题或建议，请查看帮助文档或联系开发者。