import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import time
import pickle
from pprint import pprint
import pyarrow
from bokeh.models import BasicTickFormatter, HoverTool, BoxSelectTool, BoxZoomTool, ResetTool, Span, Label, Button, DatePicker, CustomJS
from bokeh.models import NumeralTickFormatter, WheelZoomTool, PanTool, SaveTool, ColumnDataSource, LinearAxis, Range1d, FactorRange
from bokeh.models.widgets import Select, inputs, Slider, CheckboxGroup, Toggle, Div
from bokeh.layouts import widgetbox, row, column, gridplot, layout
from sqlalchemy import create_engine
import pymysql
from bokeh.io import curdoc
from pytz import timezone
from bokeh.transform import cumsum
from bokeh.plotting import figure, show
import sqlite3
import pymongo
import os
import colorcet as cc

palette = cc.fire[16:253]

doc = curdoc()
doc.clear()
doc.title = 'NBA FREE THROW'
sns.set()

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
def salary_stuff(data):
    salaries = pd.read_csv(path + 'salary data/playersalaries.csv')
    salaries['Player'] = salaries['Player'].str.lower()
    salaries['Player'] = pd.Series([x.replace('.', '').replace("'", '') for x in salaries.Player], index=salaries.index)

    new = pd.DataFrame(data.groupby(['player']).agg({'shot_made':'sum'}))
    new['attempts'] = data.groupby(['player']).agg({'shot_made': 'count'})
    new['percent'] = new['shot_made']/new['attempts']
    new['salary'] = salaries.groupby(['Player'])['AdjustedSalary'].mean()
    new['salary'].fillna(80000, inplace=True)
    new['salary'] = new['salary'].astype('int64')
    new = new[new['attempts']>24]
    print(new.sort_values(by = 'percent').head(20).to_string())

    print(new.sort_values(by = 'percent', ascending=False).head(20).to_string())

    print(new.sort_values(by = 'salary', ascending=False).head(20).to_string())

    print(new.sort_values(by = 'salary').head(20).to_string())
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

path = os.getcwd().replace("\\", '/') + '/'
data_path = path + 'data/'
timee = datetime.datetime.now()
print(timee)

teamNames = get_team_names()

# dictionary with all games for each team between 2016-2017 and 2020 seasons or 2008-2009 to 2015-2016 seasons. Structure:
# year{
#       team{
#           playoffs / regular season{
#                       url }
pickle_in = open(data_path + "all_games_all_years_2009_2016.pickle", "rb")
data_2016 = pickle.load(pickle_in)
pickle_in = open(data_path + "all_games_all_years_2017_2020.pickle", "rb")
data_2020 = pickle.load(pickle_in)
# print(data_2016.keys(), data_2016[list(data_2016.keys())[0]])
# SQLITE3 DATABASE (matchup)
engine = sqlite3.connect(data_path + 'nba_matchup_data.db')
# SQLITE3 DATABASE (play by play)
engine_playbyplay = sqlite3.connect(data_path + 'nba_playbyplay_data.db')
# SQLITE3 DATABASE (boxscore)
engine_boxscore = sqlite3.connect(data_path + 'nba_boxscore_data.db')
# SQLITE3 DATABASE (freethrow)
engine_freethrow = sqlite3.connect(data_path + 'nba_freethrow_data.db')
# MONGODB DATABASE
mongo_client = pymongo.MongoClient('localhost', 27017)
db = mongo_client['NBA']
collection = db['basic_game_info']
data_2016.update(data_2020)
# all game_id's in a list
all_games = [item.split('gameId=')[1] for sublist in NestedDictValues(data_2016) for item in sublist]

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
def improving_ft(data):
    # find how many shots each player made in each season
    idf = data.groupby(['player', 'season'])['shot_made'].agg(['sum','count']).rename(columns={'sum':'shot_made'})
    idf['percent'] = 100 * idf['shot_made'] / idf['count']
    idf = idf[idf['count'] > 100] # only look for players/seasons with over 100 attempts

    coc = idf.reset_index(drop=False,)
    coc = coc.groupby('player').agg({'season':list})
    cool = pd.DataFrame(coc['season'].tolist(), index = coc.index, columns = [f'Season_{x+1}' for x in range(4)])
    # nice is dictionary with 4 lists. Each element in each list is a different player, but the same element across lists are the same player

    nice = {str(x+1) : [] for x in range(4)}
    for x in cool.itertuples():
        col_nums = {'1': x.Season_1, '2': x.Season_2, '3':x.Season_3,'4':x.Season_4,}
        for i in range(4):
            try:
                nice[str(i+1)].append(idf.at[(x.Index, col_nums[str(i+1)]), 'percent'])
            except:
                nice[str(i+1)].append(np.nan)
    num = 0
    no_num = 0
    for x in nice.keys():
        try:
            for i in range(len(nice[x])):
                if nice[str(int(x)+2)][int(i)] > nice[str(int(x)+1)][int(i)]:
                    num += 1
                elif nice[str(int(x)+2)][int(i)] < nice[str(int(x)+1)][int(i)]:
                    no_num +=1
        except Exception as e:
            pass
    # print overview stats
    print('Times a player shoots better season over season: ',num)
    print('Times a player shoots worse season over season: ',no_num)
    print(f'Percentage of time a Player shoots better: {100*num/(no_num+ num):.1f}%',)
    print(f'Percentage of time a Player shoots worse: {100*no_num/(no_num+ num):.1f}%',)

    plot_data = pd.DataFrame.from_dict(nice)
    plot_data.index = cool.index

    p = figure(plot_width=1100, plot_height=750, title=f"Do Players Improve?",
               tools=[BoxSelectTool(), BoxZoomTool(), ResetTool(),
                      WheelZoomTool(), SaveTool(), PanTool()],
               y_axis_label='Percentage (%)', x_axis_label='Season', )

    for x in plot_data.itertuples():
        p.line(plot_data.columns, np.array(list(x)[1:]),alpha = 0.22, color = 'red')
    for plot in [p, ]:
        plot.yaxis[0].formatter = NumeralTickFormatter(format="0,0")
        plot.yaxis.ticker.desired_num_ticks = 15
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
        plot.xgrid.visible = False
        plot.yaxis.axis_label_text_font_size = "15pt"
        plot.xaxis.axis_label_text_font_size = "15pt"
        plot.xaxis.major_label_text_font_size = "15pt"
        plot.yaxis.major_label_text_font_size = "13pt"
        # plot.legend.location = "top_left"
        # plot.legend.click_policy = "hide"
    # widgets = column([select_metric])
    dashboard = row([p])
    doc.add_root(dashboard)
    show(dashboard)
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
def position_matters(data):
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
    def make_source(df, metric = 'percent'):
        return ColumnDataSource(data = {'x': df.index, 'y': df[metric], 'percent': df['percent'], 'made': df['shot_made'], 'attempts': df['count']})
    def update_metric(attr, old, new):
        if new == 'Percentage':
            src.data = dict(make_source(groupby_position,).data)
            p.yaxis.axis_label = 'Percentage (%)'
        elif new == 'Attempts':
            src.data = dict(make_source(groupby_position,'count').data)
            p.yaxis.axis_label = 'Shots'
        elif new == "Shots Made":
            src.data = dict(make_source(groupby_position,'shot_made').data)
            p.yaxis.axis_label = 'Shots'

    doc = curdoc()
    doc.clear()
    doc.title = 'NBA FREE THROWS'

    season_stats = get_season_stats()
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
    src = make_source(groupby_position)

    select_metric = Select(title='Metric', value=f"Percentage", options=['Percentage', "Attempts", "Shots Made"], width=175)
    select_metric.on_change('value', update_metric)

    p = figure(plot_width=1100, plot_height=750, x_range=list(groupby_position.index),
               tools=[BoxSelectTool(), BoxZoomTool(), ResetTool(), WheelZoomTool(), SaveTool(), PanTool()],
               x_axis_label="Position", y_axis_label="Percentage (%)", toolbar_location="right", title=f"Free Throw Stats by Position")
    p.vbar('x', top='y', source=src, width=0.6, alpha=0.75, name='bars', fill_color='orangered', line_color = 'black', line_width = 2)
    p.add_tools(HoverTool(mode='vline', tooltips=[("Position", "@x"), ("Percentage (%)", "@percent{(0.0)}"),("Attempts", "@attempts{(0,0)}"), ("Shots Made", "@made{(0,0)}"),],))
    for plot in [p,]:
        plot.yaxis[0].formatter = NumeralTickFormatter(format="0,0")
        plot.yaxis.ticker.desired_num_ticks=15
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
        plot.xgrid.visible = False
        plot.yaxis.axis_label_text_font_size = "15pt"
        plot.xaxis.axis_label_text_font_size = "15pt"
        plot.xaxis.major_label_text_font_size = "15pt"
        plot.yaxis.major_label_text_font_size = "13pt"
        # plot.legend.location = "top_left"
        # plot.legend.click_policy = "hide"
    widgets = column([select_metric])
    dashboard = row([widgets, p])
    doc.add_root(dashboard)
    show(dashboard)
def make_home_away_charts(data):
    def home_away(data_, szn):
        data_ = data_[data_['season'] == szn]
        home_shot_made = data_[data_['Players_team'] == 'home']['shot_made'].copy()
        away_shot_made = data_[data_['Players_team'] == 'away']['shot_made'].copy()
        home_versus_away = {'made_home': home_shot_made.sum(),
                            'made_away': away_shot_made.sum(),
                            'total_home': len(home_shot_made.index),
                            'total_away': len(away_shot_made.index),
                            'home_made_percentage': home_shot_made.sum() / len(home_shot_made.index),
                            'away_made_percentage': away_shot_made.sum() / len(away_shot_made.index)}
        return home_versus_away

    fool = {str(i): home_away(data, i) for i in data['season'].unique()}

    away = [fool[i]['away_made_percentage'] * 100 for i in data['season'].unique()]
    home = [fool[i]['home_made_percentage'] * 100 for i in data['season'].unique()]

    home_shots = len(data[data['Players_team'] == 'home']['shot_made'].index)
    away_shots = len(data[data['Players_team'] == 'away']['shot_made'].index)

    p = figure(plot_width=1100, plot_height=750, y_range = (72, 79),
               tools=[BoxSelectTool(), BoxZoomTool(), ResetTool(), WheelZoomTool(), SaveTool(), PanTool()],
               x_axis_label="Position", y_axis_label="Percentage (%)", toolbar_location="right", title=f"HOME COURT ADVANTAGE")
    src_away = ColumnDataSource(data = {'x': [x - 0.2 for x in range(len(data['season'].unique()))], 'y': away, 'season': list(data['season'].unique()), 'label': ['Away' for _ in data['season'].unique()]})
    src_home = ColumnDataSource(data = {'x': [x + 0.2 for x in range(len(data['season'].unique()))], 'y': home, 'season': list(data['season'].unique()), 'label': ['Home' for _ in data['season'].unique()]})
    p.vbar('x', top='y', source=src_home, width=0.3, alpha=0.65, legend_label='Home', fill_color='orangered', line_color = 'orangered', line_width = 2, name = 'home')
    p.vbar('x', top='y', source=src_away, width=0.3, alpha=0.65, legend_label='Away', fill_color='blue', line_color = 'blue', line_width = 2, name = 'away')
    home_avg = p.line([i for i in range(len(home))], [np.mean(home) for x in home], color = 'orangered', legend_label = 'Home Average',name='home_avg',  line_width = 4)
    home_avg.visible = False
    away_avg = p.line([i for i in range(len(away))], [np.mean(away) for x in away], color = 'blue', legend_label = 'Away Average',name='away_avg', line_width = 4)
    away_avg.visible = False
    p.add_tools(HoverTool(mode='vline', tooltips=[("Season", "@season"), ("Percentage (%)", "@y{(0.0)}"),],names = ['home', 'away']))
    p.add_tools(HoverTool(mode='vline', tooltips=[("Average (%)", "@y{(0.0)}"),],names = ['home_avg', 'away_avg']))
    p.xaxis.major_label_overrides = {i: v for i, v in enumerate(data['season'].unique())}

    fdata = pd.Series({'Away': away_shots, 'Home': home_shots}).reset_index(name='attempts').rename(columns={'index': 'category'})
    fdata['angle'] = fdata['attempts'] / fdata['attempts'].sum() * 2 * np.pi
    fdata['color'] = ['blue', 'orangered', ]
    fdata['percent'] = (100* fdata['attempts'] / fdata['attempts'].sum()).round(1)

    w = figure(plot_height=750, title="Away Court Advantage", toolbar_location=None,)

    w.wedge(x=0, y=1, radius=0.8,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='category', source=fdata, alpha = 0.75)
    w.add_tools(HoverTool(tooltips=[("Percentage (%)", "@percent{(0.0)}"),("Attempts", "@attempts{(0,0)}")],))
    w.outline_line_alpha = 0
    w.yaxis.ticker = []
    w.xaxis.ticker = []
    w.legend.click_policy = "hide"
    w.xaxis.axis_line_width = 0
    w.yaxis.axis_line_width = 0
    w.title.align = 'center'
    w.title.text_font_size = '12pt'

    for plot in [p]:
        plot.yaxis[0].formatter = NumeralTickFormatter(format="0,0")
        plot.yaxis.ticker.desired_num_ticks=10
        plot.xaxis.major_label_orientation = np.pi / 4
        plot.xaxis.ticker.desired_num_ticks=len(data['season'].unique())
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
        plot.xgrid.visible = False
        plot.yaxis.axis_label_text_font_size = "15pt"
        plot.xaxis.axis_label_text_font_size = "15pt"
        plot.xaxis.major_label_text_font_size = "12pt"
        plot.yaxis.major_label_text_font_size = "13pt"
        # plot.legend.location = "top_left"
        plot.legend.click_policy = "hide"

    dashboard = row([p, w])
    doc.add_root(dashboard)
    show(dashboard)
    # fig1 = plt.figure()
    # fig1.suptitle('AWAY COURT ADVANTAGE', fontsize=20)
    # ax2 = fig1.add_subplot(111)
    # ax2.pie([home_shots, away_shots], labels=['HOME - {:.1f}%'.format(100 * home_shots / (home_shots + away_shots)),
    #                                           'AWAY - {:.1f}%'.format(100 * away_shots / (home_shots + away_shots))],
    #         startangle=90, labeldistance=0.35, textprops={'fontsize': 18, 'color': 'white', 'weight': 'bold'})
    # plt.show()


def score_thing(data):
    score_before = []
    for x in data.itertuples():
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

    data['score_before'] = pd.Series(score_before, index=data.index)
    data['Score_Difference_abs'] = pd.Series([np.abs(int(x.split('-')[0]) - int(x.split('-')[1])) for x in data["score_before"]], index=data.index)
    data['Score_Difference'] = pd.Series(
        [int(x.split('-')[0]) - int(x.split('-')[1]) for x in data["score_before"]], index=data.index)

    score_dif = pd.DataFrame(data.groupby(['Score_Difference'])['shot_made'].sum())
    score_dif['count'] = data.groupby(['Score_Difference'])['shot_made'].count()
    score_dif['percent'] = 100 * score_dif['shot_made'] / score_dif['count']
    score_dif = score_dif[score_dif.index >= -40]
    score_dif = score_dif[score_dif.index <= 40]

    p = figure(plot_width=1100, plot_height=750, y_range = (60, 85),
               tools=[BoxSelectTool(), BoxZoomTool(), ResetTool(), WheelZoomTool(), SaveTool(), PanTool()],
               x_axis_label="Difference in Score", y_axis_label="Percentage (%)", toolbar_location="right", title=f"HOME COURT ADVANTAGE")
    src = ColumnDataSource({'x': list(score_dif.index), 'y':score_dif['percent'].tolist(), 'bottom' : [0 for _ in range(len(score_dif.index))]})
    p.vbar('x', top='y',bottom='bottom', source=src, width = 0.6)

    score_dif_abs = pd.DataFrame(data.groupby(['Score_Difference_abs'])['shot_made'].sum())
    score_dif_abs['count'] = data.groupby(['Score_Difference_abs'])['shot_made'].count()
    score_dif_abs['percent'] = 100 * score_dif_abs['shot_made'] / score_dif_abs['count']
    score_dif_abs = score_dif_abs[score_dif_abs.index >= -40]
    score_dif_abs = score_dif_abs[score_dif_abs.index <= 40]

    w = figure(plot_width=1100, plot_height=750, y_range = (60, 85),
               tools=[BoxSelectTool(), BoxZoomTool(), ResetTool(), WheelZoomTool(), SaveTool(), PanTool()],
               x_axis_label="Difference in Score (abs)", y_axis_label="Percentage (%)", toolbar_location="right", title=f"HOME COURT ADVANTAGE")
    abs_src = ColumnDataSource({'x': list(score_dif_abs.index), 'y':score_dif_abs['percent'].tolist(), 'bottom' : [0 for _ in range(len(score_dif_abs.index))]})
    w.vbar('x', top='y',bottom='bottom', source=abs_src, width = 0.6)
    show(row([p,w]))


# df = consolidate_to_single_df()


pickle_in = open(path + "data.pickle","rb")
df = pickle.load(pickle_in)
# make_home_away_charts(df)
# position_matters(df)
score_thing(df)
print()
# def make_map(data):
#     # state_data = pd.DataFrame(data.groupby(['State'])['shot_made'].sum())
#     # bb = data.groupby(['State'])['shot_made'].count()
#     #
#     # state_data['count'] = bb
#     # state_data['percent'] = state_data['shot_made'] / state_data['count']
#     # print(state_data.sort_values('percent'))
#
#     city_data = pd.DataFrame(data.groupby(['City'])['shot_made'].sum())
#     city_data['count'] = data.groupby(['City'])['shot_made'].count()
#     city_data['percent'] = city_data['shot_made'] / city_data['count']
#
#     lat_ = []
#     lon_ = []
#     for x in city_data.itertuples():
#         for y in teamNames.itertuples():
#             if x.Index == y.City:
#                 lat_.append(y.Lat)
#                 lon_.append(y.Lon)
#                 break
#     city_data['lat'] = lat_
#     city_data['lon'] = lon_
#
#     top = np.array([city_data.at['Portland', 'percent'], city_data.at['Seattle', 'percent']])
#     midtop = np.array([city_data.at['San Fransisco', 'percent'], city_data.at['Denver', 'percent'],
#                        city_data.at['Sacramento', 'percent'], city_data.at['Indianapolis', 'percent'],
#                        city_data.at['Washington', 'percent'], city_data.at['Philadelphia', 'percent'],
#                        city_data.at['Salt Lake City', 'percent'], city_data.at['Jersey City', 'percent'],
#                        city_data.at['Brooklyn', 'percent'], city_data.at['New York', 'percent'],
#                        city_data.at['Toronto', 'percent'], city_data.at['Detroit', 'percent'], city_data.at['Boston', 'percent'],
#                        city_data.at['Chicago', 'percent'], city_data.at['Cleveland', 'percent'],
#                        city_data.at['Milwaukee', 'percent'], city_data.at['Minneapolis', 'percent']])
#     midlow = np.array([city_data.at['Phoenix', 'percent'], city_data.at['Charlotte', 'percent'],
#                        city_data.at['Atlanta', 'percent'], city_data.at['Oklahoma City', 'percent'],
#                        city_data.at['Memphis', 'percent'], city_data.at['Los Angeles', 'percent']])
#     bottom = np.array([city_data.at['Houston', 'percent'], city_data.at['Miami', 'percent'],
#                        city_data.at['Orlando', 'percent'], city_data.at['New Orleans', 'percent'],
#                        city_data.at['Dallas', 'percent'], city_data.at['San Antonio', 'percent']])
#
#     pacific = np.array([city_data.at['Seattle', 'percent'],city_data.at['Portland', 'percent'],
#                         city_data.at['Los Angeles', 'percent'],
#                         city_data.at['Sacramento', 'percent'],city_data.at['San Fransisco', 'percent'],])
#     mountain = np.array([city_data.at['Salt Lake City', 'percent'],city_data.at['Phoenix', 'percent'],city_data.at['Denver', 'percent'],])
#     central = np.array([city_data.at['Minneapolis', 'percent'],city_data.at['Memphis', 'percent'],
#                         city_data.at['Milwaukee', 'percent'],city_data.at['Chicago', 'percent'],
#                         city_data.at['San Antonio', 'percent'],city_data.at['Oklahoma City', 'percent'],
#                         city_data.at['Houston', 'percent'],city_data.at['New Orleans', 'percent'],city_data.at['Dallas', 'percent']])
#     eastern = np.array([city_data.at['Toronto', 'percent'],city_data.at['Indianapolis', 'percent'],city_data.at['Washington', 'percent'],
#                         city_data.at['Boston', 'percent'],city_data.at['Philadelphia', 'percent'],city_data.at['Charlotte', 'percent'],
#                         city_data.at['New York', 'percent'],city_data.at['Brooklyn', 'percent'],city_data.at['Atlanta', 'percent'],
#                         city_data.at['Jersey City', 'percent'],city_data.at['Cleveland', 'percent'],city_data.at['Orlando', 'percent'],
#                         city_data.at['Detroit', 'percent'], city_data.at['Miami', 'percent']])
#
#
#
#
#     fig = plt.figure()
#     m = Basemap(projection='lcc', resolution='l',
#                 lat_0=39.8333333, lon_0=-98.585522,
#                 width=5E6, height=3E6)
#     m.shadedrelief()
#     m.drawcoastlines(color='gray')
#     m.drawcountries(color='gray')
#     m.drawstates(color='gray')
#     m.scatter(city_data['lon'].values, city_data['lat'].values, latlon=True,
#               c=city_data['percent'],s=250,alpha = 0.8, cmap = 'YlOrRd')
#     plt.colorbar(label=r'Percentage (%)')
#     plt.tick_params(axis='y', labelsize=20)
#
#     fig2 = plt.figure()
#     m2 = Basemap(projection='lcc', resolution='l',
#                 lat_0=39.8333333, lon_0=-98.585522,
#                 width=5E6, height=3E6)
#     m2.shadedrelief()
#     m2.drawcoastlines(color='gray')
#     m2.drawcountries(color='gray')
#     m2.drawstates(color='gray')
#     plt.fill_between([0, 5000000], [3000000 * 0.75, 3000000 * 0.75], [3000000, 3000000], facecolor='blue', alpha=0.2,
#                      label='{:.1f}%'.format(100 * top.mean()))
#     plt.fill_between([0, 5000000], [3000000 / 2, 3000000 / 2], [3000000 * 0.75, 3000000 * 0.75], facecolor='yellow',
#                      alpha=0.2, label='{:.1f}%'.format(100 * midtop.mean()))
#     plt.fill_between([0, 5000000], [3000000 / 4, 3000000 / 4], [3000000 / 2, 3000000 / 2], facecolor='red', alpha=0.2,
#                      label='{:.1f}%'.format(100 * midlow.mean()))
#
#     plt.fill_between([0,5000000], [3000000/4,3000000/4],facecolor='green', alpha = 0.2, label = '{:.1f}%'.format(100*bottom.mean()))
#     m2.scatter(city_data['lon'].values, city_data['lat'].values, latlon=True, c='black', s=60)
#     plt.legend(loc = 'lower left')
#
#     fig3 = plt.figure()
#     m3 = Basemap(projection='lcc', resolution='l',
#                 lat_0=39.8333333, lon_0=-98.585522,
#                 width=5E6, height=3E6)
#     m3.shadedrelief()
#     m3.drawcoastlines(color='gray')
#     m3.drawcountries(color='gray')
#     m3.drawstates(color='gray')
#     plt.fill_between([0, (5000000/4)-50000],[0,0],[3000000,3000000], facecolor='blue', alpha=0.2,
#                      label='Pacific: {:.1f}%'.format(100 * pacific.mean()))
#     plt.fill_between([(5000000/4)-50000, (5000000/2)-50000],[0,0],[3000000,3000000], facecolor='yellow',
#                      alpha=0.2, label='Mountain: {:.1f}%'.format(100 * mountain.mean()))
#     plt.fill_between([(5000000/2)-50000, (5000000*0.75)-250000],[0,0],[3000000,3000000], facecolor='red', alpha=0.2,
#                      label='Central: {:.1f}%'.format(100 * central.mean()))
#     plt.fill_between([(5000000*0.75)-250000,5000000],[0,0],[3000000,3000000],facecolor='green', alpha = 0.2, label = 'Eastern: {:.1f}%'.format(100*eastern.mean()))
#
#     m3.scatter(city_data['lon'].values, city_data['lat'].values, latlon=True, c='black', s=60)
#     plt.legend(loc = 'lower left')
# # make_map(df)
# def salary_AND_best_worst(data):
#     salaries = pd.read_csv(path + 'salary data/playersalaries.csv')
#     salaries['Player'] = salaries['Player'].str.lower()
#     salaries['Player'] = pd.Series([x.replace('.', '').replace("'", '') for x in salaries.Player], index=salaries.index)
#
#     new = pd.DataFrame(data.groupby(['player']).agg({'shot_made':'sum'}))
#     new['attempts'] = data.groupby(['player']).agg({'shot_made': 'count'})
#     new['percent'] = new['shot_made']/new['attempts']
#     new['salary'] = salaries.groupby(['Player'])['AdjustedSalary'].mean()
#     new['salary'].fillna(80000, inplace=True)
#     new['salary'] = new['salary'].astype('int64')
#     new = new[new['attempts']>30]
#
#     worst_shooters = new.sort_values(by = 'percent').head(10)
#     fig1 = plt.figure()
#     ax1 = fig1.add_subplot(111)
#     ax1.barh([' '.join([x.split(' ')[0].capitalize(),x.split(' ')[1].capitalize()]) for x in worst_shooters.index], worst_shooters['percent'].values*100, color= '#f4ce42')
#     ax1.set(xlabel = 'Percentage (%)', ylabel = 'Player', xlim = [25, 50])
#     ax1.tick_params(axis='y', labelsize=15)
#     ax1.tick_params(axis='x', labelsize=14)
#     style = dict(size=18, color='darkgray')
#     for x in range(len(worst_shooters.index)):
#         ax1.text(100*worst_shooters['percent'][x]+1,x, 'Attempts: {}'.format(str(worst_shooters['attempts'][x])), **style)
#
#     best_shooters = new.sort_values(by = 'percent', ascending=False).head(12)
#     fig2 = plt.figure()
#     ax2 = fig2.add_subplot(111)
#     ax2.barh(np.flip([' '.join([x.split(' ')[0].capitalize(),x.split(' ')[1].capitalize()]) for x in best_shooters.index]), np.flip(best_shooters['percent'].values)*100, color= '#f4ce42')
#     ax2.set(xlabel = 'Percentage (%)', ylabel = 'Player', xlim = [85, 100])
#     ax2.tick_params(axis='y', labelsize=15)
#     ax2.tick_params(axis='x', labelsize=14)
#     for x in range(len(best_shooters.index)):
#         ax2.text(100*np.flip(best_shooters['percent'].values)[x]+1,x, 'Attempts: {}'.format(str(np.flip(best_shooters['attempts'].values)[x])), **style)
#
#     fig = plt.figure()
#     ax0 = fig.add_subplot(121)
#     ax02 = fig.add_subplot(122)
#     ax0.set(xlabel=r'Salary', ylabel='Percentage (%)', )
#     ax02.set(xlabel = r'$\log_{10}({\rm Salary})$', )
#     ax02.yaxis.set_ticks_position('none')
#     ax02.scatter(np.log10(new['salary'].values), new['percent'].values,  c = 'red', s = 10, alpha = 0.32)
#     ax0.scatter(new['salary'].values, new['percent'].values,  c = 'red', s = 10, alpha = 0.32)
# salary_AND_best_worst(df)
# def score_thing(data):
#     score_before = []
#     for x in data.itertuples():
#         if x.shot_made == 0:
#             score_before.append(x.score_after)
#         else:
#             cc = x.score_after
#             first_num = int(cc.split(' - ')[0])
#             second_num = int(cc.split(' - ')[1])
#             if x.Players_team == 'away':
#                 first_num-=1
#                 score_before.append('{} - {}'.format(first_num, second_num))
#             else:
#                 second_num-=1
#                 score_before.append('{} - {}'.format(first_num, second_num))
#
#     data['score_before'] = pd.Series(score_before, index = data.index)
#     data['Score_Difference_abs'] = pd.Series([np.abs(int(x.split('-')[0])-int(x.split('-')[1])) for x in data["score_before"]], index = data.index)
#     data['Score_Difference'] = pd.Series(
#         [int(x.split('-')[0]) - int(x.split('-')[1]) for x in data["score_before"]], index=data.index)
#
#     score_dif = pd.DataFrame(data.groupby(['Score_Difference'])['shot_made'].sum())
#     score_dif['count'] =data.groupby(['Score_Difference'])['shot_made'].count()
#     score_dif['percent'] = 100*score_dif['shot_made']/score_dif['count']
#     score_dif = score_dif[score_dif.index >= -40]
#     score_dif = score_dif[score_dif.index <= 40]
#     fig = plt.figure()
#     ax1= fig.add_subplot(111)
#     ax1.set(ylim = [60, 85], ylabel = 'Percentage (%)', xlabel = 'Difference in Score')
#     ax1.tick_params(axis = 'y', labelsize = 18)
#     ax1.tick_params(axis='x', labelsize=15)
#     ax1.bar(score_dif.index, score_dif.percent.values)
#
#     score_dif_abs = pd.DataFrame(data.groupby(['Score_Difference_abs'])['shot_made'].sum())
#     score_dif_abs['count'] =data.groupby(['Score_Difference_abs'])['shot_made'].count()
#     score_dif_abs['percent'] = 100*score_dif_abs['shot_made']/score_dif_abs['count']
#     score_dif_abs = score_dif_abs[score_dif_abs.index >= -40]
#     score_dif_abs = score_dif_abs[score_dif_abs.index <= 40]
#     fig2 = plt.figure()
#     ax2= fig2.add_subplot(111)
#     ax2.set(ylim = [60, 85], ylabel = 'Percentage (%)',xlabel = 'Difference in Score (abs)')
#     ax2.tick_params(axis='y', labelsize=18)
#     ax2.tick_params(axis='x', labelsize=15)
#     ax2.bar(score_dif_abs.index, score_dif_abs.percent.values)
# score_thing(df)
# def time_charts(data):
#     period_df = pd.DataFrame(data.groupby(['period'])['shot_made'].sum())
#     period_df['count'] =data.groupby(['period'])['shot_made'].count()
#     period_df['percent'] = 100*period_df['shot_made']/period_df['count']
#
#     fig1 = plt.figure()
#     ax1 = fig1.add_subplot(111)
#     ax1.bar(period_df.index, period_df.percent)
#     ax1.set(ylim = [60, 85], ylabel = 'Percentage (%)', xlabel = 'Period', xticklabels =  ['','Q1','Q2','Q3','Q4','OT','2OT','3OT','4OT',])
#     ax1.plot([period_df.index.min(), period_df.index.max()], [period_df.percent.min(),period_df.percent.max()], c = 'orange', linewidth = 6,linestyle='--')
#     ax1.tick_params(axis='both',which = 'both', labelsize=16)
#     t_o_g = []
#     for x in df.itertuples():
#         p = int(x.time.split(':')[0])
#         if x.period == float(1):
#             p = p + 36
#         elif x.period == float(2):
#             p = p+24
#         elif x.period == float(3):
#             p = p+12
#         else:
#             p = p
#         t_o_g.append('{}'.format(p))
#     df['time_of_game'] = pd.Series(t_o_g, index = df.index)
#     time_of_game = pd.DataFrame(df.groupby(['time_of_game'])['shot_made'].sum())
#     time_of_game['attempts'] = df.groupby(['time_of_game'])['shot_made'].count()
#     time_of_game['percent'] = 100* time_of_game['shot_made'] / time_of_game['attempts']
#     time_of_game.index = time_of_game.index.astype(int)
#
#     fig2 = plt.figure()
#     ax2 = fig2.add_subplot(111)
#     ax2.bar(time_of_game.sort_index(ascending = False).index, time_of_game.sort_index()['percent'].values)
#     ax2.bar([0, 12, 24, 36], [time_of_game.sort_index(ascending = False)['percent'].values[y] for y in [0, 12, 24, 36]])
#     ax2.tick_params(axis = 'x', which = 'both', labelsize=12)
#     ax2.set(ylim= [60,85],xticks= [x for x in range(48)],xticklabels = [x for x in range(48)][::1],ylabel = 'Percentage (%)', xlabel = 'Minute of Game ')
#     ax2.tick_params(axis='y', labelsize=16)
# time_charts(df)
# improving_ft(df)


