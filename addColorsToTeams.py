import os
import mysql.connector


class AddColorsToDB(object):
    def __init__(self):
        self.filename = os.getcwd() + "\\laxstatscraper\\inputData\\teamColors.txt"
        self.run()

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

    def add_to_database(self,  key, colors):
        team_id = self.get_team_id_contains(key)
        try:
            self.cur.execute("""UPDATE Team SET primary_color=%s, secondary_color=%s WHERE id=%s""", (
                colors[0],
                colors[1],
                team_id
            ))
            self.conn.commit()
            print('{} colors updated to {} and {}!'.format(
                key, colors[0], colors[1]))
        except mysql.connector.Error as err:
            print('There was an error: {}'.format(err))

    def get_color_dict(self):
        team_colors = {}
        try:
            with open(self.filename) as f:
                print("File opened!")
                for line in f:
                    data = self.parse_line(line)
                    team_colors[data[0]] = [data[1], data[2]]
            return team_colors
        except FileNotFoundError as err:
            print("Couldn't find file {}!".format(self.filename))

    def parse_line(self, line):
        data = line.split("||")
        clean = []
        for d in data:
            clean.append(d.strip())
        return clean

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='laxstats.c1rvoewfjdxl.us-east-2.rds.amazonaws.com',
            user='laxadmin',
            passwd='laxstats#32',
            database='laxstats'
        )
        self.cur = self.conn.cursor()
        print("Connection successful!")

    def run(self):
        self.create_connection()
        team_colors = self.get_color_dict()
        for key in team_colors:
            self.add_to_database(key, team_colors[key])
        self.cur.close()
        print("Connection closed!")


addColors = AddColorsToDB()
