# -*- coding: utf-8 -*-

from scrapy import Selector


html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>bobby基本信息</title>
</head>
<body>
    <div id="info">
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

sel = Selector(text=html)

name_xpath = "//*[@id='info']/div/p[1]/text()"
name = ""
tag_texts = sel.xpath(name_xpath).extract()
if tag_texts:
    name = tag_texts[0]
print(name)


info = sel.xpath("//div[contains(@class, 'teacher_info')]/p[last()]/text()").extract()[0]
print(info)

info_class = sel.xpath("//div[contains(@class, 'teacher_info')]/p[last()]/@class").extract()[0]
print(info_class)

teacher_info = sel.xpath("//p[@class='age']|//p[@class='work_years']").extract()
print(teacher_info)
#tag = sel.xpath("//*[@id='info']/div/p[1]").extract()
#print(tag)

#tag = sel.xpath("//*[@id='info']/div/p[1]/text()").extract()
#print(tag)