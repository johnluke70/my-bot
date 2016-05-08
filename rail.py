import os
import fnmatch
import shutil
import gzip
import time
import datetime
import subprocess
import requests
import json
import token
import re
from string import ascii_letters, punctuation, whitespace
from requests.auth import HTTPBasicAuth

# import stomp


# Define Global Path Vars
homedir = '/Users/John/Dropbox/Programming/TrainApp/'
extractdir = homedir + 'extracts/'
downloaddir = '/Users/John/Downloads/'


def getCreds(vtype):
    credFile = "rail_token.txt"
    f = open(credFile)
    cred = f.readline()
    return cred


def getStaticData():
    url = "https://datafeeds.networkrail.co.uk/ntrod/CifFileAuthenticate?type=CIF_HU_TOC_FULL_DAILY&day=toc-full"
    # set auth tokens
    # This is a daily file, check it doesn't exist.
    # TODO fix the daily thing - just skips atm
    # TODO - can remove all checks. will download daily via cron....
    for f in os.listdir(extractdir):
        if fnmatch.fnmatch(f, 'CIF*.gz'):
            ftime = os.path.getmtime(extractdir + f)
            ftime = datetime.datetime.fromtimestamp(ftime)
            ctime = datetime.datetime.fromtimestamp(time.time())
            if ftime.year >= ctime.year:
                # print(ftime.year)
                # print(ctime.year)
                if ftime.month >= ctime.month:
                    # print(ftime.month)
                    # print(ctime.month)
                    if ftime.day >= ftime.day:
                        # print(ftime.month)
                        # print(ctime.month)
                        print('Already have current file. Skipping...')
            else:
                print("Don't have current file. Downloading...")
                r = requests.get(url, auth=HTTPBasicAuth(token.getToken('railuser'), token.getToken('railpass')))
                print(r.url)


def moveStaticData():
    for f in os.listdir(downloaddir):
        if fnmatch.fnmatch(f, 'CIF*.gz'):
            shutil.move(downloaddir + f, extractdir + f)
            print('Moved ' + f + ' to ' + extractdir)


def extractStaticData(filename):
    # TODO check for json first.. extracting is slowest operation
    print('Extracting ' + filename)
    pre, ext = os.path.splitext(filename)
    jfilename = pre + '.json'
    gfile = gzip.open(filename, 'rb')
    jfile = open(jfilename, 'wb')
    jfile.write(gfile.read())
    gfile.close()
    jfile.close()
    print('Extracted to ' + jfilename)


def parseStaticData(usrDept, usrDest, earliest, latest='blah', searchdate='blah'):
    # This function parses each line of json and works out whether relevant
    # Returns nested list of viable journeys.
    # filename = './extracts/reduced.json'
    # TODO make time input a bit friendlier. 7am = 700 atm
    filename = './extracts/CIF_HU_TOC_FULL_DAILY-toc-full.json'
    print('Parsing JSON')
    try:
        input_file = open(filename)
    except FileNotFoundError:
            extractStaticData(filename)
            input_file = open(filename)
    print('opened file')

    if searchdate == 'blah':
        # Use Today's date
        searchdate = datetime.date.today().strftime("%Y-%m-%d")

    # searchdate = '2016-05-08'
    # usrDept = 'CHRX'
    # usrDest = 'CHSLHRS'
    ignore = ascii_letters + punctuation + whitespace  # To get rid of trailing Hs in time data
    i = 0
    resultset = []  # Nested list to contain ALL results
    for line in input_file:
        jline = json.loads(line)

        if 'JsonScheduleV1' in jline:
            # print('This is the line \n')
            if 'schedule_segment' in jline['JsonScheduleV1']:
                if 'schedule_location' in jline['JsonScheduleV1']['schedule_segment']:
                    if jline['JsonScheduleV1']['schedule_end_date'] == searchdate:
                        callpoints = jline['JsonScheduleV1']['schedule_segment']['schedule_location']

                        result1 = []
                        listStation = []
                        listSchedul = []

                        for stop in callpoints:
                            if stop['location_type'] == 'LO':
                                # LO = Line Origin
                                station = stop['tiploc_code']
                                timestr = stop['departure']
                                timeint = int(''.join(j for j in timestr if j.isdigit()))
                                listStation.append(station)
                                listSchedul.append(timeint)

                            elif stop['location_type'] == 'LI':
                                # LI = Line 'Intra'?!
                                if stop['departure']:
                                    # train stops here
                                    station = stop['tiploc_code']
                                    timestr = stop['departure']
                                    timeint = int(''.join(j for j in timestr if j.isdigit()))
                                    listStation.append(station)
                                    listSchedul.append(timeint)
                                    # ELSE train passes here - Ignore it!

                            elif stop['location_type'] == 'LT':
                                # LT = Line Terminates
                                station = stop['tiploc_code']
                                timestr = stop['arrival']
                                timeint = int(''.join(j for j in timestr if j.isdigit()))
                                listStation.append(station)
                                listSchedul.append(timeint)

                    # print(listStation)
                    # print(listSchedul)

                    # At this point - listStation & listSchedule have the stops in for each json line
                        if usrDept in listStation:
                            l = listStation.index(usrDept)
                            if earliest <= listSchedul[l] <= latest:
                                if usrDest in listStation[l:]:
                                    j = 0
                                    for a, b in zip(listStation, listSchedul):
                                        result1.append(a + ':' + str(b))
                                        j += 1
                                    resultset.append(result1)

    resultset = dedupListOLists(resultset)
    nojourneys = resultset.__len__()
    if nojourneys > 0:
        if nojourneys == 1:
            print('Found 1 journey')
        else:
            print('Found ' + str(nojourneys) + ' journeys')
        for result in resultset:
            print(result)


def dedupListOLists(varList):
    # Dedupes list of lists (based on first element!)
    matches = []
    dedupped = []
    for singList in varList:
        if singList[0] not in matches:
            dedupped.append(singList)
            matches.append(singList[0])
    return dedupped


def getJourney(start='WLOE', finish='TUNWELL', dep_time='now', arr_time='now', date='today'):
    # This is a wrapper function for external calls

    # getStaticData()
    # moveStaticData()
    # extractStaticData('./extracts/CIF_HU_TOC_FULL_DAILY-toc-full.gz')

    parseStaticData('WLOE', 'TUNWELL', 900, 1300, '2016-05-08')

def getHelp():
    strHelp = 'start, end , arrival time, dept time, date'
    return strHelp

if __name__ == '__main__':
    getJourney()
