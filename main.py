from file_handler import read_file, wirte_file,read_pdf,read_excel,read_csv_file,read_json_file
from data_processor import process_text
import argparse
import os

def process_file(input_path, output_path):
    """
    处理单个文件
    """
    try:
        content = read_file(input_path)
        if content is not None:
            processed_content = process_text(content)
            wirte_file(output_path, processed_content)
            print(f"文件 {input_path} 处理完成，结果已保存到 {output_path}")
    except Exception as e:
        print(f"处理文件时出错：{e}")
def batch_process(input_folder, output_folder):
    """
    批量处理文件
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename + ".processed")

        # 根据文件类型选择不同的处理函数
        if filename.endswith(".pdf"):
            content = read_pdf(input_path)
        elif filename.endswith(".xlsx"):
            content = read_excel(input_path)
        else:
            content = read_file(input_path)

        if content is not None:
            processed_content = process_text(content)
            wirte_file(output_path, processed_content)


def main():
    parser = argparse.ArgumentParser(description="智能文件处理工具")
    parser.add_argument("input", help="输入文件或文件夹路径")
    parser.add_argument("output", help="输出文件或文件夹路径")
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    if os.path.isfile(input_path):
        process_file(input_path, output_path)
    elif os.path.isdir(input_path):
        batch_process(input_path, output_path)
    else:
        print("错误：输入路径无效")

if __name__ == '__main__':
    main()