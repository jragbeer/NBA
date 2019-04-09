from selenium import webdriver
import time
import bs4 as bs
import re
import datetime
import pandas as pd
import re
import pickle

# read in NBA free throws dataset
path = 'C:/Users/Julien/PycharmProjects/nba/'
data = pd.read_csv(path + 'free_throws.csv')

def get_data(URL):
    """

    This function goes through the data returned by grab_soup and finds the players playing in that game.

    :param URL: url to go to to retrieve data
    :return: players - dictionary of players in that game


    """
    def grab_soup(url_, browser = "firefox"):
        """
        This function enables a driver (using Firefox or Chrome), goes to the URL, and retrieves the data after the JS is loaded.

        :param url_: url to go to to retrieve data
        :param browser: browser to use, defaults to firefox (requires geckodriver.exe on path)
        :return:

        soup - the data of the page
        driver - the browser (process) instance
        """
        if browser == 'chrome':
            driver = webdriver.Chrome()
        else:
            driver = webdriver.Firefox()
        driver.get(url_) # go to the URL
        html = driver.page_source
        time.sleep(1) # sleep for 1 second  to ensure all JS scripts are loaded
        html = driver.execute_script("return document.body.outerHTML;") # execute javascript code
        soup_ = bs.BeautifulSoup(html, 'lxml') # read the data as html (using lxml driver)
        return soup_, driver

    soup, driver = grab_soup(URL)
    try:
        reg = r'\/.\w{1,}-\w{1,}' # regex to find the team membership data on the page
        players = {'1':[], '2':[]}
        # recursively add players to each list in the *players* dictionary
        # 1 corresponds to away team, 2 for home team
        for each in range(1,3):
            for xx in soup.find_all('table')[each]:
                b = xx.find_all('td',  {'class': 'name'})
                for i in range(len(b)):
                    try:
                        y = b[i].find_all(href = True)[0]
                        players[str(each)].append(re.search(reg, y['href'])[0].replace('/', '').replace('-', ' '))
                    except:
                        pass
        driver.quit() # after all players are found, close the browswer instance
    except:
        driver.quit() # if the page doesn't load properly, close the browswer instance
    return players
def main():
    """

    This function goes through each of the game_id's in the nba free throw dataset, finds the players on each team, and returns it as a dictionary.
    These entries are put into a larger dictionary. After every entry, the file is saved as a pickle.

    :return: nothing
    """
    timee = datetime.datetime.now()
    print(timee)

    # pickle_in = open("game_id_player_mapping.pickle","rb")
    # game_id_dict = pickle.load(pickle_in)

    game_id_dict = {}
    print(len(game_id_dict.keys())) # print how many games are in the game_id_dict so far (gives ability to split webscraping across multiple sessions)

    # sometimes a page doesn't load correctly. If that happens, delete the key so that the next for loop catches it.
    for x in list(game_id_dict.keys()):
        if len(game_id_dict[x]['1']) == 0:
            try:
                del game_id_dict[x]
            except KeyError:
                pass

    # for each game_id, go to the URL and retrieve the data. Put the data into game_id_dict so that it is stored.
    for x in data['game_id'].unique():
        try:
            time1 = datetime.datetime.now()
            x = int(x)
            if str(x) not in list(game_id_dict.keys()):
                url = "http://www.espn.com/nba/boxscore?gameId={}".format(x)
                teams = get_data(url)
                game_id_dict[str(x)]=teams
                print(datetime.datetime.now()-time1, x, teams) # print out how long it took to grab data from webpage
                pickle_out = open("game_id_player_mapping.pickle", "wb")
                pickle.dump(game_id_dict, pickle_out)
                pickle_out.close()
                # time.sleep(1)
        # if going to the website fails, move on to the next one
        except:
            pass
    print(datetime.datetime.now()-timee) #print how long the entire script ran

main()
