# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import re

class IcoratingSpider(scrapy.Spider):
    name = 'icorating'
    allowed_domains = ['icorating.com']
    start_urls = ['http://icorating.com']

    def details(self, response):
        category = response.xpath('normalize-space(//div[div[1][contains(text(), "Category")]]/div[2]/text())').extract_first()
        one_liner = response.xpath('normalize-space(//div[div[1][contains(text(), "Description")]]/div[2]/text())').extract_first()
        description = response.xpath('normalize-space(//div[div[1][contains(text(), "Features")]]/div[2])').extract_first()        
        accepted_currency = response.xpath('normalize-space(//div[div[1][contains(text(), "Accepts")]]/div[2]/text())').extract_first()
        year_and_country = response.xpath('normalize-space(//div[div[1][contains(text(), "Founded")]]/div[2]/text())').extract_first()
        tech_details = response.xpath('normalize-space(//div[div[1][contains(text(), "Technical details")]]/div[2]/text())').extract_first()
        token_distribution = response.xpath('normalize-space(//div[div[1][contains(text(), "Tokens distribution")]]/div[2]/text())').extract_first()
        token_sales = response.xpath('normalize-space(//div[div[1][contains(text(), "Token Sales")]]/div[2]/text())').extract_first()
        report = response.css('.ico-card-report__button').xpath('normalize-space(./@href)').extract_first()

        country = ''
        year_founded = ''

        try:
            year_and_country_data = year_and_country.split(',')
            try:
                year_founded = year_and_country_data[0].strip()
            except:
                pass
            try:
                country = year_and_country_data[1].strip()
            except:
                pass

            if (re.sub("\D", "", year_founded) == ''):
                try:
                    year_founded = year_and_country_data[1].strip()
                except:
                    year_founded = ''
                try:
                    country = year_and_country_data[0].strip()
                except:
                    country = ''
        except:
            pass

        year_founded = re.sub("\D", "", year_founded)

        logo_big = response.css('.ico-logo').xpath('normalize-space(./img/@src)').extract()

        ico_team_rows = response.css('#tab-4').xpath('./div').extract_first()

        if (ico_team_rows):
            pass
        else:
            ico_team_rows = ''

        #twitter_url = response.css('.ico-tweets-project').xpath('./a/@href').extract_first();
        #tweets_relative_url = '/api/project/' + twitter_url + '/tweets'
        #tweets_url = response.urljoin(tweets_relative_url)
     
        yield {
            'name':response.meta.get('name'), 
            'image': logo_big, 
            'opening_date': response.meta.get('opening_date'),
            'closing_date': response.meta.get('closing_date'),
            'one_liner': one_liner.replace("'", "''"),
            'description': description.replace("'", "''"),
            'category': category.replace("'", "''"),
            'country': country.replace("'", "''"),
            'year_founded': year_founded,
            'accepted_currency': accepted_currency, 
            'team_members': ico_team_rows.replace("'", "''"),
            'tech_details': tech_details.replace("'", "''"),
            'token_distribution': token_distribution.replace("'", "''"),
            'token_sales': token_sales.replace("'", "''"),
            'hype_score': response.meta.get('hype_score'), 
            'risk_score': response.meta.get('risk_score'), 
            'investment_potential': response.meta.get('investment_potential'),
            'overall_rating': response.meta.get('overall_rating'),
            'report': report,
            'social_links': response.meta.get('social_links').replace("'", "''"),
            'exception': ''
        } 

    def parse(self, response):
        i = 0
        for ico in response.css('.ico-projects-table').xpath('./tbody/tr'):
            ico_relative_url = ico.xpath('./@data-href').extract_first()
            ico_url = response.urljoin(ico_relative_url)

            name = ico.xpath('normalize-space(./td[1]/text())').extract_first()
            hype_score = ico.xpath('normalize-space(./td[2]/div/text())').extract_first()
            risk_score = ico.xpath('normalize-space(./td[3]/div/text())').extract_first()
            investment_potential = ico.xpath('normalize-space(./td[4]/div/div/text())').extract_first()
            overall_rating = ico.xpath('normalize-space(./td[5]/div/div/span/text())').extract_first()
            opening_date = ico.xpath('normalize-space(./td[6]/div/div/div/text())').extract_first()
            closing_date = ico.xpath('normalize-space(./td[7]/div/div/div/text())').extract_first()

            try:
                opening_date = datetime.strptime(opening_date, '%d.%m.%Y')
                opening_date = opening_date.strftime('%Y-%m-%d 00:00:00')
            except:
                opening_date = ''

            try:
                closing_date = datetime.strptime(closing_date, '%d.%m.%Y')
                closing_date = closing_date.strftime('%Y-%m-%d 00:00:00')
            except:
                closing_date = ''

            social_links_data = ''
            ico_social_links = []

            social_links = ico.xpath('./td[8]/div/a')

            for social in social_links:
                link = social.xpath('./@title').extract_first() + '%%DEL%%' + social.xpath('./@href').extract_first()
                ico_social_links.append(link)            
            social_links_data = '%%NEW%%' . join(ico_social_links)

            yield scrapy.Request(ico_url, self.details,
                                 meta={'name':name, 'hype_score': hype_score, 'risk_score': risk_score, 'investment_potential': investment_potential,
                                       'overall_rating': overall_rating, 'opening_date': opening_date, 'closing_date': closing_date, 'social_links': social_links_data})

