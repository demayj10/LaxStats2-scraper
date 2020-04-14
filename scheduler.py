import schedule
import mysql.connector
import time
from datetime import datetime
import os


def clear_data():
    try:
        conn = mysql.connector.connect(
            host='laxstats.c1rvoewfjdxl.us-east-2.rds.amazonaws.com',
            user='laxadmin',
            passwd='laxstats#32',
            database='laxstats'
        )
        cur = conn.cursor()

        truncate_arr = ["TRUNCATE TABLE Rankings",
                        "ALTER TABLE Rankings AUTO_INCREMENT = 1"]
        for e in truncate_arr:
            cur.execute(e)
            conn.commit()
            print(e + ": was executed")
    except mysql.connector.Error as error:
        print("Failed to truncate and reset the Rankings table: {}".format(error))
    finally:
        if (conn.is_connected()):
            cur.close()
            conn.close()
            print("\nMySQL connection is closed\n")


def run_scraper():
    print("\n")
    """
    Consider implementing test cases and only running spider if cases pass
    if tests fail, stop function execution and email me about issue
    """
    clear_data()
    os.system("python run.py")
    print("Log Parser starting....\n")
    os.system('python logParser.py')
    print("-------------------------\nScraper finished @ {}\n-------------------------\n".format(
        datetime.now().strftime("%H:%M")))


schedule.every().day.at("18:38").do(run_scraper)

while True:
    schedule.run_pending()
    time.sleep(1)
