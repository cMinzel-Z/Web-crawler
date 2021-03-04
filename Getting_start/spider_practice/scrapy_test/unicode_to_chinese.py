# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 19:25:03 2020

@author: Minzel
"""


import json
 

# 这是json文件存放的位置
json_filename = './csdn.json' 

# 这是保存处理后文件的位置
final_filename = './finnal.json'   
    
# 用来存储数据
data = {}

with open(json_filename) as json_file:
    data = json.load(json_file)
    for key in data:
        key["title"] = key["title"].encode("utf-8").decode("utf-8")
        key["author"] = key["author"].encode("utf-8").decode("utf-8")

# 检查是否转码成功
print(data[1200])

with open(final_filename, 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile, ensure_ascii=False)
