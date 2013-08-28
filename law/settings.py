# Scrapy settings for law project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'law'

SPIDER_MODULES = ['law.spiders']
NEWSPIDER_MODULE = 'law.spiders'

ITEM_PIPELINES = ['law.pipelines.LawPipeline']

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'law (+http://www.yourdomain.com)'
