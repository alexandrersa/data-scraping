# -*- coding: utf-8 -*-

import scrapy
import sys
import pandas as pd
from urllib.parse import urlparse
from scrapy import Spider, Request, spidermiddlewares

class CrawlerSpider(scrapy.Spider):

    name = "Crawler"

    allowed_domains = []
    start_urls = []
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'

    def start_requests(self):
        with sys.stdin as f:
            urls = [x.strip() for x in f.readlines()]
        self.allowed_domains = [urlparse(url).hostname for url in urls]
        self.start_urls = self.allowed_domains
        # Refresh the regex cache for `allowed_domains`
        # thx to - http://stackoverflow.com/questions/5161815/dynamically-add-to-allowed-domains-in-a-scrapy-spider
        for mw in self.crawler.engine.scraper.spidermw.middlewares:
            if isinstance(mw, spidermiddlewares.offsite.OffsiteMiddleware):
                mw.spider_opened(self)
        for url in urls:
                yield Request(url)

    def clean_url(self, url):
        url = url.replace("['", "")
        url = url.replace("']", "")
        url = url.lower()
        return url

    def parse(self, response):
        ext_list = [".png", ".gif", ".jpg", ".tif", ".tiff", ".bmp", ".svg"]

        # Extract the Home Page Address or Website First Page Address
        str_url = str(response.url).lower()
        parts = len(str_url.split("/"))
        if len(str_url.split("/")[parts - 1]) == 0:
            homepage = str_url.split("/")[parts - 2]
        else:
            homepage = str_url.split("/")[parts - 1]
        print(homepage)

        img_url_list = []

        ### Case 1: when <a> contains <img> with logo substring in its @src
        CHECK = False
        for tag_a in response.xpath('//a'):
            for tag_img in tag_a.xpath('.//img'):
                img_url = str(tag_img.xpath('@src').extract())
                img_url = self.clean_url(img_url)
                ind = img_url.find('logo')
                if ind > 0:
                    CHECK = True
                    img_url_list.append(img_url)

        ### Case 2: when <div> contains <img>  with logo substring in its @src
        if not CHECK:
            for tag_div in response.xpath('//div'):
                for tag_img in tag_div.xpath('.//img'):
                    img_url = str(tag_img.xpath('@src').extract())
                    img_url = self.clean_url(img_url)
                    ind = img_url.find('logo')
                    if ind > 0:
                        CHECK = True
                        img_url_list.append(img_url)

        ### Case 3: when <a> contains @href as home page address or index. and
        # <img> with possible file extension as like (.png, .gif, .jpg etc) and logo substring in its @class or @title or @alt
        if not CHECK:
            for tag_a in response.xpath('//a'):
                a_href = str(tag_a.xpath('@href').extract())
                a_href = self.clean_url(a_href)
                if a_href[:6] == str("index.") or a_href == homepage:
                    for tag_img in tag_a.xpath('.//img'):
                        img_url = str(tag_img.xpath('@src').extract())
                        img_url = self.clean_url(img_url)
                        img_name, img_ext = os.path.splitext(img_url)

                        tag_class = str(tag_img.xpath('@class').extract()).lower().strip()
                        title = str(tag_img.xpath('@title').extract()).lower().strip()
                        alt = str(tag_img.xpath('@alt').extract()).lower().strip()

                        if img_ext in ext_list or tag_class.find("logo") > 0 or title.find("logo") > 0 or \
                                alt.find("logo") > 0:
                            CHECK = True
                            img_url_list.append(img_url)

        data = {'img_url_list':img_url_list}
        df = pd.DataFrame(data)
        filename = homepage + '.csv'
        print(filename)
        df.to_csv(filename)
