#!/usr/bin/env python3
"""
智能文件处理工具 - GUI演示版本
简化版本，便于快速测试和展示
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import time
from pathlib import Path

class SimpleGUI:
    """简化版GUI"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """设置窗口"""
        self.root.title("智能文件处理工具 v2.0 - 演示版")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 设置样式
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
            
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="智能文件处理工具", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 输入文件选择
        ttk.Label(main_frame, text="选择文件:", font=('Arial', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        file_frame.columnconfigure(0, weight=1)
        
        self.file_var = tk.StringVar()
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_var, width=60)
        self.file_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(file_frame, text="浏览...", 
                  command=self.select_file).grid(row=0, column=1)
        
        # 输出格式选择
        format_frame = ttk.LabelFrame(main_frame, text="输出格式", padding="10")
        format_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 20))
        
        self.format_var = tk.StringVar(value="summary")
        ttk.Radiobutton(format_frame, text="摘要格式", variable=self.format_var, 
                       value="summary").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(format_frame, text="JSON格式", variable=self.format_var, 
                       value="json").pack(side=tk.LEFT, padx=(0, 20))
        ttk.Radiobutton(format_frame, text="纯文本", variable=self.format_var, 
                       value="text").pack(side=tk.LEFT)
        
        # 控制按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 20))
        
        self.process_button = ttk.Button(button_frame, text="开始处理", 
                                        command=self.start_processing)
        self.process_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="清空结果", 
                  command=self.clear_results).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="保存结果", 
                  command=self.save_results).pack(side=tk.LEFT)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                           maximum=100, mode='determinate')
        self.progress_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), 
                              pady=(0, 10))
        
        # 状态标签
        self.status_var = tk.StringVar(value="准备就绪")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=5, column=0, columnspan=2, sticky=tk.W)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="处理结果", padding="10")
        result_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                         pady=(20, 0))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, 
                                                    height=15, font=('Consolas', 10))
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def select_file(self):
        """选择文件"""
        filetypes = [
            ("文本文件", "*.txt"),
            ("CSV文件", "*.csv"),
            ("JSON文件", "*.json"),
            ("所有文件", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="选择要处理的文件",
            filetypes=filetypes
        )
        
        if filename:
            self.file_var.set(filename)
            
    def start_processing(self):
        """开始处理（演示版本）"""
        file_path = self.file_var.get().strip()
        
        if not file_path:
            messagebox.showerror("错误", "请选择一个文件")
            return
            
        if not Path(file_path).exists():
            messagebox.showerror("错误", "文件不存在")
            return
            
        # 禁用按钮
        self.process_button.config(state='disabled')
        self.status_var.set("正在处理...")
        self.progress_var.set(0)
        
        # 在新线程中模拟处理
        thread = threading.Thread(target=self.simulate_processing, args=(file_path,))
        thread.daemon = True
        thread.start()
        
    def simulate_processing(self, file_path):
        """模拟文件处理过程"""
        try:
            # 读取文件
            self.root.after(0, lambda: self.status_var.set("读取文件..."))
            self.root.after(0, lambda: self.progress_var.set(20))
            time.sleep(1)
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 模拟分析过程
            self.root.after(0, lambda: self.status_var.set("分析文本..."))
            self.root.after(0, lambda: self.progress_var.set(50))
            time.sleep(1)
            
            # 生成模拟结果
            self.root.after(0, lambda: self.status_var.set("生成结果..."))
            self.root.after(0, lambda: self.progress_var.set(80))
            time.sleep(1)
            
            # 创建结果
            format_type = self.format_var.get()
            result = self.generate_demo_result(content, format_type)
            
            # 显示结果
            self.root.after(0, lambda: self.display_result(result))
            self.root.after(0, lambda: self.progress_var.set(100))
            self.root.after(0, lambda: self.status_var.set("处理完成"))
            
        except Exception as e:
            error_msg = f"处理失败: {str(e)}"
            self.root.after(0, lambda: self.status_var.set(error_msg))
            self.root.after(0, lambda: messagebox.showerror("错误", error_msg))
        finally:
            # 重新启用按钮
            self.root.after(0, lambda: self.process_button.config(state='normal'))
            
    def generate_demo_result(self, content, format_type):
        """生成演示结果"""
        # 基本统计
        char_count = len(content)
        word_count = len(content.split())
        line_count = len(content.splitlines())
        
        # 简单的情感分析模拟
        positive_words = ['好', '棒', '优秀', '成功', '喜欢', 'good', 'great', 'excellent', 'amazing']
        negative_words = ['坏', '差', '失败', '讨厌', 'bad', 'terrible', 'awful', 'hate']
        
        positive_count = sum(1 for word in positive_words if word.lower() in content.lower())
        negative_count = sum(1 for word in negative_words if word.lower() in content.lower())
        
        if positive_count > negative_count:
            sentiment = "积极"
            sentiment_score = 0.6
        elif negative_count > positive_count:
            sentiment = "消极"
            sentiment_score = -0.4
        else:
            sentiment = "中性"
            sentiment_score = 0.0
        
        if format_type == "json":
            import json
            result = {
                "original_text": content[:200] + "..." if len(content) > 200 else content,
                "statistics": {
                    "char_count": char_count,
                    "word_count": word_count,
                    "line_count": line_count
                },
                "sentiment": {
                    "label": sentiment,
                    "score": sentiment_score
                },
                "processing_time": "2.5秒",
                "format": "演示版本结果"
            }
            return json.dumps(result, ensure_ascii=False, indent=2)
            
        elif format_type == "summary":
            return f"""文件处理摘要报告
====================

文件统计:
- 字符数: {char_count:,}
- 词数: {word_count:,}
- 行数: {line_count:,}

情感分析:
- 情感倾向: {sentiment}
- 情感分数: {sentiment_score:.2f}
- 积极词汇: {positive_count} 个
- 消极词汇: {negative_count} 个

处理信息:
- 处理时间: 2.5秒
- 输出格式: 摘要
- 版本: 演示版本

文本预览:
{content[:300]}{'...' if len(content) > 300 else ''}
"""
        else:  # text format
            # 简单的文本清理
            cleaned = ' '.join(content.split())
            return f"处理后的文本 (字符数: {len(cleaned)}):\n\n{cleaned}"
    
    def display_result(self, result):
        """显示结果"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, result)
        
    def clear_results(self):
        """清空结果"""
        self.result_text.delete(1.0, tk.END)
        self.progress_var.set(0)
        self.status_var.set("准备就绪")
        
    def save_results(self):
        """保存结果"""
        content = self.result_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("警告", "没有结果可保存")
            return
            
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
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("成功", f"结果已保存到:\n{filename}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")
    
    def run(self):
        """运行GUI"""
        # 显示欢迎信息
        welcome_text = """欢迎使用智能文件处理工具 v2.0！

这是演示版本，展示了以下功能：
• 文件选择和基本统计
• 简单的情感分析
• 多种输出格式
• 进度显示

使用说明：
1. 点击"浏览..."选择要处理的文件
2. 选择输出格式
3. 点击"开始处理"
4. 查看处理结果

注意：这是演示版本，实际功能更加强大！
"""
        self.result_text.insert(1.0, welcome_text)
        
        # 启动主循环
        self.root.mainloop()

def main():
    """主函数"""
    try:
        app = SimpleGUI()
        app.run()
    except Exception as e:
        print(f"GUI启动失败: {e}")
        # 显示一个简单的错误对话框
        import tkinter.messagebox as mb
        mb.showerror("启动错误", f"GUI启动失败:\n{e}\n\n请检查Python环境和依赖。")

if __name__ == "__main__":
    main()