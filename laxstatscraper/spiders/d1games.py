import scrapy
import mysql.connector
from scrapy import Selector
from ..items import Game
from ..links import TeamLinks
from ..parser import Parser
import uuid


class Division1gamesSpider(scrapy.Spider):
    name = 'd1games'
    links = TeamLinks()

    # start_urls = ['https://stats.ncaa.org/teams/493863']
    start_urls = links.team_links

    def parse(self, response):
        game = Game()
        parse = Parser()

        url = response.url
        link_checker = "stats.ncaa.org"
        if link_checker not in url:
            print("---------------------------------------------------------------------")
            print("Invalid link: {}, skipping".format(url))
            print("---------------------------------------------------------------------")
        else:
            team_name = parse.parse_team_header(response, url)[0]

            table_body = response.css('tbody').get()
            rows = Selector(text=table_body).css('tr').getall()
            useful_rows = []

            i = 0
            for row in rows:
                if i % 2 == 0:
                    useful_rows.append(row)
                i += 1
            for row in useful_rows:
                data_cells = Selector(text=row).css('td::text').getall()
                date = data_cells[0]
                other_data = Selector(text=row).css('a::text').getall()
                opp_name = other_data[0].strip()
                result = ""
                if len(other_data) > 1:
                    result = other_data[1].strip()

                game['uuid'] = str(uuid.uuid4())
                game['team'] = team_name
                game['date'] = date
                game['opponent'] = opp_name
                game['result'] = result

                yield game

            team_name = '\'{}\''.format(team_name)
            print("Scraped {:32} game data @ {}".format(
                team_name, response.url))
