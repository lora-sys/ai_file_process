#!/usr/bin/env python3
"""
智能文件处理工具 - 高级GUI界面
使用现代化设计和自定义主题
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import json
from datetime import datetime

# 添加项目路径
sys.path.append(str(Path(__file__).parent))

try:
    from improved_file_handler import file_handler
    from improved_data_processor import text_processor, result_formatter
    from improved_main import FileProcessor
    from config import config
except ImportError as e:
    print(f"导入模块失败: {e}")
    print("请确保所有改进的模块文件都存在")
    sys.exit(1)

class ModernTheme:
    """现代化主题配置"""
    
    # 颜色配置
    COLORS = {
        'primary': '#3498db',      # 主要颜色
        'secondary': '#2ecc71',    # 次要颜色
        'success': '#27ae60',      # 成功颜色
        'warning': '#f39c12',      # 警告颜色
        'danger': '#e74c3c',       # 危险颜色
        'info': '#17a2b8',         # 信息颜色
        'light': '#f8f9fa',        # 浅色
        'dark': '#343a40',         # 深色
        'white': '#ffffff',        # 白色
        'gray': '#6c757d',         # 灰色
        'light_gray': '#e9ecef',   # 浅灰色
        'bg_primary': '#f4f4f4',   # 主背景
        'bg_secondary': '#ffffff', # 次要背景
        'text_primary': '#2c3e50', # 主要文本
        'text_secondary': '#7f8c8d' # 次要文本
    }
    
    # 字体配置
    FONTS = {
        'default': ('Segoe UI', 9),
        'heading': ('Segoe UI', 12, 'bold'),
        'title': ('Segoe UI', 16, 'bold'),
        'small': ('Segoe UI', 8),
        'code': ('Consolas', 9)
    }

class AnimatedProgressBar:
    """动画进度条"""
    
    def __init__(self, parent, **kwargs):
        self.frame = ttk.Frame(parent)
        self.progress = ttk.Progressbar(
            self.frame,
            mode='determinate',
            **kwargs
        )
        self.label = ttk.Label(self.frame, text="0%")
        
        self.progress.pack(fill=tk.X, padx=(0, 10))
        self.label.pack(side=tk.RIGHT)
        
        self.value = 0
        self.animate_id = None
    
    def set_value(self, value, text=""):
        """设置进度值"""
        target = max(0, min(100, value))
        if target != self.value:
            self.animate_to(target)
        
        if text:
            self.label.config(text=text)
        else:
            self.label.config(text=f"{int(target)}%")
    
    def animate_to(self, target):
        """动画过渡到目标值"""
        if self.animate_id:
            self.frame.after_cancel(self.animate_id)
        
        diff = target - self.value
        if abs(diff) < 1:
            self.value = target
            self.progress['value'] = target
            return
        
        step = diff / 10
        self.value += step
        self.progress['value'] = self.value
        
        self.animate_id = self.frame.after(50, lambda: self.animate_to(target))
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

class ModernCard:
    """现代化卡片组件"""
    
    def __init__(self, parent, title="", **kwargs):
        self.frame = tk.Frame(
            parent,
            bg=ModernTheme.COLORS['bg_secondary'],
            relief='flat',
            bd=1,
            **kwargs
        )
        
        # 添加阴影效果
        self.shadow = tk.Frame(
            parent,
            bg=ModernTheme.COLORS['light_gray'],
            height=2
        )
        
        if title:
            self.title_frame = tk.Frame(
                self.frame,
                bg=ModernTheme.COLORS['bg_secondary'],
                height=40
            )
            self.title_label = tk.Label(
                self.title_frame,
                text=title,
                font=ModernTheme.FONTS['heading'],
                fg=ModernTheme.COLORS['text_primary'],
                bg=ModernTheme.COLORS['bg_secondary']
            )
            
            self.title_frame.pack(fill=tk.X, padx=15, pady=(15, 0))
            self.title_frame.pack_propagate(False)
            self.title_label.pack(side=tk.LEFT, pady=10)
        
        self.content_frame = tk.Frame(
            self.frame,
            bg=ModernTheme.COLORS['bg_secondary']
        )
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    def pack(self, **kwargs):
        self.shadow.pack(fill=tk.X, pady=(2, 0))
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

class PremiumFileProcessorGUI:
    """高级文件处理器GUI"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_theme()
        self.create_widgets()
        self.setup_layout()
        
        # 处理器和队列
        self.processor = FileProcessor()
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        
        # 状态变量
        self.processing = False
        self.current_task = None
        self.start_time = None
        
        # 设置队列检查
        self.check_queue()
    
    def setup_window(self):
        """设置主窗口"""
        self.root.title("智能文件处理工具 v2.0 Premium")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # 设置窗口图标
        try:
            # 这里可以设置自定义图标
            pass
        except:
            pass
        
        # 窗口居中
        self.center_window()
        
        # 设置关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_theme(self):
        """设置主题"""
        # 主窗口背景
        self.root.configure(bg=ModernTheme.COLORS['bg_primary'])
        
        # 配置ttk样式
        self.style = ttk.Style()
        
        # 自定义样式
        self.style.configure('Modern.TNotebook', 
                           background=ModernTheme.COLORS['bg_primary'],
                           borderwidth=0)
        
        self.style.configure('Modern.TNotebook.Tab',
                           padding=[20, 10],
                           font=ModernTheme.FONTS['default'])
        
        self.style.configure('Modern.TFrame',
                           background=ModernTheme.COLORS['bg_secondary'],
                           relief='flat')
        
        self.style.configure('Modern.TButton',
                           font=ModernTheme.FONTS['default'],
                           focuscolor='none')
        
        self.style.configure('Primary.TButton',
                           background=ModernTheme.COLORS['primary'],
                           foreground='white',
                           font=ModernTheme.FONTS['default'],
                           focuscolor='none')
        
        self.style.configure('Success.TButton',
                           background=ModernTheme.COLORS['success'],
                           foreground='white')
        
        self.style.configure('Modern.TEntry',
                           font=ModernTheme.FONTS['default'],
                           fieldbackground='white')
    
    def create_widgets(self):
        """创建所有控件"""
        # 主容器
        self.main_container = tk.Frame(
            self.root,
            bg=ModernTheme.COLORS['bg_primary']
        )
        
        # 顶部标题栏
        self.create_header()
        
        # 主要内容区域
        self.content_frame = tk.Frame(
            self.main_container,
            bg=ModernTheme.COLORS['bg_primary']
        )
        
        # 左侧面板
        self.create_sidebar()
        
        # 右侧主内容
        self.create_main_content()
        
        # 底部状态栏
        self.create_footer()
    
    def create_header(self):
        """创建顶部标题栏"""
        self.header_frame = tk.Frame(
            self.main_container,
            bg=ModernTheme.COLORS['primary'],
            height=80
        )
        self.header_frame.pack_propagate(False)
        
        # 标题
        title_label = tk.Label(
            self.header_frame,
            text="🚀 智能文件处理工具",
            font=ModernTheme.FONTS['title'],
            fg='white',
            bg=ModernTheme.COLORS['primary']
        )
        title_label.pack(side=tk.LEFT, padx=30, pady=25)
        
        # 版本信息
        version_label = tk.Label(
            self.header_frame,
            text="Premium v2.0",
            font=ModernTheme.FONTS['small'],
            fg='white',
            bg=ModernTheme.COLORS['primary']
        )
        version_label.pack(side=tk.RIGHT, padx=30, pady=25)
    
    def create_sidebar(self):
        """创建左侧边栏"""
        self.sidebar_frame = tk.Frame(
            self.content_frame,
            bg=ModernTheme.COLORS['bg_secondary'],
            width=300
        )
        self.sidebar_frame.pack_propagate(False)
        
        # 功能选择
        functions_card = ModernCard(self.sidebar_frame, "功能选择")
        
        self.function_var = tk.StringVar(value="single")
        
        # 单文件处理选项
        single_frame = tk.Frame(
            functions_card.content_frame,
            bg=ModernTheme.COLORS['bg_secondary']
        )
        single_radio = tk.Radiobutton(
            single_frame,
            text="📄 单文件处理",
            variable=self.function_var,
            value="single",
            font=ModernTheme.FONTS['default'],
            bg=ModernTheme.COLORS['bg_secondary'],
            fg=ModernTheme.COLORS['text_primary'],
            selectcolor=ModernTheme.COLORS['primary'],
            command=self.on_function_change
        )
        single_radio.pack(anchor=tk.W, pady=5)
        single_frame.pack(fill=tk.X, pady=5)
        
        # 批量处理选项
        batch_frame = tk.Frame(
            functions_card.content_frame,
            bg=ModernTheme.COLORS['bg_secondary']
        )
        batch_radio = tk.Radiobutton(
            batch_frame,
            text="📁 批量处理",
            variable=self.function_var,
            value="batch",
            font=ModernTheme.FONTS['default'],
            bg=ModernTheme.COLORS['bg_secondary'],
            fg=ModernTheme.COLORS['text_primary'],
            selectcolor=ModernTheme.COLORS['primary'],
            command=self.on_function_change
        )
        batch_radio.pack(anchor=tk.W, pady=5)
        batch_frame.pack(fill=tk.X, pady=5)
        
        functions_card.pack(fill=tk.X, padx=15, pady=15)
        
        # 输出格式选择
        format_card = ModernCard(self.sidebar_frame, "输出格式")
        
        self.format_var = tk.StringVar(value="summary")
        formats = [
            ("📋 摘要格式", "summary"),
            ("📊 JSON格式", "json"),
            ("📝 纯文本", "text")
        ]
        
        for text, value in formats:
            format_radio = tk.Radiobutton(
                format_card.content_frame,
                text=text,
                variable=self.format_var,
                value=value,
                font=ModernTheme.FONTS['default'],
                bg=ModernTheme.COLORS['bg_secondary'],
                fg=ModernTheme.COLORS['text_primary'],
                selectcolor=ModernTheme.COLORS['secondary']
            )
            format_radio.pack(anchor=tk.W, pady=3)
        
        format_card.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # 处理统计
        self.stats_card = ModernCard(self.sidebar_frame, "处理统计")
        
        self.stats_labels = {}
        stats_items = [
            ("已处理文件", "processed"),
            ("处理失败", "failed"),
            ("处理时间", "time"),
            ("当前状态", "status")
        ]
        
        for label, key in stats_items:
            frame = tk.Frame(
                self.stats_card.content_frame,
                bg=ModernTheme.COLORS['bg_secondary']
            )
            
            tk.Label(
                frame,
                text=f"{label}:",
                font=ModernTheme.FONTS['small'],
                bg=ModernTheme.COLORS['bg_secondary'],
                fg=ModernTheme.COLORS['text_secondary']
            ).pack(side=tk.LEFT)
            
            value_label = tk.Label(
                frame,
                text="0" if key != "status" else "准备就绪",
                font=ModernTheme.FONTS['default'],
                bg=ModernTheme.COLORS['bg_secondary'],
                fg=ModernTheme.COLORS['text_primary']
            )
            value_label.pack(side=tk.RIGHT)
            
            self.stats_labels[key] = value_label
            frame.pack(fill=tk.X, pady=2)
        
        self.stats_card.pack(fill=tk.X, padx=15, pady=(0, 15))
    
    def create_main_content(self):
        """创建主要内容区域"""
        self.main_frame = tk.Frame(
            self.content_frame,
            bg=ModernTheme.COLORS['bg_primary']
        )
        
        # 文件选择区域
        self.create_file_selection()
        
        # 处理控制区域
        self.create_control_panel()
        
        # 结果显示区域
        self.create_result_display()
    
    def create_file_selection(self):
        """创建文件选择区域"""
        self.file_card = ModernCard(self.main_frame, "文件选择")
        
        # 输入文件/文件夹
        input_frame = tk.Frame(
            self.file_card.content_frame,
            bg=ModernTheme.COLORS['bg_secondary']
        )
        
        tk.Label(
            input_frame,
            text="输入路径:",
            font=ModernTheme.FONTS['default'],
            bg=ModernTheme.COLORS['bg_secondary'],
            fg=ModernTheme.COLORS['text_primary']
        ).pack(anchor=tk.W, pady=(0, 5))
        
        input_select_frame = tk.Frame(
            input_frame,
            bg=ModernTheme.COLORS['bg_secondary']
        )
        
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(
            input_select_frame,
            textvariable=self.input_var,
            font=ModernTheme.FONTS['default'],
            width=50
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.input_button = tk.Button(
            input_select_frame,
            text="浏览...",
            font=ModernTheme.FONTS['default'],
            bg=ModernTheme.COLORS['info'],
            fg='white',
            relief='flat',
            padx=20,
            command=self.select_input
        )
        self.input_button.pack(side=tk.RIGHT)
        
        input_select_frame.pack(fill=tk.X)
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 输出文件/文件夹
        output_frame = tk.Frame(
            self.file_card.content_frame,
            bg=ModernTheme.COLORS['bg_secondary']
        )
        
        tk.Label(
            output_frame,
            text="输出路径:",
            font=ModernTheme.FONTS['default'],
            bg=ModernTheme.COLORS['bg_secondary'],
            fg=ModernTheme.COLORS['text_primary']
        ).pack(anchor=tk.W, pady=(0, 5))
        
        output_select_frame = tk.Frame(
            output_frame,
            bg=ModernTheme.COLORS['bg_secondary']
        )
        
        self.output_var = tk.StringVar()
        self.output_entry = tk.Entry(
            output_select_frame,
            textvariable=self.output_var,
            font=ModernTheme.FONTS['default'],
            width=50
        )
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.output_button = tk.Button(
            output_select_frame,
            text="浏览...",
            font=ModernTheme.FONTS['default'],
            bg=ModernTheme.COLORS['info'],
            fg='white',
            relief='flat',
            padx=20,
            command=self.select_output
        )
        self.output_button.pack(side=tk.RIGHT)
        
        output_select_frame.pack(fill=tk.X)
        output_frame.pack(fill=tk.X)
        
        self.file_card.pack(fill=tk.X, padx=15, pady=15)
    
    def create_control_panel(self):
        """创建控制面板"""
        self.control_card = ModernCard(self.main_frame, "处理控制")
        
        # 进度条
        progress_frame = tk.Frame(
            self.control_card.content_frame,
            bg=ModernTheme.COLORS['bg_secondary']
        )
        
        tk.Label(
            progress_frame,
            text="处理进度:",
            font=ModernTheme.FONTS['default'],
            bg=ModernTheme.COLORS['bg_secondary'],
            fg=ModernTheme.COLORS['text_primary']
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.progress_bar = AnimatedProgressBar(progress_frame)
        self.progress_bar.pack(fill=tk.X, pady=(0, 15))
        
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 控制按钮
        button_frame = tk.Frame(
            self.control_card.content_frame,
            bg=ModernTheme.COLORS['bg_secondary']
        )
        
        self.process_button = tk.Button(
            button_frame,
            text="🚀 开始处理",
            font=ModernTheme.FONTS['heading'],
            bg=ModernTheme.COLORS['primary'],
            fg='white',
            relief='flat',
            padx=30,
            pady=10,
            command=self.start_processing
        )
        self.process_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = tk.Button(
            button_frame,
            text="⏹️ 停止处理",
            font=ModernTheme.FONTS['default'],
            bg=ModernTheme.COLORS['danger'],
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            state='disabled',
            command=self.stop_processing
        )
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = tk.Button(
            button_frame,
            text="🗑️ 清空结果",
            font=ModernTheme.FONTS['default'],
            bg=ModernTheme.COLORS['warning'],
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            command=self.clear_results
        )
        self.clear_button.pack(side=tk.LEFT)
        
        button_frame.pack()
        
        self.control_card.pack(fill=tk.X, padx=15, pady=(0, 15))
    
    def create_result_display(self):
        """创建结果显示区域"""
        self.result_card = ModernCard(self.main_frame, "处理结果")
        
        # 结果文本区域
        self.result_text = scrolledtext.ScrolledText(
            self.result_card.content_frame,
            font=ModernTheme.FONTS['code'],
            bg='white',
            fg=ModernTheme.COLORS['text_primary'],
            relief='flat',
            bd=1,
            height=15
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 结果控制按钮
        result_button_frame = tk.Frame(
            self.result_card.content_frame,
            bg=ModernTheme.COLORS['bg_secondary']
        )
        
        self.save_button = tk.Button(
            result_button_frame,
            text="💾 保存结果",
            font=ModernTheme.FONTS['default'],
            bg=ModernTheme.COLORS['success'],
            fg='white',
            relief='flat',
            padx=20,
            command=self.save_results
        )
        self.save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.export_button = tk.Button(
            result_button_frame,
            text="📤 导出报告",
            font=ModernTheme.FONTS['default'],
            bg=ModernTheme.COLORS['info'],
            fg='white',
            relief='flat',
            padx=20,
            command=self.export_report
        )
        self.export_button.pack(side=tk.LEFT)
        
        result_button_frame.pack()
        
        self.result_card.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    
    def create_footer(self):
        """创建底部状态栏"""
        self.footer_frame = tk.Frame(
            self.main_container,
            bg=ModernTheme.COLORS['dark'],
            height=30
        )
        self.footer_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            self.footer_frame,
            text="准备就绪",
            font=ModernTheme.FONTS['small'],
            fg='white',
            bg=ModernTheme.COLORS['dark']
        )
        self.status_label.pack(side=tk.LEFT, padx=15, pady=5)
        
        # 时间显示
        self.time_label = tk.Label(
            self.footer_frame,
            text="",
            font=ModernTheme.FONTS['small'],
            fg='white',
            bg=ModernTheme.COLORS['dark']
        )
        self.time_label.pack(side=tk.RIGHT, padx=15, pady=5)
        
        self.update_time()
    
    def setup_layout(self):
        """设置布局"""
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        self.header_frame.pack(fill=tk.X)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左右布局
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
    
    def update_time(self):
        """更新时间显示"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def on_function_change(self):
        """功能选择改变时的回调"""
        function = self.function_var.get()
        if function == "single":
            self.input_button.config(text="选择文件", command=self.select_input_file)
            self.output_button.config(text="选择文件", command=self.select_output_file)
        else:
            self.input_button.config(text="选择文件夹", command=self.select_input_folder)
            self.output_button.config(text="选择文件夹", command=self.select_output_folder)
    
    def select_input(self):
        """选择输入"""
        if self.function_var.get() == "single":
            self.select_input_file()
        else:
            self.select_input_folder()
    
    def select_output(self):
        """选择输出"""
        if self.function_var.get() == "single":
            self.select_output_file()
        else:
            self.select_output_folder()
    
    def select_input_file(self):
        """选择输入文件"""
        file_path = filedialog.askopenfilename(
            title="选择输入文件",
            filetypes=[
                ("文本文件", "*.txt"),
                ("CSV文件", "*.csv"),
                ("JSON文件", "*.json"),
                ("PDF文件", "*.pdf"),
                ("Excel文件", "*.xlsx;*.xls"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.input_var.set(file_path)
            if not self.output_var.get():
                output_path = Path(file_path).with_suffix('.processed.txt')
                self.output_var.set(str(output_path))
    
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
            self.output_var.set(file_path)
    
    def select_input_folder(self):
        """选择输入文件夹"""
        folder_path = filedialog.askdirectory(title="选择输入文件夹")
        if folder_path:
            self.input_var.set(folder_path)
            if not self.output_var.get():
                output_path = Path(folder_path).parent / f"{Path(folder_path).name}_processed"
                self.output_var.set(str(output_path))
    
    def select_output_folder(self):
        """选择输出文件夹"""
        folder_path = filedialog.askdirectory(title="选择输出文件夹")
        if folder_path:
            self.output_var.set(folder_path)
    
    def start_processing(self):
        """开始处理"""
        input_path = self.input_var.get().strip()
        output_path = self.output_var.get().strip()
        
        if not input_path or not output_path:
            messagebox.showerror("错误", "请选择输入和输出路径")
            return
        
        if not Path(input_path).exists():
            messagebox.showerror("错误", "输入路径不存在")
            return
        
        if self.processing:
            messagebox.showwarning("警告", "正在处理中，请等待完成")
            return
        
        # 开始处理
        self.processing = True
        self.start_time = datetime.now()
        
        # 更新UI状态
        self.process_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.update_status("正在处理...")
        
        # 启动处理线程
        function_type = self.function_var.get()
        format_type = self.format_var.get()
        
        thread = threading.Thread(
            target=self.process_worker,
            args=(function_type, input_path, output_path, format_type)
        )
        thread.daemon = True
        thread.start()
    
    def stop_processing(self):
        """停止处理"""
        if self.processing:
            # 这里可以实现停止逻辑
            self.processing = False
            self.update_status("已停止")
            self.reset_ui_state()
    
    def process_worker(self, function_type, input_path, output_path, format_type):
        """处理工作线程"""
        try:
            if function_type == "single":
                success = self.processor.process_single_file(
                    input_path, output_path, format_type
                )
                
                if success:
                    try:
                        with open(output_path, 'r', encoding='utf-8') as f:
                            result_content = f.read()
                        
                        self.result_queue.put({
                            'type': 'success',
                            'message': f"文件处理完成: {input_path}",
                            'content': result_content
                        })
                    except Exception as e:
                        self.result_queue.put({
                            'type': 'success',
                            'message': f"文件处理完成: {input_path}",
                            'content': f"处理成功，但无法读取结果文件: {e}"
                        })
                else:
                    self.result_queue.put({
                        'type': 'error',
                        'message': f"文件处理失败: {input_path}"
                    })
            
            else:  # batch
                result = self.processor.process_batch(
                    input_path, output_path, format_type
                )
                
                self.result_queue.put({
                    'type': 'batch_complete',
                    'result': result,
                    'message': f"批量处理完成: 成功 {result.get('processed', 0)} 个，失败 {result.get('errors', 0)} 个"
                })
        
        except Exception as e:
            self.result_queue.put({
                'type': 'error',
                'message': f"处理过程中发生错误: {str(e)}"
            })
        
        finally:
            self.result_queue.put({'type': 'complete'})
    
    def check_queue(self):
        """检查结果队列"""
        try:
            while True:
                result = self.result_queue.get_nowait()
                self.handle_result(result)
        except queue.Empty:
            pass
        
        self.root.after(100, self.check_queue)
    
    def handle_result(self, result):
        """处理结果"""
        result_type = result['type']
        
        if result_type == 'success':
            self.append_result(f"✅ {result['message']}\n")
            if 'content' in result:
                self.append_result(f"处理结果:\n{'-'*50}\n{result['content']}\n{'-'*50}\n\n")
            self.update_stats('processed', 1)
            
        elif result_type == 'batch_complete':
            batch_result = result['result']
            self.append_result(f"✅ {result['message']}\n")
            self.append_result(f"详细统计: 总计 {batch_result.get('total', 0)} 个文件\n\n")
            self.progress_bar.set_value(100, "完成")
            
        elif result_type == 'error':
            self.append_result(f"❌ {result['message']}\n\n")
            self.update_stats('failed', 1)
            
        elif result_type == 'complete':
            self.processing = False
            self.update_status("处理完成")
            self.reset_ui_state()
            
            # 计算处理时间
            if self.start_time:
                elapsed = datetime.now() - self.start_time
                self.update_stats('time', f"{elapsed.seconds}秒")
    
    def update_status(self, message):
        """更新状态"""
        self.status_label.config(text=message)
        self.stats_labels['status'].config(text=message)
    
    def update_stats(self, key, value):
        """更新统计信息"""
        if key in ['processed', 'failed']:
            current = int(self.stats_labels[key].cget('text'))
            self.stats_labels[key].config(text=str(current + value))
        else:
            self.stats_labels[key].config(text=str(value))
    
    def reset_ui_state(self):
        """重置UI状态"""
        self.process_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.progress_bar.set_value(0, "准备就绪")
    
    def append_result(self, text):
        """添加结果"""
        self.result_text.insert(tk.END, text)
        self.result_text.see(tk.END)
    
    def clear_results(self):
        """清空结果"""
        self.result_text.delete(1.0, tk.END)
        # 重置统计
        self.stats_labels['processed'].config(text="0")
        self.stats_labels['failed'].config(text="0")
        self.stats_labels['time'].config(text="0")
    
    def save_results(self):
        """保存结果"""
        content = self.result_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("警告", "没有可保存的结果")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="保存处理结果",
            defaultextension=".txt",
            filetypes=[
                ("文本文件", "*.txt"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("成功", f"结果已保存到: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {e}")
    
    def export_report(self):
        """导出处理报告"""
        report_data = {
            "处理时间": datetime.now().isoformat(),
            "处理模式": "单文件处理" if self.function_var.get() == "single" else "批量处理",
            "输出格式": self.format_var.get(),
            "输入路径": self.input_var.get(),
            "输出路径": self.output_var.get(),
            "统计信息": {
                "已处理文件": self.stats_labels['processed'].cget('text'),
                "处理失败": self.stats_labels['failed'].cget('text'),
                "处理时间": self.stats_labels['time'].cget('text'),
            },
            "处理结果": self.result_text.get(1.0, tk.END).strip()
        }
        
        file_path = filedialog.asksaveasfilename(
            title="导出处理报告",
            defaultextension=".json",
            filetypes=[
                ("JSON文件", "*.json"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(report_data, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("成功", f"报告已导出到: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {e}")
    
    def on_closing(self):
        """关闭程序时的处理"""
        if self.processing:
            if messagebox.askokcancel("退出", "正在处理中，确定要退出吗？"):
                self.processing = False
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """运行GUI"""
        self.root.mainloop()

def main():
    """主函数"""
    try:
        app = PremiumFileProcessorGUI()
        app.run()
    except Exception as e:
        print(f"GUI启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()