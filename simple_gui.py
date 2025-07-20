#!/usr/bin/env python3
"""
智能文件处理工具 - 简化GUI界面
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import time
import os
from pathlib import Path

try:
    from improved_file_handler import file_handler
    from improved_data_processor import text_processor, result_formatter
    from config import config
except ImportError:
    # 如果导入失败，使用原始模块
    print("使用简化模式运行...")
    file_handler = None
    text_processor = None
    result_formatter = None

class SimpleFileProcessorGUI:
    """简化版文件处理器GUI"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_variables()
        self.create_widgets()
        
        # 处理队列
        self.queue = queue.Queue()
        self.is_processing = False
        
        # 启动队列检查
        self.check_queue()
    
    def setup_window(self):
        """设置主窗口"""
        self.root.title("智能文件处理工具 v2.0")
        self.root.geometry("900x600")
        self.root.minsize(700, 500)
        
        # 配置样式
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except:
            pass
    
    def setup_variables(self):
        """设置变量"""
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.processing_mode = tk.StringVar(value="single")
        self.output_format = tk.StringVar(value="summary")
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="就绪")
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="智能文件处理工具", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # 处理模式
        mode_frame = ttk.LabelFrame(main_frame, text="处理模式", padding="10")
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Radiobutton(mode_frame, text="单文件处理", 
                       variable=self.processing_mode, value="single",
                       command=self.on_mode_change).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(mode_frame, text="批量处理", 
                       variable=self.processing_mode, value="batch",
                       command=self.on_mode_change).pack(side=tk.LEFT)
        
        # 文件选择
        file_frame = ttk.LabelFrame(main_frame, text="文件选择", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 输入
        input_frame = ttk.Frame(file_frame)
        input_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(input_frame, text="输入:").pack(side=tk.LEFT)
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_path)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))
        self.input_button = ttk.Button(input_frame, text="选择文件", 
                                      command=self.select_input)
        self.input_button.pack(side=tk.RIGHT)
        
        # 输出
        output_frame = ttk.Frame(file_frame)
        output_frame.pack(fill=tk.X)
        
        ttk.Label(output_frame, text="输出:").pack(side=tk.LEFT)
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_path)
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))
        self.output_button = ttk.Button(output_frame, text="保存为", 
                                       command=self.select_output)
        self.output_button.pack(side=tk.RIGHT)
        
        # 选项设置
        options_frame = ttk.LabelFrame(main_frame, text="输出格式", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        formats = [("摘要格式", "summary"), ("JSON格式", "json"), ("纯文本", "text")]
        for text, value in formats:
            ttk.Radiobutton(options_frame, text=text, 
                           variable=self.output_format, value=value).pack(side=tk.LEFT, padx=(0, 20))
        
        # 控制按钮
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(pady=(0, 10))
        
        self.process_button = ttk.Button(control_frame, text="🚀 开始处理", 
                                        command=self.start_processing)
        self.process_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(control_frame, text="⏹ 停止", 
                                     command=self.stop_processing, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(control_frame, text="🗑 清空", 
                                      command=self.clear_all)
        self.clear_button.pack(side=tk.LEFT)
        
        # 进度条
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var)
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        self.status_label.pack()
        
        # 结果显示
        result_frame = ttk.LabelFrame(main_frame, text="处理结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建标签页
        self.notebook = ttk.Notebook(result_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 摘要标签
        summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(summary_frame, text="处理摘要")
        self.summary_text = scrolledtext.ScrolledText(summary_frame, wrap=tk.WORD, 
                                                     font=('Consolas', 10))
        self.summary_text.pack(fill=tk.BOTH, expand=True)
        
        # 详细结果标签
        detail_frame = ttk.Frame(self.notebook)
        self.notebook.add(detail_frame, text="详细结果")
        self.detail_text = scrolledtext.ScrolledText(detail_frame, wrap=tk.WORD, 
                                                    font=('Consolas', 10))
        self.detail_text.pack(fill=tk.BOTH, expand=True)
        
        # 日志标签
        log_frame = ttk.Frame(self.notebook)
        self.notebook.add(log_frame, text="处理日志")
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, 
                                                 font=('Consolas', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 底部按钮
        bottom_frame = ttk.Frame(result_frame)
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(bottom_frame, text="💾 保存结果", 
                  command=self.save_result).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(bottom_frame, text="📋 复制", 
                  command=self.copy_result).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(bottom_frame, text="🗑 清除结果", 
                  command=self.clear_results).pack(side=tk.LEFT)
    
    def on_mode_change(self):
        """处理模式改变"""
        mode = self.processing_mode.get()
        if mode == "single":
            self.input_button.config(text="选择文件")
            self.output_button.config(text="保存为")
        else:
            self.input_button.config(text="选择文件夹")
            self.output_button.config(text="输出文件夹")
    
    def select_input(self):
        """选择输入"""
        mode = self.processing_mode.get()
        
        if mode == "single":
            filename = filedialog.askopenfilename(
                title="选择要处理的文件",
                filetypes=[
                    ("文本文件", "*.txt"),
                    ("CSV文件", "*.csv"),
                    ("JSON文件", "*.json"),
                    ("PDF文件", "*.pdf"),
                    ("Excel文件", "*.xlsx *.xls"),
                    ("所有文件", "*.*")
                ]
            )
            if filename:
                self.input_path.set(filename)
                # 自动设置输出路径
                if not self.output_path.get():
                    base_name = Path(filename).stem
                    ext = ".json" if self.output_format.get() == "json" else ".txt"
                    self.output_path.set(f"{base_name}_processed{ext}")
        else:
            dirname = filedialog.askdirectory(title="选择要处理的文件夹")
            if dirname:
                self.input_path.set(dirname)
                if not self.output_path.get():
                    self.output_path.set(f"{dirname}_processed")
    
    def select_output(self):
        """选择输出"""
        mode = self.processing_mode.get()
        
        if mode == "single":
            ext = ".json" if self.output_format.get() == "json" else ".txt"
            filename = filedialog.asksaveasfilename(
                title="保存处理结果",
                defaultextension=ext,
                filetypes=[
                    ("文本文件", "*.txt"),
                    ("JSON文件", "*.json"),
                    ("所有文件", "*.*")
                ]
            )
            if filename:
                self.output_path.set(filename)
        else:
            dirname = filedialog.askdirectory(title="选择输出文件夹")
            if dirname:
                self.output_path.set(dirname)
    
    def start_processing(self):
        """开始处理"""
        if self.is_processing:
            return
        
        if not self.validate_inputs():
            return
        
        # 更新UI
        self.is_processing = True
        self.process_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress_var.set(0)
        self.status_var.set("开始处理...")
        self.clear_results()
        
        # 启动处理线程
        thread = threading.Thread(target=self.process_files, daemon=True)
        thread.start()
    
    def stop_processing(self):
        """停止处理"""
        self.is_processing = False
        self.status_var.set("正在停止...")
    
    def clear_all(self):
        """清空所有"""
        if self.is_processing:
            if not messagebox.askyesno("确认", "正在处理中，确定要清空吗？"):
                return
            self.stop_processing()
        
        self.input_path.set("")
        self.output_path.set("")
        self.progress_var.set(0)
        self.status_var.set("就绪")
        self.clear_results()
    
    def clear_results(self):
        """清空结果"""
        self.summary_text.delete(1.0, tk.END)
        self.detail_text.delete(1.0, tk.END)
        self.log_text.delete(1.0, tk.END)
    
    def validate_inputs(self):
        """验证输入"""
        if not self.input_path.get():
            messagebox.showerror("错误", "请选择输入文件或文件夹")
            return False
        
        if not self.output_path.get():
            messagebox.showerror("错误", "请设置输出路径")
            return False
        
        input_path = Path(self.input_path.get())
        if not input_path.exists():
            messagebox.showerror("错误", f"输入路径不存在: {input_path}")
            return False
        
        return True
    
    def process_files(self):
        """处理文件（线程函数）"""
        try:
            input_path = self.input_path.get()
            output_path = self.output_path.get()
            mode = self.processing_mode.get()
            output_format = self.output_format.get()
            
            self.queue.put(("log", f"开始处理: {input_path}"))
            
            if mode == "single":
                self.process_single_file(input_path, output_path, output_format)
            else:
                self.process_batch_files(input_path, output_path, output_format)
                
        except Exception as e:
            self.queue.put(("error", f"处理出错: {str(e)}"))
        finally:
            self.queue.put(("finished", None))
    
    def process_single_file(self, input_path, output_path, output_format):
        """处理单个文件"""
        try:
            self.queue.put(("status", "读取文件..."))
            self.queue.put(("progress", 10))
            
            # 检查模块是否可用
            if not file_handler or not text_processor:
                # 使用简化处理
                with open(input_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.queue.put(("status", "处理文本..."))
                self.queue.put(("progress", 50))
                
                # 简单处理
                processed_content = f"文件: {input_path}\n"
                processed_content += f"字符数: {len(content)}\n"
                processed_content += f"词数: {len(content.split())}\n"
                processed_content += f"行数: {len(content.splitlines())}\n\n"
                processed_content += "原始内容:\n" + content[:1000]
                if len(content) > 1000:
                    processed_content += "\n...(内容过长，已截断)"
                
            else:
                # 使用完整处理
                content = file_handler.read_file(input_path)
                if content is None:
                    self.queue.put(("error", "无法读取文件"))
                    return
                
                self.queue.put(("status", "分析文本..."))
                self.queue.put(("progress", 50))
                
                result = text_processor.process_text(content)
                
                if output_format == "json":
                    processed_content = result_formatter.to_json(result)
                elif output_format == "summary":
                    processed_content = result_formatter.to_summary_text(result)
                else:
                    processed_content = result.processed_text
            
            self.queue.put(("status", "保存文件..."))
            self.queue.put(("progress", 90))
            
            # 保存文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(processed_content)
            
            self.queue.put(("progress", 100))
            self.queue.put(("status", "处理完成"))
            self.queue.put(("success", f"文件已保存到: {output_path}"))
            self.queue.put(("summary", processed_content[:1000]))
            self.queue.put(("detail", processed_content))
            
        except Exception as e:
            self.queue.put(("error", f"处理文件失败: {str(e)}"))
    
    def process_batch_files(self, input_folder, output_folder, output_format):
        """批量处理文件"""
        try:
            self.queue.put(("status", "扫描文件..."))
            
            input_path = Path(input_folder)
            output_path = Path(output_folder)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # 获取文件列表
            files = []
            for ext in ['.txt', '.csv', '.json']:
                files.extend(input_path.glob(f'*{ext}'))
            
            if not files:
                self.queue.put(("error", "没有找到支持的文件"))
                return
            
            self.queue.put(("log", f"找到 {len(files)} 个文件"))
            
            processed = 0
            errors = 0
            
            for i, file_path in enumerate(files):
                if not self.is_processing:
                    break
                
                try:
                    self.queue.put(("status", f"处理 {file_path.name}..."))
                    
                    # 简单处理
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    processed_content = f"文件: {file_path.name}\n内容:\n{content[:500]}"
                    
                    output_file = output_path / f"{file_path.stem}_processed.txt"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(processed_content)
                    
                    processed += 1
                    progress = (i + 1) / len(files) * 100
                    self.queue.put(("progress", progress))
                    
                except Exception as e:
                    errors += 1
                    self.queue.put(("log", f"处理 {file_path.name} 失败: {str(e)}"))
            
            summary = f"批量处理完成:\n成功: {processed}\n失败: {errors}\n总计: {len(files)}"
            self.queue.put(("success", summary))
            self.queue.put(("summary", summary))
            
        except Exception as e:
            self.queue.put(("error", f"批量处理失败: {str(e)}"))
    
    def check_queue(self):
        """检查队列消息"""
        try:
            while True:
                msg_type, data = self.queue.get_nowait()
                
                if msg_type == "status":
                    self.status_var.set(data)
                elif msg_type == "progress":
                    self.progress_var.set(data)
                elif msg_type == "log":
                    self.log_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {data}\n")
                    self.log_text.see(tk.END)
                elif msg_type == "summary":
                    self.summary_text.insert(tk.END, data)
                elif msg_type == "detail":
                    self.detail_text.insert(tk.END, data)
                elif msg_type == "success":
                    messagebox.showinfo("成功", data)
                elif msg_type == "error":
                    messagebox.showerror("错误", data)
                elif msg_type == "finished":
                    self.on_finished()
                    
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)
    
    def on_finished(self):
        """处理完成"""
        self.is_processing = False
        self.process_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        if not self.status_var.get().endswith("完成"):
            self.status_var.set("就绪")
    
    def save_result(self):
        """保存结果"""
        current_tab = self.notebook.select()
        tab_text = self.notebook.tab(current_tab, "text")
        
        if tab_text == "处理摘要":
            content = self.summary_text.get(1.0, tk.END).strip()
        elif tab_text == "详细结果":
            content = self.detail_text.get(1.0, tk.END).strip()
        else:
            content = self.log_text.get(1.0, tk.END).strip()
        
        if not content:
            messagebox.showwarning("警告", "没有内容可保存")
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
                messagebox.showinfo("成功", "结果已保存")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {e}")
    
    def copy_result(self):
        """复制结果"""
        current_tab = self.notebook.select()
        tab_text = self.notebook.tab(current_tab, "text")
        
        if tab_text == "处理摘要":
            content = self.summary_text.get(1.0, tk.END).strip()
        elif tab_text == "详细结果":
            content = self.detail_text.get(1.0, tk.END).strip()
        else:
            content = self.log_text.get(1.0, tk.END).strip()
        
        if not content:
            messagebox.showwarning("警告", "没有内容可复制")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("成功", "内容已复制到剪贴板")
    
    def run(self):
        """运行GUI"""
        self.root.mainloop()

def main():
    """主函数"""
    try:
        app = SimpleFileProcessorGUI()
        app.run()
    except Exception as e:
        print(f"GUI启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()