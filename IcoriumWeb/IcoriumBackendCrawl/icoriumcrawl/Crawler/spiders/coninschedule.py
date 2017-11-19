# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from scrapy.utils.markup import remove_tags
import re

class CoinscheduleSpider(scrapy.Spider):
    name = 'coinschedule'
    allowed_domains = ['www.coinschedule.com']
    start_urls = ['https://www.coinschedule.com/index.php?live_view=2']

    def details(self, response):
        symbol_name_table = response.xpath('//table[3]')

        symbol_name_data = symbol_name_table.xpath('./tr[1]/td[3]').extract_first()
        try:
            symbol_name_data = remove_tags(symbol_name_data)
        except:
            pass
 
        if (symbol_name_data):
            pass
        else:
            symbol_name_data = symbol_name_table.xpath('./tr[1]/td[1]').extract_first()
            symbol_name_data = remove_tags(symbol_name_data)

        try: 
            symbol_name = symbol_name_data.split('(')

            try:
               name = symbol_name[0].strip()
            except:
               name = symbol_name_data

            try:
               symbol = symbol_name[1]
               symbol = symbol.replace(')', '')
               symbol = symbol.strip()
            except:
               symbol = ''
        except:
            name = symbol_name
            symbol = ''

        one_liner = response.css('div.text-center').xpath('./text()').extract_first()

        project_type = response.xpath('normalize-space(//tr[th/text() = "Project Type"]/td[1])').extract_first()

        if 'Token' in project_type:
           underlying_technology = response.xpath('normalize-space(//tr[th/text() = "Platform"]/td[1])').extract_first()
        else:
           underlying_technology = project_type

        category =  response.xpath('normalize-space(//tr[th/text() = "Category"]/td[1]/text())').extract_first()
        country = response.xpath('normalize-space(//tr[th/text() = "Location"]/td[1]/text())').extract_first()
        website_url = response.xpath('normalize-space(//tr[th/text() = "Website"]/td[1]/a/@href)').extract_first()
        whitepaper_url = response.xpath('normalize-space(//tr[th/text() = "Whitepaper"]/td[1]/a/@href)').extract_first()
        bitcoin_url = response.xpath('normalize-space(//tr[th/text() = "Bitcoin Talk"]/td[1]/a/@href)').extract_first()
        opening_date = response.xpath('normalize-space(//tr[th/text() = "Start Date"]/td[1]/text())').extract_first()
        closing_date = response.xpath('normalize-space(//tbody[th/text() = "End Date"]/td[1]/text())').extract_first()
        ico_total = response.xpath('normalize-space(//tr[th/text() = "Total Supply"]/td[1]/text())').extract_first()
        ico_total = ico_total.replace(',', '')

        ico_total_test = ico_total.replace('.', '')
        if (ico_total_test != re.sub("\D", "", ico_total)):
            ico_total = ''

        description = response.xpath('normalize-space(//tbody[th[contains(text(), "Details")]]/tr[2]/td)').extract_first()
        description = remove_tags(description)

        token_distribution = response.xpath('normalize-space(//tbody[th[contains(text(), "Distribution")]]/tr[3]/td)').extract_first()

        if (opening_date == ''):
            opening_date = ''
        elif 'TBA' in opening_date:
            opening_date = ''
        elif (opening_date):
            opening_date = opening_date.replace('1st', '1')
            opening_date = opening_date.replace('2nd', '2')
            opening_date = opening_date.replace('3rd', '3')
            opening_date = opening_date.replace('th', '')
            try:
                opening_date = datetime.strptime(opening_date, '%B %d %Y %H:%M %Z')
                opening_date = opening_date.strftime('%Y-%m-%d %H:%M:00')
            except ValueError:
                opening_date = datetime.strptime(opening_date, '%B %d %Y')
                opening_date = opening_date.strftime('%Y-%m-%d 00:00:00')
        else:
            opening_date = ''

        if (closing_date == ''):
            closing_date = ''
        elif 'TBA' in closing_date:
            closing_date = ''
        elif (closing_date):
            closing_date = closing_date.replace('1st', '1')
            closing_date = closing_date.replace('2nd', '2')
            closing_date = closing_date.replace('3rd', '3')
            closing_date = closing_date.replace('th', '')
            try:
                closing_date = datetime.strptime(closing_date, '%B %d %Y %H:%M %Z')
                closing_date = closing_date.strftime('%Y-%m-%d %H:%M:00')
            except ValueError:
                closing_date = datetime.strptime(closing_date, '%B %d %Y')
                closing_date = closing_date.strftime('%Y-%m-%d 00:00:00')
        else:
            closing_date = ''

        team_data = response.xpath('//div[h3/text() = "Team"]/tr/td/table/tbody/tr')

        team_members = []
        team_members_data = ''

        i = 0
        if (team_data):
           for member in team_data:
               if (i > 0):
                   team_member = member.xpath('normalize-space(./td[1]/text())').extract_first() + '%%DEL%%' + member.xpath('normalize-space(./td[2]/text())').extract_first()
                   team_members.append(team_member)            
               i += 1
           team_members_data = '%%NEW%%' . join(team_members)

        social_links = response.css('.tbl_links').xpath('./tr')
        ico_social_links = []
        social_links_data = ''

        for social in social_links:
            link = social.xpath('normalize-space(./td[2]/a/text())').extract_first() + '%%DEL%%' + social.xpath('normalize-space(./td[2]/a/@href)').extract_first()
            
            ico_social_links.append(link)
            social_links_data = '%%NEW%%' . join(ico_social_links)

        yield {
            'symbol': symbol,
            'name': name.replace("'", "''"), 
            'country': country.replace("'", "''"), 
            'category': category.replace("'", "''"), 
            'opening_date': opening_date, 
            'closing_date': closing_date,
            'one_liner': one_liner.replace("'", "''"),
            'description': description.replace("'", "''"),
            'social_links': social_links_data.replace("'", "''"),
            'team_members': team_members_data.replace("'", "''"),
            'underlying_technology': underlying_technology.replace("'", "''"),
            'website_url': website_url,
            'whitepaper_url': whitepaper_url,
            'bitcoin_url': bitcoin_url,
            'ico_total' : ico_total,
            'token_distribution' : token_distribution,
            'exception': ''
        } 

    def parse(self, response):
        for ico in response.css('table.table-bordered').xpath('//tbody/tr'):
            relative_ico_url = ico.xpath('./td[1]/table/tr[1]/td[2]/a/@href').extract_first()
            ico_url = response.urljoin(relative_ico_url)

            if 'coinschedule.com' in ico_url:
               yield scrapy.Request(ico_url, self.details)

