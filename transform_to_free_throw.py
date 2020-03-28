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
import pymongo
import traceback


def find_player(a):
    intermediate = [x.split(' free')[0] for x in a]
    final=[]
    for x in intermediate:
        c = re.search(r"(\S*\s\S+\s)(?=(makes|misses))", x)
        try:
            final.append(c.group().strip())
        except Exception as ie:
            print(x)
            print(str(ie))
            final.append(x.split(' m')[0].strip())
    return final

def transform(gameid):
    data = pd.read_sql(f""" select * from gameid_{gameid} """, engine_playbyplay)
    data['end_result'] = data['score'].values[-1]
    data['period'] = [x.replace('ST', "").replace("RD", "").replace("TH", '').replace("ND", "") for x in data['quarter']]
    # filter for free throw lines only
    data = data[data['play'].str.contains('free throw')]
    data['game_id'] = gameid
    data['shot_made'] = [1 if 'makes' in x else 0 for x in data['play']]
    # parse player name out of *play* column
    data['player'] = find_player(data['play'])
    # what season of the NBA did this game occur?
    for y in range(2017, 2021):
        if str(gameid) in big_dict[str(y)]:
            data['season'] = f"{y-1} - {y}"
    # regular season or playoffs?
    if gameid in big_dict["regular"]:
        data['playoffs'] = 'regular'
    elif gameid in big_dict["playoffs"]:
        data['playoffs'] = 'playoffs'
    teams_ = data['team'].unique()
    # which team is which for the score column?
    for p in data.itertuples():
        if p.score != '0 - 0':
            q = p.team
            break
    data['game'] = [f"{[x for x in teams_ if x != q][0].upper()} - {q.upper()}" for x in data.index]

    # drop columns that aren't needed
    data.drop(['quarter'],1, inplace=True)
    return data

if __name__ == '__main__':
    # Set-up
    # cluster = LocalCluster()
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
    path = 'C:/Users/Julien/PycharmProjects/nba/data/'
    timee = datetime.datetime.now()
    print(timee)

    # dictionary with all games for each team between 2016-2017 and 2019-2020 seasons
    pickle_in = open("all_games_all_years.pickle", "rb")
    dat = pickle.load(pickle_in)

    # all possible game_ids in dataset
    big_dict = {'playoffs': [], 'regular': [], '2017': [], '2018': [], '2019': [], '2020': [], }
    for yr in range(2017, 2021):
        for team in teams:
            for szn in ['playoffs', 'regular']:
                answer = [k.split('gameId=')[1].strip() for k in dat[yr][team][szn]]
                if szn == 'playoffs':
                    big_dict["playoffs"].append(answer)
                else:
                    big_dict["regular"].append(answer)
                big_dict[str(yr)].append(answer)
    for i in big_dict.keys():
        big_dict[i] = set([item for sublist in big_dict[i] for item in sublist])

    #SQLITE3 DATABASE (play by play)
    engine_playbyplay = sqlite3.connect(path + 'nba_playbyplay_data.db')
    #SQLITE3 DATABASE (boxscore)
    engine_freethrow = sqlite3.connect(path + 'nba_freethrow_data.db')
    games_currently_in = pd.read_sql('select game_id from freethrow', engine_freethrow)['game_id'].to_list()
    games_currently_in = set(games_currently_in)
    # main function
    num = len(games_currently_in)
    for y in big_dict.keys():
        for i in big_dict[y]:
            if i not in games_currently_in:
                try:
                    df = transform(i)
                    df.to_sql('freethrow', engine_freethrow, if_exists='append', index=False)
                    print(i, f'{num} done')
                    num+=1
                except Exception as e:
                    print(str(e))
                    print(f'error {i}')
