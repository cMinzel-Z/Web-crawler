import scrapy
import pandas as pd
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup


class ActivitySpider12(CrawlSpider):
    name = "act12"
    allowed_domains = ["freedom-leisure.co.uk"]
    start_urls = ["https://www.freedom-leisure.co.uk/centres/morriston-leisure-centre/"]
    rules = (
        Rule(callback='parse_item', follow=True),
    )
    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 5,
        'CLOSESPIDER_PAGECOUNT': 100,
        'CLOSESPIDER_ERRORCOUNT': 20
    }

    def parse_item(self, response):
        try:
            web_text = response.text
        except:
            web_text = ""
        act_list = ["Gym Suite", "Gym Studio", "Swimming Pool", "Swim Fit",
                "Lane swimming", "leisure pool", "Squash Court",
                "Badminton Court", "Fitness Suite", "Personal Training",
                "Gymnastics", "Aerobic Classes", "Yoga", "Pilates",
                "Zumba", "Dance Class", "Dance Aerobics", "Toning Class",
                "Step Class", "strength and conditioning studio",
                "strength and conditioning class", "strength and conditioning gym",
                "Total Body Conditioning", "Bum", "Leg", "Tum", "Power class",
                "Power class", "Walking group", "Aqua aerobics", "Water Workout",
                "Core stability", "HiTT Workout", "Martial Arts Class", "Karate Class",
                "Cycle studio", "Group cycle", "Training", "Triathlon club",
                "Football", "5 a side football", "Trampolining", "Volleyball",
                "Netball", "Basketball", "Boxfit", "Boxing", "Interval fitness",
                "Circuits"]
        act_list = [s.lower() for s in act_list]
        def checkActivity(act_list, web_text):
            exsit_list = []
            for text in act_list:
                if text in web_text:
                    exsit_list.append(text)
            return exsit_list

        def get_text_bs(html):
            tree = BeautifulSoup(html, 'lxml')

            body = tree.body
            if body is None:
                return None

            for tag in body.select('script'):
                tag.decompose()
            for tag in body.select('style'):
                tag.decompose()

            text = body.get_text(separator='\n')
            text = text.replace("\n", " ").replace("\t", " ").replace("\r", " ")
            return text.lower()

        web_text = get_text_bs(web_text)

        exsit_list = checkActivity(act_list, web_text)
        activities = ', '.join(exsit_list)
        start_url = ', '.join(self.start_urls)
        
        item = {}
        item['start_url'] = start_url
        item['activities'] = activities
        return item


process = CrawlerProcess(settings={
    "FEEDS": {
        "data/items_12.json": {"format": "json"},
    },
})

process.crawl(ActivitySpider12)
process.start()
