# 🖥️ GUI界面使用指南

智能文件处理工具 v2.0 提供了两个图形界面版本，以满足不同用户的需求。

## 🚀 快速启动

### Windows 用户
直接双击 `启动GUI.bat` 文件即可启动。

### 所有平台
```bash
# 方法1: 使用启动脚本（推荐）
python launch_gui.py

# 方法2: 直接启动现代化界面
python modern_gui.py

# 方法3: 启动简化界面
python simple_gui.py
```

## 🎯 界面选择

### 现代化GUI界面 (`modern_gui.py`)
**推荐日常使用**

**特色功能:**
- 🎨 现代化设计，美观易用
- 📋 多标签页设计（处理/配置/帮助）
- 📊 详细的统计信息和图表
- 📈 实时进度显示
- 🔧 完整的配置管理
- 💾 多种输出格式支持
- 🚀 并发处理支持
- 📱 响应式布局

**适用场景:**
- 需要详细分析结果
- 批量处理大量文件
- 需要调整配置参数
- 日常办公使用

### 简化GUI界面 (`simple_gui.py`)
**适合快速处理**

**特色功能:**
- ⚡ 启动速度快
- 🎯 操作简单直观
- 💻 资源占用低
- 🔄 兼容性好
- 🚀 一键切换到高级界面

**适用场景:**
- 快速处理单个文件
- 系统配置较低
- 网络环境受限
- 初次体验

## 📱 现代化GUI详细功能

### 1. 文件处理标签页

#### 处理模式选择
- **单文件处理**: 处理单个文档文件
- **批量处理**: 处理整个文件夹中的文件

#### 文件选择
- **输入路径**: 选择要处理的文件或文件夹
- **输出路径**: 设置处理结果的保存位置
- **智能推荐**: 系统会根据输入自动推荐输出路径

#### 输出格式
- **摘要格式**: 包含统计信息、情感分析等关键信息
- **JSON格式**: 完整的结构化数据，便于程序处理
- **纯文本**: 仅包含处理后的文本内容

#### 处理控制
- **🚀 开始处理**: 启动文件处理
- **⏹ 停止处理**: 中止正在进行的处理
- **🗑 清空结果**: 清除所有处理结果

#### 结果展示
- **处理摘要**: 显示处理结果概览
- **详细结果**: 显示完整的JSON格式结果
- **统计信息**: 显示文件统计和分析数据

### 2. 配置设置标签页

#### 处理配置
- **最大文件大小**: 设置单个文件的大小限制（MB）
- **并发处理数**: 设置同时处理的文件数量

#### NLP配置
- **启用语言检测**: 自动识别文本语言
- **启用情感分析**: 分析文本的情感倾向

#### 文件格式支持
显示当前支持的文件格式列表

### 3. 使用帮助标签页
包含详细的使用说明和功能介绍

## 🎮 操作流程

### 单文件处理流程
1. 选择"单文件处理"模式
2. 点击"选择文件"，选择要处理的文件
3. 系统自动设置输出路径（可手动修改）
4. 选择输出格式（摘要/JSON/纯文本）
5. 点击"🚀 开始处理"
6. 查看处理结果和统计信息

### 批量处理流程
1. 选择"批量处理"模式
2. 点击"选择文件夹"，选择包含文件的文件夹
3. 选择输出文件夹
4. 选择输出格式
5. 点击"🚀 开始处理"
6. 监控处理进度
7. 查看批量处理报告

## 💡 使用技巧

### 文件选择技巧
- 支持拖拽文件到输入框
- 支持的格式：`.txt`, `.csv`, `.json`, `.pdf`, `.xlsx`, `.xls`
- 文件大小建议不超过100MB

### 输出格式选择
- **文档分析**: 推荐使用"摘要格式"
- **数据处理**: 推荐使用"JSON格式"
- **文本提取**: 推荐使用"纯文本"

### 性能优化
- 批量处理时建议调整并发处理数
- 大文件处理时可能需要较长时间
- 定期清空处理结果释放内存

### 错误处理
- 如果处理失败，查看错误信息
- 检查文件是否被其他程序占用
- 确保有足够的磁盘空间

## 🐛 常见问题

### Q: GUI启动失败
**A:** 
1. 检查Python版本（需要3.8+）
2. 运行 `pip install -r requirements.txt`
3. 检查tkinter是否安装

### Q: 文件处理失败
**A:**
1. 确认文件格式被支持
2. 检查文件是否损坏
3. 确认有足够的磁盘空间

### Q: 处理速度慢
**A:**
1. 调整并发处理数设置
2. 关闭不必要的其他程序
3. 考虑处理文件大小

### Q: 中文显示乱码
**A:**
1. 确认系统支持UTF-8编码
2. 检查字体设置
3. 尝试更换文件编码

## 🔧 高级功能

### 配置文件管理
GUI界面允许直接编辑配置文件，包括：
- 处理参数调整
- NLP模型设置
- 日志记录配置

### 结果导出
- 支持将处理结果保存为多种格式
- 可批量导出处理报告
- 支持自定义导出模板

### 插件扩展
GUI界面支持加载自定义处理插件，扩展功能。

## 📞 技术支持

如果在使用过程中遇到问题：
1. 查看帮助标签页中的详细说明
2. 检查错误日志文件
3. 参考本使用指南
4. 联系技术支持团队

---

*最后更新: 2024年1月*