# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector
import logging
import os
from datetime import date
from config.index import DatabaseConfig


class LaxstatscraperPipeline(object):

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        config = DatabaseConfig()
        self.conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            passwd=config.passwd,
            database=config.database
        )
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        if spider.name == "d1players":
            # self.insert_player(item)
            self.update_player(item)
        elif spider.name == "d1teams":
            # self.insert_team(item)
            self.update_team(item)
        elif spider.name == 'd1coaches':
            # self.insert_coach(item)
            self.update_coach(item)
        elif spider.name == 'd1games':
            # self.insert_game(item)
            self.update_game(item)
        elif spider.name == 'd1':
            # self.insert_division(item)
            self.update_division(item)
        elif spider.name == 'd1rankings':
            self.insert_ranking(item)

    # Attempts to insert the player data in the database; returns True if successful, else False
    def insert_player(self, item, team_id):
        try:
            self.cur.execute("""INSERT INTO Player (uuid, team_id, first_name, last_name, jersey, year, position, games_played, goals, assists, points, shots, shot_pct, sog, sog_pct, groundballs, turnovers, caused_turnovers, faceoff_wins, faceoffs_taken, faceoff_win_pct, penalties, penalty_time, goals_allowed, saves, save_pct) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                item['uuid'],
                team_id,
                item['first_name'],
                item['last_name'],
                item['jersey'],
                item['year'],
                item['position'],
                item['games_played'],
                item['goals'],
                item['assists'],
                item['points'],
                item['shots'],
                item['shot_pct'],
                item['sog'],
                item['sog_pct'],
                item['groundballs'],
                item['turnovers'],
                item['caused_turnovers'],
                item['faceoff_wins'],
                item['faceoffs_taken'],
                item['faceoff_win_pct'],
                item['penalties'],
                item['penalty_time'],
                item['goals_allowed'],
                item['saves'],
                item['save_pct']
            ))
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print("There was an error while trying to insert player \'{} {}\' for \'{}\': {}".format(
                item['first_name'], item['last_name'], item['team'], err))
            return False

    def update_player(self, item):
        team_id = self.get_team_id(item['team'])

        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        playerFileName = os.path.join(os.path.dirname(os.path.realpath(
            __file__)), 'logs\\players\\{}.log'.format(date.today()))
        logging.basicConfig(filename=playerFileName, level=logging.DEBUG)
        player_logger = logging.getLogger(playerFileName)

        if team_id > 0:
            player_id = self.get_player_id(
                item['first_name'], item['last_name'], item['jersey'], team_id, item['team'])

            if player_id > 0:
                self.cur.execute("""UPDATE Player SET position=%s, games_played=%s, goals=%s, assists=%s, points=%s, shots=%s, shot_pct=%s, sog=%s, sog_pct=%s, groundballs=%s, turnovers=%s, caused_turnovers=%s, faceoff_wins=%s, faceoffs_taken=%s, faceoff_win_pct=%s, penalties=%s, penalty_time=%s, goals_allowed=%s, saves=%s, save_pct=%s WHERE id=%s""", (
                    item['position'],
                    item['games_played'],
                    item['goals'],
                    item['assists'],
                    item['points'],
                    item['shots'],
                    item['shot_pct'],
                    item['sog'],
                    item['sog_pct'],
                    item['groundballs'],
                    item['turnovers'],
                    item['caused_turnovers'],
                    item['faceoff_wins'],
                    item['faceoffs_taken'],
                    item['faceoff_win_pct'],
                    item['penalties'],
                    item['penalty_time'],
                    item['goals_allowed'],
                    item['saves'],
                    item['save_pct'],
                    player_id
                ))
                player_logger.info("Player \'{} {}\' has been updated for team \'{}\'".format(
                    item['first_name'], item['last_name'], item['team']))
            else:
                player_logger.warning("Player \'{} {}\' for team \'{}\' not found in database, adding...".format(
                    item['first_name'], item['last_name'], item['team']))
                res = self.insert_player(item, team_id)

                if res:
                    player_logger.info("Player \'{} {}\' for team \'{}\' has been added to the database".format(
                        item['first_name'], item['last_name'], item['team']))
                else:
                    player_logger.critical("Player \'{} {}\' for team \'{}\' has not been added to the database, an error must've occured in the insert proccess!".format(
                        item['first_name'], item['last_name'], item['team']))
        return

    # Attempts to insert the team data in the database; returns True if successful, else False
    def insert_team(self, item):
        try:
            self.cur.execute("""INSERT INTO Team (uuid, division_id, logo_url, team_name, wins, loses, ties) VALUES (%s, %s, %s, %s, %s, %s, %s)""", (
                item['uuid'],
                item['division_id'],
                item['logo'],
                item['name'],
                item['wins'],
                item['loses'],
                item['ties']
            ))
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print("There was an error while trying to insert team '{}': {}".format(
                item['name'], err))
            return False

    def update_team(self, item):
        team_id = self.get_team_id(item['name'])

        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        teamFileName = os.path.join(os.path.dirname(os.path.realpath(
            __file__)), 'logs\\teams\\{}.log'.format(date.today()))
        logging.basicConfig(filename=teamFileName, level=logging.DEBUG)
        team_logger = logging.getLogger(teamFileName)

        if team_id > 0:
            self.cur.execute("""UPDATE Team SET wins=%s, loses=%s, ties=%s WHERE team_name=%s""", (
                item['wins'],
                item['loses'],
                item['ties'],
                item['name']
            ))
            self.conn.commit()
            team_logger.info("Team {} has been updated".format(item['name']))
        else:
            team_logger.warning("Team {} not found in database, adding...".format(
                item['name']))
            res = self.insert_team(item)

            if res:
                team_logger.info("Team {} has been added to the database".format(
                    item['name']))
            else:
                team_logger.critical(
                    "Team '{}' has not been added to the database, an error must've occured during the insert process!".format(item['name']))

    # Attempts to insert the coach data in the database; returns True if successful, else False
    def insert_coach(self, item, team_id):
        try:
            self.cur.execute("""INSERT INTO Coach (uuid, team_id, first_name, last_name, seasons, wins, loses) VALUES (%s, %s, %s, %s, %s, %s, %s)""", (
                item['uuid'],
                team_id,
                item['first_name'],
                item['last_name'],
                item['seasons'],
                item['wins'],
                item['loses']
            ))
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print("There was an error while trying to insert coach \'{} {}\' for \'{}\': {}".format(
                item["first_name"], item["last_name"], item["team"], err))
            return False

    def update_coach(self, item):
        team_id = self.get_team_id(item['team'])

        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        coachFileName = os.path.join(os.path.dirname(os.path.realpath(
            __file__)), 'logs\\coaches\\{}.log'.format(date.today()))
        logging.basicConfig(filename=coachFileName, level=logging.DEBUG)
        coach_logger = logging.getLogger(coachFileName)

        if team_id > 0:
            coach_id = self.get_coach_id(
                item['first_name'], item['last_name'], team_id)

            if coach_id > 0:
                self.cur.execute("""UPDATE Coach SET wins=%s, loses=%s, seasons=%s WHERE first_name=%s AND last_name=%s AND team_id=%s""", (
                    item['wins'],
                    item['loses'],
                    item['seasons'],
                    item['first_name'],
                    item['last_name'],
                    team_id
                ))
                self.conn.commit()
                coach_logger.info("Coach \'{} {}\' has been updated for Team \'{}\'".format(
                    item['first_name'], item['last_name'], item['team']))
            else:
                coach_logger.warning(
                    "Coach \'{} {}\' for \'{}\' not found in database, adding...".format(item['first_name'], item['last_name'], item['team']))
                res = self.insert_coach(item, team_id)

                if res:
                    coach_logger.info(
                        "Coach \'{} {}\' for \'{}\' has been added to the database".format(item['first_name'], item['last_name'], item['team']))
                else:
                    coach_logger.critical(
                        "Coach \'{} {}\' for \'{}\' has not been added to the database, an error must've occured during the insert process!".format(item['first_name'], item['last_name'], item['team']))
        else:
            coach_logger.critical("Team Id for \'{}\' not found, Coach \'{} {}\' has not been added".format(
                item['team'], item['first_name'], item['last_name']))

    # Attempts to insert the game data in the database; returns True if successful, else False
    def insert_game(self, item, team_id, opp_id):
        try:
            date_arr = item['date'].split("/")
            year = date_arr[2]
            day = date_arr[1]
            month = date_arr[0]
            fixed_date = year + '-' + month + '-' + day
            self.cur.execute("""INSERT INTO Game (uuid, team_id, date, opponent_id, result) VALUES (%s, %s, %s, %s, %s)""", (
                item['uuid'],
                team_id,
                fixed_date,
                opp_id,
                item['result']
            ))
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print("There was an error while trying to insert game between \'{}\' and \'{}\': {}".format(
                item['team'], item['opponent'], err))
            return False

    def update_game(self, item):
        team_id = self.get_team_id(item['team'])
        opp_id = self.get_team_id_contains(item['opponent'] + "%")

        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        gameFileName = os.path.join(os.path.dirname(os.path.realpath(
            __file__)), 'logs\\games\\{}.log'.format(date.today()))
        logging.basicConfig(filename=gameFileName, level=logging.DEBUG)
        game_logger = logging.getLogger(gameFileName)

        if team_id > 0 and opp_id > 0:
            game_id = self.get_game_id(team_id, opp_id)

            if game_id > 0:
                date_arr = item['date'].split("/")
                year = date_arr[2]
                day = date_arr[1]
                month = date_arr[0]
                fixed_date = year + '-' + month + '-' + day
                self.cur.execute("""UPDATE Game SET date=%s, result=%s WHERE id=%s""", (
                    fixed_date,
                    item['result'],
                    game_id
                ))
                self.conn.commit()
                game_logger.info("Game between \'{}\' and \'{}\' on \'{}\' has been added to database".format(
                    item['team'], item['opponent'], fixed_date))
            else:
                game_logger.warning(
                    "Game between \'{}\' and \'{}\' not found in database, adding...".format(item['team'], item['opponent']))
                res = self.insert_game(item, team_id, opp_id)

                if res:
                    game_logger.info(
                        "Game between \'{}\' and \'{}\' has been added to the database".format(item['team'], item['opponent']))
                else:
                    game_logger.critical("Game between \'{}\' and \'{}\' has not been added to the database, an error must've occured during the insert process!".format(
                        item['team'], item['opponent']))
        else:
            if team_id < 1:
                game_logger.critical("Game Team \'{}\' not found in database, game not added".format(
                    item['team']))
            if opp_id < 1:
                game_logger.critical("Game Opponent \'{}\' not found in database, game not added. TEAM: {}".format(
                    item['opponent'], item['team']))

    # Attempts to insert the division data in the database; returns True if successful, else False
    def insert_division(self, item):
        try:
            current_date = date.today()
            self.cur.execute("""INSERT INTO Division (div_name, last_updated) VALUES (%s, %s)""", (
                item['name'],
                current_date
            ))
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print("There was an error while trying to insert divsion \'{}\': {}".format(
                item['name'], err))
            return False

    def update_division(self, item):
        div_id = self.get_div_id(item['name'])

        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        divisionFileName = os.path.join(os.path.dirname(os.path.realpath(
            __file__)), 'logs\\divisions\\{}.log'.format(date.today()))
        logging.basicConfig(filename=divisionFileName, level=logging.DEBUG)
        division_logger = logging.getLogger(divisionFileName)

        if div_id > 0:
            # Date is not updating in database
            current_date = str(date.today())
            self.cur.execute("""UPDATE Division SET last_updated=%s WHERE id=%s""", (
                current_date,
                div_id
            ))
            division_logger.info(
                "Division \'{}\' has been updated".format(item['name']))
        else:
            division_logger.warning("Division \'{}\' not found in database, adding now...".format(
                item['name']))
            res = self.insert_division(item)

            if res:
                division_logger.info(
                    "Division \'{}\' has been added to the database".format(item['name']))
            else:
                division_logger.critical(
                    "Division \'{}\' has not been added to the database, an error must've occured in the insert process!".format(item['name']))

    def insert_ranking(self, item):
        team_id = self.get_team_id_contains(item['team'])
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        rankingFileName = os.path.join(os.path.dirname(os.path.realpath(
            __file__)), 'logs\\rankings\\{}.log'.format(date.today()))
        logging.basicConfig(filename=rankingFileName, level=logging.DEBUG)
        ranking_logger = logging.getLogger(rankingFileName)
        if team_id > 0:
            self.cur.execute("""INSERT INTO Rankings (rank, team_id) VALUES (%s, %s)""", (
                item['rank'],
                team_id
            ))
            self.conn.commit()
            ranking_logger.info("Team \'{}\' with rank #{} has been successfully been added to the database.".format(
                item['team'], item['rank']))
        else:
            ranking_logger.warning("Couldn't add ranking for team \'{}\' because a corresponding id could not be found in the database.".format(
                item['team']))

    # Helper method to find if team is in DB already with similar name
    def get_team_id_contains(self, team):
        team_id = 0
        try:
            self.cur.execute("""SELECT id FROM Team WHERE team_name LIKE %s""", (
                team + "%",
            ))
            for x in self.cur.fetchall()[0]:
                team_id = x
        except mysql.connector.Error:
            print("Team id not found")
        finally:
            return team_id

    # Helper method to find if team is in DB already with exact name; returns 0 if id not found
    def get_team_id(self, team_name):
        team_id = 0
        try:
            self.cur.execute("""SELECT id FROM Team WHERE team_name=%s""", (
                team_name,
            ))
            for x in self.cur.fetchall()[0]:
                team_id = x
        except mysql.connector.Error as err:
            print("Something went wrong trying to find the team id for {}: {}".format(
                team_name, err))
        finally:
            return team_id

    # Helper method to find if the division is already in the database; returns 0 if id not found
    def get_div_id(self, div_name):
        div_id = 0
        try:
            self.cur.execute("""SELECT id FROM Division WHERE div_name=%s""", (
                div_name,
            ))
            for x in self.cur.fetchall()[0]:
                div_id = x
        except mysql.connector.Error as err:
            print("Something went wrong trying to find the {} id: {}".format(
                div_name, err))
        finally:
            return div_id

    # Helper method to find if the coach is already in the database; returns 0 if id not found
    def get_coach_id(self, first_name, last_name, team_id):
        coach_id = 0
        try:
            self.cur.execute("""SELECT id FROM Coach WHERE first_name=%s AND last_name=%s AND team_id=%s""", (
                first_name,
                last_name,
                team_id
            ))
            for x in self.cur.fetchall()[0]:
                coach_id = x
        except mysql.connector.Error as err:
            print("Something went wrong trying to find the coach id for {} {}: {}".format(
                first_name, last_name, err))
        finally:
            return coach_id

    # Helper method to find if the player is already in the database; returns 0 if id not found
    def get_player_id(self, first_name, last_name, jersey, team_id, team_name):
        player_id = 0
        try:
            self.cur.execute("""SELECT id FROM Player WHERE first_name=%s AND last_name=%s AND jersey=%s AND team_id=%s""", (
                first_name,
                last_name,
                jersey,
                team_id
            ))
            for x in self.cur.fetchall()[0]:
                player_id = x
        except mysql.connector.Error as err:
            print("Something went wrong trying to find the player id for #{}, {} {} of {}: {}".format(
                jersey, first_name, last_name, team_name, err))
        finally:
            return player_id

    # Helper method to find if the player is already in the database; returns 0 if id not found
    def get_game_id(self, team_id, opponent_id):
        game_id = 0
        try:
            self.cur.execute("""SELECT id FROM Game WHERE team_id=%s AND opponent_id=%s""", (
                team_id,
                opponent_id
            ))
            for x in self.cur.fetchall()[0]:
                game_id = x
        except mysql.connector.Error as err:
            print("Something went wrong trying to find the game id for the game between team_id={} and opponent_id={}: {}".format(
                team_id, opponent_id, err))
        finally:
            return game_id
