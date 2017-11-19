# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime

class TokenmarketSpider(scrapy.Spider):
    name = 'tokenmarket'
    allowed_domains = ['tokenmarket.net']
    start_urls = ['https://tokenmarket.net/blockchain/all-assets?sorting=best&archived=true&all=true']

    def details(self, response):
        i = 0
        logo_big = ''
        logo_big = response.css('#asset-logo-primary').xpath('@src').extract() 

        symbol = response.xpath('normalize-space(//tr[th/text() = "Symbol"]/td[1]/text())').extract_first()
        description = response.xpath('normalize-space(//tr[th/text() = "Concept"]/td[1]/p/text())').extract_first()
        country = response.xpath('normalize-space(//tr[th/text() = "Country of origin"]/td/text())').extract_first()
        technology_data = response.xpath('normalize-space(//tr[th/text() = "Blockchain"]/td)').extract_first()
        opening_date = response.xpath('normalize-space(//tr[th/text() = "Crowdsale opening date"]/td[1]/p/text())').extract_first()
        closing_date = response.xpath('normalize-space(//tr[th/text() = "Crowdsale closing date"]/td[1]/p/text())').extract_first()

        if (symbol):
            pass
        else:
            symbol = response.meta.get('symbol')

        if (country == '(data missing)'):
            country = ''

        try:
            technology_data = technology_data.split('(')

            try:
               technology = technology_data[0].strip()
            except:
               technology = technology_data
        except:
            technology = technology_data

        if (opening_date == ''):
            opening_date = ''
        elif 'TBA' in opening_date:
            opening_date = ''
        elif (opening_date):
            try:
                opening_date = datetime.strptime(opening_date, '%d. %b %Y')
                opening_date = opening_date.strftime('%Y-%m-%d 00:00:00')
            except ValueError:
                opening_date = ''
        else:
            opening_date = ''

        if (closing_date == ''):
            closing_date = ''
        elif (closing_date):
            try:
                closing_date = datetime.strptime(closing_date, '%d. %b %Y')
                closing_date = closing_date.strftime('%Y-%m-%d 00:00:00')
            except ValueError:
                closing_date = ''
        else:
            closing_date = ''

        social_links =  response.xpath('//div[h2[contains(text(),"Links")]]/table[1]/tr')
        ico_social_links = []
        social_links_data = ''

        for social in social_links:
            link = social.xpath('normalize-space(./td/a)').extract_first() + '%%DEL%%' + social.xpath('normalize-space(./td/a/@href)').extract_first()
            
            ico_social_links.append(link)
        social_links_data = '%%NEW%%' . join(ico_social_links)

        members_data = response.xpath('//tr[th/text() = "Members"]/td/p')
        members = []

        for member in members_data:
            data = member.xpath('normalize-space(./text())').extract_first()
            data = data.replace(' - ', '%%DEL%%')
            members.append(data)
        team_members = '%%NEW%%' . join(members)

        articles = ''
        twitter_posts = ''
        facebook_posts = ''

        i = 0
        for ico_news in response.css('.asset-list-news'):
            posts = []
            for ico_articles in ico_news.xpath('./tr'):
                post = ico_articles.xpath('normalize-space(./td[1]/p/a/@href)').extract_first() + '%%DEL%%' + ico_articles.xpath('normalize-space(./td[1]/p/a/text())').extract_first()
                post = bytes(post, 'utf-8').decode('ascii', 'ignore')
                posts.append(post)
            if 'twitter' in ico_articles.xpath('normalize-space(./td[1]/p/a/@href)').extract_first():
                twitter_posts = '%%NEW%%' . join(posts)
            else:
                articles = '%%NEW%%' . join(posts)

        posts = []
        for ico_facebook in response.css('.asset-list-facebook').xpath('tr'):
            post = ico_facebook.xpath('normalize-space(./td[1]/p/a/@href)').extract_first() + '%%DEL%%' + ico_facebook.xpath('normalize-space(./td[1]/p/a/text())').extract_first()
            post = bytes(post, 'utf-8').decode('ascii', 'ignore')
            posts.append(post)
        facebook_posts = '%%NEW%%' . join(posts)

        yield {
            'symbol': symbol.replace("'", "''"),
            'name':response.meta.get('name').replace("'", "''"), 
            'one_line': response.meta.get('one_line').replace("'", "''"),
            'image': logo_big,
            'opening_date': opening_date,
            'closing_date': closing_date,
            'description': description.replace("'", "''"),
            'country': country.replace("'", "''"),
            'team_members': team_members.replace("'", "''"),
            'technology': technology.replace("'", "''"),
            'social_links': social_links_data.replace("'", "''"),
            'articles': articles.replace("'", "''"),
            'facebook_posts': facebook_posts.replace("'", "''"),
            'twitter_posts': twitter_posts.replace("'", "''"),
            'exception': ''
        } 

    def parse(self, response):
        for ico in response.css('.table-assets').xpath('./tbody/tr'):
            ico_url = ico.xpath('./td[4]/div/a/@href').extract_first()

            symbol = ico.xpath('normalize-space(./td[5]/text())').extract_first()
            name = ico.xpath('normalize-space(./td[4]/div/a/text())').extract_first()
            image = ico.xpath('normalize-space(./td[2]/a/img/@src)').extract_first()
            one_line = ico.xpath('normalize-space(./td[6]/text())').extract_first()

            logo_list = []
            logo_list.append(image)

            if 'tokenmarket.net' in ico_url:
               yield scrapy.Request(ico_url, self.details,
                                 meta={'symbol':symbol, 'name':name, 'image': image, 'one_line': one_line})
            else:
               yield {
                   'symbol': symbol.replace("'", "''"),
                   'name':name.replace("'", "''"), 
                   'one_line': one_line.replace("'", "''"),
                   'image': logo_list,
                   'opening_date': '',
                   'closing_date': '',
                   'description': '',
                   'country': '',
                   'team_members': '',
                   'technology': '',
                   'social_links': '',
                   'articles': '',
                   'facebook_posts': '',
                   'twitter_posts': '',
               } 
