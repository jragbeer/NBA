import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import time
import pickle
from pprint import pprint
import pyarrow
from bokeh.models import BasicTickFormatter, HoverTool, BoxSelectTool, BoxZoomTool, ResetTool, Span, Label, Button, DatePicker, CustomJS, Panel, RangeSlider
from bokeh.models import NumeralTickFormatter, WheelZoomTool, PanTool, SaveTool, ColumnDataSource, LinearAxis, Range1d, FactorRange,BoxAnnotation, Tabs
from bokeh.models.widgets import Select, RadioGroup, DataTable, StringFormatter, TableColumn, NumberFormatter, Div, inputs, Slider, CheckboxGroup, Toggle
from bokeh.layouts import widgetbox, row, column, gridplot, layout
from bokeh.io import curdoc
from bokeh.events import ButtonClick, SelectionGeometry
from dateutil import parser
from bokeh.palettes import brewer
import colorcet as cc
from sqlalchemy import create_engine
import pymysql
from pytz import timezone
from bokeh.transform import cumsum
from bokeh.plotting import figure, show
import sqlite3
import pymongo
import os

def clean_player2(df):
    df['player'] = pd.Series([x.replace('.', '').replace("'", '') for x in df.player], index=df.index)
    df['player'] = df['player'].str.lower()
    df['player'].replace('nene', 'nene hilario', inplace=True)
    df['player'].replace('metta world', "Metta World Peace".lower(), inplace=True)
    df['player'].replace('ron artest', "Metta World Peace".lower(), inplace=True)
    df['player'].replace('wes matthews', "wesley matthews", inplace=True)
    df['player'].replace("amar'e stoudemire", "amare stoudemire", inplace=True)
    df['player'].replace('jose juan', "Jose Juan Barea".lower(), inplace=True)
    df['player'].replace('jose barea', "Jose Juan Barea".lower(), inplace=True)
    df['player'].replace('jj barea', "Jose Juan Barea".lower(), inplace=True)
    df['player'].replace("hedo turkoglu", "Hidayet Turkoglu".lower(), inplace=True)
    df['player'].replace('ish smith', "Ishmael Smith".lower(), inplace=True)
    df['player'].replace("glenn robinson", "glenn robinson iii", inplace=True)
    df['player'].replace('lou williams', "louis williams", inplace=True)
    df['player'].replace("larry nance", "larry nance jr", inplace=True)
    df['player'].replace("peja stojakovic", "Predrag Stojakovic".lower(), inplace=True)
    df['player'].replace("dj mbenga", "Didier Ilunga-Mbenga".lower(), inplace=True)
    df['player'].replace("jeff taylor", "Jeffery Taylor".lower(), inplace=True)
    df['player'].replace("mo williams", "Maurice Williams".lower(), inplace=True)
    df['player'].replace("dennis schroder", "Dennis Schroeder".lower(), inplace=True)
    df['player'].replace("byron mullens", "bj mullens", inplace=True)
    df['player'].replace("daniel green", "danny green", inplace=True)
    df['player'].replace("nando de", "nando de colo", inplace=True)
    df['player'].replace("lou amundson", "louis amundson", inplace=True)
    df['player'].replace('luc mbah', "Luc Mbah a Moute".lower(), inplace=True)
    df['player'].replace("toure' murry", "toure murry", inplace=True)
    df['player'].replace("tim hardaway", "tim hardaway jr", inplace=True)
    df['player'].replace("patty mills", "patrick mills", inplace=True)
    df['player'].replace("rasho nesterovic", "Radoslav Nesterovic".lower(), inplace=True)
    df['player'].replace("bill walker", "henry walker", inplace=True)
    df['player'].replace("w russell", "walker russell", inplace=True)
    df['player'].replace("will solomon", "Willie Solomon".lower(), inplace=True)
    df['player'].replace("jake tsakalidis", "Iakovos Tsakalidis".lower(), inplace=True)
    df['player'].replace("cheick samb", "Cheikh Samb".lower(), inplace=True)
    df['player'].replace("slava kravtsov", "Vyacheslav Kravtsov".lower(), inplace=True)
    df['player'].replace("slava medvedenko", "Stanislav Medvedenko".lower(), inplace=True)
    df['player'].replace("tarance kinsey", "tarence kinsey", inplace=True)
    df['player'].replace("viacheslav kravtsov", "Vyacheslav Kravtsov".lower(), inplace=True)
    df['player'].replace("juan carlos", "Juan Carlos Navarro".lower(), inplace=True)
    return df
def clean_player_df(df):
    df['player'] = pd.Series([x.replace('.', '').replace("'", '') for x in df.player], index=df.index)
    df['player'] = df['player'].str.lower()
    df['player'].replace('nene', 'nene hilario', inplace=True)
    pp = {"edy tavares":'walter tavares'}
    pp["jerome adolphus"] = "jerome jordan"
    pp["michael kidd"] = 'michael kidd-gilchrist'
    pp["bryce dejean"] = "bryce dejean-jones"
    pp["luc mbah a moute"] = 'luc richard'
    pp["michael carter"] = 'michael carter-williams'
    pp["rondae hollis"] = "rondae hollis-jefferson"
    pp["metta world"] = "Metta World Peace"
    pp["ron artest"] = "Metta World Peace"
    pp["wes matthews"] = "wesley matthews"
    pp["amar'e stoudemire"] = "amare stoudemire"
    pp["jose juan"] = "Jose Juan Barea"
    pp["jose barea"] = "Jose Juan Barea"
    pp["jj barea"] = "Jose Juan Barea"
    pp["hedo turkoglu"] = "Hidayet Turkoglu"
    pp["ish smith"] = "Ishmael Smith"
    pp["glenn robinson"] = "glenn robinson iii"
    pp["lou williams"] = "louis williams"
    pp["larry nance"] = "larry nance jr"
    pp["peja stojakovic"] = "Predrag Stojakovic"
    pp["dj mbenga"] = "Didier Ilunga-Mbenga"
    pp["jeff taylor"] = "Jeffery Taylor"
    pp["mo williams"] = "Maurice Williams"
    pp["dennis schroder"] = "Dennis Schroeder"
    pp["byron mullens"] = "bj mullens"
    pp["daniel green"] = "danny green"
    pp["nando de"] = "nando de colo"
    pp["lou amundson"] = "louis amundson"
    pp["luc mbah"] = "Luc Mbah a Moute"
    pp["toure' murry"] = "toure murry"
    pp["tim hardaway"] = "tim hardaway jr"
    pp["patty mills"] = "patrick mills"
    pp["rasho nesterovic"] = "Radoslav Nesterovic"
    pp["bill walker"] = "henry walker"
    pp["w russell"] = "walker russell"
    pp["will solomon"] = "Willie Solomon"
    pp["jake tsakalidis"] = "Iakovos Tsakalidis"
    pp["cheick samb"] = "Cheikh Samb"
    pp["slava kravtsov"] = "Vyacheslav Kravtsov"
    pp["slava medvedenko"] = "Stanislav Medvedenko"
    pp["tarance kinsey"] = "tarence kinsey"
    pp["viacheslav kravtsov"] = "Vyacheslav Kravtsov"
    pp["juan carlos"] = "Juan Carlos Navarro"
    pp['karl anthony'] = 'karl-anthony towns'
    pp['kentavious caldwell'] = "kentavious caldwell-pope"
    pp['al farouq'] = 'al-farouq aminu'
    pp['willie cauley'] = 'willie cauley-stein'
    pp['luc mbah a moute'] = 'luc richard'
    pp_keys = list(pp.keys())
    home_team_roster = []
    away_team_roster = []
    for x in df.itertuples():
        h = []
        a = []
        for y in range(len(x.home_team_roster)):

            if x.home_team_roster[y] in pp_keys:
                h.append(pp[x.home_team_roster[y]].lower())
            else:
                h.append(x.home_team_roster[y])
        for z in range(len(x.away_team_roster)):
            if x.away_team_roster[z] in pp_keys:
                a.append(pp[x.away_team_roster[z]].lower())
            else:
                a.append(x.away_team_roster[z])
        home_team_roster.append(h)
        away_team_roster.append(a)
    df['home_team_roster'] = pd.Series(home_team_roster, index = df.index)
    df['away_team_roster'] = pd.Series(away_team_roster, index = df.index)

    df = clean_player2(df)
    return df
def get_salary_scatter_data(data):
    salaries = pd.read_csv(path + 'salary data/playersalaries.csv')
    salaries['Player'] = salaries['Player'].str.lower()
    salaries['Player'] = pd.Series([x.replace('.', '').replace("'", '') for x in salaries.Player], index=salaries.index)
    new = pd.DataFrame(data.groupby(['player']).agg({'shot_made':'sum'}))
    new['attempts'] = data.groupby(['player']).agg({'shot_made': 'count'})
    new['percent'] = 100*new['shot_made']/new['attempts']
    new['salary'] = salaries.groupby(['Player'])['AdjustedSalary'].mean()
    new['salary'].fillna(80000, inplace=True)
    new['salary'] = new['salary'].astype('int64')
    new = new[new['attempts']>30]
    return new
def NestedDictValues(d):
  for v in d.values():
    if isinstance(v, dict):
      yield from NestedDictValues(v)
    else:
      yield v
def get_team_names():
    try:
        teamNames = pd.read_parquet(data_path + 'nba_player_analysis_teams.parquet')
    except:
        teamNames = pd.read_csv(data_path + 'nba_player_analysis_teams.csv', index_col='Abbrev')
        teamNames['State'] = [i.split(',')[1] for i in teamNames.Location.values]
        teamNames['City'] = [i.split(',')[0] for i in teamNames.Location.values]
    return teamNames
def get_gameid_player_mapping():
    """

    :return: dataframe of gameid, away and home team rosters
    """
    game_ids = pd.read_sql("""SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%' """,
                           engine_boxscore)['name'].to_list()
    game_ids = set(int(x.replace('gameid_', '')) for x in game_ids)
    # create a list of dictionaries with data, to be made into a dataframe.
    all_mappings = []
    for each in game_ids:
        idf = pd.read_sql(f"select * from gameid_{each}", engine_boxscore, )
        data = {"game_id": each}
        teamz = [z for z in idf['team']]
        data["away_team_roster"] = idf[idf['team'] == teamz[0]]['player'].to_list()
        data["home_team_roster"] = idf[idf['team'] == teamz[-1]]['player'].to_list()
        all_mappings.append(data)
    return pd.DataFrame(all_mappings)
def consolidate_to_single_df():
    # game_id_players = get_gameid_player_mapping()
    pickle_in = open("game_id_players.pickle", "rb")
    game_id_players = pickle.load(pickle_in)
    print(datetime.datetime.now()-timee)
    # idf = pd.concat([pd.read_csv(path + 'free_throws.csv'), pd.read_sql('select * from freethrow', engine_freethrow)])
    idf = pd.read_sql('select * from freethrow', engine_freethrow)
    idf.rename(columns = {'score':'score_after'}, inplace =True)
    idf['game_id'] = idf['game_id'].astype(int)
    idf = idf[idf['game'] != 'WEST - EAST']
    idf = idf[idf['game'] != 'EAST - WEST']
    idf = pd.merge(idf, game_id_players, how = 'left', on = 'game_id')

    idf['Home Team'] = pd.Series([x.split('-')[1].strip() for x in idf['game']], index=idf.index)
    for k, v in {"GS": "GSW", 'NJ': 'NJN', 'NO': 'NOP', 'NY': 'NYK', 'UTAH': 'UTA',}.items():
        idf.replace(k, v, inplace = True)

    salaries = pd.read_csv(path + 'salary data/playersalaries.csv')
    salaries['Player'] = salaries['Player'].str.lower()
    salaries['Player'] = pd.Series([x.replace('.', '').replace("'", '') for x in salaries.Player], index=salaries.index)

    data = pd.merge(idf, teamNames, how = 'left', right_index=True, left_on = 'Home Team')
    data['Location'] = data['Location'].astype(str)
    data['State'] = [i.split(',')[1] for i in data.Location.values]
    data['City'] = [i.split(',')[0] for i in data.Location.values]

    player_team = []
    for x in data.itertuples():
        pp = x.player
        try:
            ww = pp.split()[0][0] + '. ' + pp.split()[1]
        except IndexError:
            ww = 'Nene'
        if ww in x.home_team_roster:
            player_team.append('home')
        elif ww in x.away_team_roster:
            player_team.append('away')
        else:
            player_team.append('0')
            # print(ww, x.away_team_roster, x.home_team_roster)
    data['Players_team'] = pd.Series(player_team, index = data.index)
    data = data[data['Players_team'] != '0']
    return data
    # pickle_out = open("data.pickle","wb")
    # pickle.dump(data, pickle_out)
    # pickle_out.close()
def make_map(data):
    # state_data = pd.DataFrame(data.groupby(['State'])['shot_made'].sum())
    # bb = data.groupby(['State'])['shot_made'].count()
    #
    # state_data['count'] = bb
    # state_data['percent'] = state_data['shot_made'] / state_data['count']
    # print(state_data.sort_values('percent'))

    city_data = pd.DataFrame(data.groupby(['City'])['shot_made'].sum())
    city_data['count'] = data.groupby(['City'])['shot_made'].count()
    city_data['percent'] = city_data['shot_made'] / city_data['count']

    lat_ = []
    lon_ = []
    for x in city_data.itertuples():
        for y in teamNames.itertuples():
            if x.Index == y.City:
                lat_.append(y.Lat)
                lon_.append(y.Lon)
                break
    city_data['lat'] = lat_
    city_data['lon'] = lon_

    top = np.array([city_data.at['Portland', 'percent'], city_data.at['Seattle', 'percent']])
    midtop = np.array([city_data.at['San Fransisco', 'percent'], city_data.at['Denver', 'percent'],
                       city_data.at['Sacramento', 'percent'], city_data.at['Indianapolis', 'percent'],
                       city_data.at['Washington', 'percent'], city_data.at['Philadelphia', 'percent'],
                       city_data.at['Salt Lake City', 'percent'], city_data.at['Jersey City', 'percent'],
                       city_data.at['Brooklyn', 'percent'], city_data.at['New York', 'percent'],
                       city_data.at['Toronto', 'percent'], city_data.at['Detroit', 'percent'], city_data.at['Boston', 'percent'],
                       city_data.at['Chicago', 'percent'], city_data.at['Cleveland', 'percent'],
                       city_data.at['Milwaukee', 'percent'], city_data.at['Minneapolis', 'percent']])
    midlow = np.array([city_data.at['Phoenix', 'percent'], city_data.at['Charlotte', 'percent'],
                       city_data.at['Atlanta', 'percent'], city_data.at['Oklahoma City', 'percent'],
                       city_data.at['Memphis', 'percent'], city_data.at['Los Angeles', 'percent']])
    bottom = np.array([city_data.at['Houston', 'percent'], city_data.at['Miami', 'percent'],
                       city_data.at['Orlando', 'percent'], city_data.at['New Orleans', 'percent'],
                       city_data.at['Dallas', 'percent'], city_data.at['San Antonio', 'percent']])

    pacific = np.array([city_data.at['Seattle', 'percent'],city_data.at['Portland', 'percent'],
                        city_data.at['Los Angeles', 'percent'],
                        city_data.at['Sacramento', 'percent'],city_data.at['San Fransisco', 'percent'],])
    mountain = np.array([city_data.at['Salt Lake City', 'percent'],city_data.at['Phoenix', 'percent'],city_data.at['Denver', 'percent'],])
    central = np.array([city_data.at['Minneapolis', 'percent'],city_data.at['Memphis', 'percent'],
                        city_data.at['Milwaukee', 'percent'],city_data.at['Chicago', 'percent'],
                        city_data.at['San Antonio', 'percent'],city_data.at['Oklahoma City', 'percent'],
                        city_data.at['Houston', 'percent'],city_data.at['New Orleans', 'percent'],city_data.at['Dallas', 'percent']])
    eastern = np.array([city_data.at['Toronto', 'percent'],city_data.at['Indianapolis', 'percent'],city_data.at['Washington', 'percent'],
                        city_data.at['Boston', 'percent'],city_data.at['Philadelphia', 'percent'],city_data.at['Charlotte', 'percent'],
                        city_data.at['New York', 'percent'],city_data.at['Brooklyn', 'percent'],city_data.at['Atlanta', 'percent'],
                        city_data.at['Jersey City', 'percent'],city_data.at['Cleveland', 'percent'],city_data.at['Orlando', 'percent'],
                        city_data.at['Detroit', 'percent'], city_data.at['Miami', 'percent']])




    fig = plt.figure()
    m = Basemap(projection='lcc', resolution='l',
                lat_0=39.8333333, lon_0=-98.585522,
                width=5E6, height=3E6)
    m.shadedrelief()
    m.drawcoastlines(color='gray')
    m.drawcountries(color='gray')
    m.drawstates(color='gray')
    m.scatter(city_data['lon'].values, city_data['lat'].values, latlon=True,
              c=city_data['percent'],s=250,alpha = 0.8, cmap = 'YlOrRd')
    plt.colorbar(label=r'Percentage (%)')
    plt.tick_params(axis='y', labelsize=20)

    fig2 = plt.figure()
    m2 = Basemap(projection='lcc', resolution='l',
                lat_0=39.8333333, lon_0=-98.585522,
                width=5E6, height=3E6)
    m2.shadedrelief()
    m2.drawcoastlines(color='gray')
    m2.drawcountries(color='gray')
    m2.drawstates(color='gray')
    plt.fill_between([0, 5000000], [3000000 * 0.75, 3000000 * 0.75], [3000000, 3000000], facecolor='blue', alpha=0.2,
                     label='{:.1f}%'.format(100 * top.mean()))
    plt.fill_between([0, 5000000], [3000000 / 2, 3000000 / 2], [3000000 * 0.75, 3000000 * 0.75], facecolor='yellow',
                     alpha=0.2, label='{:.1f}%'.format(100 * midtop.mean()))
    plt.fill_between([0, 5000000], [3000000 / 4, 3000000 / 4], [3000000 / 2, 3000000 / 2], facecolor='red', alpha=0.2,
                     label='{:.1f}%'.format(100 * midlow.mean()))

    plt.fill_between([0,5000000], [3000000/4,3000000/4],facecolor='green', alpha = 0.2, label = '{:.1f}%'.format(100*bottom.mean()))
    m2.scatter(city_data['lon'].values, city_data['lat'].values, latlon=True, c='black', s=60)
    plt.legend(loc = 'lower left')

    fig3 = plt.figure()
    m3 = Basemap(projection='lcc', resolution='l',
                lat_0=39.8333333, lon_0=-98.585522,
                width=5E6, height=3E6)
    m3.shadedrelief()
    m3.drawcoastlines(color='gray')
    m3.drawcountries(color='gray')
    m3.drawstates(color='gray')
    plt.fill_between([0, (5000000/4)-50000],[0,0],[3000000,3000000], facecolor='blue', alpha=0.2,
                     label='Pacific: {:.1f}%'.format(100 * pacific.mean()))
    plt.fill_between([(5000000/4)-50000, (5000000/2)-50000],[0,0],[3000000,3000000], facecolor='yellow',
                     alpha=0.2, label='Mountain: {:.1f}%'.format(100 * mountain.mean()))
    plt.fill_between([(5000000/2)-50000, (5000000*0.75)-250000],[0,0],[3000000,3000000], facecolor='red', alpha=0.2,
                     label='Central: {:.1f}%'.format(100 * central.mean()))
    plt.fill_between([(5000000*0.75)-250000,5000000],[0,0],[3000000,3000000],facecolor='green', alpha = 0.2, label = 'Eastern: {:.1f}%'.format(100*eastern.mean()))

    m3.scatter(city_data['lon'].values, city_data['lat'].values, latlon=True, c='black', s=60)
    plt.legend(loc = 'lower left')
def get_season_stats():
    try:
        season_stats = pd.read_parquet(data_path + 'season_stats_cleaned.parquet')
    except:
        season_stats = pd.read_csv("Seasons_Stats.csv")
        season_stats['Pos'].replace('C-F', "C-PF", inplace = True)
        season_stats['Pos'].replace('C-SF', "PF", inplace=True)
        season_stats['Pos'].replace('F', "SF", inplace=True)
        season_stats['Pos'].replace('F-C', "PF", inplace=True)
        season_stats['Pos'].replace('G', "SG", inplace=True)
        season_stats['Pos'].replace('PF-C', "C-PF", inplace=True)
        season_stats['Pos'].replace('F-G', "PF-SF", inplace=True)
        season_stats['Pos'].replace('G-F', "PF-SF", inplace=True)
        season_stats['Pos'].replace('SF-PF', "PF-SF", inplace=True)
        season_stats['Pos'].replace('PG-SF', "SG", inplace=True)
        season_stats['Pos'].replace('PG-SF', "SG", inplace=True)
        season_stats['Pos'].replace('SG-SF', "SF-SG", inplace=True)
        season_stats['Pos'].replace('PG-SG', "SG-PG", inplace=True)
        season_stats['Pos'].replace('SF-PG', "SG", inplace=True)
        season_stats['Pos'].replace('SG-PF', "SF", inplace=True)
    return season_stats
doc = curdoc()
doc.clear()
doc.title = 'NBA Free Throw Analysis'

path = os.getcwd().replace("\\", '/') + '/'
data_path = path + 'data/'
timee = datetime.datetime.now()
print(timee)
season_stats = get_season_stats()
# teamNames = get_team_names()

# dictionary with all games for each team between 2016-2017 and 2020 seasons or 2008-2009 to 2015-2016 seasons. Structure:
# year{
#       team{
#           playoffs / regular season{
#                       url }
# pickle_in = open(data_path + "all_games_all_years_2009_2016.pickle", "rb")
# data_2016 = pickle.load(pickle_in)
# pickle_in = open(data_path + "all_games_all_years_2017_2020.pickle", "rb")
# data_2020 = pickle.load(pickle_in)
# print(data_2016.keys(), data_2016[list(data_2016.keys())[0]])
# SQLITE3 DATABASE (matchup)
# engine = sqlite3.connect(data_path + 'nba_matchup_data.db')
# # SQLITE3 DATABASE (play by play)
# engine_playbyplay = sqlite3.connect(data_path + 'nba_playbyplay_data.db')
# # SQLITE3 DATABASE (boxscore)
# engine_boxscore = sqlite3.connect(data_path + 'nba_boxscore_data.db')
# # SQLITE3 DATABASE (freethrow)
# engine_freethrow = sqlite3.connect(data_path + 'nba_freethrow_data.db')
# MONGODB DATABASE
# mongo_client = pymongo.MongoClient('localhost', 27017)
# db = mongo_client['NBA']
# collection = db['basic_game_info']
# data_2016.update(data_2020)
# # all game_id's in a list
# all_games = [item.split('gameId=')[1] for sublist in NestedDictValues(data_2016) for item in sublist]

# df = consolidate_to_single_df()

# pickle_in = open(path + "data.pickle","rb")
# df = pickle.load(pickle_in)
data = pd.read_parquet(path + 'nba_free_throw_data.parquet')
# ----------------------------------------
def update_absolute(attr, old, new):
    score_dif_source.data = dict(make_score_dif_source(new).data)
def make_score_dif_source(i):
    if i == "+/- Difference":
        c = [int(x.split('-')[0]) - int(x.split('-')[1]) for x in data["score_before"]]
    elif i == 'Absolute Difference':
        c = [np.abs(int(x.split('-')[0]) - int(x.split('-')[1])) for x in data["score_before"]]
    data['Score_Difference'] = pd.Series(c, index=data.index)
    score_dif = pd.DataFrame(data.groupby(['Score_Difference'])['shot_made'].sum())
    score_dif['count'] = data.groupby(['Score_Difference'])['shot_made'].count()
    score_dif['percent'] = 100 * score_dif['shot_made'] / score_dif['count']
    score_dif = score_dif[(score_dif.index >= -40) & (score_dif.index <= 40)]
    return ColumnDataSource({'x': list(score_dif.index), 'y': score_dif['percent'].tolist(), })

select_absolute = Select(title='+/- or Absolute?', value=f"+/- Difference", options=['+/- Difference', "Absolute Difference", ], width=175)
select_absolute.on_change('value', update_absolute)

t_o_g = []
score_before = []

for x in data[['shot_made', "score_after", 'period', 'minute_of_game', 'Players_team']].itertuples():
    if x.shot_made == 0: # if shot was missed, just look at the score
        score_before.append(x.score_after)
    else: # else, see which team the player was on, then subtract one from that team's score
        score = x.score_after
        first_num = int(score.split(' - ')[0])
        second_num = int(score.split(' - ')[1])
        if x.Players_team == 'away':
            first_num -= 1
        else:
            second_num -= 1
        score_before.append(f'{first_num} - {second_num}')

    if x.period == float(4):
        out = x.minute_of_game + 36
    elif x.period == float(2):
        out = x.minute_of_game + 12
    elif x.period == float(3):
        out = x.minute_of_game + 24
    else:
        out = x.minute_of_game
    t_o_g.append(out)

data['time_of_game'] = t_o_g
data['score_before'] = pd.Series(score_before, index=data.index)
score_dif_source = make_score_dif_source(select_absolute.value)
score_dif_chart = figure(plot_width=900, plot_height=500, y_range = (60, 85),
           tools=[BoxSelectTool(), BoxZoomTool(), ResetTool(), WheelZoomTool(), SaveTool(), PanTool()],
           x_axis_label="Difference in Score", y_axis_label="Percentage (%)", toolbar_location="right", title=f"HOME COURT ADVANTAGE")
score_dif_chart.vbar('x', top='y',bottom=0, source=score_dif_source, width = 0.6, color='blue', line_color='blue', alpha=0.65,)
score_dif_chart.add_tools(HoverTool(tooltips=[("Difference in Score", "@x"),("Percentage (%)", "@y{(0.0)}"),],))
score_dif_chart.yaxis.ticker.desired_num_ticks = 10
# ----------------------------------------

what = get_salary_scatter_data(data)
what.index = [' '.join([x.split(' ')[0].capitalize(),x.split(' ')[1].capitalize()]) for x in what.index]

def update_slider(attr, old, new):
    new_what = what[what['attempts'] >= int(new)].copy()
    scatter_src.data = dict(ColumnDataSource(data={'x': new_what['salary'], 'y': new_what['percent'], 'player': new_what.index, 'attempts': new_what['attempts'], }).data)
    worst_shooters_ = new_what.sort_values(by='percent').head(10)
    worst_names_ = list(worst_shooters_.index)
    worst_source.data = dict(ColumnDataSource(data={'right': worst_shooters_['percent'], 'y': worst_names_, 'attempts': worst_shooters_['attempts']}).data)
    worst_shooter_chart.y_range.factors = worst_names_
    best_shooters_ = new_what.sort_values(by = 'percent', ascending=False).head(12)
    best_names_ = list(best_shooters_.index)
    best_names_.reverse()
    best_source.data = dict(ColumnDataSource(data={'right': best_shooters_['percent'].sort_values(), 'y': best_names_, 'attempts': best_shooters_.sort_values('percent')['attempts']}).data)
    best_shooter_chart.y_range.factors = best_names_

slider = Slider(start=30, end=what['attempts'].max(), step=100, value=30, title="Minimum Attempts", width = 200)
slider.on_change('value', update_slider)

best_shooters = what.sort_values(by = 'percent', ascending=False).head(12)
best_names = list(best_shooters.index)
best_names.reverse()

worst_shooters = what.sort_values(by = 'percent').head(10)
worst_names = list(worst_shooters.index)
worst_shooter_chart = figure(plot_width=600, plot_height=500, y_range = worst_names,
           tools=[BoxSelectTool(), BoxZoomTool(), ResetTool(), WheelZoomTool(), SaveTool(), PanTool()],
           x_axis_label="Percentage (%)", toolbar_location="right", title=f"Worst Shooters in NBA History")
worst_source = ColumnDataSource(data = {'right': worst_shooters['percent'], 'y': worst_names, 'attempts':worst_shooters['attempts']})
worst_shooter_chart.hbar('y', right='right', source = worst_source,  height=0.6, alpha=0.65,  fill_color='blue', line_color = 'blue', line_width = 2, name = 'away')
worst_shooter_chart.add_tools(HoverTool(tooltips=[("Player", "@y"),("Percentage (%)", "@right{(0.0)}"),("Attempts", "@attempts{(0,0)}"),],))
worst_shooter_chart.ygrid.visible = False

best_shooter_chart = figure(plot_width=600, plot_height=500, y_range = best_names,
           tools=[BoxSelectTool(), BoxZoomTool(), ResetTool(), WheelZoomTool(), SaveTool(), PanTool()],
           x_axis_label="Percentage (%)", toolbar_location="right", title=f"Best Shooters in NBA History")
best_source = ColumnDataSource(data = {'right': best_shooters['percent'].sort_values(), 'y': best_names, 'attempts':best_shooters.sort_values('percent')['attempts']})
best_shooter_chart.hbar('y', right='right', source = best_source,  height=0.6, alpha=0.65,  fill_color='orangered', line_color = 'orangered', line_width = 2, name = 'away')
best_shooter_chart.add_tools(HoverTool(tooltips=[("Player", "@y"),("Percentage (%)", "@right{(0.0)}"),("Attempts", "@attempts{(0,0)}")],))
best_shooter_chart.ygrid.visible = False
# -------------------------------------
salary_scatter = figure(plot_width=900, plot_height=500, x_axis_label="Today's Adj. Salary",
           tools=[BoxSelectTool(), BoxZoomTool(), ResetTool(), WheelZoomTool(), SaveTool(), PanTool()],
           y_axis_label="Percentage (%)", toolbar_location="right", title=f"Career FT% vs Mean Salaries in the NBA")
scatter_src = ColumnDataSource(data = {'x': what['salary'], 'y': what['percent'], 'player':what.index, 'attempts': what['attempts'],})
salary_scatter.circle('x', 'y', source=scatter_src,  alpha=0.55, size = 6,  fill_color='orangered', line_color = 'blue', line_width = 2, name = 'away')
salary_scatter.add_tools(HoverTool(tooltips=[("Player", "@player"),("Salary", "@x{(0,0)}"),("Percentage (%)", "@y"),("Attempts", "@attempts{(0,0)}"),],))
salary_scatter.xaxis[0].formatter = NumeralTickFormatter(format="$0.0 a")
salary_scatter.xaxis.major_label_orientation = np.pi / 4

for plot in [best_shooter_chart, worst_shooter_chart, salary_scatter,]:
    plot.x_range.start = 0
# ----------------------------------------

def make_position_bar_source(df, metric = 'percent'):
    return ColumnDataSource(data = {'x': df.index, 'y': df[metric], 'percent': df['percent'], 'made': df['shot_made'], 'attempts': df['count']})
def update_metric_position(attr, old, new):
    if new == 'Percentage':
        src.data = dict(make_position_bar_source(groupby_position,).data)
        position_matters_bar.yaxis.axis_label = 'Percentage (%)'
        position_matters_bar.title.text = f"Percentage by Position"
    elif new == 'Attempts':
        src.data = dict(make_position_bar_source(groupby_position,'count').data)
        position_matters_bar.yaxis.axis_label = 'Shots'
        position_matters_bar.title.text = f"Shots Attempted by Position"
    elif new == "Shots Made":
        src.data = dict(make_position_bar_source(groupby_position,'shot_made').data)
        position_matters_bar.yaxis.axis_label = 'Shots'
        position_matters_bar.title.text = f"Shots Made by Position"

select_metric_position = Select(title='Metric', value=f"Percentage", options=['Percentage', "Attempts", "Shots Made"], width=175)
select_metric_position.on_change('value', update_metric_position)

# find how many times player played at each position
tmp = season_stats.groupby(['Player', 'Pos']).agg({'Pos':'count'}).unstack()
# find how max of each player's position, put that as player's position
positions = pd.DataFrame(tmp.idxmax(axis=1), columns=['pos'])
positions['position'] = [x[1] for x in positions['pos']]
positions.index = [x.lower().replace('*', '') for x in positions.index]
positions['player'] = positions.index
positions = clean_player2(positions)
positions.index = positions['player']
positions.drop(['pos', 'player'], 1, inplace=True)
data['player'] = data['player'].str.lower() # lower names so join works
full_data = pd.merge(data, positions, how = 'inner', right_index=True, left_on = 'player')

# find simple stats for each position
groupby_position = pd.DataFrame(full_data.groupby(['position'])['shot_made'].sum())
groupby_position['count'] = full_data.groupby(['position'])['shot_made'].count()
groupby_position['percent'] = 100 * groupby_position['shot_made'] / groupby_position['count']
groupby_position = groupby_position.sort_values("percent", ascending=False)

src = make_position_bar_source(groupby_position)
position_matters_bar = figure(plot_width=600, plot_height=500, x_range=list(groupby_position.index),
           tools=[BoxSelectTool(), BoxZoomTool(), ResetTool(), WheelZoomTool(), SaveTool(), PanTool()],
           x_axis_label="Position", y_axis_label="Percentage (%)", toolbar_location="right", title=f"Percentage by Position")
position_matters_bar.vbar('x', top='y', source=src, width=0.6, alpha=0.75, name='bars', fill_color='orangered', line_color = 'orangered', line_width = 2)
position_matters_bar.add_tools(HoverTool(mode='vline', tooltips=[("Position", "@x"), ("Percentage (%)", "@percent{(0.0)}"),("Attempts", "@attempts{(0,0)}"), ("Shots Made", "@made{(0,0)}"),],))
position_matters_bar.yaxis[0].formatter = NumeralTickFormatter(format="0,0")

# ----------------------------------------

def home_away(data_, szn):
    data_ = data_[data_['season'] == szn].copy()
    home_shot_made = data_[data_['Players_team'] == 'home']['shot_made'].copy()
    away_shot_made = data_[data_['Players_team'] == 'away']['shot_made'].copy()
    home_versus_away = {'made_home': home_shot_made.sum(),
                        'made_away': away_shot_made.sum(),
                        'total_home': len(home_shot_made.index),
                        'total_away': len(away_shot_made.index),
                        'home_made_percentage': home_shot_made.sum() / len(home_shot_made.index),
                        'away_made_percentage': away_shot_made.sum() / len(away_shot_made.index)}
    return home_versus_away
def update_metric_home_away(attr, old, new):
    if new == 'Attempts':
        away_ = [tmp_dict[i]['total_away'] * 100 for i in data['season'].unique()]
        home_ = [tmp_dict[i]['total_home'] * 100 for i in data['season'].unique()]
        home_away_bar.y_range.start = min(min(home_), min(away_)) * 0.75
        home_away_bar.y_range.end = max(max(home_), max(away_)) * 1.2
        home_away_bar.yaxis.axis_label = "Shots"
    elif new == 'Shots Made':
        away_ = [tmp_dict[i]['made_home'] * 100 for i in data['season'].unique()]
        home_ = [tmp_dict[i]['made_away'] * 100 for i in data['season'].unique()]
        home_away_bar.y_range.end = max(max(home_), max(away_)) * 1.2
        home_away_bar.y_range.start = min(min(home_), min(away_)) * 0.75
        home_away_bar.yaxis.axis_label = "Shots"
    elif new == 'Percentage':
        away_ = [tmp_dict[i]['away_made_percentage'] * 100 for i in data['season'].unique()]
        home_ = [tmp_dict[i]['home_made_percentage'] * 100 for i in data['season'].unique()]
        home_away_bar.y_range.end = 79
        home_away_bar.y_range.start = 72
        home_away_bar.yaxis.axis_label = "Percentage (%)"

    src_away.data = dict(ColumnDataSource(
        data={'x': [x - 0.2 for x in range(len(data['season'].unique()))], 'y': away_, 'season': list(data['season'].unique()), 'label': ['Away' for _ in data['season'].unique()]}).data)
    src_home.data = dict(ColumnDataSource(
        data={'x': [x + 0.2 for x in range(len(data['season'].unique()))], 'y': home_, 'season': list(data['season'].unique()), 'label': ['Home' for _ in data['season'].unique()]}).data)
    home_avg_src.data = dict(ColumnDataSource(data={'x': [i for i in range(len(home_))], 'y': [np.mean(home_) for x in home_]}).data)
    away_avg_src.data = dict(ColumnDataSource(data={'x': [i for i in range(len(away_))], 'y': [np.mean(away_) for x in away_]}).data)
    home_away_bar.xaxis.ticker.desired_num_ticks = len(data['season'].unique())
    home_away_bar.xaxis.major_label_overrides = {i: v for i, v in enumerate(data['season'].unique())}
    # home_away_bar.xaxis.ticker = [i for i in data['season'].unique()]

select_metric_home_away = Select(title='Metric', value=f"Percentage", options=['Percentage', "Attempts", "Shots Made"], width=175)
select_metric_home_away.on_change('value', update_metric_home_away)

tmp_dict = {str(i): home_away(data, i) for i in data['season'].unique()}
away = [tmp_dict[i]['away_made_percentage'] * 100 for i in data['season'].unique()]
home = [tmp_dict[i]['home_made_percentage'] * 100 for i in data['season'].unique()]

home_away_bar = figure(plot_width=700, plot_height=500, y_range = (72, 79),
           tools=[BoxSelectTool(), BoxZoomTool(), ResetTool(), WheelZoomTool(), SaveTool(), PanTool()],
           x_axis_label="Position", y_axis_label="Percentage (%)", toolbar_location="right", title=f"Home Court Advantage?")
src_away = ColumnDataSource(data = {'x': [x - 0.2 for x in range(len(data['season'].unique()))], 'y': away, 'season': list(data['season'].unique()), 'label': ['Away' for _ in data['season'].unique()]})
src_home = ColumnDataSource(data = {'x': [x + 0.2 for x in range(len(data['season'].unique()))], 'y': home, 'season': list(data['season'].unique()), 'label': ['Home' for _ in data['season'].unique()]})
home_away_bar.vbar('x', top='y', source=src_home, width=0.3, alpha=0.65, legend_label='Home', fill_color='orangered', line_color = 'orangered', line_width = 2, name = 'home')
home_away_bar.vbar('x', top='y', source=src_away, width=0.3, alpha=0.65, legend_label='Away', fill_color='blue', line_color = 'blue', line_width = 2, name = 'away')

home_avg_src = ColumnDataSource(data={'x':[i for i in range(len(home))],'y':[np.mean(home) for x in home]})
away_avg_src = ColumnDataSource(data={'x':[i for i in range(len(away))],'y':[np.mean(away) for x in away]})
home_avg = home_away_bar.line('x', 'y', source = home_avg_src, color = 'orangered', legend_label = 'Home Average',name='home_avg',  line_width = 4)
away_avg = home_away_bar.line('x', 'y', source = away_avg_src, color = 'blue', legend_label = 'Away Average',name='away_avg', line_width = 4)
home_avg.visible = False
away_avg.visible = False

home_away_bar.add_tools(HoverTool(mode='vline', tooltips=[("Season", "@season"), ("Value", "@y{(0.0)}"),],names = ['home', 'away']))
home_away_bar.add_tools(HoverTool(mode='vline', tooltips=[("Average (%)", "@y{(0.0)}"),],names = ['home_avg', 'away_avg']))
home_away_bar.xaxis.ticker.desired_num_ticks = len(data['season'].unique())
home_away_bar.xaxis.major_label_overrides = {i: v for i, v in enumerate(data['season'].unique())}

home_away_bar.yaxis[0].formatter = NumeralTickFormatter(format="0,0")
home_away_bar.xaxis.major_label_orientation = np.pi / 4
home_away_bar.xgrid.visible = False
home_away_bar.legend.location = "top_left"
home_away_bar.legend.click_policy = "hide"
home_away_bar.legend.orientation = "horizontal"

# ----------------------------------------
def update_metric_period(attr, old, new):
    if new == 'Attempts':
        tmp = ColumnDataSource(data={'percent': period_df['percent'],'y': period_df['count'], 'x': period_df.index, 'attempts': period_df['count'],'periods':periods})
        period_chart.yaxis.axis_label = 'Shots'
        period_chart.title.text = f"Shots Attempted by Quarter"
        period_chart.y_range.end = period_df['count'].max() * 1.2
        period_chart.y_range.start = period_df['count'].min() * 0.75
    elif new == 'Shots Made':
        tmp = ColumnDataSource(data={'percent': period_df['percent'],'y': period_df['shot_made'], 'x': period_df.index, 'attempts': period_df['count'],'periods':periods})
        period_chart.yaxis.axis_label = 'Shots'
        period_chart.title.text = f"Shots Made by Quarter"
        period_chart.y_range.end = period_df['shot_made'].max() * 1.2
        period_chart.y_range.start = period_df['shot_made'].min() * 0.75
    elif new == 'Percentage':
        tmp = ColumnDataSource(data={'percent': period_df['percent'],'y': period_df['percent'], 'x': period_df.index, 'attempts': period_df['count'],'periods':periods})
        period_chart.yaxis.axis_label = 'Percentage (%)'
        period_chart.title.text = f"Percentage by Quarter"
        period_chart.y_range.end = 85
        period_chart.y_range.start = 60
    period_src.data = dict(tmp.data)

select_metric_period = Select(title='Metric', value=f"Percentage", options=['Percentage', "Attempts", "Shots Made"], width=175)
select_metric_period.on_change('value', update_metric_period)

period_df = pd.DataFrame(data.groupby(['period'])['shot_made'].sum())
period_df['count'] =data.groupby(['period'])['shot_made'].count()
period_df['percent'] = 100*period_df['shot_made']/period_df['count']
periods = ['Q1','Q2','Q3','Q4','OT','2OT','3OT','4OT']
period_chart = figure(plot_width=600, plot_height=500, tools=[BoxSelectTool(), BoxZoomTool(), ResetTool(), WheelZoomTool(), SaveTool(), PanTool()],
           x_axis_label="Percentage (%)", toolbar_location="right", title=f"Performance by Quarter", y_range = (60, 85))
period_src = ColumnDataSource(data = {'percent': period_df['percent'], 'y': period_df['percent'], 'x': period_df.index, 'attempts':period_df['count'], 'periods':periods})
period_chart.vbar('x', top='y', bottom=0, source = period_src,  width=0.6, alpha=0.65,  fill_color='blue', line_color = 'blue', line_width = 2, name = 'away')
period_chart.add_tools(HoverTool(tooltips=[("Period", "@periods"),("Percentage (%)", "@percent{(0.0)}"),("Attempts", "@attempts{(0,0)}"),],))
period_chart.xaxis.ticker.desired_num_ticks = len(period_df.index)
period_chart.yaxis.ticker.desired_num_ticks = 10
period_chart.xaxis.major_label_overrides = {i+1: v for i, v in enumerate(periods)}

# ----------------------------------------

def update_metric_minute(attr, old, new):
    if new == 'Attempts':
        tmp = ColumnDataSource(data={'percent': time_of_game_special['percent'],'y': time_of_game_special['attempts'], 'x': time_of_game_special.index, 'attempts': time_of_game_special['attempts'],})
        tmp2 = ColumnDataSource(data={'percent': time_of_game_ns['percent'],'y': time_of_game_ns['attempts'], 'x': time_of_game_ns.index, 'attempts': time_of_game_ns['attempts'],})

        time_of_game_chart.yaxis.axis_label = 'Shots'
        time_of_game_chart.title.text = f"Shots Attempted by Minute"
        time_of_game_chart.y_range.end = time_of_game['attempts'].max() * 1.2
        time_of_game_chart.y_range.start = time_of_game['attempts'].min() * 0.75
    elif new == 'Shots Made':
        tmp2 = ColumnDataSource(data={'percent': time_of_game_ns['percent'],'y': time_of_game_ns['shot_made'], 'x': time_of_game_ns.index, 'attempts': time_of_game_ns['attempts'],})

        tmp = ColumnDataSource(data={'percent': time_of_game_special['percent'],'y': time_of_game_special['shot_made'], 'x': time_of_game_special.index, 'attempts': time_of_game_special['attempts'],})
        time_of_game_chart.yaxis.axis_label = 'Shots'
        time_of_game_chart.title.text = f"Shots Made by Minute"
        time_of_game_chart.y_range.end = time_of_game['shot_made'].max() * 1.2
        time_of_game_chart.y_range.start = time_of_game['shot_made'].min() * 0.75
    elif new == 'Percentage':
        tmp = ColumnDataSource(data={'percent': time_of_game_special['percent'],'y': time_of_game_special['percent'], 'x': time_of_game_special.index, 'attempts': time_of_game_special['attempts'],})
        tmp2 = ColumnDataSource(data={'percent': time_of_game_ns['percent'],'y': time_of_game_ns['percent'], 'x': time_of_game_ns.index, 'attempts': time_of_game_ns['attempts'],})

        time_of_game_chart.yaxis.axis_label = 'Percentage (%)'
        time_of_game_chart.title.text = f"Percentage by Minute"
        time_of_game_chart.y_range.end = 85
        time_of_game_chart.y_range.start = 60
    time_of_game_special_src.data = dict(tmp.data)
    time_of_game_src.data = dict(tmp2.data)

select_metric_minute = Select(title='Metric', value=f"Percentage", options=['Percentage', "Attempts", "Shots Made"], width=175)
select_metric_minute.on_change('value', update_metric_minute)

time_of_game = pd.DataFrame(data.groupby(['time_of_game'])['shot_made'].sum())
time_of_game['attempts'] = data.groupby(['time_of_game'])['shot_made'].count()
time_of_game['percent'] = 100 * time_of_game['shot_made'] / time_of_game['attempts']
time_of_game.index = time_of_game.index.astype(str)

time_of_game_chart = figure(plot_width=900, plot_height=500, tools=[BoxSelectTool(), BoxZoomTool(), ResetTool(), WheelZoomTool(), SaveTool(), PanTool()],
                            x_axis_label="Minute of the game", toolbar_location="right", title=f"Each and Every Minute", y_range=(60, 85), x_range = (list(time_of_game.index)))

time_of_game_special = time_of_game.iloc[0:-1:12, :].copy()
time_of_game_ns = time_of_game.drop(index=[str(i) for i in range(0,len(time_of_game.index),12)])

time_of_game_src = ColumnDataSource(data={'percent': time_of_game_ns['percent'], 'y': time_of_game_ns['percent'], 'x': time_of_game_ns.index, 'attempts': time_of_game_ns['attempts'], })
time_of_game_special_src = ColumnDataSource(data={'percent': time_of_game_special['percent'], 'y': time_of_game_special['percent'], 'x': time_of_game_special.index, 'attempts': time_of_game_special['attempts'], })

time_of_game_chart.vbar('x', top='y', bottom=0, source=time_of_game_src, width=0.6, alpha=0.65, fill_color='blue', line_color='blue', line_width=2, name='away')
time_of_game_chart.vbar('x', top='y', bottom=0, source=time_of_game_special_src, width=0.6, alpha=0.65, fill_color='orangered', line_color='orangered', line_width=2, name='special')

time_of_game_chart.add_tools(HoverTool(mode='vline', tooltips=[("Minute", "@x"), ("Percentage (%)", "@percent{(0.0)}"), ("Attempts", "@attempts{(0,0)}"), ], ))
# time_of_game_chart.xaxis.ticker.desired_num_ticks = len(time_of_game.index)
time_of_game_chart.yaxis.ticker.desired_num_ticks = 10
time_of_game_chart.xgrid.visible = False
time_of_game_chart.yaxis[0].formatter = NumeralTickFormatter(format="0,0")

# ----------------------------------------
for plot in [best_shooter_chart, worst_shooter_chart, salary_scatter, score_dif_chart, position_matters_bar, home_away_bar, period_chart, time_of_game_chart]:
    plot.outline_line_width = 3
    plot.outline_line_alpha = 0.3
    plot.axis.minor_tick_line_alpha = 0
    plot.axis.major_tick_line_color = 'black'
    plot.axis.major_tick_in = -1
    plot.yaxis.major_label_text_font_style = 'bold'
    plot.xaxis.major_label_text_font_style = 'bold'
    plot.yaxis.major_label_text_font = "Arial"
    plot.xaxis.major_label_text_font = "Arial"
    plot.title.align = 'center'
    plot.title.text_font_size = '12pt'
    plot.xaxis.axis_line_width = 0
    plot.yaxis.axis_line_width = 0
    plot.yaxis.axis_label_text_font_style = "bold"
    plot.xaxis.axis_label_text_font_style = "bold"
    plot.toolbar.active_scroll = "auto"
    plot.toolbar.autohide = True
    plot.yaxis.axis_label_text_font_size = "10pt"
    plot.xaxis.axis_label_text_font_size = "10pt"
    plot.xaxis.major_label_text_font_size = "10pt"
    plot.yaxis.major_label_text_font_size = "10pt"

tab1 = Panel(child=row([slider, best_shooter_chart]), title="Best Shooters")
tab2 = Panel(child=row([slider, worst_shooter_chart]), title="Worst Shooters")
tab3 = Panel(child=row([slider, salary_scatter]), title="Salary vs Efficiency")
tab4 = Panel(child=row([select_absolute, score_dif_chart]), title="Score Difference")
tab5 = Panel(child=row([select_metric_home_away,home_away_bar]), title="Home vs Away")
tab6 = Panel(child=row([select_metric_position, position_matters_bar]), title="Position Matters")
tab7 = Panel(child=row([select_metric_period, period_chart]), title="Quarters")
tab8 = Panel(child=row([select_metric_minute, time_of_game_chart]), title="Each Minute")
tt = Tabs(tabs=[tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8])
dashboard = column([tt])
curdoc().add_root(dashboard)
show(dashboard)
print(datetime.datetime.now(), datetime.datetime.now()-timee)

