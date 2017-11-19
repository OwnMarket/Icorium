# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymssql
from scrapy.conf import settings

class CrawlerPipeline(object):
    def __init__(self):
        self.conn = pymssql.connect(settings['MSSQL_SERVER'], settings['MSSQL_USER'], settings['MSSQL_PWD'], settings['MSSQL_DB'])        
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if (spider.name == 'coinschedule'):
           try:
              self.cursor.execute("INSERT INTO coinschedule(symbol, name, description, country, category, opening_date, closing_date, team_members, website_url, social_links, underlying_technology, whitepaper_url, ico_total, bitcoin_url, one_liner, token_distribution) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (item['symbol'], item['name'], item['description'], item['country'], item['category'], item['opening_date'], item['closing_date'], item['team_members'], item['website_url'], item['social_links'], item['underlying_technology'], item['whitepaper_url'], item['ico_total'], item['bitcoin_url'], item['one_liner'], item['token_distribution'])) 
              self.conn.commit()
           except BaseException as e:
              print ('Exception: ' + str(e))
        elif (spider.name == 'tokenmarket'): 
           try:
              image_url = item['image_local_url'][0]['path']
              image_url = image_url.replace('full/', '')
           except:
              image_url = ''

           try:
              self.cursor.execute("INSERT INTO tokenmarket(symbol, name, description, country, one_line, image, technology, opening_date, closing_date, team_members, social_links, articles, facebook_posts, twitter_posts) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (item['symbol'], item['name'], item['description'], item['country'], item['one_line'], image_url, item['technology'], item['opening_date'], item['closing_date'], item['team_members'], item['social_links'], item['articles'], item['facebook_posts'], item['twitter_posts']))
              self.conn.commit()
           except BaseException as e:
              print ('Exception: ' + str(e))
        elif (spider.name == 'icolist'): 
           try:
              image_url = item['image_local_url'][0]['path']
              image_url = image_url.replace('full/', '')
           except:
              image_url = ''

           #try:
           self.cursor.execute("INSERT INTO icolist(symbol, name, description, image, status, currency, opening_date, closing_date, social_links, round, ico_scale, ico_total, total_raised, ico_scale_currency, ico_total_currency, total_raised_currency) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (item['symbol'], item['name'], item['description'], image_url, item['status'], item['currency'], item['opening_date'], item['closing_date'], item['social_links'], item['round'], item['ico_scale'], item['ico_total'], item['total_raised'], item['ico_scale_currency'], item['ico_total_currency'], item['total_raised_currency']))
           self.conn.commit()
           #except BaseException as e:
           #   print ('Exception: ' + str(e))
        elif (spider.name == 'icorating'): 
           try:
              image_url = item['image_local_url'][0]['path']
              image_url = image_url.replace('full/', '')
           except:
              image_url = ''

           try:
              self.cursor.execute("INSERT INTO icorating(name, one_liner, description, image, country, year_founded, category, opening_date, closing_date, social_links, team_members, tech_details, hype_score, risk_score, investment_potential, overall_rating, token_distribution, token_sales, accepted_currency, report) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (item['name'], item['one_liner'], item['description'], image_url, item['country'], item['year_founded'], item['category'], item['opening_date'], item['closing_date'], item['social_links'], item['team_members'], item['tech_details'], item['hype_score'], item['risk_score'], item['investment_potential'], item['overall_rating'], item['token_distribution'], item['token_sales'], item['accepted_currency'], item['report']))
              self.conn.commit()
           except BaseException as e:
              print ('Exception: ' + str(e))
        elif (spider.name == 'smithandcrown'): 
           try: 
              self.cursor.execute("INSERT INTO smithandcrown(symbol, name, one_liner, opening_date, closing_date, total_raised_amount, total_raised_currency, country, year, underlying_technology, accepted_currency, category, round, ico_total, ico_scale, social_links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (item['symbol'], item['name'], item['one_liner'], item['opening_date'], item['closing_date'], item['total_raised_amount'], item['total_raised_currency'], item['country'], item['year'], item['underlying_technology'], item['accepted_currency'], item['category'], item['round'], item['ico_total'], item['ico_scale'], item['social_links']))              
              self.conn.commit()
           except BaseException as e:
              print ('Exception: ' + str(e)) 
        return item
