# -*- coding: utf-8 -*-


class Logo(object):

    def extract_home_page(self, response) -> str:
        """Extract the Home Page Address or Website First Page Address.
        :param response:
        :return:
        """
        str_url = str(response.url).lower()
        parts = str_url.split("/")
        homepage = parts[2]
        protocol = parts[0]
        url = '{}//{}'.format(protocol, homepage)
        return url

    def clean_url(self, url: str) -> str:
        """This feature will normalize url."""
        try:
            url = url.replace("['", "")
            url = url.replace("']", "")
        except Exception:
            pass
        return url

    def get_logo(self, response) -> str:
        """Instance to find logo url in website."""
        ### Case 1: when <a> contains <img> with logo substring in its @src
        CHECK = False
        logo_path = None

        for tag_a in response.xpath('//a'):
            for tag_img in tag_a.xpath('.//img'):
                img_url = str(tag_img.xpath('@src').extract())

                if 'logo' in img_url.lower():
                    CHECK = True

                    if "http" in img_url:
                        logo_path = img_url
                    else:
                        img_url = self.clean_url(img_url)
                        logo_path = self.extract_home_page(response) + img_url

        ### Case 2: when <div> contains <img>  with logo substring in its @src
        if not CHECK:
            for tag_div in response.xpath('//div'):
                for tag_img in tag_div.xpath('.//img'):
                    img_url = str(tag_img.xpath('@src').extract())
                    ind = img_url.find('logo')
                    if img_url and ind > 0:
                        CHECK = True
                        if "http" in img_url:
                            logo_path = img_url
                        else:
                            img_url = self.clean_url(img_url)
                            logo_path = self.extract_home_page(response) + img_url

        ### Case 3: when <a> contains <img> with logo substring in its @class
        if not CHECK:
            for tag_a in response.xpath('//a'):
                img_url = tag_a.xpath('.//img[contains(@class,"logo")]/@src').extract()

                if img_url:
                    CHECK = True
                    if isinstance(img_url, list):
                        for i in img_url:
                            if "http" in i:
                                logo_path = i
                            else:
                                img_url = self.clean_url(i)
                                logo_path = self.extract_home_page(response) + i
                    else:
                        if "http" in img_url:
                            logo_path = img_url
                        else:
                            img_url = self.clean_url(img_url)
                            logo_path = self.extract_home_page(response) + img_url

        ### Case 4: when <a> contains <div> with logo into background-image
        if not CHECK:
            for tag_a in response.xpath('//a'):
                img_url = tag_a.xpath('//div[contains(@class,"logo")]/@style').re_first(r'url\(([^\)]+)')
                if img_url:
                    CHECK = True
                    if "http" in img_url:
                        logo_path = img_url
                    else:
                        img_url = self.clean_url(img_url)
                        logo_path = self.extract_home_page(response) + img_url

        return logo_path
