# -*- coding: utf-8 -*-

import json
from urllib.parse import urlparse
import sys
import scrapy
from scrapy import Request, spidermiddlewares
from .phones import Phones
from .logo import Logo


class CrawlerSpider(scrapy.Spider):
    """Main class to crawler websites."""
    name = "Crawler"

    logo = Logo()
    phones = Phones()

    allowed_domains = []
    start_urls = []

    def save_file(self, data: dict):
        """Create stout file in json format."""
        sys.stdout = open('crawler/spiders/website_data.json', 'a+')
        json.dump(data, sys.stdout, indent=4, separators=(',', ':'))
        sys.stdout.close()

    def start_requests(self):
        """Create requests."""
        with sys.stdin as f:
            urls = [x.strip() for x in f.readlines()]
        self.allowed_domains = [urlparse(url).hostname for url in urls]
        self.start_urls = self.allowed_domains

        for mw in self.crawler.engine.scraper.spidermw.middlewares:
            if isinstance(mw, spidermiddlewares.offsite.OffsiteMiddleware):
                mw.spider_opened(self)
        for url in urls:
            yield Request(url)

    def parse(self, response):
        """
        Method is in charge of processing the response
        and returning scraped data.
        """
        data = {'logo': self.logo.get_logo(response),
                'phones': self.phones.get_phones(response),
                'website': response.request.url
                }

        self.save_file(data)
