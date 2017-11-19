# -*- coding: utf-8 -*-

# Scrapy settings for Crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Bot'

SPIDER_MODULES = ['Crawler.spiders']
NEWSPIDER_MODULE = 'Crawler.spiders'

#FEED_EXPORT_FIELDS = ['symbol','name','image','status','one_line','logo_big','opening_date','closing_date','description','country','technology','website_url','facebook_url','twitter_url','telegram_url','medium_url','slack_url','github_url'] 

#FEED_EXPORT_FIELDS = ['symbol','name','image','status','one_line','logo_big','opening_date','closing_date','description','country','team_members','technology','website_url','facebook_url','twitter_url','telegram_url','medium_url','slack_url','github_url','articles','facebook_posts','twitter_posts'] 

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Crawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Crawler.middlewares.CrawlerSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'Crawler.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
    'Crawler.pipelines.CrawlerPipeline': 300,
}

#s3://aws_key:aws_secret@mybucket/ 
IMAGES_STORE = 's3://images.icorium.io/'
AWS_ACCESS_KEY_ID = 'AKIAIUZY7FJDTN72Y4PA'
AWS_SECRET_ACCESS_KEY= '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'

#IMAGES_STORE = 'images'
IMAGES_URLS_FIELD = 'image'
IMAGES_RESULT_FIELD = 'image_local_url'

IMAGES_THUMBS = {
    'small': (50, 50),
    'big': (250, 250),
}
# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MSSQL_SERVER = 'icoriummasterdb.cqc4c8d1cdmf.us-west-2.rds.amazonaws.com'
MSSQL_USER = 'icouser'
MSSQL_PWD = 'D6zqZ6UXfd'
MSSQL_DB = 'Icorium'
