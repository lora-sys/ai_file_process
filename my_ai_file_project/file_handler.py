import csv
import json
import logging
logging.basicConfig(filename='fileerror.log',level=logging.ERROR,format='%(asctime)s -%(levelname)s-%(message)s',encoding='utf-8')
def read_file(file_path):
    """
    读取指定路径内的文件内容并返回字符串
    """
    try:
        with open(file_path,'r',encoding='utf-8') as file:
            content=file.read()
            return content;
    except FileNotFoundError:
        print(f"错误：文件{file_path}没有找到")
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return None
    
def wirte_file(file_path,content,mode="w"):
    """
    将内容写入指定路径的文件
    mode 参数可以是 'w' (写入) 或 'a' (追加)，默认为 'w'
    """
    try :
        with open(file_path,mode,encoding='utf-8') as file:
            file.write(content)
            print(f"内容成功写入文件 {file_path}成功！")
    except Exception as e:
        print(f"写入文件时发生错误：{e}")
def read_file_readlines(file_path):
    """
    读取文件一行内容并返回一行内容,返回一个包括所有行列表
    """
    # """
    # 读取指定路径的文件内容，并返回一个去除换行符的行列表。
    # Args:
    #     file_path (str): 文件路径。
    # Returns:
    #     list or None: 包含去除换行符的字符串的列表，如果读取文件失败则返回 None。
    # """
    try:
        with open(file_path,'r',encoding='utf-8') as file:
            lines=file.readlines()
            stripped_lines=[]
            for line in lines:
                stripped_lines.append(line.rstrip('\n'))
            return stripped_lines
    except FileNotFoundError:
        print(f"错误： 文件没有找到{file_path}")
        return None
    except Exception as e:
        print(f"读取文件时发生错误 : {e}")
        return None
def read_file_readline(file_path):
    """
    读取文件一行内容并返回一行内容,返回一行
    """
    try:
        with open(file_path,'r',encoding='utf-8') as file:
            while(True):
                line=file.readline()
                if not line:
                    break
                print(line,end='')#避免重复换行
               
    except FileNotFoundError:
        print(f"错误： 文件没有找到{file_path}")
        return None
    except Exception as e:
        print(f"读取文件时发生错误 : {e}")
        return None   
def read_csv_file(file_path,delimiter=',',quotechar='"'):
    """
    读取指定路径csv文件,返回包括一个包含所有行的列表
    args;
    file_path:(str):文件路径
    delimiter (str, optional): 分隔符，默认为逗号 (,)。
        quotechar (str, optional): 引号字符，默认为双引号 (").
    returns :
      list or None:包括所有行的列表,如果读取文件夹失败则返回None
    """
    try:
        with open(file_path,'r',encoding='utf-8') as file:
            reader=csv.reader(file,delimiter=delimiter,quotechar=quotechar)
            lines=list(reader)
            return lines
    except FileNotFoundError:
        print(f"错误：文件'{file_path}'未找到。")
        return None
    except Exception as e:
        print(f"读取文件发生错误：{e}")
        return None
def write_csv_file(file_path,data,headers=None,delimiter=',',quotechar='"'):
    """
      将数据写入指定路径的 CSV 文件。
      headers (list, optional): CSV 文件的表头。
        delimiter (str, optional): 分隔符，默认为逗号 (,)。
        quotechar (str, optional): 引号字符，默认为双引号 (").
  Args:
      file_path (str): 文件路径。
      data (list): 需要写入的数据。
      headers (list, optional): CSV 文件的表头
    """
    try :
        with open(file_path,'w',encoding='utf-8',newline='') as file:
            writer=csv.writer(file,delimiter=delimiter,quotechar=quotechar)
            if headers:
                writer.writerow(headers)#将第一行作为数据表头
            writer.writerows(data)
            print(f"内容写入文件：'{file_path}'成功")
    except Exception as e:
        print(f'写入文件发生错误： {e}')
def read_json_file(file_path):
    """
    读取 JSON 文件并返回解析后的 Python 数据结构。

    Args:
        file_path (str): JSON 文件的路径。

    Returns:
        dict or list or None: 如果成功读取 JSON 文件，则返回解析后的 Python 数据结构（字典或列表）。
                           如果文件无法读取或解析，则返回 None。

    Raises:
        IOError: 如果发生输入输出错误 (例如, 没有权限访问文件, 文件路径指向目录)。
    """
    try :
        with open(file_path,'r',encoding='utf-8') as file:
            data=json.load(file)
            return data 
    except FileNotFoundError:
        logging.error(f'文件未找到：{file_path}')
        return None
    except PermissionError:
        logging.error(f'没有权限访问文件：{file_path}')
        raise IOError(f'没有权限访问文件：{file_path}')
    except IsADirectoryError:
        logging.error(f'文件路径指向目录而不是文件：{file_path}')
        raise IOError(f'文件路径指向目录而不是文件：{file_path}')
    except json.JSONDecodeError:
        logging.error(f'json文件格式不正确:{file_path}')
        return None
    except OSError as e:
        logging.error(f'发生其他错误i/0错误,错误信息：{file_path}')
        raise IOError(f'发生其他错误i/0错误,错误信息：{file_path}')
     
def write_json_file(file_path,data):
    """
    将 Python 数据结构写入 JSON 文件。

    Args:
        file_path (str): JSON 文件的路径。
        data (dict or list): 要写入的 Python 数据结构。

    Returns:
        bool: 如果成功写入，返回 True,否则返回 False。

    Raises:
        IOError: 如果发生输入输出错误（如文件无法打开、磁盘空间不足等）。
    """
    try :
         with open(file_path,'w',encoding='utf-8') as file:
             json.dump(data,file,indent=4,ensure_ascii=False)
             return True
    except FileNotFoundError:
        logging.error(f'文件未找到：{file_path}')
        return None
    except PermissionError:
        logging.error(f'没有权限访问文件：{file_path}')
        raise IOError(f'没有权限访问文件：{file_path}')
    except IsADirectoryError:
        logging.error(f'文件路径指向目录而不是文件：{file_path}')
        raise IOError(f'文件路径指向目录而不是文件：{file_path}')
    except json.JSONDecodeError:
        logging.error(f'json文件格式不正确:{file_path}')
        return None
    except OSError as e:
        logging.error(f'发生其他错误i/0错误,错误信息：{file_path}')
        raise IOError(f'发生其他错误i/0错误,错误信息：{file_path}') 
    return False               

