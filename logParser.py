import os
from datetime import date


def parseLine(line):
    if (('INFO' in line or 'WARNING' in line or 'CRITICAL' in line or 'ERROR' in line) and 'scrapy' not in line and 'log_count' not in line):
        start = 'WARNING'
        if ('INFO' in line):
            start = 'INFO'
        elif ('CRITICAL' in line):
            start = 'CRITICAL'
        elif ('ERROR' in line):
            start = 'ERROR'
        arr = line.split(':')
        text = start + ':' + arr[len(arr) - 1]
        return text
    return "None"


def writeToFile(fileOut, line_dict):
    with open(fileOut, "a+") as f:
        f.write('File contains {} ERROR messages, {} CRITICAL messages, {} WARNING messages and {} INFO messages\n'.format(
            len(line_dict["error"]), len(line_dict["critical"]), len(line_dict["warning"]), len(line_dict["info"])))

        f.write('\n-----ERROR-----\n')
        for line in line_dict["error"]:
            f.write('{}\n'.format(line))
        f.write('\n-----CRITICAL-----\n')
        for line in line_dict["critical"]:
            f.write('{}\n'.format(line))
        f.write('\n-----WARNING-----\n')
        for line in line_dict["warning"]:
            f.write('{}\n'.format(line))
        f.write('\n-----INFO-----\n')
        for line in line_dict["info"]:
            f.write('{}\n'.format(line))


path = os.path.split(os.getcwd())[0]
folders = ['divisions', 'teams', 'coaches', 'games', 'players', 'rankings']
for folder in folders:
    inPath = path + "\\laxstatscraper\\laxstatscraper\\logs"
    filenameIn = inPath + "\\{}\\{}.log".format(folder, date.today())

    outPath = path + "\\laxstatscraper\\laxstatscraper\\cleanLogs"
    filenameOut = outPath + "\\{}\\{}.log".format(folder, date.today())
    log_dict = {"info": [], "warning": [], "critical": [], "error": []}
    try:
        with open(filenameIn) as fIn:
            print("Opened file {}".format(filenameIn))
            for line in fIn:
                res = parseLine(line.rstrip())
                if res != "None":
                    if 'WARNING' in res:
                        log_dict["warning"].append(res)
                    elif 'INFO' in res:
                        log_dict["info"].append(res)
                    else:
                        log_dict["critical"].append(res)
            print("Finished parsing file {}\n".format(filenameIn))
        writeToFile(filenameOut, log_dict)
    except FileNotFoundError:
        print("Whoops! File {} could not be found!\n".format(filenameIn))
