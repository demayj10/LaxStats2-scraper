# -*- coding: utf-8 -*-
import scrapy
import mysql.connector
from ..items import Team
from ..links import TeamLinks
from ..parser import Parser
import uuid
import os
import logging
from datetime import date

# Spider created 1/26/2020 by John DeMay
# To run the spider: 'scrapy crawl d1Teams'


class Division1teamSpider(scrapy.Spider):
    name = 'd1teams'
    links = TeamLinks()

    start_urls = links.team_links
    # start_urls = ['https://stats.ncaa.org/teams/493885',
    #               'https://stats.ncaa.org/teams/493890']

    # Still need to connect primary and secondary colors for team

    def parse(self, response):
        team = Team()
        parse = Parser()

        url = response.url
        link_checker = "stats.ncaa.org"
        if link_checker not in url:
            print("---------------------------------------------------------------------")
            print("Invalid link: {}, skipping".format(url))
            print("---------------------------------------------------------------------")
        else:
            team_logo = response.xpath(
                '//*[@id="contentarea"]/fieldset[1]/legend/img').attrib['src']

            result = parse.parse_team_header(response, url)
            team_name = result[0]
            record_arr = result[1]

            team['uuid'] = str(uuid.uuid4())
            team['division_id'] = 1
            team['logo'] = team_logo
            team['name'] = team_name
            if len(record_arr) > 2:
                team['wins'] = int(record_arr[0], 10)
                team['ties'] = int(record_arr[1], 10)
                team['loses'] = int(record_arr[2], 10)
            else:
                team['wins'] = int(record_arr[0], 10)
                team['ties'] = 0
                team['loses'] = int(record_arr[1], 10)

            yield team

            team_name = '\'{}\''.format(team_name)
            print("Scraped {:32} team data @ {}".format(
                team_name, response.url))
