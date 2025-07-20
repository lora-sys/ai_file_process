#!/usr/bin/env python3
"""
现代化GUI界面 - 使用tkinter和ttk
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import json
import os
from pathlib import Path
from datetime import datetime
import queue

# 导入处理模块
from improved_file_handler import file_handler
from improved_data_processor import text_processor, result_formatter
from config import config

class ModernFileProcessorGUI:
    """现代化文件处理器GUI"""
    
    def __init__(self, root):
        self.root = root
        self.setup_main_window()
        self.create_variables()
        self.create_widgets()
        self.setup_layout()
        self.setup_styles()
        
        # 线程通信
        self.result_queue = queue.Queue()
        self.check_queue()
    
    def setup_main_window(self):
        """设置主窗口"""
        self.root.title("智能文件处理工具 v2.0")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # 设置图标（如果有的话）
        try:
            # self.root.iconbitmap("icon.ico")
            pass
        except:
            pass
    
    def create_variables(self):
        """创建变量"""
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.output_format = tk.StringVar(value="summary")
        self.processing_mode = tk.StringVar(value="single")
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="就绪")
        
    def create_widgets(self):
        """创建控件"""
        # 主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        
        # 标题
        self.title_label = ttk.Label(
            self.main_frame, 
            text="🤖 智能文件处理工具", 
            font=("Arial", 16, "bold")
        )
        
        # 创建notebook（标签页）
        self.notebook = ttk.Notebook(self.main_frame)
        
        # 处理标签页
        self.process_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.process_frame, text="文件处理")
        
        # 配置标签页
        self.config_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.config_frame, text="配置设置")
        
        # 帮助标签页
        self.help_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.help_frame, text="使用帮助")
        
        self.create_process_widgets()
        self.create_config_widgets()
        self.create_help_widgets()
        
        # 状态栏
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_label = ttk.Label(
            self.status_frame, 
            textvariable=self.status_var
        )
        self.progress_bar = ttk.Progressbar(
            self.status_frame, 
            variable=self.progress_var,
            mode='determinate'
        )
    
    def create_process_widgets(self):
        """创建处理界面控件"""
        # 处理模式选择
        mode_frame = ttk.LabelFrame(self.process_frame, text="处理模式", padding="10")
        
        ttk.Radiobutton(
            mode_frame, text="单文件处理", 
            variable=self.processing_mode, value="single",
            command=self.on_mode_changed
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Radiobutton(
            mode_frame, text="批量处理", 
            variable=self.processing_mode, value="batch",
            command=self.on_mode_changed
        ).pack(side=tk.LEFT, padx=10)
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(self.process_frame, text="文件选择", padding="10")
        
        # 输入路径
        ttk.Label(file_frame, text="输入路径:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.input_entry = ttk.Entry(file_frame, textvariable=self.input_path, width=50)
        self.input_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)
        self.input_button = ttk.Button(
            file_frame, text="选择文件", 
            command=self.select_input_file
        )
        self.input_button.grid(row=0, column=2, padx=5, pady=5)
        
        # 输出路径
        ttk.Label(file_frame, text="输出路径:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_entry = ttk.Entry(file_frame, textvariable=self.output_path, width=50)
        self.output_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.EW)
        self.output_button = ttk.Button(
            file_frame, text="选择位置", 
            command=self.select_output_path
        )
        self.output_button.grid(row=1, column=2, padx=5, pady=5)
        
        file_frame.columnconfigure(1, weight=1)
        
        # 输出格式选择
        format_frame = ttk.LabelFrame(self.process_frame, text="输出格式", padding="10")
        
        ttk.Radiobutton(
            format_frame, text="摘要格式", 
            variable=self.output_format, value="summary"
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Radiobutton(
            format_frame, text="JSON格式", 
            variable=self.output_format, value="json"
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Radiobutton(
            format_frame, text="纯文本", 
            variable=self.output_format, value="text"
        ).pack(side=tk.LEFT, padx=10)
        
        # 处理按钮
        button_frame = ttk.Frame(self.process_frame)
        
        self.process_button = ttk.Button(
            button_frame, text="🚀 开始处理", 
            command=self.start_processing,
            style="Accent.TButton"
        )
        self.process_button.pack(side=tk.LEFT, padx=10)
        
        self.stop_button = ttk.Button(
            button_frame, text="⏹ 停止处理", 
            command=self.stop_processing,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        self.clear_button = ttk.Button(
            button_frame, text="🗑 清空结果", 
            command=self.clear_results
        )
        self.clear_button.pack(side=tk.LEFT, padx=10)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(self.process_frame, text="处理结果", padding="10")
        
        # 创建Notebook用于显示不同类型的结果
        self.result_notebook = ttk.Notebook(result_frame)
        
        # 摘要标签页
        self.summary_frame = ttk.Frame(self.result_notebook)
        self.result_notebook.add(self.summary_frame, text="处理摘要")
        
        self.summary_text = scrolledtext.ScrolledText(
            self.summary_frame, 
            wrap=tk.WORD, 
            height=10, 
            font=("Consolas", 10)
        )
        self.summary_text.pack(fill=tk.BOTH, expand=True)
        
        # 详细结果标签页
        self.detail_frame = ttk.Frame(self.result_notebook)
        self.result_notebook.add(self.detail_frame, text="详细结果")
        
        self.detail_text = scrolledtext.ScrolledText(
            self.detail_frame, 
            wrap=tk.WORD, 
            height=10, 
            font=("Consolas", 9)
        )
        self.detail_text.pack(fill=tk.BOTH, expand=True)
        
        # 统计信息标签页
        self.stats_frame = ttk.Frame(self.result_notebook)
        self.result_notebook.add(self.stats_frame, text="统计信息")
        
        self.create_stats_widgets()
        
        self.result_notebook.pack(fill=tk.BOTH, expand=True)
        
        # 布局
        mode_frame.pack(fill=tk.X, pady=5)
        file_frame.pack(fill=tk.X, pady=5)
        format_frame.pack(fill=tk.X, pady=5)
        button_frame.pack(fill=tk.X, pady=10)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def create_stats_widgets(self):
        """创建统计信息控件"""
        # 左侧统计信息
        left_stats = ttk.Frame(self.stats_frame)
        left_stats.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # 基本统计
        basic_frame = ttk.LabelFrame(left_stats, text="基本统计", padding="10")
        basic_frame.pack(fill=tk.X, pady=5)
        
        self.char_count_var = tk.StringVar(value="0")
        self.word_count_var = tk.StringVar(value="0")
        self.sentence_count_var = tk.StringVar(value="0")
        self.language_var = tk.StringVar(value="未知")
        
        ttk.Label(basic_frame, text="字符数:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(basic_frame, textvariable=self.char_count_var).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(basic_frame, text="词数:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(basic_frame, textvariable=self.word_count_var).grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(basic_frame, text="句子数:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(basic_frame, textvariable=self.sentence_count_var).grid(row=2, column=1, sticky=tk.W)
        
        ttk.Label(basic_frame, text="语言:").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(basic_frame, textvariable=self.language_var).grid(row=3, column=1, sticky=tk.W)
        
        # 提取统计
        extract_frame = ttk.LabelFrame(left_stats, text="提取统计", padding="10")
        extract_frame.pack(fill=tk.X, pady=5)
        
        self.number_count_var = tk.StringVar(value="0")
        self.date_count_var = tk.StringVar(value="0")
        self.entity_count_var = tk.StringVar(value="0")
        
        ttk.Label(extract_frame, text="数字:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(extract_frame, textvariable=self.number_count_var).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(extract_frame, text="日期:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(extract_frame, textvariable=self.date_count_var).grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(extract_frame, text="实体:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(extract_frame, textvariable=self.entity_count_var).grid(row=2, column=1, sticky=tk.W)
        
        # 右侧情感分析
        right_stats = ttk.Frame(self.stats_frame)
        right_stats.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        sentiment_frame = ttk.LabelFrame(right_stats, text="情感分析", padding="10")
        sentiment_frame.pack(fill=tk.X, pady=5)
        
        self.sentiment_var = tk.StringVar(value="未分析")
        self.compound_var = tk.StringVar(value="0.000")
        self.positive_var = tk.StringVar(value="0.000")
        self.negative_var = tk.StringVar(value="0.000")
        self.neutral_var = tk.StringVar(value="0.000")
        
        ttk.Label(sentiment_frame, text="总体倾向:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(sentiment_frame, textvariable=self.sentiment_var).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(sentiment_frame, text="综合分数:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(sentiment_frame, textvariable=self.compound_var).grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(sentiment_frame, text="积极:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(sentiment_frame, textvariable=self.positive_var).grid(row=2, column=1, sticky=tk.W)
        
        ttk.Label(sentiment_frame, text="消极:").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(sentiment_frame, textvariable=self.negative_var).grid(row=3, column=1, sticky=tk.W)
        
        ttk.Label(sentiment_frame, text="中性:").grid(row=4, column=0, sticky=tk.W)
        ttk.Label(sentiment_frame, textvariable=self.neutral_var).grid(row=4, column=1, sticky=tk.W)
    
    def create_config_widgets(self):
        """创建配置界面控件"""
        # 处理配置
        process_config_frame = ttk.LabelFrame(
            self.config_frame, text="处理配置", padding="10"
        )
        process_config_frame.pack(fill=tk.X, pady=5)
        
        # 最大文件大小
        ttk.Label(process_config_frame, text="最大文件大小 (MB):").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.max_file_size_var = tk.StringVar(
            value=str(config.get('processing.max_file_size_mb', 100))
        )
        ttk.Entry(
            process_config_frame, textvariable=self.max_file_size_var, width=10
        ).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        # 并发处理数
        ttk.Label(process_config_frame, text="并发处理数:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.max_workers_var = tk.StringVar(
            value=str(config.get('processing.max_workers', 4))
        )
        ttk.Entry(
            process_config_frame, textvariable=self.max_workers_var, width=10
        ).grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        
        # NLP配置
        nlp_config_frame = ttk.LabelFrame(
            self.config_frame, text="NLP配置", padding="10"
        )
        nlp_config_frame.pack(fill=tk.X, pady=5)
        
        self.language_detection_var = tk.BooleanVar(
            value=config.get('nlp.detect_language', True)
        )
        ttk.Checkbutton(
            nlp_config_frame, text="启用语言检测",
            variable=self.language_detection_var
        ).pack(anchor=tk.W, pady=2)
        
        self.sentiment_analysis_var = tk.BooleanVar(
            value=config.get('nlp.sentiment_analysis', True)
        )
        ttk.Checkbutton(
            nlp_config_frame, text="启用情感分析",
            variable=self.sentiment_analysis_var
        ).pack(anchor=tk.W, pady=2)
        
        # 支持的文件格式
        format_frame = ttk.LabelFrame(
            self.config_frame, text="支持的文件格式", padding="10"
        )
        format_frame.pack(fill=tk.X, pady=5)
        
        formats_text = ", ".join(config.get('processing.supported_formats', []))
        ttk.Label(format_frame, text=formats_text, wraplength=400).pack(anchor=tk.W)
        
        # 保存配置按钮
        ttk.Button(
            self.config_frame, text="保存配置", 
            command=self.save_config
        ).pack(pady=10)
    
    def create_help_widgets(self):
        """创建帮助界面控件"""
        help_text = """
🤖 智能文件处理工具 v2.0 使用说明

✨ 主要功能:
• 智能文本分析: 自动语言检测、分词、词干化
• 情感分析: 使用VADER算法分析文本情感倾向  
• 数据提取: 自动提取数字、日期、命名实体
• 多格式支持: 支持 .txt, .csv, .json, .pdf, .xlsx 等格式
• 并发处理: 多线程批量处理，提高效率

📖 使用步骤:
1. 选择处理模式（单文件或批量处理）
2. 选择输入文件或文件夹
3. 设置输出路径
4. 选择输出格式（摘要/JSON/纯文本）
5. 点击"开始处理"按钮

📋 输出格式说明:
• 摘要格式: 包含语言、统计信息、情感分析等关键信息
• JSON格式: 完整的结构化数据，适合程序处理
• 纯文本: 仅包含处理后的文本内容

⚙️ 配置说明:
• 最大文件大小: 限制处理文件的大小（单位：MB）
• 并发处理数: 同时处理的文件数量
• 语言检测: 自动识别文本语言
• 情感分析: 分析文本的情感倾向

🎯 支持格式:
• 文本文件: .txt
• 表格文件: .csv, .xlsx, .xls  
• 数据文件: .json
• 文档文件: .pdf

💡 使用提示:
• 大文件处理可能需要较长时间，请耐心等待
• 批量处理时会显示进度条
• 可以随时停止正在进行的处理
• 处理结果会自动保存到指定路径

🐛 问题反馈:
如果遇到问题，请查看详细日志信息
        """
        
        help_text_widget = scrolledtext.ScrolledText(
            self.help_frame, 
            wrap=tk.WORD, 
            font=("Microsoft YaHei", 10)
        )
        help_text_widget.pack(fill=tk.BOTH, expand=True)
        help_text_widget.insert(tk.END, help_text)
        help_text_widget.config(state=tk.DISABLED)
    
    def setup_layout(self):
        """设置布局"""
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.title_label.pack(pady=10)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.status_frame.pack(fill=tk.X, pady=5)
        self.status_label.pack(side=tk.LEFT)
        self.progress_bar.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(20, 0))
    
    def setup_styles(self):
        """设置样式"""
        style = ttk.Style()
        
        # 设置主题
        try:
            style.theme_use('clam')
        except:
            pass
        
        # 自定义样式
        style.configure('Accent.TButton', foreground='white', background='#0078d4')
        style.map('Accent.TButton', 
                 background=[('active', '#106ebe'), ('pressed', '#005a9e')])
    
    def on_mode_changed(self):
        """处理模式改变"""
        mode = self.processing_mode.get()
        if mode == "single":
            self.input_button.config(text="选择文件")
            self.output_button.config(text="选择位置")
        else:
            self.input_button.config(text="选择文件夹")
            self.output_button.config(text="选择文件夹")
    
    def select_input_file(self):
        """选择输入文件或文件夹"""
        mode = self.processing_mode.get()
        if mode == "single":
            filename = filedialog.askopenfilename(
                title="选择要处理的文件",
                filetypes=[
                    ("所有支持的文件", "*.txt;*.csv;*.json;*.pdf;*.xlsx;*.xls"),
                    ("文本文件", "*.txt"),
                    ("CSV文件", "*.csv"),
                    ("JSON文件", "*.json"),
                    ("PDF文件", "*.pdf"),
                    ("Excel文件", "*.xlsx;*.xls"),
                    ("所有文件", "*.*")
                ]
            )
        else:
            filename = filedialog.askdirectory(title="选择要处理的文件夹")
        
        if filename:
            self.input_path.set(filename)
            # 自动设置输出路径
            self.auto_set_output_path(filename)
    
    def select_output_path(self):
        """选择输出路径"""
        mode = self.processing_mode.get()
        if mode == "single":
            filename = filedialog.asksaveasfilename(
                title="选择输出位置",
                defaultextension=".txt",
                filetypes=[
                    ("文本文件", "*.txt"),
                    ("JSON文件", "*.json"),
                    ("所有文件", "*.*")
                ]
            )
        else:
            filename = filedialog.askdirectory(title="选择输出文件夹")
        
        if filename:
            self.output_path.set(filename)
    
    def auto_set_output_path(self, input_path):
        """自动设置输出路径"""
        if not input_path:
            return
        
        path = Path(input_path)
        mode = self.processing_mode.get()
        format_type = self.output_format.get()
        
        if mode == "single":
            # 单文件处理
            if format_type == "json":
                output_path = path.with_suffix('.json')
            else:
                output_path = path.with_suffix('.processed.txt')
            self.output_path.set(str(output_path))
        else:
            # 批量处理
            output_dir = path.parent / f"{path.name}_processed"
            self.output_path.set(str(output_dir))
    
    def start_processing(self):
        """开始处理"""
        input_path = self.input_path.get().strip()
        output_path = self.output_path.get().strip()
        
        if not input_path or not output_path:
            messagebox.showerror("错误", "请选择输入和输出路径")
            return
        
        if not Path(input_path).exists():
            messagebox.showerror("错误", "输入路径不存在")
            return
        
        # 禁用处理按钮，启用停止按钮
        self.process_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # 清空之前的结果
        self.clear_results()
        
        # 启动处理线程
        self.processing_thread = threading.Thread(
            target=self.process_files_thread,
            args=(input_path, output_path),
            daemon=True
        )
        self.processing_thread.start()
    
    def stop_processing(self):
        """停止处理"""
        self.status_var.set("正在停止...")
        # 注意：实际实现中需要添加线程停止机制
        self.process_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_var.set("已停止")
    
    def process_files_thread(self, input_path, output_path):
        """处理文件的线程函数"""
        try:
            mode = self.processing_mode.get()
            format_type = self.output_format.get()
            
            if mode == "single":
                self.process_single_file_thread(input_path, output_path, format_type)
            else:
                self.process_batch_files_thread(input_path, output_path, format_type)
                
        except Exception as e:
            self.result_queue.put(("error", str(e)))
        finally:
            self.result_queue.put(("finished", None))
    
    def process_single_file_thread(self, input_path, output_path, format_type):
        """处理单个文件的线程函数"""
        self.result_queue.put(("status", f"正在读取文件: {Path(input_path).name}"))
        
        # 读取文件
        content = file_handler.read_file(input_path)
        if content is None:
            self.result_queue.put(("error", f"无法读取文件: {input_path}"))
            return
        
        self.result_queue.put(("status", "正在分析文本..."))
        self.result_queue.put(("progress", 30))
        
        # 处理文本
        result = text_processor.process_text(content)
        
        self.result_queue.put(("status", "正在生成结果..."))
        self.result_queue.put(("progress", 70))
        
        # 格式化输出
        if format_type == "json":
            output_content = result_formatter.to_json(result)
        elif format_type == "summary":
            output_content = result_formatter.to_summary_text(result)
        else:
            output_content = result.processed_text
        
        # 写入文件
        success = file_handler.write_file(output_path, output_content)
        
        if success:
            self.result_queue.put(("status", f"处理完成: {Path(output_path).name}"))
            self.result_queue.put(("result", result))
            self.result_queue.put(("progress", 100))
        else:
            self.result_queue.put(("error", f"无法写入文件: {output_path}"))
    
    def process_batch_files_thread(self, input_folder, output_folder, format_type):
        """批量处理文件的线程函数"""
        def process_func(content):
            result = text_processor.process_text(content)
            if format_type == "json":
                return result_formatter.to_json(result)
            elif format_type == "summary":
                return result_formatter.to_summary_text(result)
            else:
                return result.processed_text
        
        self.result_queue.put(("status", "开始批量处理..."))
        
        # 使用文件处理器的批量处理功能
        batch_result = file_handler.batch_process(
            input_folder, output_folder, process_func
        )
        
        self.result_queue.put(("batch_result", batch_result))
        self.result_queue.put(("progress", 100))
    
    def check_queue(self):
        """检查结果队列"""
        try:
            while True:
                msg_type, data = self.result_queue.get_nowait()
                
                if msg_type == "status":
                    self.status_var.set(data)
                elif msg_type == "progress":
                    self.progress_var.set(data)
                elif msg_type == "result":
                    self.display_result(data)
                elif msg_type == "batch_result":
                    self.display_batch_result(data)
                elif msg_type == "error":
                    messagebox.showerror("处理错误", data)
                    self.status_var.set(f"错误: {data}")
                elif msg_type == "finished":
                    self.process_button.config(state=tk.NORMAL)
                    self.stop_button.config(state=tk.DISABLED)
                    
        except queue.Empty:
            pass
        
        # 每100ms检查一次队列
        self.root.after(100, self.check_queue)
    
    def display_result(self, result):
        """显示处理结果"""
        # 显示摘要
        summary = result_formatter.to_summary_text(result)
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, summary)
        
        # 显示详细结果
        detail = result_formatter.to_json(result, indent=2)
        self.detail_text.delete(1.0, tk.END)
        self.detail_text.insert(tk.END, detail)
        
        # 更新统计信息
        self.update_stats_display(result)
    
    def display_batch_result(self, batch_result):
        """显示批量处理结果"""
        summary = f"""
批量处理完成！

总文件数: {batch_result.get('total', 0)}
成功处理: {batch_result.get('processed', 0)}
处理失败: {batch_result.get('errors', 0)}
成功率: {batch_result.get('processed', 0) / max(batch_result.get('total', 1), 1) * 100:.1f}%

处理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, summary.strip())
        
        self.status_var.set(f"批量处理完成: {batch_result.get('processed', 0)}/{batch_result.get('total', 0)}")
    
    def update_stats_display(self, result):
        """更新统计信息显示"""
        stats = result.statistics
        
        # 基本统计
        self.char_count_var.set(str(stats.get('char_count', 0)))
        self.word_count_var.set(str(stats.get('word_count', 0)))
        self.sentence_count_var.set(str(stats.get('sentence_count', 0)))
        self.language_var.set(result.language or "未知")
        
        # 提取统计
        self.number_count_var.set(str(len(result.numbers)))
        self.date_count_var.set(str(len(result.dates)))
        self.entity_count_var.set(str(len(result.entities)))
        
        # 情感分析
        if result.sentiment:
            compound = result.sentiment.get('compound', 0)
            if compound > 0.05:
                sentiment_label = "积极"
            elif compound < -0.05:
                sentiment_label = "消极"
            else:
                sentiment_label = "中性"
            
            self.sentiment_var.set(sentiment_label)
            self.compound_var.set(f"{compound:.3f}")
            self.positive_var.set(f"{result.sentiment.get('pos', 0):.3f}")
            self.negative_var.set(f"{result.sentiment.get('neg', 0):.3f}")
            self.neutral_var.set(f"{result.sentiment.get('neu', 0):.3f}")
    
    def clear_results(self):
        """清空结果"""
        self.summary_text.delete(1.0, tk.END)
        self.detail_text.delete(1.0, tk.END)
        self.progress_var.set(0)
        
        # 重置统计信息
        self.char_count_var.set("0")
        self.word_count_var.set("0")
        self.sentence_count_var.set("0")
        self.language_var.set("未知")
        self.number_count_var.set("0")
        self.date_count_var.set("0")
        self.entity_count_var.set("0")
        self.sentiment_var.set("未分析")
        self.compound_var.set("0.000")
        self.positive_var.set("0.000")
        self.negative_var.set("0.000")
        self.neutral_var.set("0.000")
    
    def save_config(self):
        """保存配置"""
        try:
            # 更新配置
            config.config['processing']['max_file_size_mb'] = int(self.max_file_size_var.get())
            config.config['processing']['max_workers'] = int(self.max_workers_var.get())
            config.config['nlp']['detect_language'] = self.language_detection_var.get()
            config.config['nlp']['sentiment_analysis'] = self.sentiment_analysis_var.get()
            
            # 保存到文件
            config.save()
            
            messagebox.showinfo("成功", "配置已保存")
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败: {e}")

def main():
    """主函数"""
    root = tk.Tk()
    app = ModernFileProcessorGUI(root)
    
    # 设置窗口关闭事件
    def on_closing():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # 启动GUI
    root.mainloop()

if __name__ == "__main__":
    main()