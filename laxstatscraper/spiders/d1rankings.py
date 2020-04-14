import scrapy
from ..items import Ranking
from scrapy import Selector
from ..parser import Data_Formatter


class Division1rankingsSpider(scrapy.Spider):
    name = 'd1rankings'

    start_urls = [
        'https://www.ncaa.com/rankings/lacrosse-men/d1/inside-lacrosse']

    def parse(self, response):
        ranking = Ranking()
        formatter = Data_Formatter()

        url = response.url
        link_checker = "www.ncaa.com/rankings"
        if link_checker not in url:
            print("---------------------------------------------------------------------")
            print("Invalid link: {}, skipping".format(url))
            print("---------------------------------------------------------------------")
        else:
            table_body = response.xpath(
                '//*[@id="block-bespin-content"]/div/article/table/tbody[1]')
            rows = table_body.css('tr').getall()
            for row in rows:
                data_cells = Selector(text=row).css('td').getall()
                rank = Selector(text=data_cells[0]).css('td::text').get()
                team = Selector(text=data_cells[1]).css('td::text').get()
                try:
                    team = team.split('(')[0].strip()

                    ranking['rank'] = rank
                    team = formatter.lengthen_abbreviated(team)

                    ranking['team'] = team

                    yield ranking
                except:
                    print("Error with splitting team ranking item")

            print("Scraped Rankings @ {}".format(response.url))
