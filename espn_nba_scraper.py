from selenium import webdriver
import time
import bs4 as bs
import re
import datetime
import pprint
import re
import pickle
from pprint import pprint
import pandas as pd
import numpy as np
import dask.dataframe as dd
from dask.distributed import Client, LocalCluster
import dask.delayed
import sqlite3
from selenium.webdriver.chrome.options import Options as chrome_options
import pymongo


def grab_soup(url_, browser="firefox"):
    """
    This function enables a driver (using Firefox or Chrome), goes to the URL, and retrieves the data after the JS is loaded.
    :param url_: url to go to to retrieve data
    :param browser: browser to use, defaults to firefox (requires geckodriver.exe on path)
    :return:
    soup - the data of the page
    driver - the browser (process) instance
    """
    if browser == 'chrome':
        chromeOptions = chrome_options()
        chromeOptions.add_experimental_option("prefs", {
            "download.default_directory": r"C:\Users\Julien\Downloads",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        chromeOptions.add_argument("--disable-gpu")
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument('--no-sandbox')
        chromeOptions.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=chromeOptions)
    else:
        firefoxOptions = firefox_options()
        firefoxOptions.set_preference("browser.download.folderList", 2)
        firefoxOptions.set_preference("browser.download.manager.showWhenStarting", False)
        firefoxOptions.set_preference("browser.download.dir", path.replace('/', '\\') + 'data\\downloads\\')
        firefoxOptions.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                      "application/octet-stream,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        driver = webdriver.Firefox(options=firefoxOptions)

    driver.get(url_)  # go to the URL
    html = driver.page_source
    time.sleep(1)  # sleep for 1 second  to ensure all JS scripts are loaded
    html = driver.execute_script("return document.body.outerHTML;")  # execute javascript code
    soup_ = bs.BeautifulSoup(html, 'lxml')  # read the data as html (using lxml driver)
    return soup_, driver


def main(URL):
    soup, driver = grab_soup(URL)
    try:
        reg = r'\/.\w{1,}-\w{1,}'
        players = {'1': [], '2': []}
        for each in range(1, 3):
            for xx in soup.find_all('table')[each]:
                b = xx.find_all('td', {'class': 'name'})
                for i in range(len(b)):
                    try:
                        y = b[i].find_all(href=True)[0]
                        players[str(each)].append(re.search(reg, y['href'])[0].replace('/', '').replace('-', ' '))
                    except:
                        pass
        driver.quit()
    except:
        driver.quit()
    return players


def make_df_matchup(cols, dat):
    row_headers = []
    team_1 = []
    team_2 = []
    for num, each in enumerate(dat):
        if num % 3 == 0:
            row_headers.append(each)
        elif (num - 1) % 3 == 0:
            team_1.append(each)
        else:
            team_2.append(each)
    return pd.DataFrame(data={str(cols[0]): row_headers, str(cols[1]): team_1, str(cols[2]): team_2})


def get_team_membership():
    for x in data['game_id'].unique():
        try:
            time1 = datetime.datetime.now()
            x = int(x)
            if str(x) not in list(game_id_dict.keys()):
                url = "http://www.espn.com/nba/boxscore?gameId={}".format(x)
                teams = main(url)
                game_id_dict[str(x)] = teams
                print(datetime.datetime.now() - time1, x, teams)
                pickle_out = open("game_id_player_mapping.pickle", "wb")
                pickle.dump(game_id_dict, pickle_out)
                pickle_out.close()
                # time.sleep(1)
        except:
            pass
    print(datetime.datetime.now() - timee)


def get_game_ids_regular_season(team, year):
    kk = [0]
    try:
        a = f"https://www.espn.com/nba/team/schedule/_/name/{team}/season/{year}/seasontype/2"
        b, c = grab_soup(a)
        kk = re.findall(r'http://www.espn.com/nba/game\?gameId=\d+', str(b))
        c.close()
        return list(set(kk))
    except:
        c.close()
        return list(set(kk))


def get_game_ids_playoffs(team, year):
    kk = [0]
    try:
        a = f"https://www.espn.com/nba/team/schedule/_/name/{team}/season/{year}/seasontype/3"
        b, c = grab_soup(a)
        kk = re.findall(r'http://www.espn.com/nba/game\?gameId=\d+', str(b))
        c.close()
        return list(set(kk))
    except:
        c.close()
        return list(set(kk))


def get_all_teams():
    try:
        a = "https://www.espn.com/nba/team/schedule/_/name/atl/season/2020"
        b, c = grab_soup(a)
        pprint(b)
        kk = re.findall(r'/nba/team/_/name/\S+",', str(b))
        pp = [x.replace('/nba/team/_/name/', '').split('/')[0].replace(",", '').replace('"', '') for x in list(kk)]
        all_teams_collection = set([i for i in pp if len(i) < 5])
        length = len(all_teams_collection)
        print(length)
        if length == 30:
            print('got all teams')
        c.close()
        return all_teams_collection
    except:
        c.close()
        return


def get_all_gameids_by_year(year_range=(2017, 2018, 2019, 2020, 2021)):
    all_games_all_years = {}
    for yr in year_range:
        print(yr)
        all_games = {}
        for i in teams:
            print('\t', i)
            regular = get_game_ids_regular_season(i, yr)
            if yr == 2020:
                playoff = []
            else:
                playoff = get_game_ids_regular_season(i, yr)
            all_games[i] = {'playoffs': playoff,
                            'regular': regular}
            time.sleep(1)
        all_games_all_years[yr] = all_games
    pprint(all_games_all_years)
    pickle_out = open("all_games_all_years.pickle", "wb")
    pickle.dump(all_games_all_years, pickle_out)
    pickle_out.close()
    print(datetime.datetime.now() - timee)

@dask.delayed
def grab_matchup_info(gameid):
    matchup_url = f"https://www.espn.com/nba/matchup?gameId={gameid}"
    soup, c = grab_soup(matchup_url, 'chrome')
    columns = []
    info = []
    table = soup.find_all('table')
    for x in table:
        for y in x.find_all('th'):
            if y.text == 'Matchup':
                columns.append(y.text)
                for p in x.find_all('td'):
                    info.append(p.text.strip())
            else:
                for k in y.find_all('img'):
                    columns.append(str(k).split('teamlogos/nba/500/')[1].split('.')[0])
                continue
    c.close()
    try:
        df = make_df_matchup(columns, info)
    except:
        return 1
    time.sleep(2)
    return df

@dask.delayed
def grab_game_info(gameid):
    matchup_url = f"https://www.espn.com/nba/game?gameId={gameid}"
    soup, c = grab_soup(matchup_url, 'chrome')
    try:
        info = soup.find_all('div', class_= 'game-info-note capacity')
        attendance = [x.text for x in info]
        network = soup.find_all('div', class_= 'game-network')
        netw = list(network)[0].text.strip()
        date = soup.find_all('span', class_= 'game-date')
        game_date = list(date)[0].text
        timee = soup.find_all('span', class_= 'time game-time')
        game_time = list(timee)[0].text
        c.close()
        return {'game_id':gameid, 'network':netw, 'time':game_time, 'date':game_date, "attendance":{"attendance":attendance[0], 'capacity':attendance[1]}}
    except Exception as e:
        c.close()
        return 1

def grab_data_parallel(func):
    # query all table names
    func_name = repr(func).split("'")[1].split('-')[0]
    if func_name == "grab_matchup_info":
        game_ids = pd.read_sql("""SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%' """, engine)['name'].to_list()
        game_ids = set(int(x.replace('gameid_', '')) for x in game_ids)
    elif func_name == "grab_game_info":
        all_docs = collection.find({})
        game_ids = set(x['game_id'] for x in all_docs)
    else:
        game_ids = []
    print(len(game_ids))
    other = []
    final = []
    games_list = []
    for yr in range(2017, 2021):
        for szn in ['playoffs', 'regular']:
            for team in teams:
                games_list.append(data[yr][team][szn])
    # all possible game_ids in dataset
    games_list = list(set([item.split('?')[1] for sublist in games_list for item in sublist]))
    # filter so that array = all game_ids without a record in database
    array = [int(i.split('=')[1]) for i in games_list if int(i.split('=')[1]) not in game_ids]
    for t, i in enumerate(array):
        try:
            try:
                dataframe = func(i)
                if isinstance(dataframe, int):
                    continue
                else:
                    other.append(i)
            except Exception as ei:
                dataframe = func(i)
                if isinstance(dataframe, int):
                    continue
                else:
                    other.append(i)
        except Exception as e:
            print(e)
            continue
        final.append(dataframe)
        if len(final) == 2000:
            break

    result = dask.compute(final)[0]
    pprint(result[0])
    if func_name == "grab_matchup_info":
        for num, each in enumerate(other):
            try:
                result[num].to_sql(f"gameid_{each}", engine, if_exists='replace', index=False)
            except IndexError:
                pass
            except AttributeError:
                pass
    elif func_name == "grab_game_info":
        for each in result:
            if isinstance(each, int):
                continue
            collection.insert_one(each)
    try:
        c.close()
    except:
        pass
    q = (datetime.datetime.now()-timee)
    print(q)
    print()

if __name__ == '__main__':

    cluster = LocalCluster()
    client = Client(cluster)

    # parse to find out all team abbreviations for URL (i.e. Toronto Raptors == tor)
    # teams = get_all_teams()
    teams = {'atl', 'bkn',
     'bos',
     'cha',
     'chi',
     'cle',
     'dal',
     'den',
     'det',
     'gs',
     'hou',
     'ind',
     'lac',
     'lal',
     'mem',
     'mia',
     'mil',
     'min',
     'no',
     'ny',
     'okc',
     'orl',
     'phi',
     'phx',
     'por',
     'sa',
     'sac',
     'tor',
     'utah',
     'wsh'}
    path = 'C:/Users/Julien/PycharmProjects/nba/data/'
    timee = datetime.datetime.now()
    print(timee)
    # dictionary with all games for each team between 2016-2017 and 2020 seasons
    pickle_in = open("all_games_all_years.pickle","rb")
    data = pickle.load(pickle_in)
    #SQLITE3 DATABASE
    engine = sqlite3.connect(path + 'nba_matchup_data.db')
    #MONGODB DATABASE
    mongo_client = pymongo.MongoClient('localhost', 27017)
    db = mongo_client['NBA']
    collection = db['basic_game_info']

    grab_data_parallel(grab_game_info)

