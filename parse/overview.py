import requests
from bs4 import BeautifulSoup as bs4
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
    print(topWeapons)
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

if __name__ == "__main__":
    getTopWeapons("darryl%237534")