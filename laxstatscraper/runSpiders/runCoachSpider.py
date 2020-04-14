from scrapy.spiderloader import SpiderLoader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
process = CrawlerProcess(settings)
spider_loader = SpiderLoader.from_settings(settings)

coach_spider = spider_loader.load("d1coaches")

print("----------------Coach spider started----------------")
process.crawl(coach_spider)
process.start()
print("----------------Coach spider finished----------------\n")
