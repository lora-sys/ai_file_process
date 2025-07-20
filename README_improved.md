# 智能文件处理工具 v2.0


一个功能强大的智能文件处理工具，支持多种文件格式的文本分析、情感识别、实体提取等功能。提供命令行和图形界面两种使用方式。

一个功能强大的智能文件处理工具，支持多种文件格式的文本分析、情感识别、实体提取等功能。


## ✨ 主要特性

- 🔍 **智能文本分析**: 自动语言检测、分词、词干化
- 💡 **情感分析**: 使用VADER算法分析文本情感倾向
- 📊 **数据提取**: 自动提取数字、日期、命名实体
- 📁 **多格式支持**: 支持 `.txt`, `.csv`, `.json`, `.pdf`, `.xlsx` 等格式
- ⚡ **并发处理**: 多线程批量处理，提高效率
- 🎯 **多种输出**: 支持摘要、JSON、纯文本等输出格式

- 🎨 **多种GUI**: 三种不同层次的图形界面，支持拖拽、实时预览等
- 🛠️ **可配置**: 灵活的配置系统，易于定制

## 🚀 安装

### 1. 基本安装

```bash
# 克隆项目
git clone <repository-url>
cd file-processing-tool

# 安装依赖
pip install -r requirements.txt
```

### 2. 下载NLP模型（可选，用于完整功能）

=======
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


> **注意**: 如果没有安装NLP模型，程序会以简化模式运行，仍可进行基本的文件处理。

## 📖 使用方法

### 🖥️ 图形界面 (推荐)

```bash
# 启动现代化GUI界面
python run_gui.py

# 或使用快速启动脚本
./start_gui.sh    # Linux/Mac
start_gui.bat     # Windows

# 演示版本 (无需复杂依赖)
python demo_gui.py
```

### 🎮 GUI功能特色

- **📄 多标签页设计**: 文件处理、实时预览、批量处理、结果分析、日志监控
- **👁️ 实时预览**: 即时查看文本处理效果，支持多语言
- **📦 批量处理**: 可视化进度条，并行处理加速
- **📈 数据分析**: 详细统计信息和性能监控
- **⚙️ 智能配置**: 可视化设置界面，一键保存配置
- **🎯 现代设计**: 美观的界面和流畅的用户体验
- **📋 右键菜单**: 便捷的复制、保存、全选操作

### 🎨 GUI界面版本

1. **📝 原版GUI** (`gui.py`) - 简洁实用
   ```bash
   python gui.py
   ```
   - 基础文件处理功能
   - 简单易用的界面
   - 轻量级设计

2. **🎨 现代化GUI** (`modern_gui.py`) - 功能丰富
   ```bash
   python modern_gui.py
   ```
   - 选项卡界面设计
   - 配置管理功能
   - 进度显示和结果查看

3. **✨ 高级GUI** (`premium_gui.py`) - 专业体验
   ```bash
   python premium_gui.py
   ```
   - 现代卡片式布局
   - 实时统计和动画效果
   - 处理报告导出功能

**Linux/Mac用户:**
```bash
# 运行启动脚本
./run_gui.sh

# 或者直接运行
python3 run_gui.py
```

#### GUI功能特点

- **直观操作**: 拖拽文件、点击选择，操作简单
- **实时反馈**: 进度条显示、实时日志更新
- **多标签显示**: 处理摘要、详细结果、处理日志分别显示
- **多种模式**: 单文件处理和批量处理模式
- **结果管理**: 支持保存、复制处理结果

#### GUI界面说明

1. **处理模式选择**
   - 单文件处理: 处理单个文件
   - 批量处理: 处理整个文件夹

2. **文件选择**
   - 输入: 选择要处理的文件或文件夹
   - 输出: 设置处理结果的保存位置

3. **输出格式**
   - 摘要格式: 包含统计信息的可读性摘要
   - JSON格式: 结构化的完整分析结果
   - 纯文本: 处理后的纯文本内容

4. **结果显示**
   - 处理摘要: 快速查看处理结果
   - 详细结果: 完整的分析数据
   - 处理日志: 详细的处理过程记录

### 💻 命令行界面
=======
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


### 🐍 Python API
=======
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

├── config.py                      # 配置管理模块
├── improved_file_handler.py       # 增强文件处理模块
├── improved_data_processor.py     # 增强数据处理模块
├── improved_main.py               # 命令行主程序
├── improved_gui.py                # 现代化GUI界面 ✨
├── demo_gui.py                    # 演示版GUI ✨
├── run_gui.py                     # GUI启动脚本 ✨
├── start_gui.sh                   # Linux/Mac启动脚本 ✨
├── start_gui.bat                  # Windows启动脚本 ✨
├── test_improvements.py           # 测试脚本
├── requirements.txt               # 依赖列表
├── README_improved.md             # 详细说明文档
├── gui.py                         # 原始GUI（保留）
├── main.py                        # 原始主程序（保留）
├── file_handler.py                # 原始文件处理（保留）
└── data_processor.py              # 原始数据处理（保留）
=======
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


### 1. 用户界面
- ✅ 全新的现代化GUI界面
- ✅ 一键启动脚本（Windows/Linux/Mac）
- ✅ 简化版GUI（降级支持）
- ✅ 实时进度显示和日志

### 2. 代码质量
- ✅ 修正所有拼写错误
- ✅ 添加类型提示
- ✅ 统一编码规范
- ✅ 优化异常处理

### 3. 功能增强
- ✅ 智能语言检测
- ✅ 实体识别
- ✅ 多种输出格式
- ✅ 详细统计信息
- ✅ 进度条显示

### 4. 性能优化
- ✅ 模型单例模式
- ✅ 并发处理优化
- ✅ 内存使用优化
- ✅ 错误恢复机制

### 5. 架构改进
- ✅ 模块解耦
- ✅ 配置管理系统
- ✅ 可扩展架构
- ✅ 完整测试覆盖

## 🐛 问题修复

- 🔧 修复数字解析错误
- 🔧 改进文件编码检测
- 🔧 优化内存使用
- 🔧 增强错误日志

## 📚 使用提示

### 新手用户
1. 使用 `run_gui.bat`（Windows）或 `./run_gui.sh`（Linux/Mac）启动
2. 选择"单文件处理"模式
3. 点击"选择文件"选择要处理的文件
4. 点击"开始处理"

### 高级用户
1. 使用命令行界面获得更多控制
2. 自定义 `config.json` 配置文件
3. 使用Python API集成到其他项目

### 故障排除

**GUI无法启动:**
```bash
# 安装缺失的依赖
pip install -r requirements.txt

# 尝试简化版GUI
python simple_gui.py
```

**NLP功能不可用:**
```bash
# 下载必要的模型
python -m spacy download en_core_web_sm
python -m spacy download zh_core_web_sm
```

## 📝 更新日志

### v2.0 (Current)
- 🎉 全新GUI界面
- 🚀 一键启动支持
- 📊 实时处理进度
- 🔧 完全重构代码架构
- 📈 性能显著提升
=======
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