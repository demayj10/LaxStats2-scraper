# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class Division(scrapy.Item):
    name = scrapy.Field()


class Team(scrapy.Item):
    uuid = scrapy.Field()
    division_id = scrapy.Field()
    logo = scrapy.Field()
    name = scrapy.Field()
    wins = scrapy.Field()
    loses = scrapy.Field()
    ties = scrapy.Field()
    # primary_color = scrapy.Field()
    # secondary_color = scrapy.Field()

class Ranking(scrapy.Item):
    rank = scrapy.Field()
    team = scrapy.Field()

class Game(scrapy.Item):
    uuid = scrapy.Field()
    team = scrapy.Field()
    date = scrapy.Field()
    opponent = scrapy.Field()
    result = scrapy.Field()

class Player(scrapy.Item):
    uuid = scrapy.Field()
    team = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    jersey = scrapy.Field()
    year = scrapy.Field()
    position = scrapy.Field()
    games_played = scrapy.Field()
    goals = scrapy.Field()
    assists = scrapy.Field()
    points = scrapy.Field()
    shots = scrapy.Field()
    shot_pct = scrapy.Field()
    sog = scrapy.Field()
    sog_pct = scrapy.Field()
    groundballs = scrapy.Field()
    turnovers = scrapy.Field()
    caused_turnovers = scrapy.Field()
    faceoff_wins = scrapy.Field()
    faceoffs_taken = scrapy.Field()
    faceoff_win_pct = scrapy.Field()
    penalties = scrapy.Field()
    penalty_time = scrapy.Field()
    goals_allowed = scrapy.Field()
    saves = scrapy.Field()
    save_pct = scrapy.Field()

# class WomensLacrossePlayer(scrapy.item):
#     uuid = scrapy.Field()
#     team = scrapy.Field()
#     first_name = scrapy.Field()
#     last_name = scrapy.Field()
#     jersey = scrapy.Field()
#     year = scrapy.Field()
#     position = scrapy.Field()
#     games_played = scrapy.Field()
#     fouls = scrapy.Field()
#     goals = scrapy.Field()
#     assists = scrapy.Field()
#     points = scrapy.Field()
#     shots = scrapy.Field()
#     shot_pct = scrapy.Field()
#     sog = scrapy.Field()
#     sog_pct = scrapy.Field()
#     groundballs = scrapy.Field()
#     caused_turnovers = scrapy.Field()
#     goals_allowed = scrapy.Field()
#     saves = scrapy.Field()
#     save_pct = scrapy.Field()
#     draw_controls = scrapy.Field()

class Coach(scrapy.Item):
    uuid = scrapy.Field()
    team = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    seasons = scrapy.Field()
    wins = scrapy.Field()
    loses = scrapy.Field()
