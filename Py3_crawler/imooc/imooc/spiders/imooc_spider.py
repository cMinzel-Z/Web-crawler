# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 17:07:04 2020

@author: Minzel
"""

import scrapy


class ImoocSpider(scrapy.Spider):
    name = 'imooc'

    start_urls = ['https://coding.imooc.com/learningpath/list?cate=hot&page=1']

    def parse(self, response):
        pagination_links = response.css('.page > a:nth-last-child(2)')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'title': extract_with_css('.courseitem > h2::text'),
            'content': extract_with_css('.courseitem > p::text'),
        }