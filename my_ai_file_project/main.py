from file_handler import read_file ,read_csv_file,write_csv_file
from file_handler import wirte_file,read_file_readline,read_file_readlines
from data_processor import filter_characters,parse_numbers,data_process,parse_date
from ai_model import analyze_sentiment
import argparse
# def main():
    
#     # wirte_file('output_w_.txt','你好 world\n',mode='w')
#     # wirte_file('output_a_.txt','你好 世界\n',mode='a')
#     file_path='E:\my_ai_file_project\data.txt'
#     file_content=read_file(file_path);
#     if file_content:
#         print("文件内容如下：")
#         print(file_content)
#     else:
#         print("无法读取文件")
# def main():
#     #读取测试readlines
#     file_path='E:\my_ai_file_project\data.txt'
#     stripped_lines=read_file_readlines(file_path)
#     if stripped_lines:
#         print("去除换行符后的列表")
#         for line in stripped_lines:
#             print(line)
#     else:
#         print("无法读取文件没无法进行后续操作")


    # file_content_readlines=read_file_readlines(file_path)
    # if file_content_readlines:
    #     print("\n文件内容如下")
    #     print(file_content_readlines)
    # else:
    #     print("\n无法读取文件")
    # #读取测试readline
    # read_file_readline(file_path)
# def main():
#     file_path='E:\my_ai_file_project\data.txt'
#     stripped_lines=read_file_readlines(file_path)
#     if stripped_lines :
#         #进行数据处理
#         process_lines=[]
#         for line in stripped_lines:
#             line=data_process(line)
#             line=filter_characters(line,"!@#$%^&*()_+=-`~")#去除特殊字符
#             number=parse_numbers(line)
#             date=parse_date(line)

#             if number is not None:
#                 process_lines.append(f"number,{number},sentiment,中性")
#             elif date is not None:
#                 process_lines.append(f"Date: {date},sentiment,中性")
#             else:
#                 sentiment_scores=analyze_sentiment(line)
#                 process_lines.append(f"Text:{line},sentiment:{sentiment_scores}")
#             # process_lines.append(line)
#         process_content="\n".join(process_lines)#用换行符连接处理后的数据
#         wirte_file("process_data.txt",process_content)
#     else:
#         print("无法读取新文件，无法进行数据处理")
def main():
    # file_path=r'E:\my_ai_file_project\csv_data.csv'
    # delimiter=';'#set new delimiter
    # quotechar='"'#set new quotechar
    parser=argparse.ArgumentParser(description='这是一个简单的命令行参数实例')
    parser.add_argument("-f", "--file", type=str, help="输入文件路径", required=True)
    parser.add_argument("-d", "--delimiter", type=str, default=";", help="CSV文件的分隔符")
    parser.add_argument("-q", "--quotechar", type=str, default='"', help="CSV文件的引号字符")
    parser.add_argument("-op","--operation",type=str,default='sentiment',choices=['sentiment','keywords','classify'],help='选择操作类型')
    parser.add_argument("-o","--output",type=str,default='process_file_data.csv',help='输出文件路径')
    args=parser.parse_args()
    file_path=args.file
    delimiter=args.delimiter
    quotechar=args.quotechar
    output_file=args.output
    csv_lines=read_csv_file(file_path,delimiter=delimiter,quotechar=quotechar)
    if csv_lines:
        process_lines=[]
        headers=csv_lines[0]
        for line in csv_lines[1:]:#跳过表头
            if len(line)>=2:
                text=line[1]
                line[1]=data_process(line[1])
                line[1]=filter_characters(line[1],"!@#$%^&*()_+=-`~")
                if args.operation=="sentiment":
                    sentiment_scores=analyze_sentiment(line[1])
                    line.append(str(sentiment_scores))#添加情感得分
                elif args.operation=="keywords":
                    line.append(f'keywords analysis is not inplemented yet')
                elif args.operation=='classify':
                    line.append(f"text classification is not inplemented yet")
                process_lines.append(line)
            else:
                print(f'跳过数据格式不正确的行：{line}')#打印数据格式不正确的行
        headers.append("sentiement")#添加新的表头
        write_csv_file("process_file_data.csv",process_lines,headers,delimiter=delimiter,quotechar=quotechar)
    else:
        print(f'无法读取文件,无法进行数据处理')




if __name__=='__main__':
    main()