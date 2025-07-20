#!/usr/bin/env python3
"""
GUI启动器 - 选择不同版本的GUI界面
"""
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
from pathlib import Path

class GUILauncher:
    """GUI启动器"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
    
    def setup_window(self):
        """设置窗口"""
        self.root.title("智能文件处理工具 - GUI启动器")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
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
    
    def create_widgets(self):
        """创建控件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(
            main_frame,
            text="🚀 智能文件处理工具",
            font=('Arial', 18, 'bold')
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(
            main_frame,
            text="选择您喜欢的GUI界面版本",
            font=('Arial', 10)
        )
        subtitle_label.pack(pady=(0, 30))
        
        # GUI版本选择
        versions_frame = ttk.LabelFrame(main_frame, text="可用的GUI版本", padding="20")
        versions_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # 原版GUI
        original_frame = self.create_version_card(
            versions_frame,
            "📝 原版GUI",
            "简单实用的基础界面",
            ["基本文件处理", "简单操作", "轻量级"],
            "gui.py",
            "#6c757d"
        )
        original_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 现代化GUI
        modern_frame = self.create_version_card(
            versions_frame,
            "🎨 现代化GUI",
            "功能丰富的标签页界面",
            ["选项卡界面", "进度显示", "结果查看", "配置管理"],
            "modern_gui.py",
            "#3498db"
        )
        modern_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 高级GUI
        premium_frame = self.create_version_card(
            versions_frame,
            "✨ 高级GUI",
            "专业级的卡片式布局界面",
            ["卡片式设计", "实时统计", "动画效果", "报告导出"],
            "premium_gui.py",
            "#2ecc71"
        )
        premium_frame.pack(fill=tk.X)
        
        # 底部按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        # 命令行版本按钮
        cli_button = ttk.Button(
            button_frame,
            text="🖥️ 使用命令行版本",
            command=self.show_cli_info
        )
        cli_button.pack(side=tk.LEFT)
        
        # 关闭按钮
        close_button = ttk.Button(
            button_frame,
            text="关闭",
            command=self.root.quit
        )
        close_button.pack(side=tk.RIGHT)
    
    def create_version_card(self, parent, title, description, features, script_name, color):
        """创建版本卡片"""
        # 主框架
        card_frame = tk.Frame(parent, relief='ridge', bd=1, bg='white')
        
        # 标题区域
        title_frame = tk.Frame(card_frame, bg=color, height=40)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text=title,
            font=('Arial', 12, 'bold'),
            fg='white',
            bg=color
        )
        title_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        # 启动按钮
        launch_button = tk.Button(
            title_frame,
            text="启动",
            font=('Arial', 9),
            bg='white',
            fg=color,
            relief='flat',
            padx=15,
            command=lambda: self.launch_gui(script_name, title)
        )
        launch_button.pack(side=tk.RIGHT, padx=15, pady=8)
        
        # 内容区域
        content_frame = tk.Frame(card_frame, bg='white', padx=15, pady=15)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 描述
        desc_label = tk.Label(
            content_frame,
            text=description,
            font=('Arial', 10),
            fg='#333333',
            bg='white'
        )
        desc_label.pack(anchor=tk.W, pady=(0, 10))
        
        # 特性列表
        features_label = tk.Label(
            content_frame,
            text="特性:",
            font=('Arial', 9, 'bold'),
            fg='#666666',
            bg='white'
        )
        features_label.pack(anchor=tk.W)
        
        for feature in features:
            feature_label = tk.Label(
                content_frame,
                text=f"• {feature}",
                font=('Arial', 9),
                fg='#666666',
                bg='white'
            )
            feature_label.pack(anchor=tk.W, padx=(10, 0))
        
        return card_frame
    
    def launch_gui(self, script_name, gui_name):
        """启动指定的GUI"""
        script_path = Path(__file__).parent / script_name
        
        if not script_path.exists():
            messagebox.showerror(
                "错误",
                f"GUI文件不存在: {script_name}\n请确保文件在当前目录中。"
            )
            return
        
        try:
            # 启动GUI
            if sys.platform == "win32":
                subprocess.Popen([sys.executable, str(script_path)], 
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen([sys.executable, str(script_path)])
            
            # 显示启动消息
            messagebox.showinfo("启动", f"{gui_name} 已启动！")
            
        except Exception as e:
            messagebox.showerror(
                "启动失败",
                f"无法启动 {gui_name}:\n{str(e)}"
            )
    
    def show_cli_info(self):
        """显示命令行版本信息"""
        info_window = tk.Toplevel(self.root)
        info_window.title("命令行版本使用说明")
        info_window.geometry("600x400")
        info_window.resizable(False, False)
        
        # 居中显示
        info_window.update_idletasks()
        width = info_window.winfo_width()
        height = info_window.winfo_height()
        x = (info_window.winfo_screenwidth() // 2) - (width // 2)
        y = (info_window.winfo_screenheight() // 2) - (height // 2)
        info_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # 内容
        content_frame = ttk.Frame(info_window, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(
            content_frame,
            text="🖥️ 命令行版本使用说明",
            font=('Arial', 14, 'bold')
        )
        title_label.pack(pady=(0, 20))
        
        # 使用说明文本
        usage_text = """基本用法:
python improved_main.py <输入路径> <输出路径> [选项]

示例:
# 处理单个文件
python improved_main.py document.txt output.txt

# 批量处理文件夹
python improved_main.py input_folder/ output_folder/

# 输出JSON格式
python improved_main.py document.txt result.json --format json

# 查看配置
python improved_main.py --config

# 启用详细日志
python improved_main.py document.txt output.txt --verbose

可用选项:
--format, -f    输出格式 (summary, json, text)
--config, -c    显示当前配置
--verbose, -v   启用详细日志输出
--version       显示版本信息
--help, -h      显示帮助信息

有关更多信息，请查看 README_improved.md 文件。"""
        
        text_widget = tk.Text(
            content_frame,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg='#f8f9fa',
            fg='#212529',
            relief='flat',
            bd=1
        )
        text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        text_widget.insert(1.0, usage_text)
        text_widget.config(state='disabled')
        
        # 关闭按钮
        close_btn = ttk.Button(
            content_frame,
            text="关闭",
            command=info_window.destroy
        )
        close_btn.pack()
    
    def run(self):
        """运行启动器"""
        self.root.mainloop()

def main():
    """主函数"""
    try:
        launcher = GUILauncher()
        launcher.run()
    except Exception as e:
        print(f"启动器运行失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()