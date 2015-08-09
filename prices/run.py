from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import logging
from scrapy.utils.log import configure_logging

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s: %(message)s',
    level=logging.DEBUG
)


process = CrawlerProcess(get_project_settings())
#process = CrawlerProcess({
#    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
#})

process.crawl('tinglesa')
process.start() # the script will block here until the crawling is finished
