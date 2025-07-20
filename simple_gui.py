#!/usr/bin/env python3
"""
智能文件处理工具 - 简化版GUI
适用于依赖不完整的环境
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import json
import os
from pathlib import Path

class SimpleFileProcessorGUI:
    """简化版文件处理GUI"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("智能文件处理工具 - 简化版")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # 初始化变量
        self.result_queue = queue.Queue()
        self.current_task = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 主容器
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(
            main_frame,
            text="智能文件处理工具 - 简化版",
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=(0, 20))
        
        # 输入文件选择
        input_frame = ttk.LabelFrame(main_frame, text="输入文件", padding="10")
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        input_row = ttk.Frame(input_frame)
        input_row.pack(fill=tk.X)
        
        self.input_var = tk.StringVar()
        input_entry = ttk.Entry(input_row, textvariable=self.input_var)
        input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(
            input_row,
            text="浏览...",
            command=self.browse_input
        ).pack(side=tk.RIGHT)
        
        # 输出文件选择
        output_frame = ttk.LabelFrame(main_frame, text="输出文件", padding="10")
        output_frame.pack(fill=tk.X, pady=(0, 15))
        
        output_row = ttk.Frame(output_frame)
        output_row.pack(fill=tk.X)
        
        self.output_var = tk.StringVar()
        output_entry = ttk.Entry(output_row, textvariable=self.output_var)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(
            output_row,
            text="浏览...",
            command=self.browse_output
        ).pack(side=tk.RIGHT)
        
        # 处理选项
        options_frame = ttk.LabelFrame(main_frame, text="处理选项", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.basic_processing_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_frame,
            text="基础文本处理",
            variable=self.basic_processing_var
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        self.word_count_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_frame,
            text="词数统计",
            variable=self.word_count_var
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        # 操作按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Button(
            button_frame,
            text="开始处理",
            command=self.process_file
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="清空",
            command=self.clear_form
        ).pack(side=tk.LEFT)
        
        # 结果显示
        result_frame = ttk.LabelFrame(main_frame, text="处理结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            wrap=tk.WORD,
            height=15
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # 状态栏
        self.status_var = tk.StringVar(value="准备就绪")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
    def browse_input(self):
        """浏览输入文件"""
        filename = filedialog.askopenfilename(
            title="选择输入文件",
            filetypes=[
                ("文本文件", "*.txt"),
                ("所有文件", "*.*")
            ]
        )
        if filename:
            self.input_var.set(filename)
            # 自动设置输出文件名
            input_path = Path(filename)
            output_path = input_path.parent / f"{input_path.stem}_processed.txt"
            self.output_var.set(str(output_path))
            
    def browse_output(self):
        """浏览输出文件"""
        filename = filedialog.asksaveasfilename(
            title="选择输出文件",
            defaultextension=".txt",
            filetypes=[
                ("文本文件", "*.txt"),
                ("所有文件", "*.*")
            ]
        )
        if filename:
            self.output_var.set(filename)
            
    def clear_form(self):
        """清空表单"""
        self.input_var.set("")
        self.output_var.set("")
        self.result_text.delete(1.0, tk.END)
        self.status_var.set("准备就绪")
        
    def process_file(self):
        """处理文件"""
        input_file = self.input_var.get().strip()
        output_file = self.output_var.get().strip()
        
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
            target=self._process_file_worker,
            args=(input_file, output_file),
            daemon=True
        )
        self.current_task.start()
        
        # 开始检查结果
        self.check_result()
        
    def _process_file_worker(self, input_file, output_file):
        """文件处理工作线程"""
        try:
            self.status_var.set("正在读取文件...")
            
            # 读取文件
            try:
                with open(input_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # 尝试其他编码
                try:
                    with open(input_file, 'r', encoding='gbk') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    with open(input_file, 'r', encoding='iso-8859-1') as f:
                        content = f.read()
            
            self.status_var.set("正在处理文本...")
            
            # 基础处理
            processed_content = self.simple_text_processing(content)
            
            # 生成结果
            result = self.generate_result(content, processed_content)
            
            self.status_var.set("正在保存文件...")
            
            # 保存文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            
            self.result_queue.put(("success", result, output_file))
            
        except Exception as e:
            self.result_queue.put(("error", str(e)))
            
    def simple_text_processing(self, text):
        """简单文本处理"""
        if not text:
            return ""
            
        # 基础清理
        import re
        
        # 去除多余空白
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 分词（简单按空格分割）
        words = text.split()
        
        # 去除标点符号
        import string
        words = [word.strip(string.punctuation) for word in words if word.strip(string.punctuation)]
        
        return ' '.join(words)
        
    def generate_result(self, original_text, processed_text):
        """生成结果"""
        result_parts = []
        
        # 基本统计
        result_parts.append("=== 文件处理结果 ===\n")
        
        if self.word_count_var.get():
            original_words = len(original_text.split())
            processed_words = len(processed_text.split())
            char_count = len(original_text)
            
            result_parts.append(f"原始字符数: {char_count}")
            result_parts.append(f"原始词数: {original_words}")
            result_parts.append(f"处理后词数: {processed_words}")
            result_parts.append("")
        
        if self.basic_processing_var.get():
            result_parts.append("=== 处理后文本 ===")
            result_parts.append(processed_text)
            result_parts.append("")
            
        result_parts.append("=== 原始文本 ===")
        result_parts.append(original_text)
        
        return '\n'.join(result_parts)
        
    def check_result(self):
        """检查处理结果"""
        try:
            result = self.result_queue.get_nowait()
            
            if result[0] == "success":
                _, result_text, output_file = result
                self.status_var.set(f"处理完成: {output_file}")
                
                # 显示结果
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(1.0, result_text)
                
                messagebox.showinfo("成功", f"文件处理完成!\n输出文件: {output_file}")
                
            elif result[0] == "error":
                self.status_var.set("处理失败")
                messagebox.showerror("错误", f"处理失败: {result[1]}")
                
        except queue.Empty:
            # 如果队列为空且任务还在运行，继续检查
            if self.current_task and self.current_task.is_alive():
                self.root.after(100, self.check_result)
            else:
                if not hasattr(self, '_result_checked'):
                    self.status_var.set("准备就绪")
                    self._result_checked = True
                    
    def run(self):
        """运行GUI"""
        self.root.mainloop()

def main():
    """主函数"""
    try:
        print("🚀 启动简化版GUI...")
        app = SimpleFileProcessorGUI()
        app.run()
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()