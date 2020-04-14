from scrapy.spiderloader import SpiderLoader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
process = CrawlerProcess(settings)
spider_loader = SpiderLoader.from_settings(settings)

ranking_spider = spider_loader.load("d1rankings")

print("----------------Ranking spider started----------------")
process.crawl(ranking_spider)
process.start()
print("----------------Ranking spider finished----------------\n")
