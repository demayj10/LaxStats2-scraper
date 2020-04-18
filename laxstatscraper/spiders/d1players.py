# -*- coding: utf-8 -*-
import scrapy
import mysql.connector
from scrapy import Selector
from ..items import Player
from ..links import RosterLinks
from ..parser import Parser
import uuid
import time

# Spider created 2/5/2020 by John DeMay
# Might be able to simplify the data parsing


class Division1playersSpider(scrapy.Spider):
    name = 'd1players'
    links = RosterLinks()

    # print(links.roster_links)
    # start_urls = links.roster_links
    start_urls = ['https://stats.ncaa.org/team/282/stats/15203']

    def parse(self, response):
        player = Player()
        parse = Parser()

        # Need to implement url checker
        url = response.url
        link_checker = "stats.ncaa.org"
        if link_checker not in url:
            print("---------------------------------------------------------------------")
            print("Invalid link: {}, skipping".format(url))
            print("---------------------------------------------------------------------")
        else:
            # Last run didn't pull from 7 teams
            team_name = parse.parse_team_header(response, url)[0]

            player_table_rows = response.xpath(
                '//*[@id="stat_grid"]/tbody/tr').getall()
            for row in player_table_rows:
                p_data = Selector(text=row).css('td').getall()

                p_uuid = uuid.uuid4()
                jersey = Selector(text=p_data[0]).css('td::text').get().strip()
                name = Selector(text=p_data[1]).css('a::text').get().strip()
                year = Selector(text=p_data[2]).css('td::text').get().strip()
                position = Selector(text=p_data[3]).css('td::text').get()
                if position is not None:
                    position.strip()
                games_played = Selector(text=p_data[4]).css(
                    'td::text').get().strip()
                start_time = time.time()
                goals = Selector(text=p_data[8]).css('div::text').get().strip()
                total_time = time.time() - start_time
                print('-----------------------------------------------------------------------')
                print(total_time)
                print('-----------------------------------------------------------------------')
                break
                assists = Selector(text=p_data[9]).css(
                    'div::text').get().strip()
                points = Selector(text=p_data[10]).css(
                    'div::text').get().strip()
                shots = Selector(text=p_data[11]).css(
                    'div::text').get().strip()
                shot_pct = Selector(text=p_data[12]).css(
                    'div::text').get().strip()
                sog = Selector(text=p_data[13]).css('div::text').get().strip()
                sog_pct = Selector(text=p_data[14]).css(
                    'div::text').get().strip()
                groundballs = Selector(text=p_data[18]).css(
                    'div::text').get().strip()
                turnovers = Selector(text=p_data[19]).css(
                    'div::text').get().strip()
                caused_turnovers = Selector(text=p_data[20]).css(
                    'div::text').get().strip()
                faceoff_wins = Selector(text=p_data[21]).css(
                    'div::text').get().strip()
                faceoffs_taken = Selector(text=p_data[22]).css(
                    'div::text').get().strip()
                faceoff_win_pct = Selector(text=p_data[23]).css(
                    'div::text').get().strip()
                penalties = Selector(text=p_data[24]).css(
                    'div::text').get().strip()
                penalty_time = Selector(text=p_data[25]).css(
                    'div::text').get().strip()
                goals_allowed = Selector(text=p_data[29]).css(
                    'div::text').get().strip()
                saves = Selector(text=p_data[31]).css(
                    'div::text').get().strip()
                save_pct = Selector(text=p_data[32]).css(
                    'div::text').get().strip()

                name_split = name.split(', ')
                first_name = name_split[1]
                last_name = name_split[0]

                if goals == "":
                    goals = "0"
                if assists == "":
                    assists = "0"
                if points == "":
                    points = "0"
                if shots == "":
                    shots = "0"
                if shot_pct == "":
                    shot_pct = "0.000"
                if sog == "":
                    sog = "0"
                if sog_pct == "":
                    sog_pct = "0.000"
                if groundballs == "":
                    groundballs = "0"
                if turnovers == "":
                    turnovers = "0"
                if caused_turnovers == "":
                    caused_turnovers = "0"
                if faceoff_wins == "":
                    faceoff_wins = "0"
                if faceoffs_taken == "":
                    faceoffs_taken = "0"
                if faceoff_win_pct == "":
                    faceoff_win_pct = "0.000"
                if penalties == "":
                    penalties = "0"
                if penalty_time == "":
                    penalty_time = "0"
                if goals_allowed == "":
                    goals_allowed = "0"
                if saves == "":
                    saves = "0"
                if save_pct == "":
                    save_pct = "0.000"

                player['uuid'] = str(p_uuid)
                player['team'] = team_name
                player['first_name'] = first_name
                player['last_name'] = last_name
                player['jersey'] = jersey
                player['year'] = year
                player['position'] = position
                player['games_played'] = int(games_played, 10)
                player['goals'] = int(goals, 10)
                player['assists'] = int(assists, 10)
                player['points'] = int(points, 10)
                player['shots'] = int(shots, 10)
                player['shot_pct'] = float(shot_pct)
                player['sog'] = int(sog, 10)
                player['sog_pct'] = float(sog_pct)
                player['groundballs'] = int(groundballs, 10)
                player['turnovers'] = int(turnovers, 10)
                player['caused_turnovers'] = int(caused_turnovers, 10)
                player['faceoff_wins'] = int(faceoff_wins, 10)
                player['faceoffs_taken'] = int(faceoffs_taken, 10)
                player['faceoff_win_pct'] = float(faceoff_win_pct)
                player['penalties'] = int(penalties, 10)
                player['penalty_time'] = int(penalty_time, 10)
                player['games_played'] = int(games_played, 10)
                player['goals_allowed'] = int(goals_allowed, 10)
                player['saves'] = int(saves, 10)
                player['save_pct'] = float(save_pct)

                yield player

            team_name = '\'{}\''.format(team_name)
            print("Scraped {:32} player data @ {}".format(
                team_name, response.url))
