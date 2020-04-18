import time
import os
from datetime import datetime
from datetime import date
import logging


def get_time(elapsed_time):
    hours = elapsed_time / 3600
    seconds = elapsed_time % 60
    minutes = (elapsed_time - seconds) / 60

    hours_string = str(int(hours))
    minutes_string = str(int(minutes))
    seconds_string = str(int(seconds))

    if hours < 10:
        hours_string = "0" + hours_string
    if minutes < 10:
        minutes_string = "0" + minutes_string
    if seconds < 10:
        seconds_string = "0" + seconds_string

    string = "{}:{}:{}".format(hours_string, minutes_string, seconds_string)
    return string


def get_command():
    commands = ['python laxstatscraper\\runSpiders\\runDivisionSpider.py', 'laxstatscraper\\python runSpiders\\runTeamSpider.py', 'laxstatscraper\\python runSpiders\\runCoachSpider.py',
                'python laxstatscraper\\runSpiders\\runPlayerSpider.py', 'laxstatscraper\\python runSpiders\\runRankingSpider.py', 'laxstatscraper\\python runSpiders\\runGameSpider.py']
    run_command = ''
    for command in commands:
        run_command += '{} && '.format(command)
    run_command = run_command[:-3]
    return run_command


def run_spiders():
    commands = ['python laxstatscraper\\runSpiders\\runDivisionSpider.py',
                'python laxstatscraper\\runSpiders\\runTeamSpider.py',
                'python laxstatscraper\\runSpiders\\runCoachSpider.py',
                'python laxstatscraper\\runSpiders\\runPlayerSpider.py',
                'python laxstatscraper\\runSpiders\\runRankingSpider.py',
                'python laxstatscraper\\runSpiders\\runGameSpider.py']

    spider_times = []

    for command in commands:
        start_time = time.time()
        os.system(command)
        elapsed_time = time.time() - start_time
        time_string = get_time(elapsed_time)

        spider_times.append(time_string)

    return spider_times


def output_times(spider_times, total):
    f = open('laxstatscraper\\cleanLogs\\runtimes.log', "a")

    f.write("{}||{},{},{},{},{},{},{}\n".format(date.today(
    ), spider_times[0], spider_times[1], spider_times[2], spider_times[3], spider_times[4], spider_times[5], total))

    f.close()

    print("\n-----------------------------------------------------------")
    print("{:28}{}".format("Division Scraper Runtime", spider_times[0]))
    print("{:28}{}".format("Team Scraper Runtime:", spider_times[1]))
    print("{:28}{}".format("Coach Scraper Runtime:", spider_times[2]))
    print("{:28}{}".format("Player Scraper Runtime:", spider_times[3]))
    print("{:28}{}".format("Ranking Scraper Runtime:", spider_times[4]))
    print("{:28}{}".format("Game Scraper Runtime:", spider_times[5]))
    print("-----------------------------------------------------------")
    print("{:28}{}".format("Total time: ", total))
    print("-----------------------------------------------------------\n")


print("\nStart spiders")
start_time = time.time()

# print(get_command())
spider_times = run_spiders()

print("Spiders finished")
elapsed_time = time.time() - start_time
total_time = get_time(elapsed_time)

output_times(spider_times, total_time)
