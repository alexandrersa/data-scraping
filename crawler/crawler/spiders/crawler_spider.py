# -*- coding: utf-8 -*-

'''
Has proposes create a feature to import logo and distinct phone numbers, from
defined websites in file websites.txt.
'''

import json
from urllib.parse import urlparse
import sys
import logging
from scrapy.utils.log import configure_logging
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
        sys.stdout = open('data.json', 'a+')
        json.dump(data, sys.stdout, indent=4, separators=(',', ':'))
        sys.stdout.close()

    def start_requests(self):
        """Create requests."""
        with sys.stdin as f:
            urls = [x.strip() for x in f.readlines()]
        self.allowed_domains = [urlparse(url).hostname for url in urls]
        self.start_urls = self.allowed_domains

        configure_logging(install_root_handler=False)
        logging.basicConfig(
            filename='log.txt',
            format='%(levelname)s: %(message)s',
            level=logging.INFO
        )
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/51.0.2704.84 Safari/537.36',
            'Accept': 'application/json,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
        }
        for mw in self.crawler.engine.scraper.spidermw.middlewares:
            if isinstance(mw, spidermiddlewares.offsite.OffsiteMiddleware):
                mw.spider_opened(self)
        for url in urls:
            yield Request(url, headers=headers)

    def parse(self, response):
        """
        Method is in charge of processing the response
        and returning scraped data.
        """
        self.logger.info('Parse function called on %s', response.url)
        data = {'logo': self.logo.get_logo(response),
                'phones': self.phones.get_phones(response),
                'website': response.request.url
                }

        self.save_file(data)
