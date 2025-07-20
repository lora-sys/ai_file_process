#!/usr/bin/env python3
"""
智能文件处理工具 - GUI演示脚本
演示所有GUI功能的简化版本
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import time
import json
from pathlib import Path
from datetime import datetime

class DemoGUI:
    """演示GUI类"""
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_widgets()
        self.create_demo_data()
    
    def setup_window(self):
        """设置窗口"""
        self.root.title("智能文件处理工具 v2.0 - 演示版")
        self.root.geometry("1000x800")
        self.root.minsize(900, 700)
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        # 自定义样式
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'), foreground='#2c3e50')
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
        style.configure('Success.TLabel', foreground='#27ae60')
        style.configure('Error.TLabel', foreground='#e74c3c')
        style.configure('Info.TLabel', foreground='#3498db')
        
        # 配置主题色
        style.configure('Accent.TButton', background='#3498db', foreground='white')
        style.map('Accent.TButton', background=[('active', '#2980b9')])
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 标题区域
        self.create_header(main_frame)
        
        # 主内容区域
        self.create_main_content(main_frame)
        
        # 状态栏
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """创建标题区域"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        header_frame.columnconfigure(1, weight=1)
        
        # 标题和图标
        title_frame = ttk.Frame(header_frame)
        title_frame.grid(row=0, column=0, sticky=tk.W)
        
        # 使用Unicode字符作为图标
        icon_label = ttk.Label(title_frame, text="🔍", font=('Arial', 24))
        icon_label.grid(row=0, column=0, padx=(0, 10))
        
        title_label = ttk.Label(title_frame, text="智能文件处理工具", style='Title.TLabel')
        title_label.grid(row=0, column=1)
        
        subtitle_label = ttk.Label(title_frame, text="v2.0 演示版", 
                                 font=('Arial', 10, 'italic'), foreground='#7f8c8d')
        subtitle_label.grid(row=1, column=1, sticky=tk.W)
        
        # 快速操作按钮
        quick_frame = ttk.Frame(header_frame)
        quick_frame.grid(row=0, column=1, sticky=tk.E)
        
        ttk.Button(quick_frame, text="📖 帮助", 
                  command=self.show_help).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(quick_frame, text="⚙️ 设置", 
                  command=self.show_settings).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(quick_frame, text="🎮 演示", 
                  command=self.run_demo, style='Accent.TButton').grid(row=0, column=2)
        
        # 分隔线
        separator = ttk.Separator(parent, orient='horizontal')
        separator.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(60, 0))
    
    def create_main_content(self, parent):
        """创建主内容区域"""
        # 创建notebook
        notebook = ttk.Notebook(parent)
        notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 文件处理标签页
        self.create_file_tab(notebook)
        
        # 实时预览标签页
        self.create_preview_tab(notebook)
        
        # 批量处理标签页
        self.create_batch_tab(notebook)
        
        # 结果分析标签页
        self.create_analysis_tab(notebook)
        
        # 日志监控标签页
        self.create_log_tab(notebook)
    
    def create_file_tab(self, parent):
        """创建文件处理标签页"""
        tab_frame = ttk.Frame(parent, padding="15")
        parent.add(tab_frame, text="📄 文件处理")
        
        # 左右分割
        left_frame = ttk.Frame(tab_frame)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        right_frame = ttk.Frame(tab_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        tab_frame.columnconfigure(0, weight=1)
        tab_frame.columnconfigure(1, weight=1)
        tab_frame.rowconfigure(0, weight=1)
        
        # 左侧：输入设置
        self.create_input_section(left_frame)
        
        # 右侧：结果显示
        self.create_result_section(right_frame)
    
    def create_input_section(self, parent):
        """创建输入设置区域"""
        # 文件选择
        file_frame = ttk.LabelFrame(parent, text="📁 文件选择", padding="10")
        file_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        
        ttk.Label(file_frame, text="输入文件:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        input_frame = ttk.Frame(file_frame)
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_path)
        self.input_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(input_frame, text="浏览", command=self.select_input_file).grid(row=0, column=1)
        
        ttk.Label(file_frame, text="输出文件:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        output_frame = ttk.Frame(file_frame)
        output_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
        output_frame.columnconfigure(0, weight=1)
        
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_path)
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(output_frame, text="浏览", command=self.select_output_file).grid(row=0, column=1)
        
        # 处理选项
        options_frame = ttk.LabelFrame(parent, text="⚙️ 处理选项", padding="10")
        options_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.output_format = tk.StringVar(value="summary")
        self.language_detect = tk.BooleanVar(value=True)
        self.sentiment_analysis = tk.BooleanVar(value=True)
        self.entity_extraction = tk.BooleanVar(value=True)
        
        ttk.Label(options_frame, text="输出格式:", style='Heading.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        format_frame = ttk.Frame(options_frame)
        format_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Radiobutton(format_frame, text="摘要", variable=self.output_format, value="summary").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(format_frame, text="JSON", variable=self.output_format, value="json").grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        ttk.Radiobutton(format_frame, text="文本", variable=self.output_format, value="text").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(options_frame, text="分析选项:", style='Heading.TLabel').grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        ttk.Checkbutton(options_frame, text="语言检测", variable=self.language_detect).grid(row=3, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="情感分析", variable=self.sentiment_analysis).grid(row=4, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="实体提取", variable=self.entity_extraction).grid(row=5, column=0, sticky=tk.W)
        
        # 处理按钮
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.process_button = ttk.Button(button_frame, text="🚀 开始处理", 
                                       command=self.start_processing, style='Accent.TButton')
        self.process_button.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        button_frame.columnconfigure(0, weight=1)
        
        self.demo_button = ttk.Button(button_frame, text="🎮 运行演示", command=self.demo_processing)
        self.demo_button.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(parent, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def create_result_section(self, parent):
        """创建结果显示区域"""
        result_frame = ttk.LabelFrame(parent, text="📊 处理结果", padding="10")
        result_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        # 结果文本区域
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=20)
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 操作按钮
        result_buttons = ttk.Frame(result_frame)
        result_buttons.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(result_buttons, text="📋 复制", command=self.copy_result).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(result_buttons, text="💾 保存", command=self.save_result).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(result_buttons, text="🧹 清空", command=self.clear_result).grid(row=0, column=2)
    
    def create_preview_tab(self, parent):
        """创建预览标签页"""
        tab_frame = ttk.Frame(parent, padding="15")
        parent.add(tab_frame, text="👁️ 实时预览")
        
        # 上下分割
        input_frame = ttk.LabelFrame(tab_frame, text="输入文本", padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        output_frame = ttk.LabelFrame(tab_frame, text="处理预览", padding="10")
        output_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        tab_frame.columnconfigure(0, weight=1)
        tab_frame.rowconfigure(0, weight=1)
        tab_frame.rowconfigure(1, weight=1)
        
        # 输入文本区域
        self.preview_input = scrolledtext.ScrolledText(input_frame, height=8)
        self.preview_input.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.preview_input.bind('<KeyRelease>', self.update_preview)
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        
        # 预览输出区域
        self.preview_output = scrolledtext.ScrolledText(output_frame, height=8, state='disabled')
        self.preview_output.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        # 添加示例文本
        sample_text = """Hello world! This is a sample text for demonstration. 
It contains numbers like 123 and 456.78, dates like 2024-01-01, 
and various entities. The sentiment of this text is quite positive!
这是一段中文示例文本，用于演示多语言处理能力。"""
        self.preview_input.insert(1.0, sample_text)
        self.update_preview()
    
    def create_batch_tab(self, parent):
        """创建批量处理标签页"""
        tab_frame = ttk.Frame(parent, padding="15")
        parent.add(tab_frame, text="📦 批量处理")
        
        # 批量处理界面
        folder_frame = ttk.LabelFrame(tab_frame, text="文件夹选择", padding="10")
        folder_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        folder_frame.columnconfigure(1, weight=1)
        
        self.batch_input = tk.StringVar()
        self.batch_output = tk.StringVar()
        
        ttk.Label(folder_frame, text="输入文件夹:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Entry(folder_frame, textvariable=self.batch_input).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(folder_frame, text="选择", command=self.select_input_folder).grid(row=0, column=2)
        
        ttk.Label(folder_frame, text="输出文件夹:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        ttk.Entry(folder_frame, textvariable=self.batch_output).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 5), pady=(5, 0))
        ttk.Button(folder_frame, text="选择", command=self.select_output_folder).grid(row=1, column=2, pady=(5, 0))
        
        # 批量处理选项
        batch_options_frame = ttk.LabelFrame(tab_frame, text="批量选项", padding="10")
        batch_options_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.parallel_processing = tk.BooleanVar(value=True)
        self.max_workers = tk.IntVar(value=4)
        
        ttk.Checkbutton(batch_options_frame, text="并行处理", variable=self.parallel_processing).grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(batch_options_frame, text="最大并发数:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        ttk.Spinbox(batch_options_frame, from_=1, to=16, textvariable=self.max_workers, width=10).grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=(5, 0))
        
        # 批量处理按钮
        ttk.Button(tab_frame, text="🚀 开始批量处理", command=self.start_batch_processing, style='Accent.TButton').grid(row=2, column=0, pady=(10, 0))
        
        # 批量处理进度
        self.batch_progress = tk.DoubleVar()
        self.batch_progress_bar = ttk.Progressbar(tab_frame, variable=self.batch_progress, maximum=100)
        self.batch_progress_bar.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # 批量处理结果
        batch_result_frame = ttk.LabelFrame(tab_frame, text="批量处理结果", padding="10")
        batch_result_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        batch_result_frame.columnconfigure(0, weight=1)
        batch_result_frame.rowconfigure(0, weight=1)
        tab_frame.rowconfigure(4, weight=1)
        
        self.batch_result_text = scrolledtext.ScrolledText(batch_result_frame, height=8)
        self.batch_result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        tab_frame.columnconfigure(0, weight=1)
    
    def create_analysis_tab(self, parent):
        """创建结果分析标签页"""
        tab_frame = ttk.Frame(parent, padding="15")
        parent.add(tab_frame, text="📈 结果分析")
        
        # 统计信息显示
        stats_frame = ttk.LabelFrame(tab_frame, text="统计信息", padding="10")
        stats_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 创建统计标签
        self.stats_labels = {}
        stats_items = [
            ("处理文件数", "files_count"),
            ("总字符数", "total_chars"),
            ("总词数", "total_words"),
            ("平均情感分数", "avg_sentiment")
        ]
        
        for i, (label, key) in enumerate(stats_items):
            ttk.Label(stats_frame, text=f"{label}:").grid(row=i//2, column=(i%2)*2, sticky=tk.W, padx=(0, 5), pady=2)
            self.stats_labels[key] = ttk.Label(stats_frame, text="0", style='Info.TLabel')
            self.stats_labels[key].grid(row=i//2, column=(i%2)*2+1, sticky=tk.W, padx=(0, 20), pady=2)
        
        # 详细分析结果
        analysis_frame = ttk.LabelFrame(tab_frame, text="详细分析", padding="10")
        analysis_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        analysis_frame.columnconfigure(0, weight=1)
        analysis_frame.rowconfigure(0, weight=1)
        tab_frame.rowconfigure(1, weight=1)
        
        self.analysis_text = scrolledtext.ScrolledText(analysis_frame, height=15)
        self.analysis_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        tab_frame.columnconfigure(0, weight=1)
        tab_frame.columnconfigure(1, weight=1)
    
    def create_log_tab(self, parent):
        """创建日志标签页"""
        tab_frame = ttk.Frame(parent, padding="15")
        parent.add(tab_frame, text="📋 日志监控")
        
        # 日志控制
        log_control_frame = ttk.Frame(tab_frame)
        log_control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(log_control_frame, text="日志级别:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.log_level = tk.StringVar(value="INFO")
        log_combo = ttk.Combobox(log_control_frame, textvariable=self.log_level, 
                                values=["DEBUG", "INFO", "WARNING", "ERROR"], state="readonly")
        log_combo.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(log_control_frame, text="清空日志", command=self.clear_logs).grid(row=0, column=2, padx=(0, 5))
        ttk.Button(log_control_frame, text="保存日志", command=self.save_logs).grid(row=0, column=3)
        
        # 日志显示区域
        log_frame = ttk.LabelFrame(tab_frame, text="系统日志", padding="10")
        log_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        tab_frame.rowconfigure(1, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        tab_frame.columnconfigure(0, weight=1)
        
        # 添加一些示例日志
        self.add_log("INFO", "系统启动完成")
        self.add_log("INFO", "配置加载成功")
        self.add_log("INFO", "GUI界面初始化完成")
    
    def create_status_bar(self, parent):
        """创建状态栏"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.columnconfigure(1, weight=1)
        
        # 状态信息
        self.status_var = tk.StringVar(value="就绪")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.grid(row=0, column=0, sticky=tk.W)
        
        # 时间显示
        self.time_var = tk.StringVar()
        time_label = ttk.Label(status_frame, textvariable=self.time_var)
        time_label.grid(row=0, column=2, sticky=tk.E)
        
        # 版本信息
        version_label = ttk.Label(status_frame, text="v2.0 演示版", font=('Arial', 8))
        version_label.grid(row=0, column=1, sticky=tk.E, padx=(0, 20))
        
        self.update_time()
    
    def create_demo_data(self):
        """创建演示数据"""
        self.demo_files = [
            "document1.txt",
            "analysis.csv", 
            "report.json",
            "data.xlsx"
        ]
        
        self.demo_results = {
            "files_processed": 0,
            "total_chars": 0,
            "total_words": 0,
            "avg_sentiment": 0.0
        }
    
    # 事件处理方法
    def select_input_file(self):
        """选择输入文件"""
        file_path = filedialog.askopenfilename(
            title="选择输入文件",
            filetypes=[
                ("所有支持的文件", "*.txt;*.csv;*.json;*.pdf;*.xlsx"),
                ("文本文件", "*.txt"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.input_path.set(file_path)
            # 自动设置输出路径
            path = Path(file_path)
            output_path = path.parent / f"{path.stem}_processed{path.suffix}"
            self.output_path.set(str(output_path))
            self.add_log("INFO", f"选择输入文件: {file_path}")
    
    def select_output_file(self):
        """选择输出文件"""
        file_path = filedialog.asksaveasfilename(
            title="选择输出文件",
            defaultextension=".txt",
            filetypes=[
                ("文本文件", "*.txt"),
                ("JSON文件", "*.json"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.output_path.set(file_path)
            self.add_log("INFO", f"选择输出文件: {file_path}")
    
    def select_input_folder(self):
        """选择输入文件夹"""
        folder_path = filedialog.askdirectory(title="选择输入文件夹")
        if folder_path:
            self.batch_input.set(folder_path)
            self.add_log("INFO", f"选择输入文件夹: {folder_path}")
    
    def select_output_folder(self):
        """选择输出文件夹"""
        folder_path = filedialog.askdirectory(title="选择输出文件夹")
        if folder_path:
            self.batch_output.set(folder_path)
            self.add_log("INFO", f"选择输出文件夹: {folder_path}")
    
    def start_processing(self):
        """开始处理"""
        input_file = self.input_path.get()
        output_file = self.output_path.get()
        
        if not input_file or not output_file:
            messagebox.showerror("错误", "请选择输入和输出文件")
            return
        
        self.add_log("INFO", "开始文件处理")
        self.status_var.set("正在处理...")
        
        # 模拟处理过程
        self.simulate_processing()
    
    def demo_processing(self):
        """演示处理功能"""
        self.result_text.delete(1.0, tk.END)
        
        demo_result = """📊 文件处理完成

=== 基本信息 ===
文件名: demo_document.txt
文件大小: 2.3 KB
处理时间: 0.8 秒
语言: 英文 (en)

=== 文本统计 ===
字符数: 2,345
单词数: 456
句子数: 23
平均词长: 5.1

=== 情感分析 ===
情感倾向: 积极 ✓
置信度: 85%
积极分数: 0.723
消极分数: 0.123
中性分数: 0.154

=== 提取信息 ===
📞 电话号码: +1-555-0123, (555) 456-7890
📧 邮箱地址: example@email.com, user@domain.org
🔗 网址: https://example.com, www.sample.org
📅 日期: 2024-01-15, 2024-03-20
🔢 数字: 123, 456.78, 99.9%

=== 命名实体 ===
👤 人名: John Smith, Mary Johnson
🏢 组织: Microsoft Corporation, Google Inc.
🌍 地点: New York, San Francisco
💰 金额: $1,000, €500

=== 关键词 ===
🔑 主要关键词: technology, innovation, development, analysis, system
📈 词频统计: 
  - technology (15次)
  - system (12次)  
  - analysis (8次)
  - development (6次)
  - innovation (5次)

=== 处理建议 ===
✅ 文本质量良好
✅ 语言检测准确
✅ 实体识别完整
⚠️  建议检查部分数字格式
💡 可考虑添加更多技术术语

处理完成！结果已保存到输出文件。"""
        
        self.result_text.insert(tk.END, demo_result)
        self.status_var.set("演示完成")
        self.add_log("INFO", "演示处理完成")
        
        # 更新统计信息
        self.update_stats(chars=2345, words=456, sentiment=0.723)
    
    def start_batch_processing(self):
        """开始批量处理"""
        input_folder = self.batch_input.get()
        output_folder = self.batch_output.get()
        
        if not input_folder or not output_folder:
            messagebox.showerror("错误", "请选择输入和输出文件夹")
            return
        
        self.add_log("INFO", "开始批量处理")
        self.status_var.set("批量处理中...")
        
        # 模拟批量处理
        self.simulate_batch_processing()
    
    def simulate_processing(self):
        """模拟文件处理过程"""
        def process():
            steps = [
                (10, "读取文件..."),
                (25, "语言检测..."),
                (40, "文本分析..."),
                (60, "情感分析..."),
                (80, "实体提取..."),
                (95, "生成报告..."),
                (100, "处理完成")
            ]
            
            for progress, message in steps:
                time.sleep(0.5)
                self.root.after(0, lambda p=progress, m=message: self.update_progress(p, m))
            
            # 显示结果
            self.root.after(0, self.show_processing_result)
        
        threading.Thread(target=process, daemon=True).start()
    
    def simulate_batch_processing(self):
        """模拟批量处理过程"""
        def process():
            files = ["file1.txt", "file2.csv", "file3.json", "file4.pdf", "file5.xlsx"]
            total_files = len(files)
            
            self.batch_result_text.delete(1.0, tk.END)
            self.batch_result_text.insert(tk.END, "开始批量处理...\n\n")
            
            for i, filename in enumerate(files):
                progress = ((i + 1) / total_files) * 100
                
                # 更新进度
                self.root.after(0, lambda p=progress: self.update_batch_progress(p))
                
                # 模拟处理每个文件
                self.root.after(0, lambda f=filename, idx=i+1: self.update_batch_result(f, idx, total_files))
                
                time.sleep(1)
            
            # 完成
            self.root.after(0, self.finish_batch_processing)
        
        threading.Thread(target=process, daemon=True).start()
    
    def update_progress(self, value, message):
        """更新进度条"""
        self.progress_var.set(value)
        self.status_var.set(message)
        if value == 100:
            self.add_log("INFO", "文件处理完成")
    
    def update_batch_progress(self, value):
        """更新批量处理进度"""
        self.batch_progress.set(value)
    
    def update_batch_result(self, filename, current, total):
        """更新批量处理结果"""
        message = f"[{current}/{total}] 处理文件: {filename} ✓\n"
        self.batch_result_text.insert(tk.END, message)
        self.batch_result_text.see(tk.END)
        self.add_log("INFO", f"批量处理: {filename}")
    
    def finish_batch_processing(self):
        """完成批量处理"""
        summary = "\n=== 批量处理完成 ===\n"
        summary += "总文件数: 5\n"
        summary += "成功处理: 5\n"
        summary += "失败文件: 0\n"
        summary += "处理时间: 5.2 秒\n"
        
        self.batch_result_text.insert(tk.END, summary)
        self.status_var.set("批量处理完成")
        self.add_log("INFO", "批量处理全部完成")
    
    def show_processing_result(self):
        """显示处理结果"""
        result = """🎉 文件处理成功完成！

=== 处理摘要 ===
✅ 文件读取: 成功
✅ 语言检测: 英文 (置信度: 98%)
✅ 文本分析: 完成
✅ 情感分析: 积极情感 (0.65)
✅ 实体提取: 发现 12 个实体
✅ 文件保存: 成功

=== 详细结果 ===
原文字符数: 1,234
处理后词数: 186
发现数字: 8 个
发现日期: 3 个
发现邮箱: 2 个
发现链接: 1 个

✨ 处理完成，结果已保存！"""

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result)
        
        # 更新统计
        self.update_stats(chars=1234, words=186, sentiment=0.65)
    
    def update_preview(self, event=None):
        """更新实时预览"""
        text = self.preview_input.get(1.0, tk.END).strip()
        if not text:
            return
        
        # 模拟简单的文本处理
        words = text.split()
        char_count = len(text)
        word_count = len(words)
        
        # 简单的情感分析（基于关键词）
        positive_words = ["good", "great", "excellent", "positive", "happy", "love", "like", "amazing"]
        negative_words = ["bad", "terrible", "awful", "negative", "sad", "hate", "dislike", "horrible"]
        
        pos_count = sum(1 for word in words if word.lower() in positive_words)
        neg_count = sum(1 for word in words if word.lower() in negative_words)
        
        if pos_count > neg_count:
            sentiment = "积极"
        elif neg_count > pos_count:
            sentiment = "消极"
        else:
            sentiment = "中性"
        
        # 生成预览结果
        preview_result = f"""📝 实时分析结果

📊 基本统计:
• 字符数: {char_count}
• 词数: {word_count}
• 句子数: {text.count('.') + text.count('!') + text.count('?')}

💭 情感分析:
• 情感倾向: {sentiment}
• 积极词汇: {pos_count} 个
• 消极词汇: {neg_count} 个

🔍 检测到的元素:
• 数字: {len([w for w in words if any(c.isdigit() for c in w)])} 个
• 邮箱: {text.count('@')} 个
• 链接: {text.count('http')} 个
• 大写词: {len([w for w in words if w.isupper() and len(w) > 1])} 个

⚡ 实时处理完成！"""
        
        # 更新预览输出
        self.preview_output.config(state='normal')
        self.preview_output.delete(1.0, tk.END)
        self.preview_output.insert(1.0, preview_result)
        self.preview_output.config(state='disabled')
    
    def update_stats(self, chars=0, words=0, sentiment=0.0):
        """更新统计信息"""
        self.demo_results["files_processed"] += 1
        self.demo_results["total_chars"] += chars
        self.demo_results["total_words"] += words
        self.demo_results["avg_sentiment"] = (self.demo_results["avg_sentiment"] + sentiment) / 2
        
        self.stats_labels["files_count"].config(text=str(self.demo_results["files_processed"]))
        self.stats_labels["total_chars"].config(text=f"{self.demo_results['total_chars']:,}")
        self.stats_labels["total_words"].config(text=f"{self.demo_results['total_words']:,}")
        self.stats_labels["avg_sentiment"].config(text=f"{self.demo_results['avg_sentiment']:.3f}")
        
        # 更新详细分析
        analysis = f"""📈 最新分析报告 - {datetime.now().strftime('%H:%M:%S')}

=== 处理统计 ===
总处理文件数: {self.demo_results['files_processed']}
累计字符数: {self.demo_results['total_chars']:,}
累计词数: {self.demo_results['total_words']:,}
平均情感分数: {self.demo_results['avg_sentiment']:.3f}

=== 性能指标 ===
平均处理速度: {self.demo_results['total_chars'] / max(1, self.demo_results['files_processed']):.0f} 字符/文件
文件处理效率: {'高效' if self.demo_results['files_processed'] > 2 else '标准'}
系统负载: {'正常' if self.demo_results['files_processed'] < 10 else '较高'}

=== 质量评估 ===
情感分析质量: {'优秀' if self.demo_results['avg_sentiment'] > 0.5 else '良好' if self.demo_results['avg_sentiment'] > 0 else '需改进'}
文本处理质量: 优秀
实体识别准确率: 95.2%

=== 建议 ===
{'继续保持当前处理质量' if self.demo_results['avg_sentiment'] > 0.5 else '建议优化情感分析算法'}
系统运行状态良好，可继续处理更多文件。
"""
        
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(1.0, analysis)
    
    def add_log(self, level, message):
        """添加日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # 限制日志长度
        lines = int(self.log_text.index(tk.END).split('.')[0])
        if lines > 100:
            self.log_text.delete(1.0, "10.0")
    
    def update_time(self):
        """更新时间显示"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_var.set(current_time)
        self.root.after(1000, self.update_time)
    
    # 工具方法
    def copy_result(self):
        """复制结果"""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.result_text.get(1.0, tk.END))
            messagebox.showinfo("成功", "结果已复制到剪贴板")
            self.add_log("INFO", "复制处理结果到剪贴板")
        except Exception as e:
            messagebox.showerror("错误", f"复制失败: {e}")
    
    def save_result(self):
        """保存结果"""
        content = self.result_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("警告", "没有可保存的结果")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="保存结果",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("成功", f"结果已保存到: {file_path}")
                self.add_log("INFO", f"保存结果到文件: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {e}")
    
    def clear_result(self):
        """清空结果"""
        self.result_text.delete(1.0, tk.END)
        self.add_log("INFO", "清空处理结果")
    
    def clear_logs(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END)
        self.add_log("INFO", "日志已清空")
    
    def save_logs(self):
        """保存日志"""
        content = self.log_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("警告", "没有可保存的日志")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="保存日志",
            defaultextension=".log",
            filetypes=[("日志文件", "*.log"), ("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("成功", f"日志已保存到: {file_path}")
                self.add_log("INFO", f"保存日志到文件: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {e}")
    
    def show_help(self):
        """显示帮助"""
        help_text = """🔍 智能文件处理工具 v2.0 - 帮助

📖 主要功能:
• 智能文本分析和处理
• 多语言支持和语言检测
• 情感分析和实体识别
• 批量文件处理
• 实时预览和分析

🚀 使用方法:
1. 选择处理模式（单文件/批量）
2. 选择输入文件或文件夹
3. 设置输出位置和格式
4. 配置处理选项
5. 点击开始处理

📋 支持格式:
• 文本文件 (.txt)
• CSV文件 (.csv)
• JSON文件 (.json)
• PDF文件 (.pdf)
• Excel文件 (.xlsx)

💡 提示:
• 使用"🎮 演示"按钮查看功能演示
• 实时预览标签页可即时查看处理效果
• 批量处理支持并行加速
• 所有操作都有详细日志记录

如需更多帮助，请查看项目文档。"""
        
        messagebox.showinfo("帮助", help_text)
    
    def show_settings(self):
        """显示设置对话框"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("设置")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # 居中显示
        settings_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 100,
            self.root.winfo_rooty() + 100
        ))
        
        ttk.Label(settings_window, text="⚙️ 系统设置", style='Title.TLabel').pack(pady=20)
        
        # 设置选项
        settings_frame = ttk.Frame(settings_window, padding="20")
        settings_frame.pack(fill='both', expand=True)
        
        ttk.Checkbutton(settings_frame, text="启用自动保存").pack(anchor='w', pady=5)
        ttk.Checkbutton(settings_frame, text="显示详细日志").pack(anchor='w', pady=5)
        ttk.Checkbutton(settings_frame, text="启用声音提示").pack(anchor='w', pady=5)
        
        ttk.Label(settings_frame, text="界面主题:").pack(anchor='w', pady=(10, 5))
        theme_combo = ttk.Combobox(settings_frame, values=["默认", "深色", "高对比度"], state="readonly")
        theme_combo.set("默认")
        theme_combo.pack(anchor='w', pady=5)
        
        # 按钮
        button_frame = ttk.Frame(settings_window)
        button_frame.pack(fill='x', padx=20, pady=20)
        
        ttk.Button(button_frame, text="确定", command=settings_window.destroy).pack(side='right', padx=(5, 0))
        ttk.Button(button_frame, text="取消", command=settings_window.destroy).pack(side='right')
    
    def run_demo(self):
        """运行完整演示"""
        demo_window = tk.Toplevel(self.root)
        demo_window.title("功能演示")
        demo_window.geometry("600x400")
        demo_window.transient(self.root)
        demo_window.grab_set()
        
        # 居中显示
        demo_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 50,
            self.root.winfo_rooty() + 50
        ))
        
        ttk.Label(demo_window, text="🎮 功能演示", style='Title.TLabel').pack(pady=20)
        
        demo_text = scrolledtext.ScrolledText(demo_window, wrap=tk.WORD, height=20, width=70)
        demo_text.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        demo_content = """🎯 智能文件处理工具演示指南

=== 核心功能演示 ===

1. 📄 单文件处理
   • 支持多种格式 (.txt, .csv, .json, .pdf, .xlsx)
   • 自动语言检测 (中文/英文/其他)
   • 智能文本分析和处理
   • 情感倾向分析
   • 命名实体识别

2. 👁️ 实时预览
   • 即时文本分析
   • 动态结果更新
   • 多语言实时处理
   • 可视化统计信息

3. 📦 批量处理
   • 文件夹批量处理
   • 并行加速处理
   • 进度实时监控
   • 详细处理报告

4. 📈 结果分析
   • 处理统计汇总
   • 性能指标监控
   • 质量评估报告
   • 趋势分析图表

5. 📋 日志监控
   • 实时日志记录
   • 多级别日志过滤
   • 日志导出功能
   • 错误追踪机制

=== 使用建议 ===

🔥 快速上手:
   1. 点击"🎮 运行演示"体验功能
   2. 使用"实时预览"了解处理效果
   3. 尝试批量处理提高效率

⚡ 高级技巧:
   • 配置并行处理数优化性能
   • 选择合适的输出格式
   • 利用实时预览调试文本
   • 监控日志排查问题

🛠️ 自定义设置:
   • 调整文件大小限制
   • 启用/禁用特定分析功能
   • 设置界面主题
   • 配置自动保存

开始探索这些强大的功能吧！"""
        
        demo_text.insert(1.0, demo_content)
        demo_text.config(state='disabled')
        
        # 关闭按钮
        ttk.Button(demo_window, text="开始体验", command=demo_window.destroy).pack(pady=(0, 20))


def main():
    """主函数"""
    root = tk.Tk()
    app = DemoGUI(root)
    
    # 设置窗口关闭事件
    def on_closing():
        if messagebox.askokcancel("退出", "确定要退出演示程序吗？"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # 启动消息
    root.after(1000, lambda: messagebox.showinfo(
        "欢迎", 
        "🎉 欢迎使用智能文件处理工具！\n\n"
        "这是功能演示版本，展示了所有主要功能。\n"
        "点击各个标签页探索不同功能，\n"
        "或点击"🎮 演示"按钮查看详细说明。\n\n"
        "开始体验吧！"
    ))
    
    root.mainloop()


if __name__ == "__main__":
    main()