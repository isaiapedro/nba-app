#remove warnings
import warnings
warnings.filterwarnings('ignore')

#matrix manipulation
import pandas as pd

#scrapping data
import cloudscraper
from bs4 import BeautifulSoup
import html5lib

#date
from datetime import datetime

def getPlayers():
    current_year = datetime.now().year

    year = current_year + 1

    player_stats_url = 'https://www.basketball-reference.com/leagues/NBA_{}_per_game.html'

    scraper = cloudscraper.create_scraper() 

    url = player_stats_url.format(year)
    data = scraper.get(url)

    with open('player/html/{}.html'.format(year), 'w+',  encoding='utf-8') as f:
        f.write(data.text)

    dfs = []

    with open('player/html/{}.html'.format(year), encoding="utf-8") as f:
        page = f.read()

    soup = BeautifulSoup(page, "html.parser")
    player_table = soup.find(id="switcher_per_game_stats")

    try:
        player = pd.read_html(str(player_table))[0]

    except Exception as e:
        print(f"An unexpected error occuried: {e}")
        return False

    player['Year'] = year

    dfs.append(player)

    players = pd.concat(dfs)

    players = players.dropna(axis=0, subset=['Age'])

    players.to_csv("player/csv/{}.csv".format(year))

    players.reset_index(inplace=True)

    players.to_json("player/json/{}.json".format(year), orient='records', lines=True)

    return True