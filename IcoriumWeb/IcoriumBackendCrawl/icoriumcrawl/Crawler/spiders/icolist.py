# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.markup import remove_tags
import re

class IcolistSpider(scrapy.Spider):
    name = 'icolist'
    allowed_domains = ['ico-list.com']
    start_urls = ['https://ico-list.com']

    def details(self, response):
        logo_list = []
        relative_logo = response.css('.avatar').xpath('./@src').extract_first()
        if (relative_logo != ''):
            logo = response.urljoin(relative_logo)
            logo_list.append(logo)
        else: 
            logo = response.meta.get('image')
            logo_list.append(logo)

        description = response.css('.message').extract_first()
        description = remove_tags(description)
        description = description.replace('\r\n', ' ')
        description = description.replace('\t', '')

        yield {
            'symbol': response.meta.get('symbol'),
            'name': response.meta.get('name').replace("'", "''"), 
            'status': response.meta.get('status'), 
            'image': logo_list,
            'ico_scale': response.meta.get('ico_scale'), 
            'ico_scale_currency': response.meta.get('ico_scale_currency'), 
            'ico_total': response.meta.get('ico_total'),
            'ico_total_currency': response.meta.get('ico_total_currency'),
            'currency': response.meta.get('currency'),
            'opening_date': response.meta.get('opening_date'), 
            'closing_date': response.meta.get('closing_date'),
            'social_links': response.meta.get('social_links').replace("'", "''"),
            'round': response.meta.get('round'),
            'description': description.replace("'", "''"),
            'total_raised': response.meta.get('total_raised'), 
            'total_raised_currency': response.meta.get('total_raised_currency'), 
            'exception': ''
        } 

    def parse(self, response):
        for ico in response.css('#coinlist').xpath('./tbody/tr'):
            relative_ico_url = ico.xpath('normalize-space(./td[2]/a/@href)').extract_first()
            ico_url = response.urljoin(relative_ico_url)
            status = ico_url

            symbol_name_data = ico.xpath('normalize-space(./td[2]/a/text())').extract_first()
            symbol_name_data = symbol_name_data.replace('【Pre】', '')
            symbol_name = symbol_name_data.split('（')

            try:
               name = symbol_name[0]
            except:
               name = symbol_name_data

            try:
               symbol = symbol_name[1]
               symbol = symbol.replace('）', '')
               symbol = symbol.strip()
            except:
               symbol = ''

            image_relative = ico.xpath('normalize-space(./td[1]/img/@src)').extract_first()
            image = response.urljoin(image_relative)
            ico_scale = ico.xpath('normalize-space(./td[4]/text())').extract_first()
            ico_total = ico.xpath('normalize-space(./td[5]/text())').extract_first()

            ico_exp = 1
            ico_scale = ico_scale.lower()
            ico_scale_currency = ''
            if symbol.lower() in ico_scale:
               ico_scale = ico_scale.replace(symbol.lower(), '')
               ico_scale_currency = symbol

            if name.lower() in ico_scale:
               ico_scale = ico_scale.replace(name.lower(), '')
               ico_scale_currency = name

            if 'millions' in ico_scale:
               ico_scale = ico_scale.replace('millions', '')
               ico_exp = 6
            if 'million' in ico_scale:
               ico_scale = ico_scale.replace('million', '')
               ico_exp = 6
            if 'm' in ico_scale:
               ico_scale = ico_scale.replace('m', '')
               ico_exp = 6
            if 'tokens' in ico_scale:
               ico_scale = ico_scale.replace('tokens', '')
               ico_scale_currency = 'token'
            elif 'token' in ico_scale:
               ico_scale = ico_scale.replace('token', '')
               ico_scale_currency = 'token'
            elif 'eth' in ico_scale:
               ico_scale = ico_scale.replace('eth', '')
               ico_scale_currency = 'ETH'
            elif 'btc' in ico_scale:
               ico_scale = ico_scale.replace('btc', '')
               ico_scale_currency = 'BTC'
            elif 'usd' in ico_scale:
               ico_scale = ico_scale.replace('usd', '')
               ico_scale_currency = 'USD'
            elif '$' in ico_scale:
               ico_scale = ico_scale.replace('$', '')
               ico_scale_currency = 'USD'

            ico_scale = ico_scale.replace(',', '')
            ico_scale = ico_scale.replace(' ', '')
            ico_scale_test = ico_scale.replace('.', '')
            if (ico_scale_test == re.sub("\D", "", ico_scale)):
                if (ico_exp > 1):
                    ico_scale = float(ico_scale) * 10**ico_exp
            else:
                ico_scale = ''

            ico_exp = 1
            ico_total = ico_total.lower()
            ico_total_currency = ''
            if symbol.lower() in ico_total:
               ico_total = ico_total.replace(symbol.lower(), '')
               ico_total_currency = symbol

            if name.lower() in ico_total:
               ico_total = ico_total.replace(name.lower(), '')
               ico_total_currency = name

            if 'millions' in ico_total:
               ico_total = ico_total.replace('millions', '')
               ico_exp = 6
            if 'million' in ico_total:
               ico_total = ico_total.replace('million', '')
               ico_exp = 6
            if 'm' in ico_total:
               ico_total = ico_total.replace('m', '')
               ico_exp = 6
            if 'tokens' in ico_total:
               ico_total = ico_total.replace('tokens', '')
               ico_total_currency = 'token'
            elif 'token' in ico_total:
               ico_total = ico_total.replace('token', '')
               ico_total_currency = 'token'
            elif 'eth' in ico_total:
               ico_total = ico_total.replace('eth', '')
               ico_total_currency = 'ETH'
            elif 'btc' in ico_total:
               ico_total = ico_total.replace('btc', '')
               ico_total_currency = 'BTC'
            elif 'usd' in ico_total:
               ico_total = ico_total.replace('usd', '')
               ico_total_currency = 'USD'
            elif '$' in ico_total:
               ico_total = ico_total.replace('$', '')
               ico_total_currency = 'USD'

            ico_total = ico_total.replace(',', '')
            ico_total = ico_total.replace(' ', '')
            ico_total_test = ico_total.replace('.', '')
            if (ico_total_test == re.sub("\D", "", ico_total)):
                if (ico_exp > 1):
                    ico_total = float(ico_total) * 10**ico_exp
            else:
                ico_total = ''

            currency = ico.xpath('normalize-space(./td[6]/text())').extract_first()

            opening_date = ''
            closing_date = ico.xpath('normalize-space(./td[7]/text())').extract_first() + ' 00:00:00'

            round = ''

            total_raised = ''
            total_raised_currency = ''

            ico_social_links = []

            social_links = ico.xpath('./td[3]/a')

            for social in social_links:
                type = social.xpath('./i/@class').extract_first()
                type = type.replace('fa fa-', '')
                type = type.replace(' directLink', '')
                link = type + '%%DEL%%' + social.xpath('./@href').extract_first()
             
                ico_social_links.append(link)     

            social_links_data = '%%NEW%%' . join(ico_social_links)

            yield scrapy.Request(ico_url, self.details,
                                 meta={'total_raised': total_raised, 'total_raised_currency': total_raised_currency, 'symbol': symbol, 'name':name, 'status': status, 'image': image, 'ico_scale': ico_scale, 'ico_scale_currency': ico_scale_currency, 
                                       'ico_total': ico_total, 'ico_total_currency': ico_total_currency, 'currency': currency, 'opening_date': opening_date, 'closing_date': closing_date, 'social_links': social_links_data, 'round': round})

        for ico in response.css('#tba-list').xpath('./tbody/tr'):
            relative_ico_url = ico.xpath('normalize-space(./td[2]/a/@href)').extract_first()
            ico_url = response.urljoin(relative_ico_url)
            status = ico_url

            symbol_name_data = ico.xpath('normalize-space(./td[2]/a/text())').extract_first()
            symbol_name_data = symbol_name_data.replace('【Pre】', '')
            symbol_name = symbol_name_data.split('（')

            try:
               name = symbol_name[0]
            except:
               name = symbol_name_data

            try:
               symbol = symbol_name[1]
               symbol = symbol.replace('）', '')
               symbol = symbol.strip()
            except:
               symbol = ''

            image_relative = ico.xpath('normalize-space(./td[1]/img/@src)').extract_first()
            image = response.urljoin(image_relative)
            round = ico.xpath('normalize-space(./td[4]/text())').extract_first()
            ico_scale = ''
            ico_total = ''
            total_raised = ''
            ico_scale_currency = ''
            ico_total_currency = ''
            total_raised_currency = ''
            closing_date = ''

            currency = ''

            opening_date = ico.xpath('normalize-space(./td[5]/text())').extract_first() + ' 00:00:00'

            ico_social_links = []

            social_links = ico.xpath('./td[3]/a')

            for social in social_links:
                type = social.xpath('./i/@class').extract_first()
                type = type.replace('fa fa-', '')
                type = type.replace(' directLink', '')
                link = type + '%%DEL%%' + social.xpath('./@href').extract_first()
             
                ico_social_links.append(link)     

            social_links_data = '%%NEW%%' . join(ico_social_links)

            yield scrapy.Request(ico_url, self.details,
                                 meta={'total_raised': total_raised, 'total_raised_currency': total_raised_currency, 'symbol': symbol, 'name':name, 'status': status, 'image': image, 'ico_scale': ico_scale, 'ico_scale_currency': ico_scale_currency, 
                                       'ico_total': ico_total, 'ico_total_currency': ico_total_currency, 'currency': currency, 'opening_date': opening_date, 'closing_date': closing_date, 'social_links': social_links_data, 'round': round})

        for ico in response.css('#done-list').xpath('./tbody/tr'):
            relative_ico_url = ico.xpath('normalize-space(./td[2]/a/@href)').extract_first()
            ico_url = response.urljoin(relative_ico_url)
            status = ico_url

            symbol_name_data = ico.xpath('normalize-space(./td[2]/a/text())').extract_first()
            symbol_name_data = symbol_name_data.replace('【Pre】', '')
            symbol_name = symbol_name_data.split('（')

            try:
               name = symbol_name[0]
            except:
               name = symbol_name_data

            try:
               symbol = symbol_name[1]
               symbol = symbol.replace('）', '')
               symbol = symbol.strip()
            except:
               symbol = ''

            image_relative = ico.xpath('normalize-space(./td[1]/img/@src)').extract_first()
            image = response.urljoin(image_relative)
            round = ico.xpath('normalize-space(./td[4]/text())').extract_first()
            ico_scale = ''
            ico_total = ''
            ico_scale_currency = ''
            ico_total_currency = ''

            currency = ''

            opening_date = ''
            closing_date = ''

            total_raised = ico.xpath('normalize-space(./td[5]/text())').extract_first()
            total_raised = total_raised.replace('Pending statistics', '')

            ico_exp = 1
            total_raised = total_raised.lower()
            total_raised_currency = ''

            if symbol.lower() in total_raised:
               total_raised = total_raised.replace(symbol.lower(), '')
               total_raised_currency = symbol

            if 'millions' in total_raised:
               total_raised = total_raised.replace('millions', '')
               ico_exp = 6
            if 'million' in total_raised:
               total_raised = total_raised.replace('million', '')
               ico_exp = 6
            if 'm' in total_raised:
               total_raised = total_raised.replace('m', '')
               ico_exp = 6
            if 'tokens' in total_raised:
               total_raised = total_raised.replace('tokens', '')
               total_raised_currency = 'token'
            elif 'token' in total_raised:
               total_raised = total_raised.replace('token', '')
               total_raised_currency = 'token'
            elif 'eth' in total_raised:
               total_raised = total_raised.replace('eth', '')
               total_raised_currency = 'ETH'
            elif 'btc' in total_raised:
               total_raised = total_raised.replace('btc', '')
               total_raised_currency = 'BTC'
            elif 'usd' in total_raised:
               total_raised = total_raised.replace('usd', '')
               total_raised_currency = 'USD'
            elif '$' in total_raised:
               total_raised = total_raised.replace('$', '')
               total_raised_currency = 'USD'

            total_raised = total_raised.replace(',', '')
            total_raised = total_raised.replace(' ', '')
            total_raised_test = total_raised.replace('.', '')
            if (total_raised_test == re.sub("\D", "", total_raised)):
                if (ico_exp > 1):
                    total_raised = float(total_raised) * 10**ico_exp
            else:
                total_raised = ''

            ico_social_links = []

            social_links = ico.xpath('./td[3]/a')

            for social in social_links:
                type = social.xpath('./i/@class').extract_first()
                type = type.replace('fa fa-', '')
                type = type.replace(' directLink', '')
                link = type + '%%DEL%%' + social.xpath('./@href').extract_first()
             
                ico_social_links.append(link)     

            social_links_data = '%%NEW%%' . join(ico_social_links)

            yield scrapy.Request(ico_url, self.details,
                                 meta={'total_raised': total_raised, 'total_raised_currency': total_raised_currency, 'symbol': symbol, 'name':name, 'status': status, 'image': image, 'ico_scale': ico_scale, 'ico_scale_currency': ico_scale_currency, 
                                       'ico_total': ico_total, 'ico_total_currency': ico_total_currency, 'currency': currency, 'opening_date': opening_date, 'closing_date': closing_date, 'social_links': social_links_data, 'round': round})
