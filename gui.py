import tkinter as tk
import os
from tkinter import filedialog
import main 

def select_input_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_path = os.path.abspath(file_path)
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename()
    if file_path:
        file_path = os.path.abspath(file_path)
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)

def process_file():
    input_file = input_entry.get()
    output_file = output_entry.get()
    if input_file and output_file:
        result = main.main(input_file, output_file)
        output_text.insert(tk.END, result + "\n")
    else:
        output_text.insert(tk.END, "错误：请选择输入文件和输出文件路径。\n")
def select_input_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, folder_path)

def process_folder():
    input_folder = input_entry.get()
    output_folder = output_entry.get()
    if input_folder and output_folder:
        main.batch_process(input_folder, output_folder)
        output_text.insert(tk.END, "批量处理完成！\n")
    else:
        output_text.insert(tk.END, "错误：请选择输入和输出文件夹。\n")
# 创建主窗口
root = tk.Tk()
root.title("文件处理工具")

# 输入文件路径
input_label = tk.Label(root, text="输入文件路径:")
input_label.pack()
input_entry = tk.Entry(root, width=50)
input_entry.pack()
input_button = tk.Button(root, text="选择文件", command=select_input_file)
input_button.pack()

# 输出文件路径
output_label = tk.Label(root, text="输出文件路径:")
output_label.pack()
output_entry = tk.Entry(root, width=50)
output_entry.pack()
output_button = tk.Button(root, text="选择输出文件", command=select_output_file)
output_button.pack()

# 处理按钮
process_button = tk.Button(root, text="处理文件", command=process_file)
process_button.pack()

# 显示区域
output_text = tk.Text(root, height=10, width=50)
output_text.pack()

root.mainloop()