from scrapy.spiderloader import SpiderLoader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
process = CrawlerProcess(settings)
spider_loader = SpiderLoader.from_settings(settings)

division_spider = spider_loader.load("d1")

print("----------------Division spider started----------------")
process.crawl(division_spider)
process.start()
print("----------------Division spider finished----------------\n")
