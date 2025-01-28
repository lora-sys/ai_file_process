# from file_handler import read_json_file,write_json_file
# file_path=r'E:\my_ai_file_project\data_test.json'
# read_json_file(file_path)
# data1 = {
#     "name": "John Doe",
#     "age": 30,
#     "city": "New York"
# }
# write_json_file(file_path,data1)
import spacy
nlp = spacy.load("zh_core_web_sm")
text = "这是一个测试"
doc = nlp(text)
print([token.text for token in doc])  # 期望输出：['这是', '一个', '测试']