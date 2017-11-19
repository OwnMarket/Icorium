# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import re

class SmithandcrownSpider(scrapy.Spider):
    name = "smithandcrown"
    allowed_domains = ['smithandcrown.com']
    start_urls = [
        'https://www.smithandcrown.com/icos/',
    ]

    def details(self, response):
        accepted_currency = response.xpath('normalize-space(//tr[td[1]/text() = "Accepted currencies"]/td[2]/text())').extract_first()        
        if (accepted_currency == ''):
           accepted_currency = response.xpath('normalize-space(//tr[td[1]/b/text() = "Accepted currencies:"]/td[2]/text())').extract_first()        

        round = response.xpath('normalize-space(//tr[td[1]/text() = "Investment Round"]/td[2]/text())').extract_first()        
        if (round == ''):
            round = response.xpath('normalize-space(//tr[td[1]/b/text() = "Investment Round:"]/td[2]/text())').extract_first()        

        underlying_technology = response.xpath('normalize-space(//tr[td[1]/text() = "Blockchain"]/td[2]/text())').extract_first()
        if (underlying_technology == ''):
            underlying_technology = response.xpath('normalize-space(//tr[td[1]/b/text() = "Blockchain:"]/td[2]/text())').extract_first()
        
        incorporation = response.xpath('normalize-space(//tr[td[1]/text() = "Incorporation status"]/td[2]/text())').extract_first()
        if (incorporation == ''):
            incorporation = response.xpath('normalize-space(//tr[td[1]/b/text() = "Incorporation status:"]/td[2]/text())').extract_first()

        try:
            incorporation_data = incorporation.split(',')     
            country = ''
            year = re.sub("\D", "", incorporation_data)
            try:
              country = incorporation_data[1].strip()
            except:
               pass 
        except:
            country = ''
            year = ''

        ico_exp = 1
        ico_scale = response.xpath('normalize-space(//tr[td[1]/text() = "Distributed in ICO"]/td[2]/text())').extract_first() 
        if (ico_scale == ''):
            ico_scale = response.xpath('normalize-space(//tr[td[1]/b[contains(text(), "Distributed in ICO:")]]/td[2]/text())').extract_first() 

        ico_scale = ico_scale.lower()
        if 'million' in ico_scale:
           ico_scale = ico_scale.replace('million', '')
           ico_exp = 6
        if 'billion' in ico_scale:
           ico_scale = ico_scale.replace('billion', '')
           ico_exp = 9
        ico_scale = ico_scale.replace(' ', '')
        ico_scale = ico_scale.replace(',', '')
        ico_scale_test = ico_scale.replace('.', '')
        if (ico_scale_test == re.sub("\D", "", ico_scale)):
           if (ico_exp > 1):
              ico_scale = float(ico_scale) * 10**ico_exp
        else:
           ico_scale = ''

        ico_exp = 1
        ico_total = response.xpath('normalize-space(//tr[td[1]/text() = "Token supply"]/td[2]/text())').extract_first()        
        if (ico_total == ''):
            ico_total = response.xpath('normalize-space(//tr[td[1]/b[contains(text(), "Token supply:")]]/td[2]/text())').extract_first() 
        ico_total = ico_total.lower()
        if 'million' in ico_total:
           ico_total = ico_total.replace('million', '')
           ico_exp = 6
        if 'billion' in ico_total:
           ico_total = ico_total.replace('billion', '')
           ico_exp = 9
        ico_total = ico_total.replace(' ', '')
        ico_total = ico_total.replace(',', '')
        ico_total_test = ico_total.replace('.', '')
        if (ico_total_test == re.sub("\D", "", ico_total)):
            if (ico_exp > 1):
                ico_total = float(ico_total) * 10**ico_exp
        else:
            ico_total = ''

        category = response.css('.categories').xpath('normalize-space(./ul/li/a/text())').extract_first()        

        if (category):
           category = category.replace("'", "''")

        social_links_header = response.xpath('//h3[span[contains(text(), "Official Resources")]]') 
        social_links = social_links_header.xpath('following-sibling::ul/li/a')

        ico_social_links = []
        social_links_data = ''

        for social in social_links:
            link = social.xpath('normalize-space(./span/text())').extract_first() + '%%DEL%%' + social.xpath('normalize-space(./@href)').extract_first()
            
            ico_social_links.append(link)
            social_links_data = '%%LINK%%' . join(ico_social_links)

        yield {
            'symbol': response.meta.get('symbol'), 
            'name': response.meta.get('name').replace("'", "''"), 
            'one_liner': response.meta.get('one_liner').replace("'", "''"), 
            'opening_date': response.meta.get('opening_date'), 
            'closing_date': response.meta.get('closing_date'), 
            'total_raised_amount': response.meta.get('total_raised_amount'), 
            'total_raised_currency': response.meta.get('total_raised_currency'),
            'country': country.replace("'", "''"),
            'year': year,
            'underlying_technology': underlying_technology.replace("'", "''"),
            'accepted_currency': accepted_currency.replace("'", "''"),
            'category': category,
            'round': round.replace("'", "''"),
            'ico_total': ico_total,
            'ico_scale': ico_scale,
            'social_links': social_links_data.replace("'", "''"),
        } 

    def parse(self, response):
        ongoing_icos = response.css('#icos-ongoing').xpath('./tbody/tr')
        recent_icos = response.css('#icos-recent').xpath('./tbody/tr')

        icos = ongoing_icos + recent_icos
        for ico in icos:
            ico_url = ico.xpath('@data-url').extract_first()

            social_links_data = ''

            if 'smithandcrown' not in ico_url:
               ico_social_links = []

               link = 'website%%DEL%%' + ico_url           
               ico_social_links.append(link)

               social_links_data = '%%LINK%%' . join(ico_social_links)
               ico_url = ''
               
            opening_date = ico.xpath('td[5]/@data-countdown').extract()
            if (opening_date == []):
                opening_date = ico.xpath('normalize-space(td[5]/text())').extract_first()
                try:
                    opening_date = datetime.strptime(opening_date, '%b %d, %Y')
                    opening_date = opening_date.strftime('%Y-%m-%d 00:00:00')
                except ValueError:
                    opening_date = ''
            else:
                opening_date = opening_date[0]
                try:
                    opening_date = datetime.strptime(opening_date, '%Y/%m/%d')
                    opening_date = opening_date.strftime('%Y-%m-%d 00:00:00')
                except ValueError:
                    opening_date = ''

            closing_date = ico.xpath('td[6]/@data-countdown').extract()
            if (closing_date == []):
                closing_date = ico.xpath('normalize-space(td[6]/text())').extract_first()
                try:
                    closing_date = datetime.strptime(closing_date, '%b %d, %Y')
                    closing_date = closing_date.strftime('%Y-%m-%d 00:00:00')
                except ValueError:
                    closing_date = ''
            else:
                closing_date = closing_date[0]
                try:
                    closing_date = datetime.strptime(closing_date, '%Y/%m/%d')
                    closing_date = closing_date.strftime('%Y-%m-%d 00:00:00')
                except ValueError:
                    closing_date = ''

            symbol = ico.xpath('normalize-space(@data-shortcode)').extract_first()
            name = ico.xpath('normalize-space(td[1]/div/span/text())').extract_first()
            one_liner = ico.xpath('normalize-space(td[3]/p/text())').extract_first()
            total_raised = ico.xpath('normalize-space(td[7]/text())').extract_first()

            total_raised_amount = ''
            total_raised_currency = ''
            for char in list(total_raised):
                if char.isdigit():
                   total_raised_amount += char
                else:
                   if char not in (',', '.'):
                      total_raised_currency += char
            
            if (ico_url):
                yield scrapy.Request(ico_url, self.details,
                                 meta={'symbol':symbol, 'name':name, 'one_liner': one_liner, 'opening_date': opening_date, 'closing_date': closing_date, 'total_raised_amount': total_raised_amount, 'total_raised_currency': total_raised_currency})
            else:
                yield {
                    'symbol': symbol, 
                    'name': name, 
                    'one_liner': one_liner, 
                    'opening_date': opening_date, 
                    'closing_date': closing_date, 
                    'total_raised_amount': total_raised_amount, 
                    'total_raised_currency': total_raised_currency,
                    'country': '',
                    'year': '',
                    'underlying_technology': '',
                    'accepted_currency': '',
                    'category': '',
                    'round': '',
                    'ico_total': '',
                    'ico_scale': '',
                    'social_links': social_links_data.replace("'", "''"),
                }             
