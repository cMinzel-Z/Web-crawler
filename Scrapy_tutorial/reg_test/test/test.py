# -*- coding: utf-8 -*-

import re


#line = "booooooooooobby123"
#regex_str = "^b.*3$"
#res_match = re.match(regex_str, line)
#
#if res_match:
#    print("ok")

#line = "booooooooooobby123"
## 问号适用于非贪婪匹配
#regex_str = ".*?(b.*?b).*"
#res_match = re.match(regex_str, line)
#
#if res_match:
#    print(res_match.group(1))

#line = "boooobaaaooobbbbbby123"
## 问号适用于非贪婪匹配
#regex_str = ".*(b.+b).*"
#res_match = re.match(regex_str, line)
#
#if res_match:
#    print(res_match.group(1))

line = "18782902222"

regex_str = "(1[34578][0-9]{9})"
res_match = re.match(regex_str, line)

if res_match:
    print(res_match.group(1))