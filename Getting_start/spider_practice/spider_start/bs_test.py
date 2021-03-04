# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>bobby基本信息</title>
</head>
<body>
    <div id="info-955">
        <p style="color: blue">讲师信息</p>
        <div class="teacher_info info">
            python全栈工程师，7年工作经验，喜欢钻研python技术，对爬虫、
            web开发以及机器学习有浓厚的兴趣，关注前沿技术以及发展趋势。
            <p class="age">年龄: 29</p>
            <p class="name">姓名: bobby</p>
            <p class="work_years">工作年限: 7年</p>
            <p class="position">职位: python开发工程师</p>
        </div>
        <p style="color: aquamarine">课程信息</p>
        <table class="courses">
          <tr>
            <th>课程名</th>
            <th>讲师</th>
            <th>地址</th>
          </tr>
          <tr>
            <td>django打造在线教育</td>
            <td>bobby</td>
            <td><a href="https://coding.imooc.com/class/78.html">访问</a></td>
          </tr>
          <tr>
            <td>python高级编程</td>
            <td>bobby</td>
            <td><a href="https://coding.imooc.com/class/200.html">访问</a></td>
          </tr>
          <tr>
            <td>scrapy分布式爬虫</td>
            <td>bobby</td>
            <td><a href="https://coding.imooc.com/class/92.html">访问</a></td>
          </tr>
          <tr>
            <td>django rest framework打造生鲜电商</td>
            <td>bobby</td>
            <td><a href="https://coding.imooc.com/class/131.html">访问</a></td>
          </tr>
          <tr>
            <td>tornado从入门到精通</td>
            <td>bobby</td>
            <td><a href="https://coding.imooc.com/class/290.html">访问</a></td>
          </tr>
        </table>
    </div>

</body>
</html>
"""

bs = BeautifulSoup(html, "html.parser")
#title_tag = bs.title
#print(title_tag.string)

#找到第一个元素
#div_tag = bs.find("div")
#找到所有元素
#div_tags = bs.find_all("div")
#for tag in div_tags:
#    print(tag.string)

#div_tag = bs.find("div", id="info")
div_tag = bs.find("div", id=re.compile("info-\d+"))
#childrens = div_tag.contents
#for child in childrens:
#    print(child.name)
#div_tag = bs.find(string="scrapy分布式爬虫")
#div_tag = bs.find(string=re.compile("scrapy"))
#    
#childrens = div_tag.descendants
#for child in childrens:
#    if child.name:
#        print(child.name)

parents = bs.find("p", {"class":"name"}).parents
#for parent in parents:
#    print(parent.name)


#next_siblings = bs.find("p", {"class":"name"}).next_siblings
#for sibling in next_siblings:
#    print(sibling.string)

#previous_siblings = bs.find("p", {"class":"name"}).previous_siblings
#for sibling in previous_siblings:
#    print(sibling.string)

name_tag = bs.find("p", {"class":"name"})
print(name_tag["class"])
print(name_tag.get("class"))
