from scrapy.spiderloader import SpiderLoader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
process = CrawlerProcess(settings)
spider_loader = SpiderLoader.from_settings(settings)

team_spider = spider_loader.load("d1teams")

print("----------------Team spider started----------------")
process.crawl(team_spider)
process.start()
print("----------------Team spider finished----------------\n")
