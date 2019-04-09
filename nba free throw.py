import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import time
import pickle
from mpl_toolkits.basemap import Basemap

# use seaborn's colour scheme
sns.set()

def clean_player2(df):
    """

    Cleans the *player* column of a dataframe, doing mappings, and normalization.

    :param df: dataframe with player column that you want cleaned up
    :return: df
    """
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
def clean_player_inital(df):
    """

    Cleans the *player* column of a dataframe, doing mappings, and normalization.
    Also uses clean_player2 function.

    :param df: dataframe with player column that you want cleaned up
    :return: df
    """

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

path = 'C:/Users/Julien/PycharmProjects/nba/'
timee = datetime.datetime.now()
print(timee)

# read in the teamNames / locations data. Create a few columns that allow easy filtering for State and City
teamNames = pd.read_csv(path + 'static/teams.csv', index_col='Abbrev')
teamNames['State'] = [i.split(',')[1] for i in teamNames.Location.values]
teamNames['City'] = [i.split(',')[0] for i in teamNames.Location.values]

#load pickle of team membership for each game_id
pickle_in = open("game_id_player_mapping.pickle","rb")
game_id_dict = pickle.load(pickle_in)
# turn dictionary into a dataframe for easier joining with free throws dataset
game_id_players = pd.DataFrame(data= dict(game_id = list(game_id_dict.keys()), away_team_roster = [game_id_dict[i]['1'] for i in game_id_dict.keys()], home_team_roster = [game_id_dict[i]['2'] for i in game_id_dict.keys()]))
game_id_players['game_id'] = game_id_players['game_id'].astype(int)

# main dataset to read in
df = pd.read_csv(path + 'free_throws.csv')
# rename *score* column, as it is actually the score after the FT occurred, we would also like to know the score before.
df.rename(columns = {'score':'score_after'}, inplace =True)
# type cast this column for easier joining with game_id_dict
df['game_id'] = df['game_id'].astype(int)
# delete exhibition games
df = df[df['game'] != 'WEST - EAST']
df = df[df['game'] != 'EAST - WEST']
# join the game_id_players data with the free throw data
df = pd.merge(df, game_id_players, how = 'left', on = 'game_id')

# clean the dataframe
df = clean_player_inital(df)
# create a column to identify which team is the HOME team
df['Home Team'] = pd.Series([x.split('-')[1].strip() for x in df['game']], index = df.index)

# I used 3 character shortnames in the teamNames dataset, this is done so proper joins occur
df.replace('GS', 'GSW', inplace = True)
df.replace('NJ', 'NJN', inplace = True)
df.replace('NO', 'NOP', inplace = True)
df.replace('NY', 'NYK', inplace = True)
df.replace('UTAH', 'UTA', inplace = True)

# join the teamNames and free_throws datasets. This gives location (long/lat) and city names to each row
# change name as this data is ready to be used for all proceeding functions
data = pd.merge(df, teamNames, how = 'left', right_index = True, left_on = 'Home Team')
data['Location'] = data['Location'].astype(str)
data['State'] = [i.split(',')[1] for i in data.Location.values]
data['City'] = [i.split(',')[0] for i in data.Location.values]

# create column which shows which team the player shooting the FT is on
player_team = []
for x in data.itertuples():
    pp = x.player
    if pp in x.home_team_roster:
        player_team.append('home')
    elif pp in x.away_team_roster:
        player_team.append('away')
    # some mismatches occur and some players could not be accounted for (different names that didn't match), captures over 99% of FTs
    else:
        player_team.append('0')
data['Players_team'] = pd.Series(player_team, index = data.index)
data = data[data['Players_team'] != '0']

# save the data so that we don't have to wait to load / join the data later on
pickle_out = open("data.pickle","wb")
pickle.dump(data, pickle_out)
pickle_out.close()

# pickle_in = open("data.pickle","rb")
# df = pickle.load(pickle_in)

def make_home_away_charts(data):
    """

    Creates a pie chart and a multi-bar chart for away and home stats.

    :param data: cleaned dataframe
    :return: plots 2 charts
    """
    def home_away(data_, season):
        """

        Create a dictionary with made shots, attempted shots and the percentage for both home and away for the given *season*

        :param data_: cleaned dataframe
        :param season: the season of interest
        :return: a dictionary with the total made, attempted and percentage for each season
        """
        data_ = data_[data_['season'] == season]

        home_versus_away = {'made_home': data_[data_['Players_team'] == 'home']['shot_made'].sum(),
                            'made_away': data_[data_['Players_team'] == 'away']['shot_made'].sum(),
                            'total_home': len(data_[data_['Players_team'] == 'home']['shot_made'].index),
                            'total_away': len(data_[data_['Players_team'] == 'away']['shot_made'].index),
                            'home_made_percentage': data_[data_['Players_team'] == 'home']['shot_made'].sum() / len(
                                data_[data_['Players_team'] == 'home']['shot_made'].index),
                            'away_made_percentage': data_[data_['Players_team'] == 'away']['shot_made'].sum() / len(
                                data_[data_['Players_team'] == 'away']['shot_made'].index)}

        return home_versus_away

    # create season by season stats on Home vs. Away stats (made shots, attempts, percentage)
    fool = {}
    for i in data['season'].unique():
        fool[str(i)] = home_away(data, i)

    away = [fool[i]['away_made_percentage'] * 100 for i in data['season'].unique()]
    home = [fool[i]['home_made_percentage'] * 100 for i in data['season'].unique()]

    home_shots = len(data[data['Players_team'] == 'home']['shot_made'].index)
    away_shots = len(data[data['Players_team'] == 'away']['shot_made'].index)

    # for each season, how efficient are players when they are home vs when they are a visiting player
    fig = plt.figure()
    fig.suptitle('AWAY COURT ADVANTAGE', fontsize=20)
    ax1 = fig.add_subplot(111)
    ax1.bar(np.arange(len(data['season'].unique())) + 0.2, home, width=0.35, label='HOME')
    ax1.bar(np.arange(len(data['season'].unique())) - 0.2, away, width=0.35, label="AWAY")
    # plot a line that shows the average across the dataset (75.6%) for all players
    ax1.plot(np.linspace(-1, 10, 10),
             [(100 * data['shot_made'].sum()) / len(data.index)] * len(data['season'].unique()), c='firebrick')
    ax1.tick_params(axis='x', which='both', bottom=False)
    ax1.set(ylim=[70, 80], ylabel='Percentage (%)', xlabel='Season', xticks=range(10),
            xticklabels=list(data['season'].unique()))
    ax1.yaxis.label.set_size(18)
    ax1.xaxis.label.set_size(18)
    ax1.tick_params(axis='y', labelsize=17)
    ax1.tick_params(axis='x', labelsize=14)
    plt.legend()

    # create a pie chart showing the number of shots for home vs away across the whole date range
    fig1 = plt.figure()
    fig1.suptitle('AWAY COURT ADVANTAGE', fontsize=20)
    ax2 = fig1.add_subplot(111)
    ax2.pie([home_shots, away_shots], labels=['HOME - {:.1f}%'.format(100 * home_shots / (home_shots + away_shots)),
                                              'AWAY - {:.1f}%'.format(100 * away_shots / (home_shots + away_shots))],
            startangle=90, labeldistance=0.35, textprops={'fontsize': 18, 'color': 'white', 'weight': 'bold'})
# make_home_away_charts(df)
def make_position_chart(data):
    """

    Produces a chart showing the different FT accuracy rates for each position.

    :param data: cleaned dataframe
    :return: 1 plot produced
    """

    # read in dataset from kaggle with positions foe each player
    # clean up the positions to standard ones, for instance, C-F and F-C are both the same (PF)
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

    # create a dataframe where each player is the index and their most played position is are the values
    # clean the *player* column (which is the index in this case) to allow for joining
    new = season_stats.groupby(['Player', 'Pos']).agg({'Pos':'count'}).unstack()
    positions = pd.DataFrame(new.idxmax(axis=1), columns=['pos'])
    positions['position'] = [x[1] for x in positions['pos']]
    positions.index = [x.lower().replace('*', '') for x in positions.index]
    positions['player'] = positions.index
    positions = clean_player2(positions)
    positions.index = positions['player']
    positions.drop(['pos', 'player'], 1, inplace=True)

    # join the position dataframe and the input *data* dataframe
    ttt = pd.merge(data, positions, how = 'inner', right_index=True, left_on = 'player')

    # groupby position and find FT accuracy
    af = pd.DataFrame(ttt.groupby(['position'])['shot_made'].sum())
    af['count'] = ttt.groupby(['position'])['shot_made'].count()
    af['percent'] = 100 * af['shot_made'] / af['count']

    #plot a bar chart comparing the different positions
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.bar(['PG', 'SG', 'SF', 'PF', "C"], [af.at['PG','percent'],af.at['SG','percent'],af.at['SF','percent',],af.at['PF','percent'],af.at['C','percent']])
    ax1.set_ylim([60, 85])
    ax1.set_ylabel('Percentage (%)')
    ax1.set_xlabel('Position')
    ax1.tick_params(axis = 'both', which = 'both', labelsize=18)
# make_position_chart(df)
def make_map(data):
    """

    Create 3 plots with geography data; including differnces by city, timezone and latitude.

    :param data: cleaned data
    :return: 3 plots produced
    """

    # groupby state and display data -- not used
    # state_data = pd.DataFrame(data.groupby(['State'])['shot_made'].sum())
    # bb = data.groupby(['State'])['shot_made'].count()
    # 
    # state_data['count'] = bb
    # state_data['percent'] = state_data['shot_made'] / state_data['count']
    # print(state_data.sort_values('percent'))

    # groupby city and find FT efficiency
    city_data = pd.DataFrame(data.groupby(['City'])['shot_made'].sum())
    city_data['count'] = data.groupby(['City'])['shot_made'].count()
    city_data['percent'] = city_data['shot_made'] / city_data['count']


    # create Longitude and Latitude columns for the dataframe
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


    # for each region of latitude chart (split by 4), add the cities that should be inside each list
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
    # for each region of timezone chart (split by 4), add the cities that should be inside each list
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

    #plot the geographical data,
    # First with the individual cities. Include a colourmap
    # Second with the latitude. Colour each region differently to help differentiate
    # Third with the Timezone data. The lines are drawn crudely, but each city lies in their correct timezone.

    # state lines, country lines and coastlines are drawn for a cleaner chart
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
# make_map(df)
def make_salary_AND_best_worst(data):
    """

    Creates 2 bar charts and 2 scatter plots. The bar charts show the worst 10 FT shooters (given a minimum) and the top 12 shooters.
    The scatter plots show Salaries vs. FT Accuracy. The scatterplots both show the same data,
     but there's a log10 function put on one of them to help spread the data more across the X access.

    :param data: cleaned dataframe
    :return: 4 plots produced
    """


    salaries = pd.read_csv(path + 'salary data/playersalaries.csv')
    salaries['Player'] = salaries['Player'].str.lower()
    salaries['Player'] = pd.Series([x.replace('.', '').replace("'", '') for x in salaries.Player], index=salaries.index)

    # groupby player and find their efficiency across entire date range, join with salary data and replace NULLs with 80000
    # usually players without salary info were on 10-day contracts, thus the 'low' salary
    # filter by 30 attempts
    new = pd.DataFrame(data.groupby(['player']).agg({'shot_made':'sum'}))
    new['attempts'] = data.groupby(['player']).agg({'shot_made': 'count'})
    new = new[new['attempts'] > 30]
    new['percent'] = new['shot_made']/new['attempts']
    new['salary'] = salaries.groupby(['Player'])['AdjustedSalary'].mean()
    new['salary'].fillna(80000, inplace=True)
    new['salary'] = new['salary'].astype('int64')

    # create a series with the bottom 10 shooters
    worst_shooters = new.sort_values(by = 'percent').head(10)
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.barh([' '.join([x.split(' ')[0].capitalize(),x.split(' ')[1].capitalize()]) for x in worst_shooters.index], worst_shooters['percent'].values*100, color= '#f4ce42')
    ax1.set(xlabel = 'Percentage (%)', ylabel = 'Player', xlim = [25, 50])
    ax1.tick_params(axis='y', labelsize=15)
    ax1.tick_params(axis='x', labelsize=14)
    style = dict(size=18, color='darkgray')
    for x in range(len(worst_shooters.index)):
        ax1.text(100*worst_shooters['percent'][x]+1,x, 'Attempts: {}'.format(str(worst_shooters['attempts'][x])), **style)

    # create a series with the top 12 shooters
    best_shooters = new.sort_values(by = 'percent', ascending=False).head(12)
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.barh(np.flip([' '.join([x.split(' ')[0].capitalize(),x.split(' ')[1].capitalize()]) for x in best_shooters.index]), np.flip(best_shooters['percent'].values)*100, color= '#f4ce42')
    ax2.set(xlabel = 'Percentage (%)', ylabel = 'Player', xlim = [85, 100])
    ax2.tick_params(axis='y', labelsize=15)
    ax2.tick_params(axis='x', labelsize=14)
    for x in range(len(best_shooters.index)):
        ax2.text(100*np.flip(best_shooters['percent'].values)[x]+1,x, 'Attempts: {}'.format(str(np.flip(best_shooters['attempts'].values)[x])), **style)

    # create scatter plots with but log and normal X axes.
    fig = plt.figure()
    ax0 = fig.add_subplot(121)
    ax02 = fig.add_subplot(122)
    ax0.set(xlabel=r'Salary', ylabel='Percentage (%)', )
    ax02.set(xlabel = r'$\log_{10}({\rm Salary})$', )
    ax02.yaxis.set_ticks_position('none')
    ax02.scatter(np.log10(new['salary'].values), new['percent'].values,  c = 'red', s = 10, alpha = 0.32)
    ax0.scatter(new['salary'].values, new['percent'].values,  c = 'red', s = 10, alpha = 0.32)
# make_salary_AND_best_worst(df)
def make_score_diffence_charts(data):
    """

    This function creates 2 charts showing the FT % for players depending on the score before the shot attempt.
    The first chart shows the value in absolutes (non-negative) while the second shows negatives. This is done to see if
    there is a difference in efficiency if players are winning or losing.

    :param data: cleaned dataframe
    :return: plot 2 charts
    """

    # create a column with score data before the shot was taken
    score_before = []
    for x in data.itertuples():
        # if the shot missed, the score_after is the same as the score_before
        if x.shot_made == 0:
            score_before.append(x.score_after)
        # if the shot was made, proceed
        else:
            cc = x.score_after
            first_num = int(cc.split(' - ')[0])
            second_num = int(cc.split(' - ')[1])
            # if player shooting is on the away team, decrement the first number
            if x.Players_team == 'away':
                first_num-=1
                score_before.append('{} - {}'.format(first_num, second_num))
            # if player shooting is on the home team, decrement the second number
            else:
                second_num-=1
                score_before.append('{} - {}'.format(first_num, second_num))

    # create score difference columns (abs and regular)
    data['score_before'] = pd.Series(score_before, index = data.index)
    data['Score_Difference_abs'] = pd.Series([np.abs(int(x.split('-')[0])-int(x.split('-')[1])) for x in data["score_before"]], index = data.index)
    data['Score_Difference'] = pd.Series([int(x.split('-')[0]) - int(x.split('-')[1]) for x in data["score_before"]], index=data.index)

    # groupby score difference and find FT %
    score_dif = pd.DataFrame(data.groupby(['Score_Difference'])['shot_made'].sum())
    score_dif['count'] =data.groupby(['Score_Difference'])['shot_made'].count()
    score_dif['percent'] = 100*score_dif['shot_made']/score_dif['count']
    score_dif = score_dif[score_dif.index >= -40]
    score_dif = score_dif[score_dif.index <= 40]

    # create bar charts showing the FT % across different differentials but only for times when the score is within 40 points
    fig = plt.figure()
    ax1= fig.add_subplot(111)
    ax1.set(ylim = [60, 85], ylabel = 'Percentage (%)', xlabel = 'Difference in Score')
    ax1.tick_params(axis = 'y', labelsize = 18)
    ax1.tick_params(axis='x', labelsize=15)
    ax1.bar(score_dif.index, score_dif.percent.values)

    # groupby absolute score difference and find FT %
    score_dif_abs = pd.DataFrame(data.groupby(['Score_Difference_abs'])['shot_made'].sum())
    score_dif_abs['count'] =data.groupby(['Score_Difference_abs'])['shot_made'].count()
    score_dif_abs['percent'] = 100*score_dif_abs['shot_made']/score_dif_abs['count']
    score_dif_abs = score_dif_abs[score_dif_abs.index >= -40]
    score_dif_abs = score_dif_abs[score_dif_abs.index <= 40]

    fig2 = plt.figure()
    ax2= fig2.add_subplot(111)
    ax2.set(ylim = [60, 85], ylabel = 'Percentage (%)',xlabel = 'Difference in Score (abs)')
    ax2.tick_params(axis='y', labelsize=18)
    ax2.tick_params(axis='x', labelsize=15)
    ax2.bar(score_dif_abs.index, score_dif_abs.percent.values)
# make_score_diffence_charts(df)
def make_time_charts(data):
    """

    This function creates 2 charts. One shows difference in FT% across different quarters / OTs and the other shows how FT% changes every minute of the game.

    **NOTE** For OTs, they are included in the last 5 mins of the game. So if you score with 3 mins left in 2OT, it is grouped with 3 mins left in OT and 3 mins left in regular time.

    :param data: cleaned dataframe
    :return: 2 plots produced
    """

    # groupby period
    period_df = pd.DataFrame(data.groupby(['period'])['shot_made'].sum())
    period_df['count'] =data.groupby(['period'])['shot_made'].count()
    period_df['percent'] = 100*period_df['shot_made']/period_df['count']

    #plot a bar chart with FT shooting efficiency for each period
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.bar(period_df.index, period_df.percent)
    ax1.set(ylim = [60, 85], ylabel = 'Percentage (%)', xlabel = 'Period', xticklabels =  ['','Q1','Q2','Q3','Q4','OT','2OT','3OT','4OT',])
    ax1.plot([period_df.index.min(), period_df.index.max()], [period_df.percent.min(),period_df.percent.max()], c = 'orange', linewidth = 6,linestyle='--')
    ax1.tick_params(axis='both',which = 'both', labelsize=16)

    #create a *time of game* column, where the value is the number of minutes left in the game. This means that 4 mins left in 2OT will be grouped with 4 mins left in regular time
    t_o_g = []
    for x in df.itertuples():
        p = int(x.time.split(':')[0])
        if x.period == float(1):
            p = p + 36
        elif x.period == float(2):
            p = p+24
        elif x.period == float(3):
            p = p+12
        else:
            p = p
        t_o_g.append('{}'.format(p))
    df['time_of_game'] = pd.Series(t_o_g, index = df.index)
    #groupby new *time_of_game* column
    time_of_game = pd.DataFrame(df.groupby(['time_of_game'])['shot_made'].sum())
    time_of_game['attempts'] = df.groupby(['time_of_game'])['shot_made'].count()
    time_of_game['percent'] = 100* time_of_game['shot_made'] / time_of_game['attempts']
    time_of_game.index = time_of_game.index.astype(int)
    # plot a bar chart with FT shooting efficiency for each minute (histogram essentially)
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.bar(time_of_game.sort_index(ascending = False).index, time_of_game.sort_index()['percent'].values)
    ax2.bar([0, 12, 24, 36], [time_of_game.sort_index(ascending = False)['percent'].values[y] for y in [0, 12, 24, 36]])
    ax2.tick_params(axis = 'x', which = 'both', labelsize=12)
    ax2.set(ylim= [60,85],xticks= [x for x in range(48)],xticklabels = [x for x in range(48)][::1],ylabel = 'Percentage (%)', xlabel = 'Minute of Game ')
    ax2.tick_params(axis='y', labelsize=16)
# make_time_charts(df)
def make_players_improving(data):
    """

    Create a line plot showcasing whether the NBA generally improves FT efficiency throughout their careers.

    :param data: cleaned data
    :return: plot
    """
    # create a dataframe with each player's efficiency by season
    af = pd.DataFrame(data.groupby(['player', 'season'])['shot_made'].sum())
    af['count'] = data.groupby(['player', 'season'])['shot_made'].count()
    af = af[af['count'] > 100] #limit results to players with 100 attempts that season
    af['percent'] = 100 * af['shot_made'] / af['count']
    af['years'] = [x.Index[1] for x in af.itertuples()]
    # for each player, count how many seasons that they shot 100 FTs and put it into a DF with column names *Season_ZZZ*
    list_of_players = []
    for x in af.unstack().index:
        list_of_seasons = []
        for y in af.itertuples():
            if x == y.Index[0]:
                list_of_seasons.append(y.Index[1])
        list_of_players.append(list_of_seasons)
    each_player = pd.DataFrame(list_of_players, index = af.unstack().index, columns = ['Season_{}'.format(x+1) for x in range(10)])

    # create a dataframe where each column is the player's performance in that year. Years are
    player_avg_per_year = {str(x+1) : [] for x in range(10)}
    for x in each_player.itertuples():
        yy = {'1': x.Season_1, '2': x.Season_2, '3':x.Season_3,'4':x.Season_4,'5':x.Season_5,'6':x.Season_6,'7':x.Season_7,'8':x.Season_8, '9':x.Season_9,'10':x.Season_10}
        for i in range(10):
            try:
                player_avg_per_year[str(i+1)].append(af.at[(x.Index, yy[str(i+1)]), 'percent'])
            except:
                player_avg_per_year[str(i+1)].append(np.nan)

    # count the number of times a player has improved Year over Year
    # and count how many times a player has declined YoY
    improve = 0
    decline = 0
    for x in player_avg_per_year.keys():
        try:
            for i in range(len(player_avg_per_year[x])):
                if player_avg_per_year[str(int(x)+2)][int(i)] > player_avg_per_year[str(int(x)+1)][int(i)]:
                    improve += 1
                elif player_avg_per_year[str(int(x)+2)][int(i)] < player_avg_per_year[str(int(x)+1)][int(i)]:
                    decline +=1
        except:
            pass
    print('Times a player shoots better season over season: ',improve)
    print('Times a player shoots worse season over season: ',decline)
    print('Ratio: ', improve/decline)

    # plot the players improvement / decline over the years of the dataset
    # use a line chart with a low alpha value, so that any trends are clearer
    insane = pd.DataFrame.from_dict(player_avg_per_year)
    insane.index = each_player.index
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    # plot each line in a for loop.
    for x in insane.itertuples():
        vals = list(x)[1:]
        new_vals = np.array(vals)
        ax1.plot(insane.columns, new_vals,alpha = 0.22, c = 'r')

    ax1.set(ylabel = 'Percentage (%)', xlabel = 'Season')
    ax1.tick_params(axis='both', labelsize=20)
# make_players_improving(df)

plt.show()