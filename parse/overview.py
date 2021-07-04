import os
import requests
import time
import timeit
import lxml
import cchardet
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from parse.match import Match

prefix = "https://api.tracker.gg/api/v2/valorant/standard/matches/riot/"
unratedSuffix = "?type=unrated"
compSuffix = "?type=competitive"

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}


def getTopWeapons(valTag):
    URL = "https://tracker.gg/valorant/profile/riot/" + valTag + "/overview?playlist=unrated"
    page = requests.get(URL, headers=headers)

    soup = bs4(page.content, 'html.parser')
    results = soup.find(id="app")

    result = []
    topWeapons = results.find_all('div', class_='weapon')
    for weapon in topWeapons:
        weaponName = weapon.find('div', class_='weapon__name').text
        accuracy = weapon.find('div', class_='weapon__accuracy-hits').text
        accuracy = accuracy.split()
        killsDiv = weapon.find('div', class_='weapon__main-stat')
        kills = killsDiv.find('span', class_='value').text

        result.append([weaponName, accuracy, kills])
    return result

def getRecentUnrated(valTag):
    URL = prefix + valTag + unratedSuffix
    page = requests.get(URL, headers=headers).json()
    data = page["data"]
    recent = data["matches"][0]
    return parseMatch(recent)

def getRecentComp(valTag):
    URL = prefix + valTag + compSuffix
    page = requests.get(URL, headers=headers).json()
    data = page["data"]
    recent = data["matches"][0]
    return parseMatch(recent)


def parseMatch(jsonData):
    matchWin = jsonData["segments"][0]["metadata"]["hasWon"]
    agent = jsonData["segments"][0]["metadata"]["agentName"]
    map = jsonData["metadata"]["mapName"]
    stats = jsonData["segments"][0]["stats"]
    score = [stats['roundsWon']["value"], stats['roundsLost']["value"]]
    match = Match(matchWin, score, agent, map)
    match.setKDA(stats["kills"]["value"], stats["deaths"]["value"], stats["assists"]["value"])
    match.setADR(stats["damagePerRound"]["value"])
    match.setHS(stats["headshotsPercentage"]["displayValue"])

    return match

def getRank(valTag):
    URL = "https://tracker.gg/valorant/profile/riot/" + valTag + "/overview?playlist=competitive"
    page = requests.get(URL, headers=headers)

    soup = bs4(page.content, 'html.parser')
    results = soup.find(id="app")

    rankDiv = results.find('span', class_='valorant-highlighted-stat__value').text
    return rankDiv

def getTeammates(valTag, isComp=False):
    unratedURL = "https://tracker.gg/valorant/profile/riot/" + valTag + "/matches?playlist=unrated"
    compURL = "https://tracker.gg/valorant/profile/riot/" + valTag + "/matches?playlist=competitive"
    starttime = timeit.default_timer()
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options, executable_path=os.path.abspath("parse/chromedriver.exe"))
    # Only use when running this file
    # driver = webdriver.Chrome(os.path.abspath("chromedriver.exe"))
    if isComp:
        driver.get(compURL)
    else:
        driver.get(unratedURL)
    time.sleep(5)   # Give website time to load data

    soup = bs4(driver.page_source, 'lxml')
    results = soup.find(id="app")

    friends = results.find_all('div', class_='acquaintances__list-player')

    result = []
    for friend in friends:
        nameDiv = friend.find('div', class_='name')
        name = nameDiv.find('a').text
        matches = friend.find('div', class_='matches').text

        winrateDiv = friend.find('div', class_='stat stat--right')
        winrate = winrateDiv.find_all('div')[1].text
        result.append([name, matches, winrate])

    endtime = timeit.default_timer()
    return result, round(endtime-starttime, 3)

def getFiveUnrated(valTag):
    URL = "https://tracker.gg/valorant/profile/riot/" + valTag + "/overview?playlist=unrated"
    page = requests.get(URL, headers=headers)
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options, executable_path=os.path.abspath("parse/chromedriver.exe"))
    # Only use when running this file
    # driver = webdriver.Chrome(os.path.abspath("chromedriver.exe"))
    driver.get(URL)
    time.sleep(1)  # Give website time to load data

    soup = bs4(driver.page_source, 'html.parser')
    results = soup.find(id="app")

    result = []
    recentFive = results.find_all('span', class_='timeline-match__score')
    for match in recentFive[:5]:
        f_score = int(match.find('span', class_='timeline-match__score--winner').text.strip())
        s_score = int(match.find('span', class_='timeline-match__score--loser').text.strip())

        if f_score > s_score:
            status = "W "
        elif f_score == s_score:
            status = "D "
        else:
            status = "L "

        result.append(status)

    fiveH = "".join(result)
    return fiveH

def getFiveCompetitve(valTag):
    URL = "https://tracker.gg/valorant/profile/riot/" + valTag + "/overview?playlist=competitive"
    page = requests.get(URL, headers=headers)
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options, executable_path=os.path.abspath("parse/chromedriver.exe"))
    # Only use when running this file
    # driver = webdriver.Chrome(os.path.abspath("chromedriver"))
    driver.get(URL)
    time.sleep(1)  # Give website time to load data

    soup = bs4(driver.page_source, 'html.parser')
    results = soup.find(id="app")

    result = []
    recentFive = results.find_all('span', class_='timeline-match__score')
    for matches in recentFive[:5]:
        f_score = int(matches.find('span', class_='timeline-match__score--winner').text.strip())
        s_score = int(matches.find('span', class_='timeline-match__score--loser').text.strip())

        if f_score > s_score:
            status = "W "
        elif f_score == s_score:
            status = "D "
        else:
            status = "L "

        result.append(status)

    fiveH = "".join(result)
    return fiveH


def bestMaps(valTag):
    URL = "https://tracker.gg/valorant/profile/riot/" + valTag + "/maps?playlist=unrated"
    page = requests.get(URL, headers=headers)

    soup = bs4(page.content, 'html.parser')
    results = soup.find(id="app")

    mapData = []
    maps = results.find_all('div', class_='map-stats card header-bordered responsive')
    for map in maps:
        mapName = map.find('h2').text
        count = map.find('div', class_='map-stats__header-description').text
        count = count.split(' ', 1)[0]
        winRateDiv = map.find('div', class_='numbers')
        winRate = winRateDiv.find('span', class_='value').text
        mapData.append([mapName, count, winRate])

    return mapData


if __name__ == "__main__":
    bestMaps("darryl%237534")
