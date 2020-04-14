import scrapy


class Parser():

    def __init__(self):
        super().__init__()

    # Parses the team page header and returns the team name, [record]
    def parse_team_header(self, page, url):
        team_name = ""
        record_arr = []
        # Special Case: Hobart
        if url == "https://stats.ncaa.org/team/282/stats/15203" or url == "https://stats.ncaa.org/teams/493855":
            header = page.xpath(
                '//*[@id="contentarea"]/fieldset[1]/legend/text()').get()
            header_arr = header.split("(")
            team_name = header_arr[0].strip()
            record_arr = header_arr[1].strip().split(")")[0].split("-")
        else:
            team_name = page.xpath(
                '//*[@id="contentarea"]/fieldset[1]/legend/a/text()').get()
            team_record = page.xpath(
                '//*[@id="contentarea"]/fieldset[1]/legend/text()[2]').get()
            team_record = team_record.replace('(', '')
            team_record = team_record.replace(')', '')
            record_arr = team_record.split('-')

        return team_name, record_arr

    # Parses the gross field_set that is the coach data and returns values in a tuple formatted:
    # (coach_first_name, coach_last_name, seasons, wins, loses)
    def parse_coach_data(self, page):
        coach_name = page.xpath(
            '//*[@id="head_coaches_div"]/fieldset/a/text()').get()
        field_arr = page.xpath(
            '//*[@id="head_coaches_div"]/fieldset/text()').getall()
        want_arr = []
        for x in field_arr:
            x = x.strip()
            if len(x) > 0:
                first = x[0]
                if first.isnumeric():
                    want_arr.append(x)
        coach_name = coach_name.split(' ')
        coach_first_name = coach_name[0]
        coach_last_name = coach_name[1]
        seasons = want_arr[0]
        record_full = want_arr[1]
        record_full = record_full.split('-')
        wins = record_full[0]
        loses = record_full[1]

        return coach_first_name, coach_last_name, seasons, wins, loses


class Data_Formatter():

    def __init__(self):
        super().__init__()

    # Used to unabbreviate a Team name
    # The shortend version comes from ncaa stats and lengthen is coming from rankings page
    def lengthen_abbreviated(self, name):
        team = name
        if team == "Penn State":
            team = "Penn St."
        elif team == "Ohio State":
            team = "Ohio St."

        return team
