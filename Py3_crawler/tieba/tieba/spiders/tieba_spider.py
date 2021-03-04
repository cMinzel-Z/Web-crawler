# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 16:01:57 2020

@author: Minzel
"""

import scrapy


class TiebaSpider(scrapy.Spider):
    name = 'tieba'

    start_urls = ['https://tieba.baidu.com/p/6724970612']

    def parse(self, response):
#        pagination_links = response.css('#frs_list_pager > a.next.pagination-item')
#        yield from response.follow_all(pagination_links, self.parse)
        pass

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'title': extract_with_css('.core_title_txt pull-left text-overflow::text'),
            'user': extract_with_css('.p_author_name j_user_card::text'),
            'reply': extract_with_css('.d_post_content j_d_post_content::text'),
        }