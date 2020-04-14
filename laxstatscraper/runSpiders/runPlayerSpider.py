from scrapy.spiderloader import SpiderLoader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
process = CrawlerProcess(settings)
spider_loader = SpiderLoader.from_settings(settings)

player_spider = spider_loader.load("d1players")

print("----------------Player spider started----------------")
process.crawl(player_spider)
process.start()
print("----------------Player spider finished----------------\n")
