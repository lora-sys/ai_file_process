#!/usr/bin/env python3
"""
智能文件处理工具 - 高级GUI界面
支持拖拽、实时预览、自定义主题等功能
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinterdnd2 import TkinterDnD, DND_FILES
import threading
import queue
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any, List
import webbrowser
import os

from improved_file_handler import file_handler
from improved_data_processor import text_processor, result_formatter
from improved_main import FileProcessor
from config import config

class ModernTheme:
    """现代主题配置"""
    
    # 颜色配置
    COLORS = {
        'primary': '#2196F3',
        'primary_dark': '#1976D2',
        'secondary': '#FFC107',
        'success': '#4CAF50',
        'warning': '#FF9800',
        'error': '#F44336',
        'background': '#FAFAFA',
        'surface': '#FFFFFF',
        'text_primary': '#212121',
        'text_secondary': '#757575',
        'border': '#E0E0E0'
    }
    
    # 字体配置
    FONTS = {
        'title': ('Segoe UI', 18, 'bold'),
        'subtitle': ('Segoe UI', 12, 'bold'),
        'body': ('Segoe UI', 10),
        'mono': ('Consolas', 9),
        'button': ('Segoe UI', 10, 'bold')
    }

class DragDropFrame(tk.Frame):
    """支持拖拽的框架"""
    
    def __init__(self, parent, callback=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.callback = callback
        self.configure(relief='solid', borderwidth=2)
        self.configure(bg=ModernTheme.COLORS['surface'])
        
        # 拖拽标签
        self.label = tk.Label(
            self,
            text="🗂️ 拖拽文件到此处\n或点击选择文件",
            font=ModernTheme.FONTS['body'],
            bg=ModernTheme.COLORS['surface'],
            fg=ModernTheme.COLORS['text_secondary'],
            justify='center'
        )
        self.label.pack(expand=True, fill='both', padx=20, pady=20)
        
        # 绑定拖拽事件
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_drop)
        
        # 绑定点击事件
        self.label.bind('<Button-1>', self.on_click)
        self.bind('<Button-1>', self.on_click)
        
        # 绑定鼠标悬停事件
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.label.bind('<Enter>', self.on_enter)
        self.label.bind('<Leave>', self.on_leave)
    
    def on_drop(self, event):
        """处理拖拽事件"""
        files = event.data.split()
        if files and self.callback:
            # 只取第一个文件/文件夹
            self.callback(files[0])
            self.update_display(files[0])
    
    def on_click(self, event):
        """处理点击事件"""
        if self.callback:
            file_path = filedialog.askopenfilename(
                title="选择文件",
                filetypes=[
                    ("所有支持格式", "*.txt;*.csv;*.json;*.pdf;*.xlsx"),
                    ("文本文件", "*.txt"),
                    ("CSV文件", "*.csv"),
                    ("JSON文件", "*.json"),
                    ("PDF文件", "*.pdf"),
                    ("Excel文件", "*.xlsx"),
                    ("所有文件", "*.*")
                ]
            )
            if file_path:
                self.callback(file_path)
                self.update_display(file_path)
    
    def on_enter(self, event):
        """鼠标悬停"""
        self.configure(bg=ModernTheme.COLORS['primary'], borderwidth=3)
        self.label.configure(bg=ModernTheme.COLORS['primary'], fg='white')
    
    def on_leave(self, event):
        """鼠标离开"""
        self.configure(bg=ModernTheme.COLORS['surface'], borderwidth=2)
        self.label.configure(bg=ModernTheme.COLORS['surface'], fg=ModernTheme.COLORS['text_secondary'])
    
    def update_display(self, file_path):
        """更新显示内容"""
        path = Path(file_path)
        display_text = f"📁 {path.name}\n📍 {str(path.parent)}"
        self.label.configure(text=display_text)

class AdvancedGUI(TkinterDnD.Tk):
    """高级GUI主类"""
    
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_theme()
        self.setup_variables()
        self.setup_widgets()
        self.setup_layout()
        self.file_processor = FileProcessor()
        self.processing_queue = queue.Queue()
        self.is_processing = False
        self.preview_cache = {}
        
    def setup_window(self):
        """设置主窗口"""
        self.title("🤖 智能文件处理工具 v2.0 - 高级版")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        self.configure(bg=ModernTheme.COLORS['background'])
        
        # 设置图标
        try:
            self.iconbitmap("icon.ico")
        except:
            pass
        
        # 居中显示
        self.center_window()
    
    def center_window(self):
        """窗口居中显示"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_theme(self):
        """设置主题"""
        self.style = ttk.Style()
        
        # 尝试使用更好的主题
        try:
            self.style.theme_use('clam')
        except:
            pass
        
        # 配置自定义样式
        self.style.configure('Title.TLabel', 
                           font=ModernTheme.FONTS['title'],
                           foreground=ModernTheme.COLORS['primary'])
        
        self.style.configure('Subtitle.TLabel',
                           font=ModernTheme.FONTS['subtitle'],
                           foreground=ModernTheme.COLORS['text_primary'])
        
        self.style.configure('Primary.TButton',
                           font=ModernTheme.FONTS['button'],
                           foreground='white')
        
        self.style.map('Primary.TButton',
                      background=[('active', ModernTheme.COLORS['primary_dark']),
                                ('!active', ModernTheme.COLORS['primary'])])
        
        self.style.configure('Success.TLabel',
                           foreground=ModernTheme.COLORS['success'])
        
        self.style.configure('Warning.TLabel',
                           foreground=ModernTheme.COLORS['warning'])
        
        self.style.configure('Error.TLabel',
                           foreground=ModernTheme.COLORS['error'])
    
    def setup_variables(self):
        """设置变量"""
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.output_format = tk.StringVar(value="summary")
        self.processing_mode = tk.StringVar(value="single")
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="就绪")
        self.preview_enabled = tk.BooleanVar(value=True)
        self.auto_save = tk.BooleanVar(value=False)
        
    def setup_widgets(self):
        """创建控件"""
        # 创建主容器
        self.main_container = tk.Frame(self, bg=ModernTheme.COLORS['background'])
        
        # 创建侧边栏
        self.create_sidebar()
        
        # 创建主内容区域
        self.create_main_content()
        
        # 创建状态栏
        self.create_status_bar()
    
    def create_sidebar(self):
        """创建侧边栏"""
        self.sidebar = tk.Frame(
            self.main_container,
            bg=ModernTheme.COLORS['surface'],
            width=300,
            relief='solid',
            borderwidth=1
        )
        self.sidebar.pack_propagate(False)
        
        # 标题
        title_frame = tk.Frame(self.sidebar, bg=ModernTheme.COLORS['primary'], height=60)
        title_frame.pack(fill='x', padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="🤖 智能处理",
            font=ModernTheme.FONTS['title'],
            bg=ModernTheme.COLORS['primary'],
            fg='white'
        ).pack(expand=True)
        
        # 控制面板
        control_frame = tk.Frame(self.sidebar, bg=ModernTheme.COLORS['surface'])
        control_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # 模式选择
        self.create_mode_selection(control_frame)
        
        # 文件选择
        self.create_file_selection(control_frame)
        
        # 输出选项
        self.create_output_options(control_frame)
        
        # 高级选项
        self.create_advanced_options(control_frame)
        
        # 操作按钮
        self.create_action_buttons(control_frame)
    
    def create_mode_selection(self, parent):
        """创建模式选择"""
        mode_frame = tk.LabelFrame(
            parent,
            text="处理模式",
            font=ModernTheme.FONTS['subtitle'],
            bg=ModernTheme.COLORS['surface'],
            fg=ModernTheme.COLORS['text_primary']
        )
        mode_frame.pack(fill='x', pady=(0, 15))
        
        tk.Radiobutton(
            mode_frame,
            text="📄 单文件处理",
            variable=self.processing_mode,
            value="single",
            command=self.on_mode_change,
            font=ModernTheme.FONTS['body'],
            bg=ModernTheme.COLORS['surface'],
            fg=ModernTheme.COLORS['text_primary'],
            selectcolor=ModernTheme.COLORS['primary']
        ).pack(anchor='w', padx=10, pady=5)
        
        tk.Radiobutton(
            mode_frame,
            text="📁 批量处理",
            variable=self.processing_mode,
            value="batch",
            command=self.on_mode_change,
            font=ModernTheme.FONTS['body'],
            bg=ModernTheme.COLORS['surface'],
            fg=ModernTheme.COLORS['text_primary'],
            selectcolor=ModernTheme.COLORS['primary']
        ).pack(anchor='w', padx=10, pady=5)
    
    def create_file_selection(self, parent):
        """创建文件选择区域"""
        file_frame = tk.LabelFrame(
            parent,
            text="文件选择",
            font=ModernTheme.FONTS['subtitle'],
            bg=ModernTheme.COLORS['surface'],
            fg=ModernTheme.COLORS['text_primary']
        )
        file_frame.pack(fill='x', pady=(0, 15))
        
        # 输入文件拖拽区域
        tk.Label(
            file_frame,
            text="输入文件:",
            font=ModernTheme.FONTS['body'],
            bg=ModernTheme.COLORS['surface'],
            fg=ModernTheme.COLORS['text_primary']
        ).pack(anchor='w', padx=10, pady=(10, 5))
        
        self.input_drag_frame = DragDropFrame(
            file_frame,
            callback=self.on_input_selected,
            height=80
        )
        self.input_drag_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # 输出路径
        tk.Label(
            file_frame,
            text="输出路径:",
            font=ModernTheme.FONTS['body'],
            bg=ModernTheme.COLORS['surface'],
            fg=ModernTheme.COLORS['text_primary']
        ).pack(anchor='w', padx=10, pady=(10, 5))
        
        output_entry_frame = tk.Frame(file_frame, bg=ModernTheme.COLORS['surface'])
        output_entry_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.output_entry = tk.Entry(
            output_entry_frame,
            textvariable=self.output_path,
            font=ModernTheme.FONTS['body'],
            relief='solid',
            borderwidth=1
        )
        self.output_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        tk.Button(
            output_entry_frame,
            text="📁",
            command=self.browse_output,
            relief='solid',
            borderwidth=1,
            bg=ModernTheme.COLORS['primary'],
            fg='white',
            font=ModernTheme.FONTS['body']
        ).pack(side='right')
    
    def create_output_options(self, parent):
        """创建输出选项"""
        output_frame = tk.LabelFrame(
            parent,
            text="输出选项",
            font=ModernTheme.FONTS['subtitle'],
            bg=ModernTheme.COLORS['surface'],
            fg=ModernTheme.COLORS['text_primary']
        )
        output_frame.pack(fill='x', pady=(0, 15))
        
        format_options = [
            ("📋 摘要格式", "summary"),
            ("📄 JSON格式", "json"),
            ("📝 纯文本", "text")
        ]
        
        for text, value in format_options:
            tk.Radiobutton(
                output_frame,
                text=text,
                variable=self.output_format,
                value=value,
                font=ModernTheme.FONTS['body'],
                bg=ModernTheme.COLORS['surface'],
                fg=ModernTheme.COLORS['text_primary'],
                selectcolor=ModernTheme.COLORS['secondary']
            ).pack(anchor='w', padx=10, pady=2)
    
    def create_advanced_options(self, parent):
        """创建高级选项"""
        advanced_frame = tk.LabelFrame(
            parent,
            text="高级选项",
            font=ModernTheme.FONTS['subtitle'],
            bg=ModernTheme.COLORS['surface'],
            fg=ModernTheme.COLORS['text_primary']
        )
        advanced_frame.pack(fill='x', pady=(0, 15))
        
        tk.Checkbutton(
            advanced_frame,
            text="🔍 启用实时预览",
            variable=self.preview_enabled,
            font=ModernTheme.FONTS['body'],
            bg=ModernTheme.COLORS['surface'],
            fg=ModernTheme.COLORS['text_primary'],
            selectcolor=ModernTheme.COLORS['success']
        ).pack(anchor='w', padx=10, pady=2)
        
        tk.Checkbutton(
            advanced_frame,
            text="💾 自动保存结果",
            variable=self.auto_save,
            font=ModernTheme.FONTS['body'],
            bg=ModernTheme.COLORS['surface'],
            fg=ModernTheme.COLORS['text_primary'],
            selectcolor=ModernTheme.COLORS['success']
        ).pack(anchor='w', padx=10, pady=2)
    
    def create_action_buttons(self, parent):
        """创建操作按钮"""
        button_frame = tk.Frame(parent, bg=ModernTheme.COLORS['surface'])
        button_frame.pack(fill='x', pady=(20, 0))
        
        # 主要按钮
        self.process_btn = tk.Button(
            button_frame,
            text="🚀 开始处理",
            command=self.start_processing,
            font=ModernTheme.FONTS['button'],
            bg=ModernTheme.COLORS['primary'],
            fg='white',
            relief='flat',
            borderwidth=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.process_btn.pack(fill='x', pady=(0, 10))
        
        # 次要按钮
        button_row = tk.Frame(button_frame, bg=ModernTheme.COLORS['surface'])
        button_row.pack(fill='x')
        
        self.stop_btn = tk.Button(
            button_row,
            text="⏹ 停止",
            command=self.stop_processing,
            font=ModernTheme.FONTS['body'],
            bg=ModernTheme.COLORS['warning'],
            fg='white',
            relief='flat',
            state='disabled'
        )
        self.stop_btn.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        self.clear_btn = tk.Button(
            button_row,
            text="🗑 清除",
            command=self.clear_all,
            font=ModernTheme.FONTS['body'],
            bg=ModernTheme.COLORS['error'],
            fg='white',
            relief='flat'
        )
        self.clear_btn.pack(side='right', fill='x', expand=True, padx=(5, 0))
        
        # 进度条
        self.progress_bar = ttk.Progressbar(
            button_frame,
            variable=self.progress_var,
            mode='determinate',
            style='Primary.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(fill='x', pady=(15, 0))
    
    def create_main_content(self):
        """创建主内容区域"""
        self.content_area = tk.Frame(
            self.main_container,
            bg=ModernTheme.COLORS['background']
        )
        
        # 创建标签页
        self.notebook = ttk.Notebook(self.content_area)
        
        # 结果标签页
        self.create_result_tab()
        
        # 预览标签页
        self.create_preview_tab()
        
        # 配置标签页
        self.create_config_tab()
        
        # 日志标签页
        self.create_log_tab()
        
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
    
    def create_result_tab(self):
        """创建结果标签页"""
        self.result_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.result_frame, text="📊 处理结果")
        
        # 工具栏
        toolbar = tk.Frame(self.result_frame, bg=ModernTheme.COLORS['surface'], height=40)
        toolbar.pack(fill='x', padx=5, pady=5)
        toolbar.pack_propagate(False)
        
        tk.Button(
            toolbar,
            text="💾 保存",
            command=self.save_result,
            font=ModernTheme.FONTS['body'],
            relief='flat',
            bg=ModernTheme.COLORS['success'],
            fg='white'
        ).pack(side='left', padx=5, pady=5)
        
        tk.Button(
            toolbar,
            text="📋 复制",
            command=self.copy_result,
            font=ModernTheme.FONTS['body'],
            relief='flat',
            bg=ModernTheme.COLORS['secondary'],
            fg='white'
        ).pack(side='left', padx=5, pady=5)
        
        tk.Button(
            toolbar,
            text="🗑 清除",
            command=self.clear_result,
            font=ModernTheme.FONTS['body'],
            relief='flat',
            bg=ModernTheme.COLORS['error'],
            fg='white'
        ).pack(side='left', padx=5, pady=5)
        
        # 结果显示区域
        self.result_text = scrolledtext.ScrolledText(
            self.result_frame,
            font=ModernTheme.FONTS['mono'],
            wrap=tk.WORD,
            relief='solid',
            borderwidth=1
        )
        self.result_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_preview_tab(self):
        """创建预览标签页"""
        self.preview_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.preview_frame, text="👁 预览")
        
        # 预览内容
        self.preview_text = scrolledtext.ScrolledText(
            self.preview_frame,
            font=ModernTheme.FONTS['mono'],
            wrap=tk.WORD,
            relief='solid',
            borderwidth=1,
            state='disabled'
        )
        self.preview_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_config_tab(self):
        """创建配置标签页"""
        self.config_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.config_frame, text="⚙️ 配置")
        
        # 配置工具栏
        config_toolbar = tk.Frame(self.config_frame, bg=ModernTheme.COLORS['surface'], height=40)
        config_toolbar.pack(fill='x', padx=5, pady=5)
        config_toolbar.pack_propagate(False)
        
        tk.Button(
            config_toolbar,
            text="🔄 刷新",
            command=self.refresh_config,
            font=ModernTheme.FONTS['body'],
            relief='flat',
            bg=ModernTheme.COLORS['primary'],
            fg='white'
        ).pack(side='left', padx=5, pady=5)
        
        tk.Button(
            config_toolbar,
            text="📁 打开文件",
            command=self.open_config_file,
            font=ModernTheme.FONTS['body'],
            relief='flat',
            bg=ModernTheme.COLORS['secondary'],
            fg='white'
        ).pack(side='left', padx=5, pady=5)
        
        tk.Button(
            config_toolbar,
            text="🔧 重置",
            command=self.reset_config,
            font=ModernTheme.FONTS['body'],
            relief='flat',
            bg=ModernTheme.COLORS['warning'],
            fg='white'
        ).pack(side='left', padx=5, pady=5)
        
        # 配置显示
        self.config_text = scrolledtext.ScrolledText(
            self.config_frame,
            font=ModernTheme.FONTS['mono'],
            wrap=tk.WORD,
            relief='solid',
            borderwidth=1
        )
        self.config_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # 加载配置
        self.refresh_config()
    
    def create_log_tab(self):
        """创建日志标签页"""
        self.log_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.log_frame, text="📋 日志")
        
        # 日志显示
        self.log_text = scrolledtext.ScrolledText(
            self.log_frame,
            font=ModernTheme.FONTS['mono'],
            wrap=tk.WORD,
            relief='solid',
            borderwidth=1,
            state='disabled'
        )
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = tk.Frame(
            self.main_container,
            bg=ModernTheme.COLORS['surface'],
            height=30,
            relief='solid',
            borderwidth=1
        )
        self.status_bar.pack(fill='x', side='bottom')
        self.status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(
            self.status_bar,
            textvariable=self.status_var,
            font=ModernTheme.FONTS['body'],
            bg=ModernTheme.COLORS['surface'],
            fg=ModernTheme.COLORS['text_primary'],
            anchor='w'
        )
        self.status_label.pack(side='left', fill='x', expand=True, padx=10)
        
        # 时间标签
        self.time_label = tk.Label(
            self.status_bar,
            text="",
            font=ModernTheme.FONTS['body'],
            bg=ModernTheme.COLORS['surface'],
            fg=ModernTheme.COLORS['text_secondary'],
            anchor='e'
        )
        self.time_label.pack(side='right', padx=10)
        
        # 更新时间
        self.update_time()
    
    def setup_layout(self):
        """设置布局"""
        self.main_container.pack(fill='both', expand=True)
        self.sidebar.pack(side='left', fill='y')
        self.content_area.pack(side='right', fill='both', expand=True)
    
    def update_time(self):
        """更新时间显示"""
        import datetime
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.after(1000, self.update_time)
    
    def on_mode_change(self):
        """处理模式改变事件"""
        # 更新界面元素
        pass
    
    def on_input_selected(self, file_path):
        """处理输入文件选择"""
        self.input_path.set(file_path)
        self.log_message(f"选择输入文件: {file_path}")
        
        # 自动设置输出路径
        input_path = Path(file_path)
        if input_path.is_file():
            output_path = input_path.parent / f"{input_path.stem}_processed{input_path.suffix}"
            self.output_path.set(str(output_path))
        
        # 实时预览
        if self.preview_enabled.get():
            self.update_preview(file_path)
    
    def update_preview(self, file_path):
        """更新预览"""
        if file_path in self.preview_cache:
            content = self.preview_cache[file_path]
        else:
            try:
                content = file_handler.read_file(file_path)
                if content:
                    # 只显示前1000个字符
                    content = content[:1000] + "..." if len(content) > 1000 else content
                    self.preview_cache[file_path] = content
                else:
                    content = "无法读取文件内容"
            except Exception as e:
                content = f"预览失败: {e}"
        
        self.preview_text.config(state='normal')
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, content)
        self.preview_text.config(state='disabled')
    
    def browse_output(self):
        """浏览输出路径"""
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
    
    def start_processing(self):
        """开始处理"""
        if not self.input_path.get() or not self.output_path.get():
            messagebox.showerror("错误", "请选择输入和输出路径！")
            return
        
        input_path = Path(self.input_path.get())
        if not input_path.exists():
            messagebox.showerror("错误", "输入路径不存在！")
            return
        
        # 设置UI状态
        self.is_processing = True
        self.process_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.progress_var.set(0)
        self.clear_result()
        
        # 记录日志
        self.log_message("开始处理...")
        
        # 在新线程中执行处理
        thread = threading.Thread(target=self._process_files, daemon=True)
        thread.start()
        
        # 开始监控处理进度
        self.monitor_processing()
    
    def _process_files(self):
        """在后台线程中处理文件"""
        try:
            input_path = self.input_path.get()
            output_path = self.output_path.get()
            output_format = self.output_format.get()
            mode = self.processing_mode.get()
            
            self.processing_queue.put(("status", "正在处理..."))
            
            if mode == "single":
                # 单文件处理
                self.processing_queue.put(("progress", 10))
                success = self.file_processor.process_single_file(
                    input_path, output_path, output_format
                )
                
                if success:
                    self.processing_queue.put(("progress", 100))
                    self.processing_queue.put(("status", "处理完成"))
                    
                    # 读取结果
                    try:
                        with open(output_path, 'r', encoding='utf-8') as f:
                            result = f.read()
                        self.processing_queue.put(("result", result))
                    except Exception as e:
                        self.processing_queue.put(("error", f"读取结果失败: {e}"))
                else:
                    self.processing_queue.put(("error", "处理失败"))
            else:
                # 批量处理
                self.processing_queue.put(("progress", 10))
                result = self.file_processor.process_batch(
                    input_path, output_path, output_format
                )
                
                self.processing_queue.put(("progress", 100))
                
                if result.get("success"):
                    processed = result.get("processed", 0)
                    errors = result.get("errors", 0)
                    total = result.get("total", 0)
                    
                    summary = f"🎉 批量处理完成！\n\n"
                    summary += f"📊 处理统计:\n"
                    summary += f"  • 总文件数: {total}\n"
                    summary += f"  • 成功处理: {processed}\n"
                    summary += f"  • 处理失败: {errors}\n"
                    summary += f"  • 成功率: {(processed/total*100):.1f}%" if total > 0 else "0%"
                    
                    self.processing_queue.put(("result", summary))
                    self.processing_queue.put(("status", "批量处理完成"))
                else:
                    self.processing_queue.put(("error", "批量处理失败"))
        
        except Exception as e:
            self.processing_queue.put(("error", f"处理过程中发生错误: {e}"))
        
        finally:
            self.processing_queue.put(("finished", None))
    
    def monitor_processing(self):
        """监控处理进度"""
        try:
            while True:
                try:
                    message_type, data = self.processing_queue.get_nowait()
                    
                    if message_type == "status":
                        self.status_var.set(data)
                    elif message_type == "progress":
                        self.progress_var.set(data)
                    elif message_type == "result":
                        self.result_text.delete(1.0, tk.END)
                        self.result_text.insert(tk.END, data)
                        self.log_message("处理完成")
                        
                        # 自动保存
                        if self.auto_save.get():
                            self.save_result()
                        
                    elif message_type == "error":
                        self.result_text.delete(1.0, tk.END)
                        self.result_text.insert(tk.END, f"❌ 错误: {data}")
                        self.log_message(f"错误: {data}", "ERROR")
                        messagebox.showerror("处理错误", data)
                    elif message_type == "finished":
                        self.stop_processing()
                        break
                        
                except queue.Empty:
                    break
        except:
            pass
        
        if self.is_processing:
            self.after(100, self.monitor_processing)
    
    def stop_processing(self):
        """停止处理"""
        self.is_processing = False
        self.process_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.progress_var.set(0)
        self.status_var.set("就绪")
        self.log_message("处理已停止")
    
    def clear_all(self):
        """清除所有内容"""
        self.input_path.set("")
        self.output_path.set("")
        self.clear_result()
        self.progress_var.set(0)
        self.status_var.set("就绪")
        
        # 清除预览
        self.preview_text.config(state='normal')
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.config(state='disabled')
        
        # 更新拖拽区域
        self.input_drag_frame.label.configure(text="🗂️ 拖拽文件到此处\n或点击选择文件")
        
        self.log_message("已清除所有内容")
    
    def clear_result(self):
        """清除结果"""
        self.result_text.delete(1.0, tk.END)
    
    def save_result(self):
        """保存结果"""
        content = self.result_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("警告", "没有结果可保存！")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="保存结果",
            defaultextension=".txt",
            filetypes=[
                ("文本文件", "*.txt"),
                ("JSON文件", "*.json"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("成功", "结果已保存！")
                self.log_message(f"结果已保存到: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {e}")
                self.log_message(f"保存失败: {e}", "ERROR")
    
    def copy_result(self):
        """复制结果到剪贴板"""
        content = self.result_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("警告", "没有结果可复制！")
            return
        
        self.clipboard_clear()
        self.clipboard_append(content)
        messagebox.showinfo("成功", "结果已复制到剪贴板！")
        self.log_message("结果已复制到剪贴板")
    
    def refresh_config(self):
        """刷新配置显示"""
        try:
            config_dict = config.config
            config_json = json.dumps(config_dict, indent=2, ensure_ascii=False)
            
            self.config_text.delete(1.0, tk.END)
            self.config_text.insert(tk.END, config_json)
        except Exception as e:
            self.config_text.delete(1.0, tk.END)
            self.config_text.insert(tk.END, f"配置加载失败: {e}")
    
    def open_config_file(self):
        """打开配置文件"""
        config_file = Path("config.json")
        if config_file.exists():
            try:
                import subprocess
                import sys
                
                if sys.platform == "win32":
                    subprocess.run(["notepad", str(config_file)])
                elif sys.platform == "darwin":
                    subprocess.run(["open", str(config_file)])
                else:
                    subprocess.run(["xdg-open", str(config_file)])
            except Exception as e:
                messagebox.showerror("错误", f"无法打开配置文件: {e}")
        else:
            try:
                config.save()
                messagebox.showinfo("信息", "已创建默认配置文件 config.json")
                self.refresh_config()
            except Exception as e:
                messagebox.showerror("错误", f"创建配置文件失败: {e}")
    
    def reset_config(self):
        """重置配置为默认值"""
        if messagebox.askyesno("确认", "确定要重置配置为默认值吗？"):
            try:
                config.config = config.DEFAULT_CONFIG.copy()
                config.save()
                self.refresh_config()
                messagebox.showinfo("成功", "配置已重置为默认值！")
                self.log_message("配置已重置为默认值")
            except Exception as e:
                messagebox.showerror("错误", f"重置配置失败: {e}")
    
    def log_message(self, message, level="INFO"):
        """记录日志消息"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
    
    def run(self):
        """运行GUI"""
        try:
            self.mainloop()
        except KeyboardInterrupt:
            self.quit()

def main():
    """主函数"""
    try:
        app = AdvancedGUI()
        app.run()
    except Exception as e:
        print(f"GUI启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()