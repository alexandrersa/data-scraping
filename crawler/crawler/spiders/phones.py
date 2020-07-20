# -*- coding: utf-8 -*-

import re
from functools import reduce


class Phones(object):
    name = "Phones"

    def get_phones(self, response) -> list:
        """
        :type response: object
        """
        phones = self.extract_phone_number(str(response.text))
        phone_list = []
        for phone in phones:
            phone_list.append(self.phone_format(phone))

        return reduce(
            lambda l, x: l.append(x) or l if x not in l else l, phone_list, []
        )

    def extract_phone_number(self, html: str) -> list:
        """
        :param html:
        :rtype: list
        :param html_text:
        :return:
        """
        valid_phones = []
        phone_list = re.findall(
            r'([(]?(\d{3})?[)]?(\s|-|\.)?(\d{3})(\s|-|\.)(\d{4})|'
            r'\+\d{2}\s?0?\d{10}|'
            r'[+](\d{2}) [(]?(\d{2,3})?[)]? (\d{4,5})(\s|-|\.)(\d{4})|'            
            r'[+]?(\d) [(]?(\d{3})?[)]? (\d{3})(\s|-|\.)(\d{2})(\s|-|\.)?(\d{2}))',
            html
        )
        for i in phone_list:
            if len(i) >= 10:
                for j in i:
                    if len(j) >= 10:
                        valid_phones.append(j)
        return valid_phones

    def phone_format(self, phone_number: str) -> str:
        """
        :rtype: str
        :param phone_number:
        :return:
        """
        #clean_phone_number = re.sub(r'[^0-9]+', '', phone_number)

        #phone_number = re.sub(
        #    r'(\d{1,2})(\d{2,3})(\d{3,4})(\d{4})',
        #    r'+\1 (\2) \3 \4',
        #    clean_phone_number
        #)
        return phone_number