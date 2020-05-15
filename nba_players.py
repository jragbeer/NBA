import pandas as pd
import numpy as np
import sqlite3
import datetime
import time
from datetime import timezone
from bokeh.plotting import figure, show, gmap
from bokeh.models import BasicTickFormatter, HoverTool, BoxSelectTool, BoxZoomTool, ResetTool, Span, OpenURL,FixedTicker, CustomJS, DatetimeTickFormatter, GMapOptions, LinearColorMapper, LabelSet
from bokeh.models import NumeralTickFormatter, WheelZoomTool, PanTool, SaveTool, ColumnDataSource, LinearAxis, Range1d, FuncTickFormatter,DataRange1d , Band, SingleIntervalTicker
from bokeh.models.widgets import Select, RadioGroup, DataTable, StringFormatter, TableColumn, NumberFormatter, Button, CheckboxGroup, Div,  CheckboxButtonGroup
from bokeh.layouts import widgetbox, row, column, gridplot, layout
from bokeh.io import curdoc
from bokeh.palettes import Purples, BuPu, OrRd, viridis
import webbrowser
from dateutil import parser
from os.path import dirname, join
import os
import re
from bokeh.models.glyphs import ImageURL
from bokeh.models.renderers import GlyphRenderer
from bokeh.core.properties import Instance, String
from bokeh.transform import transform, linear_cmap

doc = curdoc()
doc.title = 'NBA Stats'
#clears the html page and gives the tab a name
doc.clear()

def remove_glyphs(figure, glyph_name_list):
    a = [x for x in ts.renderers]
    print(a)
    for r in a:
        if r.name in glyph_name_list:
            col = r.glyph.y
            r.data_source.data[col] = [np.nan] * len(r.data_source.data[col])
def makediv(df, teams):
    text = '''<br><font color="#113672" size = "2"><b>Player: </b></font><br><br>
    <font color="#e82751" size = "4"><b>{}</b></font><br><br>
    <font color="#113672" size = "2"><b>Teams played on: </b></font><br><br>
    <font color="#e82751" size = "3"><b>{}</b></font><br><br>
    <font color="#113672" size = "2"><b>Games Played: </b></font>
    <font color="#e82751" size = "4"><b>{:d}</b></font><br><br>
    <font color="#113672" size = "2"><b>Years Active: </b></font>
    <font color="#e82751" size = "4"><b>{:d}</b></font><font color="#e82751" size = "3"><b>  ({:d}-{:d})</b></font><br><br>
    <font color="#113672" size = "2"><b>Career Average PPG: </b></font>
    <font color="#e82751" size = "4"><b>{:.1f}</b></font><br><br>
    <font color="#113672" size = "2"><b>Career Average APG: </b></font>
    <font color="#e82751" size = "4"><b>{:.1f}</b></font><br><br>
    <font color="#113672" size = "2"><b>Career Average RPG: </b></font>
    <font color="#e82751" size = "4"><b>{:.1f}</b></font>'''.format(
        selectplayer.value, ', '.join(teams), int(df['G'].sum()), int(len(df['G'])),df.index.levels[1].values[0],df.index.levels[1].values[-1], df['ptsavg'].mean(), df['astavg'].mean(), df['rebavg'].mean())
    return text
def player_stats(df, name):
    player = df[df['Player'] == str(name)].copy()
    return player
def cleanplayer(df, player):
    aa = player_stats(df, player)
    cc = pd.DataFrame(aa.groupby(['Player', 'Year']).agg({'TRB':'sum', 'AST':'sum', 'PTS':'sum', 'G':'sum', 'DRB':'sum',
                                                          'ORB':'sum','FTA':'sum','FT':'sum','FGA':'sum','FG':'sum',
                                                          '3PA':'sum','3P':'sum', 'PER':'mean', 'STL': 'sum', 'BLK':'sum'}))

    for x in cc.index:
        if cc['G'][x] > 82:
            cc.at[x, 'G'] = cc.at[x, 'G'] / 2
            cc.at[x, 'PTS'] = cc.at[x, 'PTS'] / 2
            cc.at[x, 'AST'] = cc.at[x, 'AST'] / 2
            cc.at[x, 'TRB'] = cc.at[x, 'TRB'] / 2
            cc.at[x, 'ORB'] = cc.at[x, 'ORB'] / 2
            cc.at[x, 'DRB'] = cc.at[x, 'DRB'] / 2

    cc.G = cc['G'].astype('int')
    cc.PTS = cc['PTS'].astype('int')
    cc.AST = cc['AST'].astype('int')
    cc.TRB = cc['TRB'].astype('int')
    cc.ORB = cc['ORB'].astype('int')
    cc.DRB = cc['DRB'].astype('int')
    cc.STL = cc['STL'].astype('int')
    cc.BLK = cc['BLK'].astype('int')
    cc['ppg'] = cc['PTS'] / cc['G']
    cc['rpg'] = cc['TRB'] / cc['G']
    cc['drpg'] = cc['DRB'] / cc['G']
    cc['orpg'] = cc['ORB'] / cc['G']
    cc['apg'] = cc['AST'] / cc['G']
    cc['blkavg'] = cc['BLK'] / cc['G']
    cc['stlavg'] = cc['STL'] / cc['G']
    cc['rebavg'] = cc['TRB'].sum() / cc['G'].sum()
    cc['ptsavg'] = cc['PTS'].sum() / cc['G'].sum()
    cc['astavg'] = cc['AST'].sum() / cc['G'].sum()
    cc['orbavg'] = cc['ORB'].sum() / cc['G'].sum()
    cc['drbavg'] = cc['DRB'].sum() / cc['G'].sum()


    return cc
def updateplayer(attr, old, new):
    teamlistp = [list(y) for x in player_stats(data, str(new))['Tm'].unique() for y in teamNames.itertuples() if
                x == y[0] and x != 'TOT']
    try:
        teamlistp.remove('Multiple Teams in a season')
    except:
        pass
    update(data, str(new), teamlistp)
def update(data_, new_, teamlistp):
    global imageglyph
    global ts_span

    new_selected_player_df = cleanplayer(data_, str(new_))

    yearsp = [x1[1] for x1 in new_selected_player_df.index.values]
    rpgp = new_selected_player_df['rpg']
    drpgp = new_selected_player_df['drpg']
    orpgp = new_selected_player_df['orpg']
    apgp = new_selected_player_df['apg']
    astavgp = new_selected_player_df['astavg']
    rebavgp = new_selected_player_df['rebavg']
    ptsavgp = new_selected_player_df['ptsavg']
    orbavgp = new_selected_player_df['orbavg']
    drbavgp = new_selected_player_df['drbavg']

    peravgp = [new_selected_player_df['PER'].sum() / len(yearsp) for y in range(len(yearsp))]

    # player_ftap = new_selected_player_df['FTA'].sum()
    # player_ftp = new_selected_player_df['FT'].sum()
    # player_career_ftavgp = player_ftp / player_ftap
    #
    # player_3pap = new_selected_player_df['3PA'].sum()
    # player_3pp = new_selected_player_df['3P'].sum()
    # player_career_3pavgp = player_3pp / player_3pap
    #
    # player_2pap = new_selected_player_df['2PA'].sum()
    # player_2pp = new_selected_player_df['2P'].sum()
    # player_career_2pavgp = player_2pp / player_2pap
    first_year = new_selected_player_df.index.levels[1].min()
    last_year = new_selected_player_df.index.levels[1].max()
    all_blockp, all_stealp = defense_scatter_all(data_, first_year, last_year)
    htmap3p = new_selected_player_df['3P'].sum() / new_selected_player_df['3PA'].sum()
    htmapftp = new_selected_player_df['FT'].sum() / new_selected_player_df['FTA'].sum()
    htmapfgp = new_selected_player_df['FG'].sum() / new_selected_player_df['FGA'].sum()
    make_heatmap(htmapfgp, htmapftp, htmap3p)
    z.y_range.end = apgp.max() + 1
    i.y_range.start = yearsp[0] - 1
    i.y_range.end = yearsp[-1] + 1
    win_shares_source.data= dict(win_shares_all(data_, first_year, last_year, new_).data)

    current_player_tsp, ts_playersp, ts_percentp = true_shooting(str(new_), data, first_year, last_year)
    ts_span.location=current_player_tsp * 0.01

    all_nba_ptsp, all_nba_astsp, all_nba_rebsp, all_nba_perp = all_nba_avg_lines(data_, first_year, last_year)

    sourceppg.data = dict(x=yearsp, y=new_selected_player_df['ppg'], avg=ptsavgp, nbaavg=all_nba_ptsp,
                                                label_avg=[ptsavgp[0], all_nba_ptsp[0]] + [0 for x in
                                                                                           range(len(yearsp) - 2)],
                                                names=['Player Avg', 'NBA Avg'] + ['' for x in
                                                                                   range(len(yearsp) - 2)],
                                                label_spots=[yearsp[0], yearsp[0]] + [yearsp[0] for x in
                                                                                     range(len(yearsp) - 2)])

    map_figure_source.data = dict(lat=[x[3] for x in teamlistp], lon=[x[4] for x in teamlistp],
                  city=[x[2] for x in teamlistp])
    sourceper.data = dict(x=yearsp, a=new_selected_player_df['PER'], avg=peravgp, nbaavg=all_nba_perp,
                                                label_avg=[peravgp[0], all_nba_perp[0]] + [0 for x in range(len(yearsp) - 2)],
                                                names=['Player Avg', 'NBA Avg'] + ['' for x in
                                                                                   range(len(yearsp) - 2)],
                                                label_spots=[yearsp[0], yearsp[0]] + [yearsp[0] for x in
                                                                                      range(len(yearsp) - 2)])
    sourcerpg.data = dict(x=yearsp, o=orpgp, d=drpgp, t=rpgp, avgt=rebavgp, avgo=orbavgp, avgd=drbavgp,
                  nbaavg=all_nba_rebsp,
                  label_avg=[rebavgp[0], all_nba_rebsp[0]] + [0 for x in range(len(yearsp) - 2)],
                  names=['Player Avg', 'NBA Avg'] + ['' for x in range(len(yearsp) - 2)],
                  label_spots=[yearsp[0], yearsp[0]] + [yearsp[0] for x in range(len(yearsp) - 2)])
    sourceapg.data = dict(x=yearsp, a=apgp, avg=astavgp, nbaavg=all_nba_astsp,
                                                label_avg=[astavgp[0], all_nba_astsp[0]] + [0 for x in
                                                                                            range(len(yearsp) - 2)],
                                                names=['Player Avg', 'NBA Avg'] + ['' for x in
                                                                                   range(len(yearsp) - 2)],
                                                label_spots=[yearsp[0], yearsp[0]] + [yearsp[0] for x in
                                                                                      range(len(yearsp) - 2)])

    stlavgp = new_selected_player_df['STL'].sum() / new_selected_player_df['G'].sum()
    blkavgp = new_selected_player_df['BLK'].sum() / new_selected_player_df['G'].sum()

    defenseallsource.data = dict(ColumnDataSource(
        data=dict(stl=all_stealp, blk=all_blockp, color=['blue'] * len(all_blockp))).data)
    defenseplayersource.data = dict(ColumnDataSource(data=dict(stl=[stlavgp], blk=[blkavgp], color=['firebrick'])).data)

    imageglyph.visible = False
    name_to_use = new_.lower().replace(' ', '_')
    name = f"{name_to_use}.png"
    if name in list_of_images:
        imageglyph = img.image_url(url=['nba/static/images/{}.png'.format(name_to_use)], x=0, y=0,
                                   w=369, h=834, anchor="bottom_left")
    else:
        imageglyph = img.image_url(url=['nba/static/images/nbalogo.png'],
                                   x=100,
                                   y=0, w=180, h=700, anchor="bottom_left")
    div.text = makediv(new_selected_player_df, [x[1] for x in teamlistp])
def updateteam(attr, old, new):
    if str(new) == 'All':
        selectplayer.options = ['All'] + sorted(sorted(list(data['Player'].unique())))
    else:
        selectplayer.options =  ['All']+sorted(newteamsDict[str(new)])
def cleandf(df):
    df.fillna(0, inplace=True)
    df.drop_duplicates(inplace=True)
    df.drop('Unnamed: 0', 1, inplace=True)
    df.Year = df.Year.astype('int')
    df.Age = df.Age.astype('int')
    df.G = df.G.astype('int')
    df.GS = df.GS.astype('int')


    df['ppg'] = df['PTS'] / df['G']
    df['rpg'] = df['TRB'] / df['G']
    df['drpg'] = df['DRB'] / df['G']
    df['orpg'] = df['ORB'] / df['G']
    df['apg'] = df['AST'] / df['G']

    df['Player'] = pd.Series([str(x).replace('*', '') for x in df['Player']], index=df.index)
    return df
def sorting(dict1, tick=1):
    xx=[]
    yy=[]
    aq = sorted(dict1, key = dict1.get, reverse=True)
    for prop in aq:
        xx.append(prop)
        yy.append(dict1[prop])
    if tick == 1:
        yy = [y for y in yy if y > 0]
    xx = xx[:len(yy)]
    return xx, yy
def update_avg_line(new):
    # Points avg lines
    if 0 in button_group.active:
        avglinep.visible = True
        nba_avglinep.visible = True
        labels_ppg.visible = True
    else:
        avglinep.visible = False
        labels_ppg.visible = False
        nba_avglinep.visible = False

    # total rebounds avg lines
    if 1 in button_group.active:
        avglinewt.visible = True
        nba_avglinewt.visible = True
        labels_rpg.visible = True
    else:
        avglinewt.visible = False
        nba_avglinewt.visible = False
        labels_rpg.visible = False

    # assists avg lines
    if 2 in button_group.active:
        avglinez.visible = True
        nba_avglinez.visible = True
        labels_apg.visible = True
    else:
        avglinez.visible = False
        nba_avglinez.visible = False
        labels_apg.visible = False

    # PER avg lines
    if 3 in button_group.active:
        avglinei.visible = True
        nba_avglinei.visible = True
        labels_per.visible = True
    else:
        avglinei.visible = False
        labels_per.visible = False
        nba_avglinei.visible = False
def make_heatmap(fg, ft, from3):
    fg = fg*100
    ft = ft*100
    from3 = from3*100
    hmapsqsource.data = dict(x=[-1], y=[0], z=[6], i=[2], color=['red'], area=['3P'], num = np.array([from3]))
    hmapellipsesource.data = dict(x=[1], y=[0], z=[7], i=[1.55], color=['red'], area=['2P'], num = np.array([fg]))
    hmaprectsource.data = dict(x=[0], y=[0], z=[2], i=[0.85], color=['red'], area=['2P'], num = np.array([fg]))
    hmapwedgesource.data = dict(x=[-1], y=[0], z=[0.98], i=np.array([3 * np.pi / 2]), u=np.array([np.pi / 2]), color=['red'], area=['FT'], num = np.array([ft]))
def defense_scatter_all(inputdf, year1, year2):
    df = inputdf.copy()
    df = df[(df['Year'] >= year1) & (df['Year'] <= year2)]

    each_player_stl = df.groupby(['Player'])['STL'].sum()
    each_player_blk = df.groupby(['Player'])['BLK'].sum()
    each_player_g = df.groupby(['Player'])['G'].sum()

    all_blks = []
    all_stls = []
    for x in each_player_blk.index:
        all_blks.append(each_player_blk[x]/each_player_g[x])
        all_stls.append(each_player_stl[x]/each_player_g[x])
    return all_blks, all_stls
def all_nba_avg_lines(inputdf, year1, year2):
    df = inputdf.copy()
    df = df[(df['Year'] >= year1) & (df['Year'] <= year2)]

    each_player_assists = df.groupby(['Year'])['AST'].sum()
    each_player_points = df.groupby(['Year'])['PTS'].sum()
    each_player_rebounds = df.groupby(['Year'])['TRB'].sum()
    each_player_per = df.groupby(['Year'])['PER'].sum()
    each_player_g = df.groupby(['Year'])['G'].sum()

    all_per = [each_player_per[x]/len(df.Player.unique()) for x in each_player_assists.index]
    all_pts = [each_player_points[x]/each_player_g[x] for x in each_player_assists.index]
    all_asts = [each_player_assists[x]/each_player_g[x] for x in each_player_assists.index]
    all_rebs = [each_player_rebounds[x]/each_player_g[x] for x in each_player_assists.index]
    return all_pts, all_asts, all_rebs, all_per
def win_shares_all(inputdf, year1, year2, player):
    df = inputdf.copy()
    df = df[(df['Year'] >= year1) & (df['Year'] <= year2)]
    each_player_ws = df.groupby(['Player']).agg({'OWS':'sum', 'DWS':'sum', 'WS':'sum'})
    q1 = each_player_ws.quantile(q=0.25)
    q2 = each_player_ws.quantile(q=0.5)
    q3 = each_player_ws.quantile(q=0.75)
    iqr = q3 - q1
    upper = q3 + 1.5 * iqr
    lower = q1 - 1.5 * iqr
    def outliers(group):
        cat = group.index
        return group[(group.WS > pd.DataFrame(upper.loc[cat])['WS']) | (group.WS < pd.DataFrame(lower.loc[cat])['WS'])]
    outx = [1,2,3]
    outy = [1,2,3]
    player_ws_span = each_player_ws.loc[str(player)]

    win_shares_source_all = ColumnDataSource(data=(
        dict(cats=['OWS','WS','DWS'],x0=[0.15,1.15,2.15], y0 =[player_ws_span.OWS, player_ws_span.WS, player_ws_span.DWS] ,upper=np.round([upper.OWS, upper.WS, upper.DWS],1), lower=np.round([lower.OWS, lower.WS, lower.DWS],1), q1=np.round([q1.OWS, q1.WS, q1.DWS],1), q2=np.round([q2.OWS, q2.WS, q2.DWS],1), color = ['black']*3,q3=np.round([q3.OWS, q3.WS, q3.DWS],1),
             outlier_x=outx, outlier_y=outy,length = [15]*3,y1 = [player_ws_span.OWS, player_ws_span.WS, player_ws_span.DWS] ,x1 = [0.85,1.85,2.85],ray_color = ["#f16913"]*3, ray_angles= ['deg']*3,top=[0.7, 0.7, 0.7], width = [0.2, 0.2, 0.2], height = [0.01, 0.01, 0.01])))
    return win_shares_source_all
def true_shooting(player_name, inputdf, year1, year2):
    def formula(pts, fga, fta):
        try:
            return 100*pts/(2*(fga + (0.44*fta)))
        except:
            return 0.1

    df = inputdf.copy()
    df = df[(df['Year'] >= year1) & (df['Year'] <= year2)]
    each_player = pd.DataFrame(df.groupby(['Player']).agg({'FGA': 'sum', 'PTS':'sum',"FTA":'sum'}))
    each_player = each_player[(each_player['FGA'] > 20) & (each_player['FTA'] > 20)]

    ts = [formula(x.PTS, x.FGA, x.FTA) for x in each_player.itertuples()]
    return formula(each_player.at[player_name, 'PTS'],each_player.at[player_name, 'FGA'],each_player.at[player_name, 'FTA']), each_player, ts

lat = 40.391975
lon = -97.685789
OrRd = OrRd[9][:6]
first_player = 'Kevin Durant'
path = 'C:/Users/Julien/PycharmProjects/nba/static/'

data = pd.read_csv(path + 'Seasons_Stats.csv')
data = cleandf(data)
list_of_images = os.listdir(path + '/images/')

teams = list(data['Tm'].unique())
teams.remove(0)

teamsDict = {t: set([y[2] for y in data.itertuples() if y[5]==t]) for t in teams}
teamNames = pd.read_csv(path + 'teams.csv', index_col='Abbrev')

newteamsDict = {teamNames.at[t, 'Name'] :teamsDict[t] for t in teamsDict}

teamabbrevdict = {teamNames.index[x]:str(teamNames.values[x][0].strip()) for x in range(len(teamNames))}
teamlist = [list(y) for x in player_stats(data, first_player)['Tm'].unique() for y in teamNames.itertuples() if x == y[0] and x != 'TOT']

selected_player_df = cleanplayer(data, first_player)
player_first_year = selected_player_df.index.levels[1].min()
player_last_year = selected_player_df.index.levels[1].max()
player_years = [x[1] for x in selected_player_df.index.values]
player_ppg = selected_player_df['ppg']
tot_reb = selected_player_df['rpg']
def_reb = selected_player_df['drpg']
off_reb = selected_player_df['orpg']
player_asts = selected_player_df['apg']
player_per = selected_player_df['PER']
peravg = [selected_player_df['PER'].sum()/len(player_years) for y in range(len(player_years))]
rebavg = selected_player_df['rebavg']
ptsavg = selected_player_df['ptsavg']
astavg = selected_player_df['astavg']
orbavg = selected_player_df['orbavg']
drbavg = selected_player_df['drbavg']
stlavg = selected_player_df['STL'].sum()/selected_player_df['G'].sum()
blkavg = selected_player_df['BLK'].sum()/selected_player_df['G'].sum()

#BOKEH

# This custom extension model will have a DOM view that should layout-able in
# Bokeh layouts, so use ``LayoutDOM`` as the base class. If you wanted to create
# a custom tool, you could inherit from ``Tool``, or from ``Glyph`` if you
# wanted to create a custom glyph, etc.
# class Surface3d(LayoutDOM):
#
#     # The special class attribute ``__implementation__`` should contain a string
#     # of JavaScript (or CoffeeScript) code that implements the JavaScript side
#     # of the custom extension model.
#     __implementation__ = JS_CODE
#     # Below are all the "properties" for this model. Bokeh properties are
#     # class attributes that define the fields (and their types) that can be
#     # communicated automatically between Python and the browser. Properties
#     # also support type validation. More information about properties in
#     # can be found here:
#     #
#     #    https://bokeh.pydata.org/en/latest/docs/reference/core.html#bokeh-core-properties
#
#     # This is a Bokeh ColumnDataSource that can be updated in the Bokeh
#     # server by Python code
#     data_source = Instance(ColumnDataSource)
#     # The vis.js library that we are wrapping expects data for x, y, z, and
#     # color. The data will actually be stored in the ColumnDataSource, but
#     # these properties let us specify the *name* of the column that should
#     # be used for each field.
#     x = String
#     y = String
#     z = String
#     extra = String
#     color = String
#
# X_data = np.random.normal(0,10,100)
# Y_data = np.random.normal(0,5,100)
# Z_data = np.random.normal(0,3,100)
# color = np.asarray([0 for x in range(50)]+[1 for x in range(50)])
# extra = np.asarray(['a' for x in range(50)]+['b' for x in range(50)])
# source200 = ColumnDataSource(data=dict(x=X_data, y=Y_data, z=Z_data, color = color, extra=extra))
# surface = Surface3d(x="x", y="y", z="z", extra="extra", color="color", data_source=source200)
selectplayer = Select(title='Player:', value='Kevin Durant', options=sorted(list(data['Player'].unique())))
selectplayer.on_change('value', updateplayer)

selectteam = Select(title='Use This To Filter *Player* By Team:', value='All', options=list(['All'] + sorted(list(newteamsDict.keys())))+['All'])
selectteam.on_change('value', updateteam)

download_source = ColumnDataSource(player_stats(data, str(selectplayer.value)))

hoverline = HoverTool(tooltips=[
    ("Year", "@x{0}"),
    ("PPG", "@y{(0.0)}"), ])
hoverline2 = HoverTool(tooltips=[
    ("Year", "@x{0}"),
    ("REB", "@t{(0.0)}"),("DREB", "@d{(0.0)}"),("OREB", "@o{(0.0)}")])
hoverstackedbar = HoverTool(tooltips=[
    ("Year", "@x{0}"),
    ("APG", "@a{(0.0)}"), ])
hoverbar = HoverTool(tooltips=[
    ("Year", "@x{0}"),
    ("PER", "@a{(0.0)}"), ])
hoverheatmap = HoverTool(tooltips=[
    ("Area", "@area"),
    ("Shot (%)", "@num{(0.0)}"), ])
hovermap = HoverTool(tooltips=[
    ("City", "@city"),])
hoverdefense = HoverTool(tooltips=[
    ("Steals", "@stl"),
("Blocks", "@blk")])
hoverws = HoverTool(names = ["q1_q2_block", "q2_q3_block"],tooltips=[
    ("Maximum", "@upper"), ('Q3', "@q3"), ('Q1', "@q1"),('Minimum', "@lower")])
hoverws_player = HoverTool(names = ["win_share_lines"], tooltips=[
    ("WS", "@y1")])

p = figure(plot_width=930, plot_height=250,
           tools=[hoverline, BoxSelectTool(), BoxZoomTool(), ResetTool(), WheelZoomTool(), SaveTool(), PanTool()],
           title="Average Points per Game",x_axis_type=None,y_axis_label="Points (ppg)", toolbar_location="right")
w = figure(plot_width=930, plot_height=250,
           tools=[hoverline2, BoxSelectTool(), BoxZoomTool(), ResetTool(), WheelZoomTool(), SaveTool(), PanTool()],
           title="Average Rebounds per Game",x_axis_type=None, y_axis_label="Rebounds (rpg)", toolbar_location="right")
z = figure(plot_width=930, plot_height=250,
           tools=[hoverstackedbar, BoxSelectTool(), BoxZoomTool(), ResetTool(), WheelZoomTool(), SaveTool(), PanTool()],
           title="Average Assits per Game", x_axis_type=None, y_axis_label="Assists (apg)", toolbar_location="right")
i = figure(plot_width=930, plot_height=200,
           tools=[hoverbar, BoxSelectTool(), BoxZoomTool(), ResetTool(), WheelZoomTool(), SaveTool(), PanTool()],
           title="PER per season",x_axis_type=None, y_axis_label="Player Efficiency Rating", toolbar_location="right")
try:
    htmap3 = selected_player_df['3P'].sum()/selected_player_df['3PA'].sum()
except:
    htmap3 = 0
try:
    htmapft = selected_player_df['FT'].sum()/selected_player_df['FTA'].sum()
except:
    htmapft = 0
try:
    htmapfg = selected_player_df['FG'].sum()/selected_player_df['FGA'].sum()
except:
    htmapfg = 0

hmapsqsource = ColumnDataSource(data=(dict(x=[-1], y=[0], z=[6], i =[2], color=['red'], area = ['3P'], num = [htmap3*100])))
hmapellipsesource = ColumnDataSource(data=(dict(x=[1], y=[0], z=[7], i =[1.55], color=['firebrick'], area = ['2P'], num = [htmapfg*100])))
hmaprectsource = ColumnDataSource(data=(dict(x=[0], y=[0], z=[2], i =[0.85], color=['firebrick'], area = ['2P'], num = [htmapfg*100])))
hmapwedgesource = ColumnDataSource(data=(dict(x=[-1], y=[0], z=[0.98], i =[3*np.pi/2], u = [np.pi/2],color=['red'], area = ['FT'], num = [htmapft*100])))

heatmap = figure(plot_width=350, plot_height=300,
           tools=[hoverheatmap],title="Career Shooting Heatmap", x_axis_location=None, y_axis_location=None,toolbar_location="right")

hmapsq = heatmap.rect('x','y','z','i', color=linear_cmap('num', OrRd, 0, 45), line_color='color', source = hmapsqsource)
hmapellipse = heatmap.ellipse('x','y','z','i', color=linear_cmap('num', OrRd, 0, 60), line_color='black', source = hmapellipsesource, )
hmaprect = heatmap.rect('x','y','z','i', color=linear_cmap('num', OrRd, 0, 60), line_color='black', source = hmaprectsource)
hmapwedge = heatmap.wedge(x='x', y='y', radius='z', start_angle='i', end_angle='u',
        color=linear_cmap('num', OrRd, 0, 90),  direction="clock",line_color='black', source = hmapwedgesource)
heatmap.x_range.end=1
heatmap.x_range.start=-5
heatmap.grid.visible = False
heatmap.outline_line_color = None

key = 'AIzaSyDDAzir5vZuZ0Z-dkCLOp3rIq5l74KLJWo'

map_options = GMapOptions(lat=lat, lng=lon, map_type="roadmap", zoom=3)
map_figure = gmap(key, map_options, title="Career Stops", width = 475, height = 350)
# map_figure = figure(plot_width=475, plot_height=350,
#            tools=[hovermap],
#            title="Map", x_axis_location=None, y_axis_location=None,toolbar_location="right")
map_figure_source = ColumnDataSource(data=dict(lat=[x[3] for x in teamlist],lon=[x[4] for x in teamlist], city = [x[2] for x in teamlist]))
map_figure.circle(x="lon", y="lat", size=12, fill_color="#c157f2", fill_alpha=0.8, source=map_figure_source)
map_figure.axis.visible = False
map_figure.add_tools(hovermap)

defense_scatter = figure(plot_width=300, plot_height=300,
           tools=[hoverdefense, BoxSelectTool(), BoxZoomTool(), ResetTool(), WheelZoomTool(), SaveTool(), PanTool()],
           title="Career Defensive Averages",toolbar_location="right", y_axis_label="Blocks (bpg)", x_axis_label="Steals (spg)")

win_shares = figure(plot_width=620, plot_height=300,x_range=['OWS','WS','DWS'],
           tools=[hoverws,hoverws_player, BoxSelectTool(), BoxZoomTool(), ResetTool(), WheelZoomTool(), SaveTool(), PanTool()],
           title="Career Win Shares",toolbar_location="right", y_axis_label="Career Win Shares (WS)")
win_shares_source= win_shares_all(data, player_first_year, player_last_year, first_player)
# stems
q3_upper_segment = win_shares.segment("cats", "upper", "cats", "q3", line_color="color", source = win_shares_source, name = 'q3_upper_segment')
q1_lower_segment = win_shares.segment("cats", "lower", "cats", "q1", line_color="color", source = win_shares_source, name = 'q1_lower_segment')
# boxes
q2_q3_block = win_shares.vbar("cats", "top", "q2", "q3", line_color="color", source = win_shares_source, fill_color = '#a30693', alpha = 0.4, name = 'q2_q3_block')
q1_q2_block = win_shares.vbar("cats", "top", "q1", "q2", line_color="color", source = win_shares_source, fill_color= '#568ce2', name = 'q1_q2_block')
# whiskers (almost-0 height rects simpler than segments)
bottom_whisker = win_shares.rect("cats", "lower", "width", "height", line_color="color", source = win_shares_source, name = 'bottom_whisker')
top_whisker = win_shares.rect("cats", "upper", "width", "height", line_color="color", source = win_shares_source, name = 'top_whisker')
win_share_lines = win_shares.segment(x0='x0', y0='y0',y1='y1', x1='x1', color="ray_color", line_width=5, line_alpha = 0.7, source = win_shares_source, name = 'win_share_lines')

current_player_ts, ts_players, ts_percent = true_shooting(first_player, data, player_first_year, player_last_year)
ts_max = max(ts_percent)*0.01
true_shooting_source = ColumnDataSource(data = dict(x = [0.25],y = [0],cur_player=[current_player_ts],  ts=[np.linspace(0,ts_max,100).reshape(100,1)], dw = [0.5], dh = [ts_max-0]))
ts = figure(plot_width=150, plot_height=350,x_range=[0, 1],x_axis_location=None, y_range=[0, ts_max],min_border_right=10, title = 'Career TS%', tools = [])
ts.image(image='ts',x='x',y='y',dw='dw',dh='dh', palette=viridis(100)[:50], source = true_shooting_source)
ts_span = Span(location=current_player_ts*0.01, dimension='width', line_color='#f16913', line_dash='solid', line_width=5, line_alpha=0.7, name = 'ts_span')
ts.add_layout(ts_span)
ts.xaxis.major_label_text_color = None
ts.xaxis.major_tick_line_color = None
ts.xaxis.minor_tick_line_color = None
ts.yaxis[0].ticker=FixedTicker(ticks=(np.linspace(0,ts_max,11))) # 11 ticks
ts.grid.visible = False
ts.outline_line_color = None

all_block, all_steal = defense_scatter_all(data, player_first_year, player_last_year)
defenseallsource = ColumnDataSource(data = dict(stl=all_steal , blk=all_block, color = ['blue']*len(all_block)))
defenseplayersource = ColumnDataSource(data = dict(stl=[stlavg] , blk=[blkavg], color = ['#c157f2']))
defense_scatter.circle(x='stl', y='blk', fill_color = 'color', size = 4, source = defenseallsource, alpha = 0.15)
defense_scatter.circle(x='stl', y='blk', fill_color = 'color', size = 10, source = defenseplayersource, alpha = 0.85)

all_nba_pts, all_nba_asts, all_nba_rebs, all_nba_per = all_nba_avg_lines(data, player_first_year, player_last_year)

color_mapper = LinearColorMapper(palette=Purples[9][::-1][3:], low=min(player_per), high=max(player_per))

sourceppg = ColumnDataSource(data = dict(x=player_years, y=player_ppg, avg = ptsavg, nbaavg = all_nba_pts, label_avg = [ptsavg[0], all_nba_pts[0]]+[0 for x in range(len(player_years)-2)], names = ['Player Avg', 'NBA Avg'] + ['' for x in range(len(player_years)-2)], label_spots = [player_years[0],player_years[0]]+ [player_years[0] for x in range(len(player_years)-2)]))
sourceper = ColumnDataSource(data = dict(x=player_years, a = player_per, avg = peravg, nbaavg = all_nba_per, label_avg = [peravg[0], all_nba_per[0]]+[0 for x in range(len(player_years)-2)], names = ['Player Avg', 'NBA Avg']+ ['' for x in range(len(player_years)-2)], label_spots = [player_years[0],player_years[0]]+ [player_years[0] for x in range(len(player_years)-2)]))
sourcerpg= ColumnDataSource(data = dict(x=player_years, o = off_reb, d = def_reb, t = tot_reb, avgt=rebavg, avgo = orbavg, avgd = drbavg, nbaavg = all_nba_rebs, label_avg = [rebavg[0], all_nba_rebs[0]]+[0 for x in range(len(player_years)-2)], names = ['Player Avg', 'NBA Avg']+ ['' for x in range(len(player_years)-2)], label_spots = [player_years[0],player_years[0]]+ [player_years[0] for x in range(len(player_years)-2)]))
sourceapg = ColumnDataSource(data = dict(x=player_years, a = player_asts, avg = astavg, nbaavg = all_nba_asts, label_avg = [astavg[0], all_nba_asts[0]]+[0 for x in range(len(player_years)-2)], names = ['Player Avg', 'NBA Avg']+ ['' for x in range(len(player_years)-2)], label_spots = [player_years[0],player_years[0]]+ [player_years[0] for x in range(len(player_years)-2)]))

p.line('x', 'y', source=sourceppg, line_width=3.5, line_color='#E24A33',alpha = 0.4)
p.circle('x', 'y', source=sourceppg, size=12, line_color='#E24A33', fill_color = '#568ce2')
z.line('x', 'a', source=sourceapg, line_width=3.5, line_color='#a30693',alpha = 0.4)
z.circle('x', 'a', source=sourceapg, size=12, line_color='#a30693', fill_color = '#568ce2')
w.vbar_stack(stackers=['d','o'], x='x', width=0.5, color=['blue', '#568ce2'], source=sourcerpg,legend_label=['DREB', 'OREB'])
i.vbar(x = 'x', top = 'a', width = 0.5, color={'field': 'a', 'transform': color_mapper}, source = sourceper)

# Selected Players' Average lines
avglinep = p.line('x', 'avg', source=sourceppg, line_width=3.5, line_color='#E24A33', alpha = 0.2)
avglinewt = w.line('x', 'avgt', source=sourcerpg, line_width=3.5, line_color='blue', alpha = 0.2)
avglinewo = w.line('x', 'avgo', source=sourcerpg, line_width=3.5, line_color='#568ce2', alpha = 0.2)
avglinewd = w.line('x', 'avgd', source=sourcerpg, line_width=3.5, line_color='blue', alpha = 0.2)
avglinez = z.line('x', 'avg', source=sourceapg, line_width=3.5, line_color='#a30693', alpha = 0.2)
avglinei = i.line('x', 'avg', source=sourceper, line_width=3.5, line_color='purple', alpha = 0.2)

#NBA Average lines
nba_avglinep = p.line('x', 'nbaavg', source=sourceppg, line_width=2.5, line_color='black', alpha = 0.2)
nba_avglinewt = w.line('x', 'nbaavg', source=sourcerpg, line_width=2.5, line_color='black', alpha = 0.2)
nba_avglinez = z.line('x', 'nbaavg', source=sourceapg, line_width=2.5, line_color='black', alpha = 0.2)
nba_avglinei = i.line('x', 'nbaavg', source=sourceper, line_width=2.5, line_color='black', alpha = 0.2)

#Set all average lines to false
avglinewd.visible = False
avglinewo.visible = False
avglinez.visible = False
avglinewt.visible = False
avglinep.visible = False
avglinei.visible = False

nba_avglinep.visible = False
nba_avglinewt.visible = False
nba_avglinez.visible = False
nba_avglinei.visible = False

labels_ppg = LabelSet(x='label_spots', y='label_avg', text='names', level='glyph',
              x_offset=5,  source=sourceppg, render_mode='canvas')
labels_ppg.visible = False
p.add_layout(labels_ppg)

labels_rpg = LabelSet(x='label_spots', y='label_avg', text='names', level='glyph',
              x_offset=5,  source=sourcerpg, render_mode='canvas')
labels_rpg.visible = False
w.add_layout(labels_rpg)

labels_apg = LabelSet(x='label_spots', y='label_avg', text='names', level='glyph',
              x_offset=5,  source=sourceapg, render_mode='canvas')
labels_apg.visible = False
z.add_layout(labels_apg)

labels_per = LabelSet(x='label_spots', y='label_avg', text='names', level='glyph',
              x_offset=5,  source=sourceper, render_mode='canvas')
labels_per.visible = False
i.add_layout(labels_per)

# checkbox_group
button_group = CheckboxButtonGroup(labels=["Average PPG Lines", "Average RPG Lines", "Average APG Lines", "Average PER Lines"], active=[], )
button_group.on_click(update_avg_line)

img = figure(plot_width=300, plot_height=200, x_range=(0, 370), y_range=(0, 834), x_axis_type=None,y_axis_type=None,tools = [])
imageglyph = img.image_url(url=['nba/static/images/kevin_durant.png'],x=0, y=0, w=369, h=834,anchor="bottom_left")
img.grid.visible = False
img.outline_line_color = None

ticker = SingleIntervalTicker(interval=1, num_minor_ticks=0)
xaxis = LinearAxis(ticker=ticker)
xaxis2 = LinearAxis(ticker=ticker)
yaxis = LinearAxis(ticker = ticker)

i.add_layout(xaxis2, 'below')

w.legend.orientation = 'horizontal'
w.legend.location = "top_left"
w.y_range.end = tot_reb.max()*1.4
w.yaxis.major_label_text_font_style = "bold"

win_shares.xgrid.visible = False

for plot in [p, w, z, i]:
    plot.ygrid.grid_line_alpha = 0.8
    plot.ygrid.grid_line_dash = [6, 4]
    plot.xaxis.axis_label_text_font_style = "bold"

for plot in [p, w, z, i, defense_scatter, map_figure, win_shares]:
    plot.outline_line_width = 4
    plot.outline_line_alpha = 0.3
    plot.outline_line_color = "navy"

for plot in [heatmap, p, w, z, i, defense_scatter, map_figure, win_shares, ts, img]:
    plot.toolbar.autohide = True
    plot.yaxis.axis_label_text_font_style = "bold"
    plot.xaxis.axis_label_text_font_style = "bold"
    plot.yaxis.major_label_text_font_style = 'bold'
    plot.xaxis.major_label_text_font_style = 'bold'
    plot.xaxis.major_label_text_font_size = "13pt"
    plot.yaxis.major_label_text_font_size = "13pt"

div = Div(width = 300, height = 400, text = makediv(selected_player_df, [x[1] for x in teamlist]))
widgets = column(selectplayer,selectteam,button_group, img, div, width=300)
year_charts = column([p,z,w, i])
square_charts = column([row(defense_scatter,heatmap),row(ts,map_figure), win_shares])
display = row([widgets, year_charts, square_charts])
doc.add_root(display)
show(display)
