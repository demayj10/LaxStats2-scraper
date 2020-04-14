import scrapy
import mysql.connector
from ..items import Coach
from ..links import TeamLinks
from ..parser import Parser
import uuid


class Division1coachesSpider(scrapy.Spider):
    name = "d1coaches"
    links = TeamLinks()

    # start_urls = ['https://stats.ncaa.org/teams/493894']
    start_urls = links.team_links

    def parse(self, response):
        coach = Coach()
        parse = Parser()

        url = response.url
        link_checker = "stats.ncaa.org"
        if link_checker not in url:
            print("---------------------------------------------------------------------")
            print("Invalid link: {}, skipping".format(url))
            print("---------------------------------------------------------------------")
        else:
            team_name = parse.parse_team_header(response, url)[0]

            coach_data = parse.parse_coach_data(response)
            coach['uuid'] = str(uuid.uuid4())
            coach['team'] = team_name
            coach['first_name'] = coach_data[0]
            coach['last_name'] = coach_data[1]
            coach['seasons'] = coach_data[2]
            coach['wins'] = coach_data[3]
            coach['loses'] = coach_data[4]

            yield coach

        team_name = '\'{}\''.format(team_name)
        print("Scraped {:32} coach data @ {}".format(
            team_name, response.url))
