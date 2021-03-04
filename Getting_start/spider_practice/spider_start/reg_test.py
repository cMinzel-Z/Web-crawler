# -*- coding: utf-8 -*-

import re

# \d{4}
1999-8-1

# b{2,4}
# (o|c)b
"bobby"
"ccbbc"

# \d{4}(y|-)
"1999y8m1d"
1998-8-1



info = "name:bobby dob:1987-10-1 ug:2005-9-1"

# 提取字符串
#print(re.findall("\d{4}", info))
# match方法是从字符串的最开始进行匹配
match_res = re.match(".*dob.*?(\d{4})", info)
#print(match_res.group(1))

# 替换字符串
result = re.sub("\d{4}", "2019", info)
#print(info)
#print(result)

# 搜索字符串
search_res = re.search("dob.*?(\d{4})", info)
#print(search_res)


#name = "my name is Bobby"
#print(re.search("bobby", name, re.IGNORECASE).group())

name = """
my name is 
bobby
"""
print(re.match(".*bobby", name, re.DOTALL).group())

