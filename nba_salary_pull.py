import datetime
import os
import re
import time
from urllib.request import urlopen, Request

import bs4 as bs
import pandas as pd

path = os.getcwd().replace("\\", '/') + '/'
def main(year1, year2):
    """
    Grabs data from the URL. It then creates a dataframe with columns: Player, Salary, Adj. Salary and Season (season is used to combine all years)
    :param year1: year to start at --- (year1, year1 +1) salary data
    :param year2: year to end at ---- (year2-1, year2) salary data
    :return: dataframe with player salaries for that year
    """
    URL = f"https://hoopshype.com/salaries/players/{year1}-{year2}/"
    request = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    soup = bs.BeautifulSoup(urlopen(request).read(), 'html.parser')
    players = [x.text.strip() for x in soup.findAll('table')[0].findAll('td', {'class': 'name'})]
    all_salaries = [x.text.strip().replace('$', '').replace(',', '') for x in soup.findAll('table')[0].findAll('td', {'class': ''})]
    salaries = list(all_salaries[0::2])
    adjusted_salaries = all_salaries[1::2]
    return pd.DataFrame(data = dict(Player = players[1:], Salary = salaries[1:], AdjustedSalary = adjusted_salaries[1:], Season = [f'{year1}-{year2}' for x in range(len(players)-1)]))

timee = datetime.datetime.now()
print(timee)
# create a list of the dataframes, to be concatenated to a larger dataframe with all salary data
bigdf = pd.concat([main(x, x+1) for x in range(2006, 2019)])
bigdf.to_csv(path + 'playersalaries.csv', index = False)
print(datetime.datetime.now()-timee)
