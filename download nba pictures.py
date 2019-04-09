import pandas as pd
import numpy as np
import wget
import datetime
import urllib

timee = datetime.datetime.now()
print(timee)

def cleandf(df):
    """

    Light cleaning of dataset, this helps to feed the correct names to the web-parser.

    :param df: input dataframe with every player's stats
    :return: cleaned df
    """

    # fill nulls, drop duplicate rows, type-cast columns and create per-game stats since the dataset contains absolute values
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
    #minor cleaning of *player* column
    df['Player'] = pd.Series([str(x).replace('*', '') for x in df['Player']], index=df.index)
    return df

#read in dataset of all players
df = pd.read_csv('Seasons_Stats.csv')
df = cleandf(df)
direc = 'C:/Users/Julien/PycharmProjects/csvsaving/static/'

pics = 0
no_pics = 0
for x in df.Player.unique():
    try:
        #get last name and first name, use as input for to the URL, then return data
        llast = x.lower().split()[1].replace("'", "").replace(".", "")
        ffirst = x.lower().split()[0].replace("'", "").replace(".", "")
        name = 'https://nba-players.herokuapp.com/players/{}/{}'.format(llast, ffirst)
        meta = urllib.request.urlopen(name).info() #open website with urllib
        # if the data returned shows that the info isn't what it should be, move on to another player
        if int(meta['Content-Length']) < 75:
            continue
        # download file and save as a png file as * firstname_lastname.png *
        else:

            filename = wget.download(name, out=direc + '{}_{}.png'.format(ffirst, llast))
            print("Content-Length:", meta)
            print('{}_{}'.format(ffirst,llast))
            pics+=1 # increment *pics* counter
    except Exception as e:
        #print error and increment *no_pics* if the player's photo could not be found
        print(str(e))
        no_pics+=1
        pass

print('number of pics', pics)
print('number of no-pics', no_pics)
print(datetime.datetime.now()-timee)