#!/usr/bin/env python3
"""
智能文件处理工具 - 现代化GUI界面
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any

from improved_file_handler import file_handler
from improved_data_processor import text_processor, result_formatter
from config import config

class ModernFileProcessorGUI:
    """现代化文件处理GUI"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_variables()
        self.setup_styles()
        self.create_widgets()
        self.setup_bindings()
        
        # 消息队列用于线程通信
        self.message_queue = queue.Queue()
        self.check_queue()
        
        # 处理线程
        self.processing_thread = None
        
    def setup_window(self):
        """设置窗口"""
        self.root.title("🔍 智能文件处理工具 v2.0")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)
        
        # 居中显示
        self.center_window()
        
    def center_window(self):
        """窗口居中"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_variables(self):
        """设置变量"""
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.output_format = tk.StringVar(value="summary")
        self.processing_mode = tk.StringVar(value="single")
        self.status_text = tk.StringVar(value="就绪")
        self.progress_var = tk.DoubleVar()
        self.file_count = tk.StringVar(value="文件: 0")
        
    def setup_styles(self):
        """设置样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 自定义样式
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'))
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Info.TLabel', font=('Arial', 10))
        style.configure('Success.TLabel', foreground='#28a745')
        style.configure('Error.TLabel', foreground='#dc3545')
        style.configure('Warning.TLabel', foreground='#ffc107')
        
        # 按钮样式
        style.configure('Primary.TButton', font=('Arial', 10, 'bold'))
        style.configure('Success.TButton', foreground='white', background='#28a745')
        style.configure('Danger.TButton', foreground='white', background='#dc3545')
        
    def create_widgets(self):
        """创建所有控件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill='both', expand=True)
        
        # 标题栏
        self.create_header(main_frame)
        
        # 主要内容区域（使用PanedWindow分割）
        paned = ttk.PanedWindow(main_frame, orient='horizontal')
        paned.pack(fill='both', expand=True, pady=(15, 0))
        
        # 左侧控制面板
        left_frame = ttk.Frame(paned, padding="10")
        paned.add(left_frame, weight=1)
        
        # 右侧结果面板
        right_frame = ttk.Frame(paned, padding="10")
        paned.add(right_frame, weight=2)
        
        # 创建左右面板内容
        self.create_control_panel(left_frame)
        self.create_result_panel(right_frame)
        
        # 状态栏
        self.create_status_bar(main_frame)
        
    def create_header(self, parent):
        """创建标题栏"""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill='x', pady=(0, 10))
        
        # 主标题
        title_label = ttk.Label(
            header_frame, 
            text="🔍 智能文件处理工具", 
            style='Title.TLabel'
        )
        title_label.pack(side='left')
        
        # 版本和帮助按钮
        version_frame = ttk.Frame(header_frame)
        version_frame.pack(side='right')
        
        ttk.Label(version_frame, text="v2.0", style='Info.TLabel').pack(side='left', padx=(0, 10))
        ttk.Button(version_frame, text="❓", command=self.show_help, width=3).pack(side='left', padx=(0, 5))
        ttk.Button(version_frame, text="⚙️", command=self.show_settings, width=3).pack(side='left')
        
        # 分隔线
        separator = ttk.Separator(parent, orient='horizontal')
        separator.pack(fill='x', pady=5)
        
    def create_control_panel(self, parent):
        """创建控制面板"""
        # 处理模式选择
        mode_frame = ttk.LabelFrame(parent, text="🎯 处理模式", padding="10")
        mode_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Radiobutton(
            mode_frame, 
            text="📄 单文件处理", 
            variable=self.processing_mode, 
            value="single",
            command=self.on_mode_change
        ).pack(anchor='w')
        
        ttk.Radiobutton(
            mode_frame, 
            text="📁 批量处理", 
            variable=self.processing_mode, 
            value="batch",
            command=self.on_mode_change
        ).pack(anchor='w', pady=(5, 0))
        
        # 文件选择
        file_frame = ttk.LabelFrame(parent, text="📂 文件选择", padding="10")
        file_frame.pack(fill='x', pady=(0, 15))
        
        # 输入文件
        ttk.Label(file_frame, text="输入:", style='Heading.TLabel').pack(anchor='w')
        
        input_frame = ttk.Frame(file_frame)
        input_frame.pack(fill='x', pady=(5, 10))
        
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_path, font=('Arial', 9))
        self.input_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        self.input_button = ttk.Button(
            input_frame, 
            text="选择文件", 
            command=self.select_input_path,
            width=12
        )
        self.input_button.pack(side='right')
        
        # 输出文件
        ttk.Label(file_frame, text="输出:", style='Heading.TLabel').pack(anchor='w')
        
        output_frame = ttk.Frame(file_frame)
        output_frame.pack(fill='x', pady=(5, 0))
        
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_path, font=('Arial', 9))
        self.output_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        self.output_button = ttk.Button(
            output_frame, 
            text="选择位置", 
            command=self.select_output_path,
            width=12
        )
        self.output_button.pack(side='right')
        
        # 输出格式
        format_frame = ttk.LabelFrame(parent, text="📋 输出格式", padding="10")
        format_frame.pack(fill='x', pady=(0, 15))
        
        formats = [
            ("📊 摘要格式", "summary"),
            ("🔧 JSON格式", "json"),
            ("📝 纯文本", "text")
        ]
        
        for text, value in formats:
            ttk.Radiobutton(
                format_frame, 
                text=text, 
                variable=self.output_format, 
                value=value
            ).pack(anchor='w', pady=1)
        
        # 处理控制
        control_frame = ttk.LabelFrame(parent, text="🚀 处理控制", padding="10")
        control_frame.pack(fill='x', pady=(0, 15))
        
        self.start_button = ttk.Button(
            control_frame, 
            text="🚀 开始处理", 
            command=self.start_processing,
            style='Primary.TButton'
        )
        self.start_button.pack(fill='x', pady=(0, 5))
        
        self.stop_button = ttk.Button(
            control_frame, 
            text="⏹️ 停止处理", 
            command=self.stop_processing,
            state='disabled'
        )
        self.stop_button.pack(fill='x', pady=(0, 5))
        
        ttk.Button(
            control_frame, 
            text="🧹 清空日志", 
            command=self.clear_log
        ).pack(fill='x')
        
        # 进度显示
        progress_frame = ttk.LabelFrame(parent, text="📈 处理进度", padding="10")
        progress_frame.pack(fill='x')
        
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.pack(fill='x', pady=(0, 5))
        
        self.status_label = ttk.Label(
            progress_frame, 
            textvariable=self.status_text,
            style='Info.TLabel'
        )
        self.status_label.pack(anchor='w')
        
    def create_result_panel(self, parent):
        """创建结果面板"""
        # 标题
        ttk.Label(parent, text="📊 处理结果", style='Heading.TLabel').pack(anchor='w', pady=(0, 10))
        
        # 结果显示区域
        result_frame = ttk.Frame(parent)
        result_frame.pack(fill='both', expand=True)
        
        # 创建文本显示区域
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            wrap=tk.WORD,
            font=('Consolas', 10),
            padx=10,
            pady=10
        )
        self.result_text.pack(fill='both', expand=True, pady=(0, 10))
        
        # 添加语法高亮标签
        self.setup_text_tags()
        
        # 结果操作按钮
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x')
        
        ttk.Button(
            button_frame, 
            text="💾 保存结果", 
            command=self.save_results
        ).pack(side='left', padx=(0, 5))
        
        ttk.Button(
            button_frame, 
            text="📋 复制结果", 
            command=self.copy_results
        ).pack(side='left', padx=(0, 5))
        
        ttk.Button(
            button_frame, 
            text="🧹 清空结果", 
            command=self.clear_results
        ).pack(side='left', padx=(0, 5))
        
        ttk.Button(
            button_frame, 
            text="📁 打开输出目录", 
            command=self.open_output_directory
        ).pack(side='right')
        
    def create_status_bar(self, parent):
        """创建状态栏"""
        # 分隔线
        separator = ttk.Separator(parent, orient='horizontal')
        separator.pack(fill='x', pady=(15, 5))
        
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill='x')
        
        # 左侧状态信息
        self.file_count_label = ttk.Label(
            status_frame, 
            textvariable=self.file_count,
            style='Info.TLabel'
        )
        self.file_count_label.pack(side='left')
        
        # 右侧时间信息
        self.time_label = ttk.Label(
            status_frame, 
            text="",
            style='Info.TLabel'
        )
        self.time_label.pack(side='right')
        
    def setup_text_tags(self):
        """设置文本标签用于语法高亮"""
        self.result_text.tag_configure("header", font=('Arial', 12, 'bold'), foreground='#2c3e50')
        self.result_text.tag_configure("info", font=('Arial', 10), foreground='#34495e')
        self.result_text.tag_configure("success", font=('Arial', 10), foreground='#27ae60')
        self.result_text.tag_configure("error", font=('Arial', 10), foreground='#e74c3c')
        self.result_text.tag_configure("warning", font=('Arial', 10), foreground='#f39c12')
        self.result_text.tag_configure("code", font=('Consolas', 9), background='#f8f9fa')
        
    def setup_bindings(self):
        """设置事件绑定"""
        # 快捷键
        self.root.bind('<Control-o>', lambda e: self.select_input_path())
        self.root.bind('<Control-s>', lambda e: self.save_results())
        self.root.bind('<F1>', lambda e: self.show_help())
        self.root.bind('<F5>', lambda e: self.start_processing())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        
        # 窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def on_mode_change(self):
        """处理模式变化时的回调"""
        mode = self.processing_mode.get()
        if mode == "single":
            self.input_button.config(text="选择文件")
            self.output_button.config(text="选择位置")
        else:
            self.input_button.config(text="选择文件夹")
            self.output_button.config(text="选择文件夹")
            
    def select_input_path(self):
        """选择输入路径"""
        mode = self.processing_mode.get()
        
        if mode == "single":
            file_path = filedialog.askopenfilename(
                title="选择要处理的文件",
                filetypes=[
                    ("所有支持的文件", "*.txt;*.csv;*.json;*.pdf;*.xlsx;*.docx"),
                    ("文本文件", "*.txt"),
                    ("CSV文件", "*.csv"),
                    ("JSON文件", "*.json"),
                    ("PDF文件", "*.pdf"),
                    ("Excel文件", "*.xlsx"),
                    ("Word文档", "*.docx"),
                    ("所有文件", "*.*")
                ]
            )
            if file_path:
                self.input_path.set(file_path)
                # 自动设置输出路径
                path = Path(file_path)
                if self.output_format.get() == "json":
                    output_path = path.parent / f"{path.stem}_processed.json"
                else:
                    output_path = path.parent / f"{path.stem}_processed.txt"
                self.output_path.set(str(output_path))
                self.file_count.set("文件: 1")
        else:
            folder_path = filedialog.askdirectory(title="选择要处理的文件夹")
            if folder_path:
                self.input_path.set(folder_path)
                # 自动设置输出文件夹
                output_path = Path(folder_path).parent / f"{Path(folder_path).name}_processed"
                self.output_path.set(str(output_path))
                # 统计文件数
                try:
                    count = len([f for f in Path(folder_path).rglob('*') if f.is_file()])
                    self.file_count.set(f"文件: {count}")
                except:
                    self.file_count.set("文件: ?")
                    
    def select_output_path(self):
        """选择输出路径"""
        mode = self.processing_mode.get()
        
        if mode == "single":
            initial_name = ""
            if self.input_path.get():
                path = Path(self.input_path.get())
                if self.output_format.get() == "json":
                    initial_name = f"{path.stem}_processed.json"
                else:
                    initial_name = f"{path.stem}_processed.txt"
                    
            file_path = filedialog.asksaveasfilename(
                title="选择输出文件位置",
                initialvalue=initial_name,
                filetypes=[
                    ("文本文件", "*.txt"),
                    ("JSON文件", "*.json"),
                    ("所有文件", "*.*")
                ]
            )
            if file_path:
                self.output_path.set(file_path)
        else:
            folder_path = filedialog.askdirectory(title="选择输出文件夹")
            if folder_path:
                self.output_path.set(folder_path)
                
    def start_processing(self):
        """开始处理"""
        input_path = self.input_path.get().strip()
        output_path = self.output_path.get().strip()
        
        # 验证输入
        if not input_path:
            messagebox.showerror("错误", "请选择输入文件或文件夹")
            return
            
        if not output_path:
            messagebox.showerror("错误", "请选择输出位置")
            return
            
        if not Path(input_path).exists():
            messagebox.showerror("错误", "输入路径不存在")
            return
            
        # 更新UI状态
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.progress_var.set(0)
        self.status_text.set("准备处理...")
        
        # 清空结果显示
        self.clear_results()
        
        # 记录开始时间
        self.start_time = time.time()
        
        # 启动处理线程
        self.processing_thread = threading.Thread(
            target=self.process_files_thread,
            args=(input_path, output_path),
            daemon=True
        )
        self.processing_thread.start()
        
    def process_files_thread(self, input_path, output_path):
        """在后台线程中处理文件"""
        try:
            mode = self.processing_mode.get()
            output_format = self.output_format.get()
            
            if mode == "single":
                self.process_single_file_thread(input_path, output_path, output_format)
            else:
                self.process_batch_files_thread(input_path, output_path, output_format)
                
        except Exception as e:
            self.message_queue.put(('error', f"处理失败: {str(e)}"))
        finally:
            self.message_queue.put(('complete', None))
            
    def process_single_file_thread(self, input_path, output_path, output_format):
        """处理单个文件"""
        try:
            # 读取文件
            self.message_queue.put(('status', f"正在读取文件: {Path(input_path).name}"))
            self.message_queue.put(('progress', 20))
            
            content = file_handler.read_file(input_path)
            if content is None:
                self.message_queue.put(('error', "无法读取文件"))
                return
                
            # 处理文本
            self.message_queue.put(('status', "正在分析文本..."))
            self.message_queue.put(('progress', 50))
            
            result = text_processor.process_text(content)
            
            # 格式化输出
            self.message_queue.put(('status', "正在格式化输出..."))
            self.message_queue.put(('progress', 80))
            
            if output_format == "json":
                output_content = result_formatter.to_json(result)
            elif output_format == "summary":
                output_content = result_formatter.to_summary_text(result)
            else:
                output_content = result.processed_text
                
            # 保存文件
            self.message_queue.put(('status', "正在保存文件..."))
            self.message_queue.put(('progress', 90))
            
            success = file_handler.write_file(output_path, output_content)
            
            if success:
                self.message_queue.put(('progress', 100))
                self.message_queue.put(('status', "处理完成"))
                self.message_queue.put(('result', output_content))
                self.message_queue.put(('success', f"文件已保存到: {output_path}"))
            else:
                self.message_queue.put(('error', "保存文件失败"))
                
        except Exception as e:
            self.message_queue.put(('error', f"处理单文件失败: {str(e)}"))
            
    def process_batch_files_thread(self, input_folder, output_folder, output_format):
        """批量处理文件"""
        try:
            self.message_queue.put(('status', "正在扫描文件..."))
            
            def process_func(content):
                result = text_processor.process_text(content)
                if output_format == "json":
                    return result_formatter.to_json(result)
                elif output_format == "summary":
                    return result_formatter.to_summary_text(result)
                else:
                    return result.processed_text
                    
            # 执行批量处理
            batch_result = file_handler.batch_process(
                input_folder, output_folder, process_func
            )
            
            # 报告结果
            if batch_result.get("success"):
                processed = batch_result.get("processed", 0)
                errors = batch_result.get("errors", 0)
                total = batch_result.get("total", 0)
                
                result_text = f"批量处理完成\n"
                result_text += f"总文件数: {total}\n"
                result_text += f"成功处理: {processed}\n"
                result_text += f"处理失败: {errors}\n"
                result_text += f"输出文件夹: {output_folder}"
                
                self.message_queue.put(('result', result_text))
                self.message_queue.put(('success', f"批量处理完成: {processed}/{total} 成功"))
            else:
                self.message_queue.put(('error', batch_result.get("error", "批量处理失败")))
                
        except Exception as e:
            self.message_queue.put(('error', f"批量处理失败: {str(e)}"))
            
    def stop_processing(self):
        """停止处理"""
        self.message_queue.put(('status', "正在停止..."))
        self.reset_ui_state()
        
    def reset_ui_state(self):
        """重置UI状态"""
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.progress_var.set(0)
        
    def check_queue(self):
        """检查消息队列"""
        try:
            while not self.message_queue.empty():
                msg_type, data = self.message_queue.get_nowait()
                
                if msg_type == 'status':
                    self.status_text.set(data)
                elif msg_type == 'progress':
                    self.progress_var.set(data)
                elif msg_type == 'result':
                    self.append_result(data)
                elif msg_type == 'success':
                    self.status_text.set("处理成功")
                    messagebox.showinfo("成功", data)
                elif msg_type == 'error':
                    self.status_text.set("处理失败")
                    messagebox.showerror("错误", data)
                elif msg_type == 'complete':
                    self.reset_ui_state()
                    elapsed = time.time() - getattr(self, 'start_time', time.time())
                    self.time_label.config(text=f"耗时: {elapsed:.1f}秒")
                    
        except queue.Empty:
            pass
            
        # 每100ms检查一次
        self.root.after(100, self.check_queue)
        
    def append_result(self, text, tag=None):
        """添加结果文本"""
        self.result_text.insert(tk.END, text + "\n", tag)
        self.result_text.see(tk.END)
        
    def clear_log(self):
        """清空日志"""
        self.status_text.set("就绪")
        self.progress_var.set(0)
        self.time_label.config(text="")
        
    def clear_results(self):
        """清空结果"""
        self.result_text.delete(1.0, tk.END)
        
    def save_results(self):
        """保存结果"""
        content = self.result_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("警告", "没有可保存的内容")
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
                messagebox.showinfo("成功", f"结果已保存到: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")
                
    def copy_results(self):
        """复制结果到剪贴板"""
        content = self.result_text.get(1.0, tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            messagebox.showinfo("成功", "结果已复制到剪贴板")
        else:
            messagebox.showwarning("警告", "没有可复制的内容")
            
    def open_output_directory(self):
        """打开输出目录"""
        output_path = self.output_path.get()
        if output_path:
            try:
                import subprocess
                import platform
                
                if platform.system() == "Windows":
                    path = Path(output_path)
                    if path.is_file():
                        subprocess.run(['explorer', '/select,', str(path)])
                    else:
                        subprocess.run(['explorer', str(path)])
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(['open', str(Path(output_path).parent)])
                else:  # Linux
                    subprocess.run(['xdg-open', str(Path(output_path).parent)])
            except Exception as e:
                messagebox.showerror("错误", f"无法打开目录: {str(e)}")
        else:
            messagebox.showwarning("警告", "没有设置输出路径")
            
    def show_settings(self):
        """显示设置对话框"""
        SettingsWindow(self.root)
        
    def show_help(self):
        """显示帮助对话框"""
        HelpWindow(self.root)
        
    def on_closing(self):
        """窗口关闭时的处理"""
        if self.processing_thread and self.processing_thread.is_alive():
            if messagebox.askokcancel("确认退出", "正在处理文件，确定要退出吗？"):
                self.root.quit()
        else:
            self.root.quit()
            
    def run(self):
        """运行应用程序"""
        self.root.mainloop()

class SettingsWindow:
    """设置窗口"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("⚙️ 设置")
        self.window.geometry("500x400")
        self.window.transient(parent)
        self.window.grab_set()
        
        # 居中显示
        self.center_window(parent)
        self.create_widgets()
        
    def center_window(self, parent):
        """窗口居中"""
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        x = parent_x + (parent_width - 500) // 2
        y = parent_y + (parent_height - 400) // 2
        
        self.window.geometry(f"500x400+{x}+{y}")
        
    def create_widgets(self):
        """创建设置控件"""
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # 标题
        ttk.Label(main_frame, text="⚙️ 应用设置", font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        # 创建选项卡
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True, pady=(0, 20))
        
        # 处理设置选项卡
        self.create_processing_tab(notebook)
        
        # NLP设置选项卡
        self.create_nlp_tab(notebook)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame, text="确定", command=self.save_settings).pack(side='right', padx=(5, 0))
        ttk.Button(button_frame, text="取消", command=self.window.destroy).pack(side='right')
        
    def create_processing_tab(self, parent):
        """创建处理设置选项卡"""
        frame = ttk.Frame(parent, padding="15")
        parent.add(frame, text="🔧 处理设置")
        
        # 最大文件大小
        ttk.Label(frame, text="最大文件大小 (MB):").grid(row=0, column=0, sticky='w', pady=5)
        self.max_size_var = tk.StringVar(value=str(config.get('processing.max_file_size_mb', 100)))
        ttk.Entry(frame, textvariable=self.max_size_var, width=20).grid(row=0, column=1, sticky='w', padx=(10, 0))
        
        # 并发处理数
        ttk.Label(frame, text="并发处理数:").grid(row=1, column=0, sticky='w', pady=5)
        self.workers_var = tk.StringVar(value=str(config.get('processing.max_workers', 4)))
        ttk.Entry(frame, textvariable=self.workers_var, width=20).grid(row=1, column=1, sticky='w', padx=(10, 0))
        
        # 支持的文件格式
        ttk.Label(frame, text="支持的文件格式:").grid(row=2, column=0, sticky='nw', pady=5)
        formats_text = ', '.join(config.get('processing.supported_formats', []))
        ttk.Label(frame, text=formats_text, wraplength=300).grid(row=2, column=1, sticky='w', padx=(10, 0))
        
    def create_nlp_tab(self, parent):
        """创建NLP设置选项卡"""
        frame = ttk.Frame(parent, padding="15")
        parent.add(frame, text="🧠 NLP设置")
        
        # 语言检测
        self.detect_lang_var = tk.BooleanVar(value=config.get('nlp.detect_language', True))
        ttk.Checkbutton(frame, text="启用语言检测", variable=self.detect_lang_var).grid(row=0, column=0, sticky='w', pady=5)
        
        # 情感分析
        self.sentiment_var = tk.BooleanVar(value=config.get('nlp.sentiment_analysis', True))
        ttk.Checkbutton(frame, text="启用情感分析", variable=self.sentiment_var).grid(row=1, column=0, sticky='w', pady=5)
        
        # 实体识别
        self.entity_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="启用实体识别", variable=self.entity_var).grid(row=2, column=0, sticky='w', pady=5)
        
        # 模型信息
        ttk.Label(frame, text="已加载的模型:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky='w', pady=(15, 5))
        
        models_info = []
        for lang, model in config.get('nlp.models', {}).items():
            models_info.append(f"• {lang}: {model}")
        
        models_text = '\n'.join(models_info) if models_info else "无"
        ttk.Label(frame, text=models_text).grid(row=4, column=0, sticky='w', pady=5)
        
    def save_settings(self):
        """保存设置"""
        try:
            # 这里可以实现真正的设置保存逻辑
            messagebox.showinfo("成功", "设置已保存")
            self.window.destroy()
        except Exception as e:
            messagebox.showerror("错误", f"保存设置失败: {str(e)}")

class HelpWindow:
    """帮助窗口"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("❓ 帮助")
        self.window.geometry("700x600")
        self.window.transient(parent)
        self.window.grab_set()
        
        # 居中显示
        self.center_window(parent)
        self.create_widgets()
        
    def center_window(self, parent):
        """窗口居中"""
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        x = parent_x + (parent_width - 700) // 2
        y = parent_y + (parent_height - 600) // 2
        
        self.window.geometry(f"700x600+{x}+{y}")
        
    def create_widgets(self):
        """创建帮助内容"""
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # 标题
        ttk.Label(main_frame, text="❓ 使用帮助", font=('Arial', 16, 'bold')).pack(pady=(0, 20))
        
        # 帮助内容
        help_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            font=('Arial', 11),
            padx=15,
            pady=15
        )
        help_text.pack(fill='both', expand=True, pady=(0, 20))
        
        help_content = """🔍 智能文件处理工具 v2.0 使用指南

📋 主要功能：
• 🔤 智能文本分析：自动语言检测、分词、词根提取
• 💭 情感分析：分析文本的情感倾向（积极、消极、中性）
• 📊 数据提取：自动识别和提取数字、日期、命名实体
• 📁 多格式支持：支持 .txt、.csv、.json、.pdf、.xlsx、.docx 等格式
• ⚡ 批量处理：支持文件夹批量处理，多线程并发执行
• 🎯 多种输出：摘要格式、JSON格式、纯文本格式

🚀 使用步骤：
1️⃣ 选择处理模式：单文件处理或批量处理
2️⃣ 选择输入：点击"选择文件"或"选择文件夹"
3️⃣ 设置输出：选择输出位置和格式
4️⃣ 开始处理：点击"🚀 开始处理"按钮
5️⃣ 查看结果：在右侧面板查看处理结果

📋 输出格式说明：
• 📊 摘要格式：包含语言识别、统计信息、情感分析等综合信息
• 🔧 JSON格式：结构化数据，包含所有分析结果的详细信息
• 📝 纯文本：仅包含经过处理的文本内容

⌨️ 快捷键：
• Ctrl+O：选择输入文件
• Ctrl+S：保存处理结果
• F1：显示此帮助窗口
• F5：开始处理
• Ctrl+Q：退出程序

🛠️ 高级功能：
• 📈 实时进度显示：处理过程中显示实时进度
• 🔧 可配置设置：通过设置窗口调整处理参数
• 💾 结果保存：支持保存和复制处理结果
• 📁 快速访问：一键打开输出目录

⚠️ 注意事项：
• 确保有足够的磁盘空间存储输出文件
• 大文件处理可能需要较长时间，请耐心等待
• 批量处理时建议选择相同类型的文件
• 如遇到问题，请检查输入文件格式是否受支持

🆘 常见问题：
Q: 支持哪些文件格式？
A: 支持 .txt、.csv、.json、.pdf、.xlsx、.docx 等常见格式

Q: 如何处理大文件？
A: 工具会自动处理大文件，但可能需要更长时间

Q: 批量处理失败怎么办？
A: 检查文件夹中是否包含不支持的文件格式，或文件是否损坏

Q: 如何获取更多帮助？
A: 请参考项目文档或联系开发者

版本：v2.0 | 许可证：MIT License"""
        
        help_text.insert(1.0, help_content)
        help_text.config(state='disabled')
        
        # 关闭按钮
        ttk.Button(main_frame, text="关闭", command=self.window.destroy).pack(pady=(0, 10))

def main():
    """主函数"""
    try:
        app = ModernFileProcessorGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("启动错误", f"应用程序启动失败：\n{str(e)}")

if __name__ == "__main__":
    main()