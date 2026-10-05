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

def getMVP():
    current_year = datetime.now().year

    year = current_year

    url_start = "https://www.basketball-reference.com/awards/awards_{}.html"

    scraper = cloudscraper.create_scraper() 

    url = url_start.format(year)
    data = scraper.get(url)

    with open('mvp/html/{}.html'.format(year), 'w+', encoding="utf-8") as f:
        f.write(data.text)

    dfs = []

    with open('mvp/html/{}.html'.format(year), encoding="utf-8") as f:
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