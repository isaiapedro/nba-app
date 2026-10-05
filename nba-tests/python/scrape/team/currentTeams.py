#remove warnings
import warnings
warnings.filterwarnings('ignore')

#matrix manipulation
import pandas as pd

#scrapping data
import cloudscraper
from bs4 import BeautifulSoup

#date
from datetime import datetime

def getTeams():
    current_year = datetime.now().year

    year = current_year + 1

    team_stats_url = "https://www.basketball-reference.com/leagues/NBA_{}_standings.html"

    scraper = cloudscraper.create_scraper() 

    url = team_stats_url.format(year)

    data = scraper.get(url)

    with open("team/html/{}.html".format(year), "w+", encoding="utf-8") as f:
        f.write(data.text)

    dfs = []

    with open("team/html/{}.html".format(year), encoding="utf-8") as f:
        page = f.read()

    soup = BeautifulSoup(page, "html.parser")
    team_table = soup.find(id="divs_standings_E")
    team = pd.read_html(str(team_table))[0]
    team['Year'] = year
    team['Team'] = team["Eastern Conference"]
    del team['Eastern Conference']
    dfs.append(team)

    soup = BeautifulSoup(page, "html.parser")
    team_table = soup.find(id="divs_standings_W")
    team = pd.read_html(str(team_table))[0]
    team['Year'] = year
    team['Team'] = team["Western Conference"]
    del team['Western Conference']
    dfs.append(team)

    teams = pd.concat(dfs)

    teams["W"] = pd.to_numeric(teams["W"], errors="coerce")
    teams = teams.dropna(axis=0, subset=['W'])

    teams.to_csv("team/csv/{}.csv".format(year))

    teams.reset_index(inplace=True)

    teams.to_json("team/json/{}.json".format(year), orient='records', lines=True)

    return True