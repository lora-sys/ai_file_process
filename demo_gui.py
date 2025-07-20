#!/usr/bin/env python3
"""
智能文件处理工具 - GUI演示版本
这是一个简化版本，用于演示GUI功能，减少依赖要求
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import json
import re
from pathlib import Path
from datetime import datetime
import time

class DemoGUI:
    """演示版GUI类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.setup_styles()
        
        # 用于线程通信的队列
        self.progress_queue = queue.Queue()
        self.result_queue = queue.Queue()
        
        # 当前任务状态
        self.current_task = None
        self.processing = False
        
        # 设置定时器检查队列
        self.root.after(100, self.check_queues)
    
    def setup_window(self):
        """设置主窗口"""
        self.root.title("智能文件处理工具 v2.0 (演示版)")
        self.root.geometry("900x650")
        self.root.minsize(700, 500)
        
        # 居中显示
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
    
    def setup_styles(self):
        """设置样式"""
        style = ttk.Style()
        
        # 配置主题
        try:
            style.theme_use('clam')
        except:
            pass
        
        # 自定义样式
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Info.TLabel', font=('Arial', 10))
        style.configure('Success.TLabel', foreground='green')
        style.configure('Error.TLabel', foreground='red')
        style.configure('Warning.TLabel', foreground='orange')
    
    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        self.create_header(main_frame)
        self.create_input_section(main_frame)
        self.create_options_section(main_frame)
        self.create_action_section(main_frame)
        self.create_progress_section(main_frame)
        self.create_results_section(main_frame)
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """创建标题区域"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="🚀 智能文件处理工具 (演示版)", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        version_label = ttk.Label(header_frame, text="v2.0", style='Info.TLabel')
        version_label.pack(side=tk.RIGHT)
        
        subtitle_label = ttk.Label(parent, 
                                 text="演示版本 - 基本文本处理功能", 
                                 style='Info.TLabel')
        subtitle_label.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
    
    def create_input_section(self, parent):
        """创建输入区域"""
        input_frame = ttk.LabelFrame(parent, text="📁 输入设置", padding="10")
        input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # 处理类型选择
        ttk.Label(input_frame, text="处理类型:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.process_type = tk.StringVar(value="single")
        type_frame = ttk.Frame(input_frame)
        type_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        ttk.Radiobutton(type_frame, text="单个文件", variable=self.process_type, 
                       value="single", command=self.on_type_changed).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(type_frame, text="演示模式", variable=self.process_type, 
                       value="demo", command=self.on_type_changed).pack(side=tk.LEFT)
        
        # 输入路径
        ttk.Label(input_frame, text="输入路径:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        input_path_frame = ttk.Frame(input_frame)
        input_path_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        input_path_frame.columnconfigure(0, weight=1)
        
        self.input_path = tk.StringVar()
        self.input_entry = ttk.Entry(input_path_frame, textvariable=self.input_path, width=50)
        self.input_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.input_browse_btn = ttk.Button(input_path_frame, text="浏览...", 
                                         command=self.browse_input)
        self.input_browse_btn.grid(row=0, column=1)
        
        # 输出路径
        ttk.Label(input_frame, text="输出路径:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        output_path_frame = ttk.Frame(input_frame)
        output_path_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        output_path_frame.columnconfigure(0, weight=1)
        
        self.output_path = tk.StringVar()
        self.output_entry = ttk.Entry(output_path_frame, textvariable=self.output_path, width=50)
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.output_browse_btn = ttk.Button(output_path_frame, text="浏览...", 
                                          command=self.browse_output)
        self.output_browse_btn.grid(row=0, column=1)
    
    def create_options_section(self, parent):
        """创建选项区域"""
        options_frame = ttk.LabelFrame(parent, text="⚙️ 处理选项", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        options_frame.columnconfigure(1, weight=1)
        
        # 输出格式
        ttk.Label(options_frame, text="输出格式:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.output_format = tk.StringVar(value="summary")
        format_frame = ttk.Frame(options_frame)
        format_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        ttk.Radiobutton(format_frame, text="摘要格式", variable=self.output_format, 
                       value="summary").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(format_frame, text="JSON格式", variable=self.output_format, 
                       value="json").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(format_frame, text="纯文本", variable=self.output_format, 
                       value="text").pack(side=tk.LEFT)
        
        # 高级选项
        advanced_frame = ttk.Frame(options_frame)
        advanced_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.enable_demo_analysis = tk.BooleanVar(value=True)
        ttk.Checkbutton(advanced_frame, text="启用演示分析", 
                       variable=self.enable_demo_analysis).pack(side=tk.LEFT, padx=(0, 20))
        
        self.verbose_mode = tk.BooleanVar(value=False)
        ttk.Checkbutton(advanced_frame, text="详细日志", 
                       variable=self.verbose_mode).pack(side=tk.LEFT)
    
    def create_action_section(self, parent):
        """创建操作区域"""
        action_frame = ttk.Frame(parent)
        action_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 主要操作按钮
        self.process_btn = ttk.Button(action_frame, text="🚀 开始处理", 
                                    command=self.start_processing)
        self.process_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(action_frame, text="⏹️ 停止", 
                                 command=self.stop_processing, state='disabled')
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = ttk.Button(action_frame, text="🗑️ 清除", 
                                  command=self.clear_all)
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # 辅助按钮
        self.demo_btn = ttk.Button(action_frame, text="🎯 演示功能", 
                                 command=self.run_demo)
        self.demo_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.help_btn = ttk.Button(action_frame, text="❓ 帮助", 
                                 command=self.show_help)
        self.help_btn.pack(side=tk.RIGHT, padx=(10, 0))
    
    def create_progress_section(self, parent):
        """创建进度区域"""
        progress_frame = ttk.LabelFrame(parent, text="📊 处理进度", padding="10")
        progress_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.progress_label = ttk.Label(progress_frame, text="就绪")
        self.progress_label.grid(row=1, column=0, sticky=tk.W)
    
    def create_results_section(self, parent):
        """创建结果区域"""
        results_frame = ttk.LabelFrame(parent, text="📋 处理结果", padding="10")
        results_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        parent.rowconfigure(6, weight=1)
        
        # 创建文本框和滚动条
        self.results_text = scrolledtext.ScrolledText(results_frame, height=8, wrap=tk.WORD)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 添加欢迎信息
        welcome_text = """欢迎使用智能文件处理工具 v2.0 演示版！

🎯 演示功能：
• 基础文本处理：字符统计、词频分析
• 简单数据提取：数字、日期识别
• 文件格式支持：文本文件读写
• 模拟情感分析：随机情感倾向
• 界面功能展示：进度条、结果显示

📝 使用提示：
1. 点击"🎯 演示功能"查看功能演示
2. 选择文本文件进行实际处理
3. 查看处理结果和统计信息

注意：这是演示版本，不包含完整的NLP功能。
"""
        self.results_text.insert(tk.END, welcome_text)
        
        # 右键菜单
        self.create_context_menu()
    
    def create_context_menu(self):
        """创建右键菜单"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="复制", command=self.copy_text)
        self.context_menu.add_command(label="全选", command=self.select_all_text)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="清除", command=self.clear_results)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="保存结果", command=self.save_results)
        
        self.results_text.bind("<Button-3>", self.show_context_menu)
    
    def create_status_bar(self, parent):
        """创建状态栏"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E))
        status_frame.columnconfigure(1, weight=1)
        
        self.status_label = ttk.Label(status_frame, text="就绪")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.time_label = ttk.Label(status_frame, text="")
        self.time_label.grid(row=0, column=2, sticky=tk.E)
        
        # 更新时间
        self.update_time()
    
    def on_type_changed(self):
        """处理类型改变事件"""
        if self.process_type.get() == "single":
            self.input_browse_btn.config(text="选择文件")
            self.output_browse_btn.config(text="保存为...")
        else:
            self.input_browse_btn.config(text="演示模式")
            self.output_browse_btn.config(text="演示模式")
    
    def browse_input(self):
        """浏览输入路径"""
        if self.process_type.get() == "single":
            filename = filedialog.askopenfilename(
                title="选择要处理的文件",
                filetypes=[
                    ("文本文件", "*.txt"),
                    ("所有文件", "*.*")
                ]
            )
            if filename:
                self.input_path.set(filename)
                # 自动设置输出路径
                input_file = Path(filename)
                output_file = input_file.parent / f"{input_file.stem}_processed{input_file.suffix}"
                self.output_path.set(str(output_file))
        else:
            messagebox.showinfo("演示模式", "演示模式不需要选择文件")
    
    def browse_output(self):
        """浏览输出路径"""
        if self.process_type.get() == "single":
            filename = filedialog.asksaveasfilename(
                title="保存处理结果",
                defaultextension=".txt",
                filetypes=[
                    ("文本文件", "*.txt"),
                    ("JSON文件", "*.json"),
                    ("所有文件", "*.*")
                ]
            )
            if filename:
                self.output_path.set(filename)
        else:
            messagebox.showinfo("演示模式", "演示模式不需要选择输出文件")
    
    def start_processing(self):
        """开始处理"""
        if self.process_type.get() == "single":
            if not self.validate_inputs():
                return
        
        self.processing = True
        self.set_ui_processing_state(True)
        
        # 在新线程中处理
        self.current_task = threading.Thread(target=self.process_files_thread)
        self.current_task.daemon = True
        self.current_task.start()
    
    def process_files_thread(self):
        """文件处理线程"""
        try:
            if self.process_type.get() == "single":
                self.process_single_file_thread()
            else:
                self.process_demo_thread()
        except Exception as e:
            self.result_queue.put(('error', f"处理失败: {str(e)}"))
        finally:
            self.result_queue.put(('complete', None))
    
    def process_single_file_thread(self):
        """单文件处理线程"""
        input_path = self.input_path.get()
        output_path = self.output_path.get()
        output_format = self.output_format.get()
        
        self.progress_queue.put(('status', f"正在处理: {Path(input_path).name}"))
        self.progress_queue.put(('progress', 20))
        
        # 读取文件
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.result_queue.put(('error', f"无法读取文件: {e}"))
            return
        
        self.progress_queue.put(('progress', 40))
        
        # 简单分析
        result = self.simple_analysis(content)
        self.progress_queue.put(('progress', 70))
        
        # 格式化输出
        if output_format == "json":
            output_content = json.dumps(result, ensure_ascii=False, indent=2)
        elif output_format == "summary":
            output_content = self.format_summary(result)
        else:
            output_content = result.get('processed_text', content)
        
        self.progress_queue.put(('progress', 90))
        
        # 保存结果
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output_content)
            self.progress_queue.put(('progress', 100))
            self.result_queue.put(('success', f"文件处理完成: {output_path}"))
            self.result_queue.put(('result', self.format_result_for_display(result)))
        except Exception as e:
            self.result_queue.put(('error', f"保存文件失败: {e}"))
    
    def process_demo_thread(self):
        """演示处理线程"""
        self.progress_queue.put(('status', "演示功能运行中..."))
        
        demo_steps = [
            ("初始化分析引擎", 10),
            ("语言检测", 25),
            ("文本清理", 40),
            ("词频统计", 55),
            ("情感分析", 70),
            ("实体识别", 85),
            ("生成报告", 100)
        ]
        
        demo_text = "这是一个演示文本。今天是2024年，天气很好，我感到很开心！这个工具真的很棒。"
        
        for step, progress in demo_steps:
            self.progress_queue.put(('status', step))
            self.progress_queue.put(('progress', progress))
            time.sleep(0.5)  # 模拟处理时间
        
        # 生成演示结果
        result = self.simple_analysis(demo_text)
        self.result_queue.put(('success', "演示功能完成！"))
        self.result_queue.put(('result', self.format_result_for_display(result)))
    
    def simple_analysis(self, text):
        """简单文本分析"""
        import random
        
        # 基础统计
        char_count = len(text)
        word_count = len(text.split())
        line_count = len(text.split('\n'))
        
        # 简单数字提取
        numbers = re.findall(r'\d+(?:\.\d+)?', text)
        numbers = [float(n) for n in numbers]
        
        # 简单日期提取
        dates = re.findall(r'\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{4}年\d{1,2}月\d{1,2}日', text)
        
        # 模拟情感分析
        sentiment_score = random.uniform(-1, 1)
        sentiment_label = "积极" if sentiment_score > 0.1 else "消极" if sentiment_score < -0.1 else "中性"
        
        # 词频统计（简单版）
        words = text.split()
        word_freq = {}
        for word in words:
            clean_word = re.sub(r'[^\w\u4e00-\u9fff]', '', word.lower())
            if clean_word and len(clean_word) > 1:
                word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
        
        # 取前5个高频词
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'original_text': text,
            'processed_text': text.strip(),
            'statistics': {
                'char_count': char_count,
                'word_count': word_count,
                'line_count': line_count,
                'unique_words': len(word_freq)
            },
            'numbers': numbers,
            'dates': dates,
            'sentiment': {
                'score': sentiment_score,
                'label': sentiment_label
            },
            'top_words': top_words,
            'timestamp': datetime.now().isoformat()
        }
    
    def format_summary(self, result):
        """格式化摘要"""
        lines = [
            "=" * 50,
            "📊 文件处理结果摘要",
            "=" * 50,
            f"🔤 字符数: {result['statistics']['char_count']}",
            f"📄 词数: {result['statistics']['word_count']}",
            f"📝 行数: {result['statistics']['line_count']}",
            f"🔠 唯一词数: {result['statistics']['unique_words']}",
            f"🔢 发现数字: {len(result['numbers'])} 个",
            f"📅 发现日期: {len(result['dates'])} 个",
            f"😊 情感倾向: {result['sentiment']['label']} ({result['sentiment']['score']:.3f})",
            "",
            "🔝 高频词汇:",
        ]
        
        for word, count in result['top_words']:
            lines.append(f"  - {word}: {count}次")
        
        if result['numbers']:
            lines.extend(["", "🔢 提取的数字:", "  " + ", ".join(map(str, result['numbers'][:10]))])
        
        if result['dates']:
            lines.extend(["", "📅 提取的日期:", "  " + ", ".join(result['dates'][:5])])
        
        lines.extend([
            "",
            "=" * 50,
            f"处理时间: {result['timestamp']}",
            "=" * 50
        ])
        
        return "\n".join(lines)
    
    def format_result_for_display(self, result):
        """格式化结果用于显示"""
        lines = ["=" * 50, "📊 处理结果详情", "=" * 50]
        
        stats = result['statistics']
        lines.extend([
            f"📝 字符数: {stats['char_count']}",
            f"📄 词数: {stats['word_count']}",
            f"📝 行数: {stats['line_count']}",
            f"🔠 唯一词数: {stats['unique_words']}",
            f"🔢 数字: {len(result['numbers'])} 个",
            f"📅 日期: {len(result['dates'])} 个",
            f"😊 情感: {result['sentiment']['label']} (分数: {result['sentiment']['score']:.3f})"
        ])
        
        if result['top_words']:
            lines.append("\n🔝 高频词汇:")
            for word, count in result['top_words'][:3]:
                lines.append(f"  • {word}: {count}次")
        
        lines.append("=" * 50)
        return "\n".join(lines)
    
    def run_demo(self):
        """运行演示功能"""
        self.process_type.set("demo")
        self.start_processing()
    
    def stop_processing(self):
        """停止处理"""
        self.processing = False
        if self.current_task and self.current_task.is_alive():
            pass  # Python线程无法强制停止
        self.set_ui_processing_state(False)
        self.add_result("⚠️ 处理已停止", "warning")
    
    def validate_inputs(self):
        """验证输入"""
        if not self.input_path.get():
            messagebox.showerror("错误", "请选择输入文件")
            return False
        
        if not self.output_path.get():
            messagebox.showerror("错误", "请选择输出路径")
            return False
        
        input_path = Path(self.input_path.get())
        if not input_path.exists():
            messagebox.showerror("错误", "输入文件不存在")
            return False
        
        if not input_path.is_file():
            messagebox.showerror("错误", "请选择文件")
            return False
        
        return True
    
    def set_ui_processing_state(self, processing):
        """设置UI处理状态"""
        if processing:
            self.process_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.progress_bar.config(mode='determinate')
        else:
            self.process_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.progress_var.set(0)
            self.progress_label.config(text="就绪")
    
    def check_queues(self):
        """检查队列更新"""
        # 检查进度队列
        try:
            while True:
                item_type, value = self.progress_queue.get_nowait()
                if item_type == 'progress':
                    self.progress_var.set(value)
                elif item_type == 'status':
                    self.progress_label.config(text=value)
        except queue.Empty:
            pass
        
        # 检查结果队列
        try:
            while True:
                item_type, value = self.result_queue.get_nowait()
                if item_type == 'success':
                    self.add_result(f"✅ {value}", "success")
                elif item_type == 'error':
                    self.add_result(f"❌ {value}", "error")
                elif item_type == 'result':
                    self.add_result(value, "info")
                elif item_type == 'complete':
                    self.set_ui_processing_state(False)
                    self.processing = False
        except queue.Empty:
            pass
        
        # 继续检查
        self.root.after(100, self.check_queues)
    
    def add_result(self, text, level="info"):
        """添加结果到文本框"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        message = f"[{timestamp}] {text}\n"
        
        self.results_text.insert(tk.END, message)
        self.results_text.see(tk.END)
        
        # 更新状态栏
        self.status_label.config(text=text[:50] + "..." if len(text) > 50 else text)
    
    def clear_all(self):
        """清除所有内容"""
        self.input_path.set("")
        self.output_path.set("")
        self.clear_results()
        self.progress_var.set(0)
        self.progress_label.config(text="就绪")
    
    def clear_results(self):
        """清除结果"""
        self.results_text.delete(1.0, tk.END)
    
    def copy_text(self):
        """复制文本"""
        try:
            text = self.results_text.selection_get()
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
        except tk.TclError:
            pass
    
    def select_all_text(self):
        """全选文本"""
        self.results_text.tag_add(tk.SEL, "1.0", tk.END)
    
    def save_results(self):
        """保存结果"""
        content = self.results_text.get(1.0, tk.END)
        if not content.strip():
            messagebox.showwarning("警告", "没有结果可保存")
            return
        
        filename = filedialog.asksaveasfilename(
            title="保存结果",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("成功", f"结果已保存到: {filename}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {e}")
    
    def show_context_menu(self, event):
        """显示右键菜单"""
        self.context_menu.post(event.x_root, event.y_root)
    
    def show_help(self):
        """显示帮助"""
        help_text = """🚀 智能文件处理工具 v2.0 演示版

📖 功能说明：
• 基础文本分析：字符、词数统计
• 简单数据提取：数字、日期识别  
• 词频分析：高频词汇统计
• 模拟情感分析：随机情感倾向
• 文件读写：支持文本文件处理

🔧 使用方法：
1. 选择处理类型（单个文件/演示模式）
2. 在单文件模式下选择输入和输出文件
3. 选择输出格式（摘要/JSON/纯文本）
4. 点击"开始处理"或"演示功能"
5. 查看处理结果

💡 提示：
• 这是演示版本，功能有限
• 完整版需要安装额外的NLP库
• 右键结果区域可保存或复制内容
• 演示模式不需要选择文件

📞 技术支持：
如有问题请查看完整版文档或联系开发者"""
        
        messagebox.showinfo("帮助", help_text)
    
    def update_time(self):
        """更新时间显示"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def on_closing(self):
        """关闭窗口事件"""
        if self.processing:
            if messagebox.askquestion("确认", "正在处理文件，确定要退出吗？") == 'no':
                return
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """运行GUI"""
        self.root.mainloop()

def main():
    """启动演示GUI"""
    try:
        app = DemoGUI()
        app.run()
    except Exception as e:
        print(f"启动GUI失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()