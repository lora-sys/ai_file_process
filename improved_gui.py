#!/usr/bin/env python3
"""
智能文件处理工具 - 现代化GUI界面
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinter.ttk import Progressbar
import threading
import queue
import json
from pathlib import Path
import webbrowser
from typing import Optional, Callable, Any

from improved_file_handler import file_handler
from improved_data_processor import text_processor, result_formatter
from config import config

class ModernStyle:
    """现代化样式配置"""
    
    # 颜色主题
    COLORS = {
        'primary': '#2196F3',
        'primary_dark': '#1976D2',
        'secondary': '#FFC107',
        'success': '#4CAF50',
        'error': '#F44336',
        'warning': '#FF9800',
        'background': '#F5F5F5',
        'surface': '#FFFFFF',
        'text_primary': '#212121',
        'text_secondary': '#757575',
        'border': '#E0E0E0',
        'hover': '#E3F2FD'
    }
    
    # 字体配置
    FONTS = {
        'title': ('Segoe UI', 16, 'bold'),
        'subtitle': ('Segoe UI', 12, 'bold'),
        'body': ('Segoe UI', 10),
        'small': ('Segoe UI', 9),
        'button': ('Segoe UI', 10, 'bold')
    }

class ProgressDialog:
    """进度对话框"""
    
    def __init__(self, parent, title="处理中..."):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x150")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.geometry("+%d+%d" % (
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 状态标签
        self.status_label = ttk.Label(
            main_frame, 
            text="准备开始...",
            font=ModernStyle.FONTS['body']
        )
        self.status_label.pack(pady=(0, 10))
        
        # 进度条
        self.progress = Progressbar(
            main_frame, 
            mode='indeterminate',
            length=300
        )
        self.progress.pack(pady=(0, 10))
        self.progress.start()
        
        # 取消按钮
        self.cancel_button = ttk.Button(
            main_frame,
            text="取消",
            command=self.cancel
        )
        self.cancel_button.pack()
        
        self.cancelled = False
        
    def update_status(self, status: str):
        """更新状态"""
        self.status_label.config(text=status)
        self.dialog.update()
        
    def cancel(self):
        """取消操作"""
        self.cancelled = True
        self.close()
        
    def close(self):
        """关闭对话框"""
        self.progress.stop()
        self.dialog.destroy()

class ResultViewer:
    """结果查看器"""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("处理结果")
        self.window.geometry("800x600")
        self.window.transient(parent)
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        # 主框架
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 工具栏
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        # 格式选择
        ttk.Label(toolbar, text="显示格式:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.format_var = tk.StringVar(value="summary")
        format_combo = ttk.Combobox(
            toolbar,
            textvariable=self.format_var,
            values=["summary", "json", "text"],
            state="readonly",
            width=15
        )
        format_combo.pack(side=tk.LEFT, padx=(0, 10))
        format_combo.bind("<<ComboboxSelected>>", self.on_format_change)
        
        # 保存按钮
        ttk.Button(
            toolbar,
            text="保存结果",
            command=self.save_result
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        # 结果显示区域
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=ModernStyle.FONTS['body'],
            height=25
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # 存储结果数据
        self.result_data = None
        
    def show_result(self, result_data):
        """显示结果"""
        self.result_data = result_data
        self.update_display()
        
    def on_format_change(self, event=None):
        """格式改变时更新显示"""
        self.update_display()
        
    def update_display(self):
        """更新显示内容"""
        if not self.result_data:
            return
            
        self.result_text.delete(1.0, tk.END)
        
        format_type = self.format_var.get()
        
        if format_type == "summary":
            content = result_formatter.to_summary_text(self.result_data)
        elif format_type == "json":
            content = result_formatter.to_json(self.result_data, indent=2)
        else:  # text
            content = self.result_data.processed_text
            
        self.result_text.insert(1.0, content)
        
    def save_result(self):
        """保存结果"""
        if not self.result_data:
            messagebox.showwarning("警告", "没有可保存的结果")
            return
            
        format_type = self.format_var.get()
        
        # 文件扩展名映射
        ext_map = {
            "summary": ".txt",
            "json": ".json",
            "text": ".txt"
        }
        
        filename = filedialog.asksaveasfilename(
            title="保存结果",
            defaultextension=ext_map[format_type],
            filetypes=[
                ("文本文件", "*.txt"),
                ("JSON文件", "*.json"),
                ("所有文件", "*.*")
            ]
        )
        
        if filename:
            try:
                content = self.result_text.get(1.0, tk.END).strip()
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("成功", f"结果已保存到: {filename}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")

class SmartFileProcessorGUI:
    """智能文件处理工具GUI主类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("智能文件处理工具 v2.0")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # 设置图标
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass  # 如果没有图标文件就忽略
            
        # 应用现代化样式
        self.setup_style()
        
        # 初始化变量
        self.current_task = None
        self.result_queue = queue.Queue()
        
        # 设置UI
        self.setup_ui()
        
        # 绑定事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_style(self):
        """设置现代化样式"""
        style = ttk.Style()
        
        # 配置样式
        style.configure('Title.TLabel', 
                       font=ModernStyle.FONTS['title'],
                       foreground=ModernStyle.COLORS['text_primary'])
        
        style.configure('Subtitle.TLabel',
                       font=ModernStyle.FONTS['subtitle'],
                       foreground=ModernStyle.COLORS['text_secondary'])
        
        style.configure('Primary.TButton',
                       font=ModernStyle.FONTS['button'])
        
        # 设置根窗口背景
        self.root.configure(bg=ModernStyle.COLORS['background'])
        
    def setup_ui(self):
        """设置用户界面"""
        # 主容器
        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # 标题区域
        self.setup_header(main_container)
        
        # 分隔线
        ttk.Separator(main_container, orient='horizontal').pack(fill=tk.X, pady=20)
        
        # 创建notebook用于标签页
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # 单文件处理标签页
        self.setup_single_file_tab()
        
        # 批量处理标签页
        self.setup_batch_processing_tab()
        
        # 配置标签页
        self.setup_config_tab()
        
        # 关于标签页
        self.setup_about_tab()
        
        # 状态栏
        self.setup_status_bar(main_container)
        
    def setup_header(self, parent):
        """设置标题区域"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 标题
        title_label = ttk.Label(
            header_frame,
            text="智能文件处理工具",
            style='Title.TLabel'
        )
        title_label.pack(side=tk.LEFT)
        
        # 版本信息
        version_label = ttk.Label(
            header_frame,
            text="v2.0",
            style='Subtitle.TLabel'
        )
        version_label.pack(side=tk.RIGHT)
        
        # 描述
        desc_label = ttk.Label(
            header_frame,
            text="支持多种文件格式的智能文本分析、情感识别和数据提取",
            style='Subtitle.TLabel'
        )
        desc_label.pack(side=tk.LEFT, padx=(20, 0))
        
    def setup_single_file_tab(self):
        """设置单文件处理标签页"""
        frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(frame, text="单文件处理")
        
        # 输入文件选择
        input_frame = ttk.LabelFrame(frame, text="输入文件", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        input_row = ttk.Frame(input_frame)
        input_row.pack(fill=tk.X)
        
        self.single_input_var = tk.StringVar()
        input_entry = ttk.Entry(input_row, textvariable=self.single_input_var, font=ModernStyle.FONTS['body'])
        input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(
            input_row,
            text="浏览...",
            command=self.browse_single_input
        ).pack(side=tk.RIGHT)
        
        # 输出设置
        output_frame = ttk.LabelFrame(frame, text="输出设置", padding="10")
        output_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 输出文件
        output_file_row = ttk.Frame(output_frame)
        output_file_row.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(output_file_row, text="输出文件:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.single_output_var = tk.StringVar()
        output_entry = ttk.Entry(output_file_row, textvariable=self.single_output_var, font=ModernStyle.FONTS['body'])
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(
            output_file_row,
            text="浏览...",
            command=self.browse_single_output
        ).pack(side=tk.RIGHT)
        
        # 输出格式
        format_row = ttk.Frame(output_frame)
        format_row.pack(fill=tk.X)
        
        ttk.Label(format_row, text="输出格式:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.single_format_var = tk.StringVar(value="summary")
        format_combo = ttk.Combobox(
            format_row,
            textvariable=self.single_format_var,
            values=["summary", "json", "text"],
            state="readonly",
            width=15
        )
        format_combo.pack(side=tk.LEFT)
        
        # 处理选项
        options_frame = ttk.LabelFrame(frame, text="处理选项", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.single_sentiment_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_frame,
            text="情感分析",
            variable=self.single_sentiment_var
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        self.single_entities_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_frame,
            text="实体识别",
            variable=self.single_entities_var
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        self.single_preview_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_frame,
            text="显示预览",
            variable=self.single_preview_var
        ).pack(side=tk.LEFT)
        
        # 操作按钮
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(
            button_frame,
            text="开始处理",
            command=self.process_single_file,
            style='Primary.TButton'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="清空",
            command=self.clear_single_form
        ).pack(side=tk.LEFT)
        
    def setup_batch_processing_tab(self):
        """设置批量处理标签页"""
        frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(frame, text="批量处理")
        
        # 输入文件夹
        input_frame = ttk.LabelFrame(frame, text="输入文件夹", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        input_row = ttk.Frame(input_frame)
        input_row.pack(fill=tk.X)
        
        self.batch_input_var = tk.StringVar()
        input_entry = ttk.Entry(input_row, textvariable=self.batch_input_var, font=ModernStyle.FONTS['body'])
        input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(
            input_row,
            text="浏览...",
            command=self.browse_batch_input
        ).pack(side=tk.RIGHT)
        
        # 输出文件夹
        output_frame = ttk.LabelFrame(frame, text="输出文件夹", padding="10")
        output_frame.pack(fill=tk.X, pady=(0, 15))
        
        output_row = ttk.Frame(output_frame)
        output_row.pack(fill=tk.X)
        
        self.batch_output_var = tk.StringVar()
        output_entry = ttk.Entry(output_row, textvariable=self.batch_output_var, font=ModernStyle.FONTS['body'])
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(
            output_row,
            text="浏览...",
            command=self.browse_batch_output
        ).pack(side=tk.RIGHT)
        
        # 批量处理选项
        options_frame = ttk.LabelFrame(frame, text="批量处理选项", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 第一行选项
        options_row1 = ttk.Frame(options_frame)
        options_row1.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(options_row1, text="输出格式:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.batch_format_var = tk.StringVar(value="summary")
        format_combo = ttk.Combobox(
            options_row1,
            textvariable=self.batch_format_var,
            values=["summary", "json", "text"],
            state="readonly",
            width=15
        )
        format_combo.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(options_row1, text="并发数:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.batch_workers_var = tk.IntVar(value=config.get('processing.max_workers', 4))
        workers_spin = ttk.Spinbox(
            options_row1,
            from_=1,
            to=8,
            textvariable=self.batch_workers_var,
            width=10
        )
        workers_spin.pack(side=tk.LEFT)
        
        # 第二行选项
        options_row2 = ttk.Frame(options_frame)
        options_row2.pack(fill=tk.X)
        
        self.batch_sentiment_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_row2,
            text="情感分析",
            variable=self.batch_sentiment_var
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        self.batch_entities_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_row2,
            text="实体识别",
            variable=self.batch_entities_var
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        self.batch_generate_report_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_row2,
            text="生成处理报告",
            variable=self.batch_generate_report_var
        ).pack(side=tk.LEFT)
        
        # 操作按钮
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(
            button_frame,
            text="开始批量处理",
            command=self.process_batch_files,
            style='Primary.TButton'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="清空",
            command=self.clear_batch_form
        ).pack(side=tk.LEFT)
        
        # 进度显示区域
        progress_frame = ttk.LabelFrame(frame, text="处理进度", padding="10")
        progress_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.batch_progress = Progressbar(progress_frame, length=400)
        self.batch_progress.pack(fill=tk.X, pady=(0, 10))
        
        self.batch_status_var = tk.StringVar(value="准备就绪")
        ttk.Label(
            progress_frame,
            textvariable=self.batch_status_var,
            font=ModernStyle.FONTS['body']
        ).pack()
        
    def setup_config_tab(self):
        """设置配置标签页"""
        frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(frame, text="配置")
        
        # 配置显示区域
        config_frame = ttk.LabelFrame(frame, text="当前配置", padding="10")
        config_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        self.config_text = scrolledtext.ScrolledText(
            config_frame,
            wrap=tk.WORD,
            font=ModernStyle.FONTS['body'],
            height=20
        )
        self.config_text.pack(fill=tk.BOTH, expand=True)
        
        # 加载当前配置
        self.load_config_display()
        
        # 操作按钮
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(
            button_frame,
            text="刷新配置",
            command=self.load_config_display
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="保存配置",
            command=self.save_config
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="重置默认",
            command=self.reset_config
        ).pack(side=tk.LEFT)
        
    def setup_about_tab(self):
        """设置关于标签页"""
        frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(frame, text="关于")
        
        # 应用信息
        info_frame = ttk.LabelFrame(frame, text="应用信息", padding="20")
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            info_frame,
            text="智能文件处理工具",
            style='Title.TLabel'
        ).pack(pady=(0, 10))
        
        ttk.Label(
            info_frame,
            text="版本: 2.0.0",
            font=ModernStyle.FONTS['subtitle']
        ).pack(pady=(0, 10))
        
        ttk.Label(
            info_frame,
            text="一个功能强大的智能文件处理工具，支持多种文件格式的文本分析、情感识别、实体提取等功能。",
            font=ModernStyle.FONTS['body'],
            wraplength=500,
            justify=tk.CENTER
        ).pack(pady=(0, 20))
        
        # 功能特性
        features_frame = ttk.LabelFrame(frame, text="主要特性", padding="20")
        features_frame.pack(fill=tk.X, pady=(0, 20))
        
        features = [
            "🔍 智能文本分析 - 自动语言检测、分词、词干化",
            "💡 情感分析 - 使用VADER算法分析文本情感倾向",
            "📊 数据提取 - 自动提取数字、日期、命名实体",
            "📁 多格式支持 - 支持txt、csv、json、pdf、xlsx等格式",
            "⚡ 并发处理 - 多线程批量处理，提高效率",
            "🎯 多种输出 - 支持摘要、JSON、纯文本等输出格式"
        ]
        
        for feature in features:
            ttk.Label(
                features_frame,
                text=feature,
                font=ModernStyle.FONTS['body']
            ).pack(anchor=tk.W, pady=2)
        
        # 链接按钮
        link_frame = ttk.Frame(frame)
        link_frame.pack(fill=tk.X)
        
        ttk.Button(
            link_frame,
            text="查看帮助文档",
            command=self.open_help
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            link_frame,
            text="项目主页",
            command=self.open_project_page
        ).pack(side=tk.LEFT)
        
    def setup_status_bar(self, parent):
        """设置状态栏"""
        status_frame = ttk.Frame(parent, relief=tk.SUNKEN, borderwidth=1)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar(value="准备就绪")
        status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=ModernStyle.FONTS['small']
        )
        status_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        # 配置信息
        config_info = f"模型: {len(config.get('nlp.models', {}))} | 最大文件: {config.get('processing.max_file_size_mb')}MB"
        ttk.Label(
            status_frame,
            text=config_info,
            font=ModernStyle.FONTS['small']
        ).pack(side=tk.RIGHT, padx=5, pady=2)
        
    # 文件浏览方法
    def browse_single_input(self):
        """浏览单个输入文件"""
        filename = filedialog.askopenfilename(
            title="选择输入文件",
            filetypes=[
                ("所有支持的文件", "*.txt;*.csv;*.json;*.pdf;*.xlsx"),
                ("文本文件", "*.txt"),
                ("CSV文件", "*.csv"),
                ("JSON文件", "*.json"),
                ("PDF文件", "*.pdf"),
                ("Excel文件", "*.xlsx"),
                ("所有文件", "*.*")
            ]
        )
        if filename:
            self.single_input_var.set(filename)
            # 自动设置输出文件名
            input_path = Path(filename)
            output_path = input_path.parent / f"{input_path.stem}_processed.txt"
            self.single_output_var.set(str(output_path))
            
    def browse_single_output(self):
        """浏览单个输出文件"""
        filename = filedialog.asksaveasfilename(
            title="选择输出文件",
            defaultextension=".txt",
            filetypes=[
                ("文本文件", "*.txt"),
                ("JSON文件", "*.json"),
                ("所有文件", "*.*")
            ]
        )
        if filename:
            self.single_output_var.set(filename)
            
    def browse_batch_input(self):
        """浏览批量输入文件夹"""
        dirname = filedialog.askdirectory(title="选择输入文件夹")
        if dirname:
            self.batch_input_var.set(dirname)
            
    def browse_batch_output(self):
        """浏览批量输出文件夹"""
        dirname = filedialog.askdirectory(title="选择输出文件夹")
        if dirname:
            self.batch_output_var.set(dirname)
            
    # 表单清空方法
    def clear_single_form(self):
        """清空单文件表单"""
        self.single_input_var.set("")
        self.single_output_var.set("")
        self.single_format_var.set("summary")
        
    def clear_batch_form(self):
        """清空批量处理表单"""
        self.batch_input_var.set("")
        self.batch_output_var.set("")
        self.batch_format_var.set("summary")
        self.batch_status_var.set("准备就绪")
        self.batch_progress['value'] = 0
        
    # 处理方法
    def process_single_file(self):
        """处理单个文件"""
        input_file = self.single_input_var.get().strip()
        output_file = self.single_output_var.get().strip()
        
        if not input_file:
            messagebox.showerror("错误", "请选择输入文件")
            return
            
        if not output_file:
            messagebox.showerror("错误", "请指定输出文件")
            return
            
        if not Path(input_file).exists():
            messagebox.showerror("错误", "输入文件不存在")
            return
            
        # 在后台线程中处理
        self.current_task = threading.Thread(
            target=self._process_single_file_worker,
            args=(input_file, output_file),
            daemon=True
        )
        self.current_task.start()
        
    def _process_single_file_worker(self, input_file, output_file):
        """单文件处理工作线程"""
        try:
            # 更新状态
            self.status_var.set("正在处理文件...")
            
            # 读取文件
            content = file_handler.read_file(input_file)
            if content is None:
                self.result_queue.put(("error", "无法读取文件"))
                return
                
            # 处理文本
            result = text_processor.process_text(content)
            
            # 生成输出内容
            format_type = self.single_format_var.get()
            if format_type == "json":
                output_content = result_formatter.to_json(result)
            elif format_type == "summary":
                output_content = result_formatter.to_summary_text(result)
            else:
                output_content = result.processed_text
                
            # 保存文件
            success = file_handler.write_file(output_file, output_content)
            
            if success:
                self.result_queue.put(("success", result, output_file))
            else:
                self.result_queue.put(("error", "保存文件失败"))
                
        except Exception as e:
            self.result_queue.put(("error", str(e)))
        finally:
            # 检查结果队列
            self.root.after(100, self.check_single_result)
            
    def check_single_result(self):
        """检查单文件处理结果"""
        try:
            result = self.result_queue.get_nowait()
            
            if result[0] == "success":
                _, result_data, output_file = result
                self.status_var.set(f"处理完成: {output_file}")
                
                # 显示结果统计
                stats = result_data.statistics
                message = f"""处理完成！
                
文件: {Path(output_file).name}
语言: {result_data.language}
字符数: {stats.get('char_count', 0)}
词数: {stats.get('word_count', 0)}
数字: {stats.get('number_count', 0)}个
日期: {stats.get('date_count', 0)}个
实体: {stats.get('entity_count', 0)}个"""

                if result_data.sentiment:
                    compound = result_data.sentiment.get('compound', 0)
                    sentiment_label = "积极" if compound > 0.05 else "消极" if compound < -0.05 else "中性"
                    message += f"\n情感倾向: {sentiment_label} ({compound:.3f})"
                
                messagebox.showinfo("处理完成", message)
                
                # 如果启用预览，显示结果查看器
                if self.single_preview_var.get():
                    viewer = ResultViewer(self.root)
                    viewer.show_result(result_data)
                    
            elif result[0] == "error":
                self.status_var.set("处理失败")
                messagebox.showerror("错误", f"处理失败: {result[1]}")
                
        except queue.Empty:
            # 如果队列为空且任务还在运行，继续检查
            if self.current_task and self.current_task.is_alive():
                self.root.after(100, self.check_single_result)
            else:
                self.status_var.set("准备就绪")
                
    def process_batch_files(self):
        """批量处理文件"""
        input_folder = self.batch_input_var.get().strip()
        output_folder = self.batch_output_var.get().strip()
        
        if not input_folder:
            messagebox.showerror("错误", "请选择输入文件夹")
            return
            
        if not output_folder:
            messagebox.showerror("错误", "请选择输出文件夹")
            return
            
        if not Path(input_folder).exists():
            messagebox.showerror("错误", "输入文件夹不存在")
            return
            
        # 在后台线程中处理
        self.current_task = threading.Thread(
            target=self._process_batch_files_worker,
            args=(input_folder, output_folder),
            daemon=True
        )
        self.current_task.start()
        
    def _process_batch_files_worker(self, input_folder, output_folder):
        """批量处理工作线程"""
        try:
            # 更新配置
            original_workers = config.get('processing.max_workers')
            config.config['processing']['max_workers'] = self.batch_workers_var.get()
            
            # 处理函数
            def process_func(content):
                result = text_processor.process_text(content)
                format_type = self.batch_format_var.get()
                
                if format_type == "json":
                    return result_formatter.to_json(result)
                elif format_type == "summary":
                    return result_formatter.to_summary_text(result)
                else:
                    return result.processed_text
            
            # 开始批量处理
            self.batch_status_var.set("正在扫描文件...")
            self.batch_progress.configure(mode='indeterminate')
            self.batch_progress.start()
            
            # 执行批量处理
            result = file_handler.batch_process(
                input_folder, output_folder, process_func
            )
            
            # 恢复原配置
            config.config['processing']['max_workers'] = original_workers
            
            self.result_queue.put(("batch_success", result))
            
        except Exception as e:
            self.result_queue.put(("batch_error", str(e)))
        finally:
            self.batch_progress.stop()
            self.root.after(100, self.check_batch_result)
            
    def check_batch_result(self):
        """检查批量处理结果"""
        try:
            result = self.result_queue.get_nowait()
            
            if result[0] == "batch_success":
                _, batch_result = result
                processed = batch_result.get('processed', 0)
                errors = batch_result.get('errors', 0)
                total = batch_result.get('total', 0)
                
                self.batch_status_var.set(f"完成: {processed}/{total} 成功, {errors} 失败")
                self.batch_progress.configure(mode='determinate', value=100)
                
                message = f"""批量处理完成！

总文件数: {total}
成功处理: {processed}
处理失败: {errors}
成功率: {(processed/total*100) if total > 0 else 0:.1f}%"""

                messagebox.showinfo("批量处理完成", message)
                
                # 生成处理报告
                if self.batch_generate_report_var.get():
                    self.generate_batch_report(batch_result)
                    
            elif result[0] == "batch_error":
                self.batch_status_var.set("批量处理失败")
                messagebox.showerror("错误", f"批量处理失败: {result[1]}")
                
        except queue.Empty:
            if self.current_task and self.current_task.is_alive():
                self.root.after(100, self.check_batch_result)
            else:
                self.batch_progress.configure(mode='determinate', value=0)
                
    def generate_batch_report(self, batch_result):
        """生成批量处理报告"""
        try:
            output_folder = self.batch_output_var.get()
            report_file = Path(output_folder) / "processing_report.txt"
            
            from datetime import datetime
            
            report_content = f"""# 批量处理报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 处理结果
- 总文件数: {batch_result.get('total', 0)}
- 成功处理: {batch_result.get('processed', 0)}
- 处理失败: {batch_result.get('errors', 0)}
- 成功率: {(batch_result.get('processed', 0)/batch_result.get('total', 1)*100):.1f}%

## 处理配置
- 输出格式: {self.batch_format_var.get()}
- 并发数: {self.batch_workers_var.get()}
- 情感分析: {'启用' if self.batch_sentiment_var.get() else '禁用'}
- 实体识别: {'启用' if self.batch_entities_var.get() else '禁用'}

## 文件路径
- 输入文件夹: {self.batch_input_var.get()}
- 输出文件夹: {self.batch_output_var.get()}
"""
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
                
            messagebox.showinfo("报告生成", f"处理报告已保存到: {report_file}")
            
        except Exception as e:
            messagebox.showwarning("警告", f"生成报告失败: {str(e)}")
            
    # 配置管理方法
    def load_config_display(self):
        """加载配置显示"""
        try:
            config_text = json.dumps(config.config, indent=2, ensure_ascii=False)
            self.config_text.delete(1.0, tk.END)
            self.config_text.insert(1.0, config_text)
        except Exception as e:
            messagebox.showerror("错误", f"加载配置失败: {str(e)}")
            
    def save_config(self):
        """保存配置"""
        try:
            config_content = self.config_text.get(1.0, tk.END).strip()
            new_config = json.loads(config_content)
            
            # 验证配置格式
            config.config = new_config
            config.save()
            
            messagebox.showinfo("成功", "配置已保存")
            
        except json.JSONDecodeError:
            messagebox.showerror("错误", "配置格式错误，请检查JSON语法")
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败: {str(e)}")
            
    def reset_config(self):
        """重置为默认配置"""
        if messagebox.askyesno("确认", "确定要重置为默认配置吗？"):
            config.config = config.DEFAULT_CONFIG.copy()
            self.load_config_display()
            messagebox.showinfo("成功", "已重置为默认配置")
            
    # 链接方法
    def open_help(self):
        """打开帮助文档"""
        try:
            help_file = Path("README_improved.md")
            if help_file.exists():
                import subprocess
                import sys
                if sys.platform.startswith('win'):
                    subprocess.run(['notepad', str(help_file)])
                else:
                    subprocess.run(['open', str(help_file)])
            else:
                messagebox.showinfo("帮助", "帮助文档不存在")
        except Exception as e:
            messagebox.showerror("错误", f"打开帮助文档失败: {str(e)}")
            
    def open_project_page(self):
        """打开项目主页"""
        messagebox.showinfo("项目主页", "项目主页功能待实现")
        
    def on_closing(self):
        """窗口关闭事件"""
        if self.current_task and self.current_task.is_alive():
            if messagebox.askyesno("确认", "有任务正在运行，确定要退出吗？"):
                self.root.destroy()
        else:
            self.root.destroy()
            
    def run(self):
        """运行GUI"""
        self.root.mainloop()

def main():
    """主函数"""
    try:
        app = SmartFileProcessorGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("致命错误", f"启动应用失败: {str(e)}")

if __name__ == "__main__":
    main()