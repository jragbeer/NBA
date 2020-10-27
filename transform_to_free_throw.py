import time
import bs4 as bs
import re
import datetime
import pprint
import os
import pickle
from pprint import pprint
import pandas as pd
import numpy as np
import sqlite3
import pymongo
import traceback

def error_handling():
    """

    This function returns a string with all of the information regarding the error

    :return: string with the error information
    """
    return traceback.format_exc()
def transform_from_playbyplay_to_freethrow(big_dict, gameid):
    """
    Convert a table found in the playbyplay DB into a dataframe of free throw data.

    :param gameid: gameid to parse from Database
    :return: dataframe where each row represents rows that would be found in original kaggle dataset
    """
    def find_player(series):
        """
        Return a list that contains a single player's name. Uses regex to parse out player name).
        :param series: pd.series of plays (text data)
        :return: a list with the player shooting. This list is the length of the series
        """
        intermediate = [x.split(' free')[0] for x in series]
        final = []
        for x in intermediate:
            c = re.search(r"(\S*\s\S+\s)(?=(makes|misses))", x)
            try:
                final.append(c.group().strip())
            except Exception as ie:
                final.append(x.split(' m')[0].strip())
        return final

    data = pd.read_sql(f""" select * from gameid_{gameid} """, engine_playbyplay)
    data['end_result'] = data['score'].iloc[-1]
    # data['period'] = [x.replace('ST', "").replace("RD", "").replace("TH", '').replace("ND", "") for x in data['quarter']]
    data['period'] = data['quarter'].str.replace('ST', "").str.replace("RD", "").str.replace("TH", '').str.replace("ND", "")
    # filter for free throw lines only
    data = data[data['play'].str.contains('free throw')]
    data['game_id'] = gameid
    data['shot_made'] = [1 if 'makes' in x else 0 for x in data['play']]
    data['shot_made'] = data['play'].str.contains('makes').astype(int)
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
    data.drop(['quarter', 'team'],1, inplace=True)
    return data
# main function
def update_freethrow_sql_table(games_dict, games_currently_in_db):
    """
    Turn big_dict into a SQL table

    :return:
    """
    num = len(games_currently_in_db)
    for y in games_dict.keys():
        for gid in games_dict[y]:
            if gid not in games_currently_in_db:
                try:
                    df = transform_from_playbyplay_to_freethrow(games_dict, gid)
                    df.to_sql('freethrow', engine_freethrow, if_exists='append', index=False)
                    print(gid, f'{num} done')
                    # print(df.to_string())
                    num+=1
                except Exception as e:
                    print(error_handling())
                    print(f'error {gid}')
    old_df = pd.read_sql("select * from freethrow", engine_freethrow, )
    old_df.drop_duplicates(inplace=True)
    old_df.to_sql('freethrow', engine_freethrow, if_exists='replace', index=False)
def get_games_currently_in_freethrow_db(games_dict):
    try:
        games_currently_in = pd.read_sql('select game_id from freethrow', engine_freethrow)['game_id'].to_list()
        return set(games_currently_in)

    except:
        gid = str(400974842) # make sure this is in big_dict
        idf = transform_from_playbyplay_to_freethrow(games_dict, gid)
        print(idf.to_string())
        idf.to_sql('freethrow', engine_freethrow, if_exists='append', index=False)
        print(f"No table was found with that name, creating a new table and adding data from gameid: {gid} to it")
        return [gid]
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
path = os.getcwd().replace('\\', '/') + '/data/'
timee = datetime.datetime.now()
print(timee)
#SQLITE3 DATABASE (play by play)
engine_playbyplay = sqlite3.connect(path + 'nba_playbyplay_data.db')
#SQLITE3 DATABASE (boxscore)
engine_freethrow = sqlite3.connect(path + 'nba_freethrow_data.db')

# dictionary with all games for each team between 2016-2017 and 2019-2020 seasons. Structure:
# year
#   team
#       playoff/regular season
#                           url to game
pickle_in = open(path + "all_games_all_years_2017_2020.pickle", "rb")
dat = pickle.load(pickle_in)

# rearrange *dat* into another dict with all possible game_ids in dataset
total_games_in_dataset = 0
big_dict = {'playoffs': [], 'regular': [], '2017': [], '2018': [], '2019': [], '2020': [], }
for yr in range(2017, 2021):
    for team in teams:
        for szn in ['playoffs', 'regular']:
            # parse game id's from dictionary
            gameid = [k.split('gameId=')[1].strip() for k in dat[yr][team][szn]]
            total_games_in_dataset+=1
            if szn == 'playoffs':
                big_dict["playoffs"].append(gameid)
            else:
                big_dict["regular"].append(gameid)
            big_dict[str(yr)].append(gameid)
print(f'total games: {total_games_in_dataset}')
# make sure each game only appears once per list
for i in big_dict.keys():
    big_dict[i] = set([item for sublist in big_dict[i] for item in sublist])

games_currently_in = get_games_currently_in_freethrow_db(big_dict)
print(f"Number of games in freethrow DB: {len(games_currently_in):,f}")
update_freethrow_sql_table(big_dict, games_currently_in)
print(datetime.datetime.now()-timee)
# print(transform_from_playbyplay_to_freethrow(big_dict, 300205002).to_string())
