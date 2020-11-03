from selenium import webdriver
import json
import time
import bs4 as bs
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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import traceback
import os
import requests

def grab_soup(url_, browser="firefox", indicator=''):
    """
    This function enables a driver (using Firefox or Chrome), goes to the URL, and retrieves the data after the JS is loaded.
    :param url_: url to go to to retrieve data
    :param browser: browser to use, defaults to firefox (requires geckodriver.exe on path)
    :param indicator: specific page that is being looked at, waits for certain elements to load depending on this value.
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
        driver = webdriver.Chrome('C:/Users/Julien/PycharmProjects/practice/chromedriver86', options=chromeOptions)
    else:
        firefoxOptions = firefox_options()
        firefoxOptions.set_preference("browser.download.folderList", 2)
        firefoxOptions.set_preference("browser.download.manager.showWhenStarting", False)
        firefoxOptions.set_preference("browser.download.dir", path.replace('/', '\\') + 'data\\downloads\\')
        firefoxOptions.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                      "application/octet-stream,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        driver = webdriver.Firefox(options=firefoxOptions)

    driver.get(url_)  # go to the URL
    # wait up to 7 seconds for element to load
    if indicator == 'game_info':
        try:
            my_elem = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.CLASS_NAME, 'attendance')))
        except TimeoutException:
            print("Loading took too much time!")
    elif indicator == 'matchup':
        try:
            my_elem = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.ID, 'gamepackage-matchup')))
        except TimeoutException:
            print("Loading took too much time!")
    elif indicator == 'playbyplay':
        try:
            my_elem = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.ID, "gamepackage-play-by-play")))
        except TimeoutException:
            print("Loading took too much time!")

    time.sleep(0.5)
    try:
        html = driver.page_source
    except:
        pass
    # sleep for 1 second  to ensure all JS scripts are loaded
    try:
        html = driver.execute_script("return document.body.outerHTML;")  # execute javascript code
    except:
        pass
    soup_ = bs.BeautifulSoup(html, 'lxml')  # read the data as html (using lxml driver)
    # pprint(soup_)
    return soup_, driver
def error_handling():
    """
    This function returns a string with all of the information regarding the error
    :return: string with the error information
    """
    return traceback.format_exc()

@dask.delayed
def grab_matchup_info(gameid):
    matchup_url = f"https://www.espn.com/nba/matchup?gameId={gameid}"
    soup, c = grab_soup(matchup_url, 'chrome', "matchup")
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


@dask.delayed
def grab_game_info(gameid):
    matchup_url = f"https://www.espn.com/nba/game?gameId={gameid}"
    soup, c = grab_soup(matchup_url, 'chrome', 'game_info')
    try:
        date = soup.find_all('span', class_= 'game-date')
        game_date = list(date)[0].text
    except Exception as e:
        game_date = 'N/A'
    try:
        timee = soup.find_all('span', class_= 'time game-time')
        game_time = list(timee)[0].text
    except Exception as e:
        game_time = 'N/A'
    try:
        info = soup.find_all('div', class_= 'game-info-note capacity')
        attendance = [x.text for x in info]
        if len(attendance) == 1:
            attendance.append(attendance[0])
    except Exception as e:
        attendance = [0, 0]
    try:
        network = soup.find_all('div', class_= 'game-network')
        netw = list(network)[0].text.strip()
    except Exception as e:
        print('network', str(e))
        netw = 'N/A'
    try:
        output = {'game_id': gameid, 'network': netw, 'time': game_time, 'date': game_date,
         "attendance": {"attendance": attendance[0],
                        'capacity': attendance[1]}}
    except:
        output = {'game_id': gameid, 'network': netw, 'time': game_time, 'date': game_date,
         "attendance": {"attendance": 0, 'capacity': 0}}
    try:
        c.close()
    except:
        pass
    try:
        return output
    except:
        return 1


@dask.delayed
def grab_playbyplay_info(gameid):
    matchup_url = f"https://www.espn.com/nba/playbyplay?gameId={gameid}"
    soup, c = grab_soup(matchup_url, 'chrome', 'playbyplay')
    accordion = soup.find_all('li', class_='accordion-item')

    teams_in_game = {}
    for num, t in enumerate(soup.find_all('div', class_='team-info-wrapper')):
        long_name = t.find('span', class_='short-name')
        short_name = t.find('span', class_='long-name')
        abbrev = t.find('span', class_='abbrev')
        teams_in_game[f'team_{num}'] = {"abbrev": abbrev.text.lower(), 'short_name':short_name.text.lower(), 'long_name':long_name.text.lower()}
    try:
        dfs = []
        for x in accordion:
            qtr = x.find_all('h3')[0]
            info = []
            imgs = []
            for tbl in x.find_all('table'):
                # get the column names
                columns = [a.text.lower() for y in tbl.find_all('thead') for a in y.find_all('th')]
                # get the contents of the data table
                for y in tbl.find_all('tbody'):
                    # get all data elements
                    for a in y.find_all('td'):
                        info.append(a.text.strip())
                    # find the logo elements, or the differentiator for each team
                    for a in y.find_all('td', class_='logo'):
                        # if there's no image, append an empty string, to be filled in later
                        imgs_in_col = a.find_all('img')
                        if imgs_in_col:
                            for k in imgs_in_col:
                                imgs.append(str(k).split('teamlogos/nba/500/')[1].split('.')[0])
                        else:
                            imgs.append(np.nan)
            dat = [[info[t] for t in range(5)]] + [[info[t] for t in range(i-5, i)] for i in range(5, len(info), 5)]
            dat = [i[:4] for i in dat]
            for i, each in enumerate(dat):
                each[1] = imgs[i]
                if '.' in each[0]:
                    each[0] = f"0:{str(each[0].split('.')[0]).zfill(2)}"
            df = pd.DataFrame.from_records(data=dat, columns=columns,)
            df['quarter'] = qtr.text.strip()[:4].upper()
            dfs.append(df)
        total_game_df = pd.concat(dfs)
        total_game_df.drop_duplicates(subset=['quarter', "score", "play", 'time'], inplace=True)
        total_game_df['team'].fillna([x['abbrev'] for x in teams_in_game.values() if x not in total_game_df["team"].unique()][0], inplace=True)
    except Exception as ie:
        print(error_handling())
        c.close()
    try:
        c.close()
    except:
        pass
    try:
        print(f"{gameid}, done")
        return total_game_df
    except:
        print(f"{gameid}, error2")
        return 1


@dask.delayed
def grab_boxscore_info(gameid):
    imgs = []
    teams_ = []
    matchup_url = f"https://www.espn.com/nba/boxscore?gameId={gameid}"
    try:
        soup, c = grab_soup(matchup_url, 'chrome', 'boxscore')
        main_div = soup.find_all('div', class_='sub-module')

        for x in main_div:
            # find the teams playing, first team in *imgs* corresponds to the first table
            for im in x.find_all('div', class_='team-name'):
                for k in im.find_all('img'):
                    imgs.append(str(k).split('teamlogos/nba/500/')[1].split('.')[0])

        if len(imgs) < 2:
            imgs = []
            for x in main_div:
                # find the teams_ playing, first team in *imgs* corresponds to the first table
                for im in x.find_all('div', class_='team-name'):
                    imgs.append(possible_teams[im.text])
                    print(possible_teams[im.text], im.text)

        for div_num, x in enumerate(main_div):
            columns = []
            info = []
            for tbl in x.find_all('table'):
                # for each table, gather the headers as a list of lists
                for y in tbl.find_all('thead'):
                    cols = []
                    for a in y.find_all('th'):
                        cols.append(a.text.lower())
                    columns.append(cols)
                # for each table, grab the data as one list of lists
                for h in tbl.find_all('tbody'):
                    info0 = []
                    for g in h.find_all('td'):
                        info0.append(g.text.strip())
                    info.append(info0)
            # only first column shouldn't match, that one is renamed player, otherwise keep column name
            columns = [u if u==v else 'player' for u, v in zip(columns[0], columns[1])]
            for each in info:
                if 'TEAM' in each:
                    each = each[:each.index('TEAM')] # remove team aggregate stats
                    if "DNP-" in each:
                        DNPs = each[each.index("DNP-")-1:]
                        bench_info = each[:each.index("DNP-")-1]
                    else:
                        bench_info = each

            starter_info = info[0]
            starter_data = [[starter_info[t] for t in range(i-len(columns), i)] for i in range(len(columns), len(starter_info)+1, len(columns))]
            starter_df = pd.DataFrame.from_records(data=starter_data, columns=columns,)
            bench_data = [[bench_info[t] for t in range(i-len(columns), i)] for i in range(len(columns), len(bench_info)+1, len(columns))]
            bench_df = pd.DataFrame.from_records(data=bench_data, columns=columns,)
            for each in ['3pt', 'ft', 'fg']:
                bench_df = split_stats_column(bench_df, each)
                starter_df = split_stats_column(starter_df, each)

            # append DNP players to bench dataframe
            try:
                DNPs = list(set(DNPs))
                DNPs.remove("DNP-COACH'S DECISION")
                for each in DNPs:
                    temp_row = {'player':each, 'min':'DNP'}
                    temp_row.update({col_name: np.nan for col_num, col_name in enumerate(bench_df.columns) if col_num > 1})
                    bench_df = pd.concat([bench_df, pd.DataFrame(temp_row, index = [0])])
            except:
                pass
            # assign starter/bench status
            starter_df['starter'] = 1
            bench_df['starter'] = 0
            # concat starter and bench dataframes
            team = pd.concat([starter_df, bench_df])
            team.reset_index(inplace=True, drop=True)
            # assign team name and remove unused columns
            team['team'] = imgs[div_num]
            team['plus_minus'] = team['+/-']
            team.drop(['+/-', 'fg', '3pt', 'ft'], 1, inplace=True)

            for col_name in [x for x in team.columns if x not in ['player', 'team', 'min']]:
                team[col_name] = pd.to_numeric(team[col_name], errors='coerce', downcast="integer")
            teams_.append(team)
        total_game_df = pd.concat(teams_)
        total_game_df.reset_index(drop=True, inplace=True)
    except Exception as ie:
        print(gameid, '\n', error_handling())
        try:
            c.close()
        except UnboundLocalError:
            pass

    try:
        c.close()
    except:
        pass
    try:
        return total_game_df
    except:
        return 1
def transform_boxscore(gameid):
    df = pd.read_sql(f"""select * from "gameid_{gameid}" """, engine_boxscore)
    df['player'].replace("Nene", "H. Nene", inplace=True)
    df = df[~df.player.str.contains("DNP")]
    df = df[~df.player.str.contains("Did not Play")]
    df = df[~df.player.str.contains("Did not play")]
    df = df[~df.player.str.contains("Did Not Play")]
    position = []
    player_name = []
    try:
        for x in df['player']:
            pos = re.search(r"(?=\w)(PF|C|SF|SG|PG|F|G)$", x)
            name = re.search(r"^.+\.\s[^.]+(?=\w+\.)", x)
            b = name.group(0)
            try:
                a = name.group(1)
                if a:
                    c = str(a) + str(b)
                else:
                    c = b
            except Exception as e:
                c = b
            player_name.append(c)
            position.append(pos.group())

        df['player'] = player_name
        df['position'] = position
        df.to_sql(f"gameid_{i}", engine_boxscore, if_exists = 'replace', index=False)
    except Exception as e:
        print(str(e))
        print(str(gameid))
def split_stats_column(dataf, col_to_split):
    if col_to_split == '3pt':
        dataf[f'3pm'] = [qq.split('-')[0] for qq in dataf[col_to_split]]
        dataf[f'3pa'] = [qq.split('-')[1] for qq in dataf[col_to_split]]
    else:
        dataf[f'{col_to_split}m'] = [qq.split('-')[0] for qq in dataf[col_to_split]]
        dataf[f'{col_to_split}a'] = [qq.split('-')[1] for qq in dataf[col_to_split]]
    return dataf

def grab_data_parallel(func):
    """

    This function runs the *func* with dask. It then puts the data into the database, depending on which function was executed.

    :param func: function to run in parallel with dask
    :return: nothing
    """
    # query all table names
    func_name = repr(func).split("'")[1].split('-')[0] # way to get func name for dask (wrapped in Delayed object)

    if func_name == "grab_matchup_info":
        game_ids = pd.read_sql("""SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%' """, engine)['name'].to_list()
        game_ids = set(int(x.replace('gameid_', '')) for x in game_ids)
    elif func_name == "grab_game_info":
        all_docs = collection.find({})
        game_ids = set(x['game_id'] for x in all_docs)
    elif func_name == "grab_playbyplay_info":
        game_ids = pd.read_sql("""SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%' """, engine_playbyplay)['name'].to_list()
        game_ids = set(int(x.replace('gameid_', '')) for x in game_ids)
    elif func_name == "grab_boxscore_info":
        game_ids = pd.read_sql("""SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%' """, engine_boxscore)['name'].to_list()
        game_ids = set(int(x.replace('gameid_', '')) for x in game_ids)
    else:
        game_ids = []
    print(len(game_ids)) # print how many game_ids are in DB
    other = []
    final = []

    # all possible game_ids in dataset
    games_list = []
    for yr in range(2009, 2017):
        for szn in ['playoffs', 'regular']:
            for team in teams:
                games_list.append(data[yr][team][szn])
    games_list = list(set([item.split('?')[1] for sublist in games_list for item in sublist]))

    # filter so that array = all game_ids without a record in database
    array = [int(i.split('=')[1]) for i in games_list if int(i.split('=')[1]) not in game_ids]
    print(len(array),' left')
    for t, i in enumerate(array):
        # print(i)
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
        if len(final) == 2000: # stop before entire *array* is done
            break
    # execute in parallel, showing one of the objects
    result = dask.compute(final)[0]
    pprint(result[0])
    # input data into one of the databases
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
    elif func_name == "grab_playbyplay_info":
        for num, each in enumerate(other):
            try:
                result[num].to_sql(f"gameid_{each}", engine_playbyplay, if_exists='replace', index=False)
            except IndexError:
                pass
            except AttributeError:
                pass
    elif func_name == "grab_boxscore_info":
        for num, each in enumerate(other):
            try:
                result[num].to_sql(f"gameid_{each}", engine_boxscore, if_exists='replace', index=False)
            except IndexError:
                pass
            except AttributeError:
                pass
    # close the driver if it's still open
    try:
        c.close()
    except:
        pass
    end_time = (datetime.datetime.now()-timee)
    print(end_time)
    print()



@dask.delayed
def get_game_ids_by_season(team, year, season_ind):
    print(year, team, season_ind)
    kk = [0]
    try:
        if season_ind == 'regular':
            url = f"https://www.espn.com/nba/team/schedule/_/name/{team}/season/{year}/seasontype/2"
        elif season_ind == 'playoffs':
            url = f"https://www.espn.com/nba/team/schedule/_/name/{team}/season/{year}/seasontype/3"
        soup, c = grab_soup(url, 'chrome')
        kk = re.findall(r'http://www.espn.com/nba/game\?gameId=\d+', str(soup))
        c.close()
        return list(set(kk))
    except:
        print(error_handling())
        try:
            c.close()
        except:
            pass
        finally:
            return list(set(kk))
def get_all_teams():
    """
    Returns a list of all team abbreviations (ie. Toronto Raptors == tor) found from the 2020 season on espn.com
    :return: a list of all 30 teams' abbreviations
    """
    try:
        soup, c = grab_soup("https://www.espn.com/nba/team/schedule/_/name/atl/season/2020", 'chrome')
        regex_return = re.findall(r'/nba/team/_/name/\S+",', str(b))
        teams_list = [x.replace('/nba/team/_/name/', '').split('/')[0].replace(",", '').replace('"', '') for x in list(regex_return)]
        all_teams_collection = set([i for i in teams_list if len(i) < 5])
        length = len(all_teams_collection)
        if length == 30:
            print('got all teams')
        c.close()
        return all_teams_collection
    except:
        c.close()
        return
def get_all_gameids_by_year_list():
    yy= []
    for yr in range(2006, 2020):
        for szn in ['regular', 'playoffs']:
            for i in teams:
                yy.append(get_game_ids_by_season(i, yr, szn))
                # if yr == 2020:
                #     if szn == 'playoffs':
                #         continue

                # print(len(yy))
                # time.sleep(1)
                # if len(yy) == 12:
                #     print('wtf')
                #     break
            else:
                continue
            break
        else:
            continue
        break
    result = dask.compute(yy)[0]
    pprint(result[0])
    pickle_out = open(path + "all_games_all_years_oct2020.pickle", "wb")
    pickle.dump(result, pickle_out)
    pickle_out.close()
    print(datetime.datetime.now() - timee)
    print()
def get_all_gameids_by_year_dict():
    output = {}
    for yr in range(2006, 2021):
        output[yr] = {}
        for t in teams:
            output[yr][t] = {}
            for szn in ['regular', 'playoffs']:
                output[yr][t][szn] = get_game_ids_by_season(t, yr, szn)
                # if yr == 2020:
                #     if szn == 'playoffs':
                #         continue

                # print(len(yy))
                # time.sleep(1)
                # if len(yy) == 12:
                #     print('wtf')
                #     break
            else:
                continue
            break
        else:
            continue
        break
    result = dask.compute(output)[0]
    pickle_out = open(path + "all_games_all_years_nov2020_dict.pickle", "wb")
    pickle.dump(result, pickle_out)
    pickle_out.close()
    print(datetime.datetime.now() - timee)
    pprint(result[2019]["regular"])
    print()

# ESPN Hidden API
def make_sure_table_has_no_duplicates(table_name, df, conn_):
    df.to_sql(table_name, conn_, if_exists='append', index=False)
    new_df = pd.read_sql(f"select * from {table_name}", conn_)
    crazy = new_df.drop_duplicates().copy()
    if len(new_df.index) > len(crazy.index):
        crazy.to_sql(table_name, conn_, if_exists='replace', index=False)
    else:
        pass
def get_data_from_api(gameid = "401071727"):
    def get_player_boxscore_data_from_api(boxscore):
        boxscore_df_ = []
        for team in boxscore:
            team_name = team['team']['slug']
            columns = team['statistics'][0]['names']
            for each in team['statistics'][0]['athletes']:
                r = pd.DataFrame(each['stats'], index=columns).T
                r['Player'] = each['athlete']['displayName']
                r['Jersey_number'] = each['athlete']['jersey']
                r['position'] = each['athlete']['position']['abbreviation']
                r['START'] = each['starter']
                r['EJECTED'] = each['ejected']
                r['DNP'] = each['didNotPlay']
                r['REASON'] = each['reason']
                r['TEAM'] = team_name
                r.columns = [x.lower().replace(' ', '_').replace("%", 'pct') for x in r.columns]
                boxscore_df_.append(r)
        return pd.concat(boxscore_df_).reset_index(drop=True)
    def get_team_boxscore_data_from_api(boxscore):
        boxscore_df_ = []
        for team in boxscore:
            r = pd.DataFrame.from_dict(team['statistics']).set_index('label').drop(columns=['name', 'abbreviation']).T
            r.index = [team['team']['slug']]
            r.columns = [x.lower().replace(' ', '_').replace("%", 'pct') for x in r.columns]
            boxscore_df_.append(r)
        return pd.concat(boxscore_df_)
    def get_game_info_data_from_api(game_info, header):
        info = {'venue': game_info['venue']['fullName'],
                'capacity': game_info['venue']['capacity'],
                'city': game_info['venue']['address']['city'],
                'state':game_info['venue']['address']['state'],
                'attendance': game_info['attendance'],
                'date': header["competitions"][0]["date"],
                'officials': ' / '.join([x['displayName'] for x in game_info['officials']])}
        parsed_header = {i['homeAway']: {'winner': i['winner'], 'team_name': i['team']['displayName'], 'abbreviation':i['team']['abbreviation']}
                         for i in header["competitions"][0]["competitors"]}
        info['home_team'] = parsed_header['home']['team_name']
        info['home_team_abbrev'] = parsed_header['home']['abbreviation']
        info['away_team'] = parsed_header['away']['team_name']
        info['away_team_abbrev'] = parsed_header['away']['abbreviation']
        if parsed_header['home']['winner']:
            info['winning_team'] = info['home_team']
        else:
            info['winning_team'] = info['away_team']
        return pd.DataFrame(info, index = [0])
    def get_playbyplay_data_from_api(play_data):
        plays = []
        for each in play_data:
            info = dict(espn_game_index = each['sequenceNumber'],
            type_of_play = each['type']['text'],
            play = each['text'],
            away_score = each["awayScore"],
            home_score = each["homeScore"],
            period = each['period']['displayValue'],
            clock = each['clock']['displayValue'],
            # team_of_player = each['team']['id'],
                        )
            plays.append(pd.DataFrame(info, index=[0]))
        output = pd.concat(plays).reset_index(drop=True)
        output['type_of_play'] = output['type_of_play'].str.replace("\n", " ")
        return output

    url = f"http://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={gameid}"
    json_return = requests.get(url).json()

    team_boxscore_df = get_team_boxscore_data_from_api(json_return['boxscore']['teams'])
    team_boxscore_df['game_id'] = gameid

    player_boxscore_df = get_player_boxscore_data_from_api(json_return['boxscore']['players'])

    game_info_data = get_game_info_data_from_api(json_return['gameInfo'], json_return['header'])
    game_info_data['game_id'] = gameid

    playbyplay_data = get_playbyplay_data_from_api(json_return['plays'])
    return team_boxscore_df, player_boxscore_df, game_info_data, playbyplay_data
def pull_from_espn_api(gid = "401071727"):
    team_boxscore, player_boxscore, matchup, playbyplay = get_data_from_api(gid)
    print(team_boxscore.to_string())
    make_sure_table_has_no_duplicates('team_boxscore', team_boxscore, new_matchup_conn)
    print(player_boxscore.to_string())
    player_boxscore.to_sql(gid, new_boxscore_conn, if_exists='replace', index=False)
    print(matchup.to_string())
    make_sure_table_has_no_duplicates('matchup', matchup, new_matchup_conn)
    print(playbyplay.to_string())
    playbyplay.to_sql(gid, new_playbyplay_conn, if_exists='replace', index=False)
    print()
    print(f"game_id:{gid} has been added to the databases")
    print(datetime.datetime.now()-timee)

if __name__ == '__main__':
    # Set-up
    # cluster = LocalCluster(threads_per_worker=12,)
    # client = Client(cluster)

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
    possible_teams = {"Rockets":'hou', "Heat":'mia', 'Raptors':'tor',
                      "Hawks":'atl', "Nets":'nj', 'Spurs':'sa',"Magic":"orl",
                      "Mavericks":'dal', "Clippers":'lac', 'Lakers':'lal',
                      "Suns":'phx', "Bucks":'mil', 'Warriors':'gs', "Bulls":"chi",
                      "Nuggets":'den', "Cavaliers":'cle', 'Bobcats':'cha',
                      "Pistons":'det', "Thunder":'okc', 'Hornets':'cha',
                      "Celtics":'bos', "Jazz":'utah', 'Pelicans':'no', "Knicks":"ny",
                      'Wizards':'wsh',"76ers":'phi', "Kings":'sac', "Pacers":'ind',
                      "Trail Blazers":'por', "Grizzlies":'mem', "Timberwolves":"min"}
    path = os.getcwd().replace("\\", "/") + "/data/"
    timee = datetime.datetime.now()
    print(timee)
    # dictionary with all games for each team between 2016-2017 and 2020 seasons or 2008-2009 to 2015-2016 seasons.
    pickle_in = open(path + "all_games_all_years_oct2020_dict.pickle","rb")
    data = pickle.load(pickle_in)
    # pprint(data)
    #SQLITE3 DATABASE (matchup)
    engine = sqlite3.connect(path + 'nba_matchup_data.db')
    #SQLITE3 DATABASE (play by play)
    engine_playbyplay = sqlite3.connect(path + 'nba_playbyplay_data.db')
    #SQLITE3 DATABASE (boxscore)
    engine_boxscore = sqlite3.connect(path + 'nba_boxscore_data.db')

    new_matchup_conn = sqlite3.connect(path + 'nba_new_matchup_data.db')
    #SQLITE3 DATABASE (play by play)
    new_playbyplay_conn = sqlite3.connect(path + 'nba_new_playbyplay_data.db')
    #SQLITE3 DATABASE (boxscore)
    new_boxscore_conn = sqlite3.connect(path + 'nba_player_boxscore_data.db')

    #MONGODB DATABASE
    mongo_client = pymongo.MongoClient('localhost', 27017)
    db = mongo_client['NBA']
    collection = db['basic_game_info']
    pprint(data)
    pull_from_espn_api()
    # main function
    # get_all_gameids_by_year_dict()



