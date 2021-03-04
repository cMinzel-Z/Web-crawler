# -*- coding: utf-8 -*-
import re
import json
from urllib import parse

import scrapy
#from scrapy.loader import ItemLoader
from scrapy import Request

from ArticleSpider.utils.common import get_md5
from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['http://news.cnblogs.com/']

    def parse(self, response):
        """
        1. 获取新闻列表页的所有URL
        2. 获取下一页的URL
        """
    #    url = response.xpath('//*[@class="news_entry"]/a/@href').extract_first("")
    #    urls = response.css('.news_entry a::attr(href)').extract()
        post_nodes = response.css('#news_list .news_block')[:1]
        for post_node in post_nodes:
            image_url = post_node.css('.entry_summary a img::attr(src)').extract_first("")
            if image_url.startswith("//"):
                image_url = "https:" + image_url
            post_url = post_node.css('h2 a::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url":image_url}, callback=self.parse_detail)
                
        # 提取下一页
        next_url = response.css("div.pager a:last-child::text").extract_first("")
        if next_url =="Next >":
            next_url = response.css("div.pager a:last-child::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
                         
    def parse_detail(self, response):
        match_re = re.match(".*?(\d+)", response.url)
        if match_re:
            post_id = match_re.group(1)
                
#            article_item = JobBoleArticleItem()
#            title = response.css("#news_title a::text").extract_first("")
#            create_date = response.css(".time::text").extract_first("")
#            match_re = re.match(".*?(\d+.*)", create_date)
#            if match_re:
#                create_date = match_re.group(1)
#            content = response.css("#news_content").extract_first()
#            tag_list = response.css(".news_tags a::text").extract()
#            tags = ",".join(tag_list)
#    #        html = requests.get(parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)))
#                
#            article_item["title"] = title
#            article_item["create_date"] = create_date
#            article_item["content"] = content
#            article_item["tags"] = tags
#            article_item["url"] = response.url
#            if response.meta.get("front_image_url", ""):
#                article_item["front_image_url"] = [response.meta.get("front_image_url", "")]
#            else:
#                article_item["front_image_url"] = []
               
            item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
            item_loader.add_css("title", "#news_title a::text")
            item_loader.add_css("content", "#news_content")
            item_loader.add_css("tags", ".news_tags a::text")
            item_loader.add_css("create_date", ".time::text")
            item_loader.add_value("url", response.url)
            if response.meta.get("front_image_url", []):
                item_loader.add_value("front_image_url", response.meta.get("front_image_url", []))
            
#            article_item = item_loader.load_item()
                
            yield Request(url=parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)), 
                          meta={"article_item":item_loader, "url": response.url}, callback=self.parse_nums)     
                
    def parse_nums(self, response):
        j_data = json.loads(response.text)   
        item_loader = response.meta.get("article_item", "")
            
#        praise_nums = j_data["DiggCount"]
#        fav_nums = j_data["TotalView"]
#        comment_nums = j_data["CommentCount"]
        
        item_loader.add_value("praise_nums", j_data["DiggCount"])
        item_loader.add_value("fav_nums", j_data["TotalView"])
        item_loader.add_value("comment_nums", j_data["CommentCount"])
        item_loader.add_value("url_object_id", get_md5(response.meta.get("url", "")))
        
#        article_item["praise_nums"] = praise_nums
#        article_item["fav_nums"] = fav_nums
#        article_item["comment_nums"] = comment_nums
#        article_item["url_object_id"] = common.get_md5(article_item["url"])
        article_item = item_loader.load_item()
        
        yield article_item