# scripts/getCurrentData.p
import pandas as pd
import cloudscraper
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')

scraper = cloudscraper.create_scraper()


def getMVP():
    years = list(range(1956, 2024))

    url_start = "https://www.basketball-reference.com/awards/awards_{}.html"

    dfs = []
    
    for year in years:
        url = url_start.format(year)
        data = scraper.get(url)

        try:
            with open('html/{}.html'.format(year), 'w+', encoding="utf-8") as f:
                f.write(data.text)
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")
            return False


    with open('html/{}.html'.format(year), encoding="utf-8") as f:
        page = f.read()

    soup = BeautifulSoup(page, "html.parser")
    soup.find('tr', class_='over_header').decompose()
    mvp_table = soup.find(id="mvp")
    mvp = pd.read_html(str(mvp_table))[0]
    mvp['Year'] = year

    dfs.append(mvp)

    mvps = pd.concat(dfs)
    mvps.to_csv("mvp/csv/{}.csv".format(year))

    mvps.reset_index(inplace=True)

    mvps.to_json("mvp/json/{}.json".format(year), orient='records', lines=True)
    
    return True

def getTeams():

    team_stats_url = "https://www.basketball-reference.com/leagues/NBA_{}_standings.html"

    url = team_stats_url.format(year)

    data = scraper.get(url)

    try:
        with open("team/html/{}.html".format(year), "w+", encoding="utf-8") as f:
            f.write(data.text)
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")
        return False

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


def getPlayers():
    year = current_year + 1

    player_stats_url = 'https://www.basketball-reference.com/leagues/NBA_{}_per_game.html'

    url = player_stats_url.format(year)
    data = scraper.get(url)

    try:
        with open('player/html/{}.html'.format(year), 'w+',  encoding='utf-8') as f:
            f.write(data.text)
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")
        return False

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


def getStats():
    year = current_year

    player_stats_url = "https://www.basketball-reference.com/leagues/NBA_{}_advanced.html"

    url = player_stats_url.format(year)
    data = scraper.get(url)

    try:
        with open('advanced/html/{}.html'.format(year), 'w+',  encoding='utf-8') as f:
            f.write(data.text)
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")
        return False

    dfs = []

    with open('advanced/html/{}.html'.format(year), encoding="utf-8") as f:
        page = f.read()

    soup = BeautifulSoup(page, "html.parser")
    # soup.find('tr', class_='thead').decompose()
    player_table = soup.find(id="switcher_advanced")

    try:
        player = pd.read_html(str(player_table))[0]

    except Exception as e:
        print(f"An unexpected error occuried: {e}")
        return False

    player['Year'] = year

    dfs.append(player)

    players = pd.concat(dfs)

    players = players.dropna(axis=0, subset=['Age'])

    players.to_csv("advanced/csv/{}.csv".format(year))

    players.reset_index(inplace=True)

    players.to_json("advanced/json/{}.json".format(year), orient='records', lines=True)

    return True

if __name__ == "__main__":
    gotTeams = False
    gotPlayers = False
    gotMVP = False
    gotStats = False

    gotTeams = getTeams()
    gotPlayers = getPlayers()
    gotMVP = getMVP()
    gotStats = getStats()

    print("\n" + "=" * 80)
    print("📋 Got Teams?")
    print("=" * 80)
    print(gotTeams)

    print("\n" + "=" * 80)
    print("💾 Got Players?")
    print("=" * 80)
    print(gotPlayers)

    print("\n" + "=" * 80)
    print("❓ Got MVP?")
    print("=" * 80)
    print(gotMVP)

    print("\n" + "=" * 80)
    print("📊 Got Stats?")
    print("=" * 80)
    print(gotStats)