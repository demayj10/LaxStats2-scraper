from scrapy.spiderloader import SpiderLoader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
process = CrawlerProcess(settings)
spider_loader = SpiderLoader.from_settings(settings)

game_spider = spider_loader.load("d1games")

print("----------------Game spider started----------------")
process.crawl(game_spider)
process.start()
print("----------------Game spider finished----------------\n")
