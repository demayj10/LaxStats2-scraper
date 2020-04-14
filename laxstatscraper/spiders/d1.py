import scrapy
from ..items import Division


class Division1Spider(scrapy.Spider):
    name = 'd1'

    start_urls = [
        'https://www.ncaa.com/rankings/lacrosse-men/d1/inside-lacrosse']

    def parse(self, response):
        division = Division()

        div_name = response.xpath(
            '//*[@id="block-bespin-content"]/nav/div[1]/h3/text()').get()

        division['name'] = div_name

        yield division
        print("Scraped '{}' @ {}".format(div_name, response.url))
