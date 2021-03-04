# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 16:01:58 2020

@author: Minzel
"""

# 1.解析xml的方式：
from lxml import etree
# 创建ElementTree对象解析xml文本
tree= etree.parse('text.xml')

# 2.解析html的方式：
#from lxml import etree
##创建ElementTree对象解析xml文本
#tree= etree.HTML('test.html')

tags = tree.xpath("/people/person/name/text()")
print(tags)
#for tag in tags:
#    print(tag)

print(tree.xpath("node()/text()"))
