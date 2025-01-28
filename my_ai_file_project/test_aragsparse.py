import argparse
parse=argparse.ArgumentParser(description="这是一个简单的命令行参数实例")
#添加命令行参数
parse.add_argument("-f","--file",type=str,help="输入文件路径",required=True)
parse.add_argument("-d","--delimiter",type=str,default=',',help='CSV文件分隔符')
parse.add_argument("-q","--quotechar",type=str,default='"',help='CSV文件的引号字符')
parse.add_argument("-o","--output",type=str,default='output.txt',help='输出文件路径')
#解析命令行参数
args=parse.parse_args()
#使用解析后参数
print(f"输入文件：{args.file}")
print(f"分隔符：{args.delimiter}")
print(f"引号字符：{args.quotechar}")
print(f"输出文件：{args.output}")
