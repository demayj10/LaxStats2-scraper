import mysql.connector
from config.index import DatabaseConfig


class TeamLinks():

    def __init__(self):
        self.create_connection()

        self.team_links = self.fill_team_links()

        self.close_connection()

    def create_connection(self):
        config = DatabaseConfig()
        self.conn = mysql.connector.connect(
            host=config.host,
            user=config.user,
            passwd=config.passwd,
            database=config.database
        )
        self.cur = self.conn.cursor()

    def fill_team_links(self):
        links = []
        self.cur.execute("""SELECT * FROM TeamLinks""")
        for link in self.cur.fetchall():
            links.append(link[1])
        return links

    def close_connection(self):
        self.cur.close()
        self.conn.close()


class RosterLinks():
    def __init__(self):
        self.create_connection()

        self.roster_links = self.fill_roster_links()

        self.close_connection()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='laxstats.c1rvoewfjdxl.us-east-2.rds.amazonaws.com',
            user='laxadmin',
            passwd='laxstats#32',
            database='laxstats'
        )
        self.cur = self.conn.cursor()

    def fill_roster_links(self):
        links = []
        self.cur.execute("""SELECT * FROM RosterLinks""")
        for link in self.cur.fetchall():
            links.append(link[1])
        return links

    def close_connection(self):
        self.cur.close()
        self.conn.close()
