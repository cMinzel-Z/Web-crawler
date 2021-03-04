# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html, features="lxml")
images = bsObj.findAll("img",{"src":re.compile("\.\.\/img\/gifts/img.*\.jpg")})

for image in images:
    print(image["src"])
    # 获取属性
    print(image.attrs)
    # 访问属性
#    print(image.attrs["src"])
    print("-"*10)
    