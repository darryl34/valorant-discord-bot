import requests
from bs4 import BeautifulSoup as bs4

prefix = "https://tracker.gg/valorant/profile/riot/"
suffix = "/overview?playlist=unrated"

def processAccuracy(accuracy):
    result = []
    accuracy = accuracy.split()
    for num in accuracy:
        result.append(float(num.strip('%'))/100.0)
    return result

def parse(valTag):
    URL = prefix + valTag + suffix
    page = requests.get(URL)

    soup = bs4(page.content, 'html.parser')
    results = soup.find(id="app")

    result = []
    topWeapons = results.find_all('div', class_='weapon')
    for weapon in topWeapons:
        weaponName = weapon.find('div', class_='weapon__name').text
        accuracy = weapon.find('div', class_='weapon__accuracy-hits').text
        accuracy = processAccuracy(accuracy)
        killsDiv = weapon.find('div', class_='weapon__main-stat')
        kills = killsDiv.find('span', class_='value').text

        result.append([weaponName, accuracy, kills])
    return result