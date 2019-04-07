from selenium import webdriver
import time
import bs4 as bs
import re
import datetime
import pandas as pd
import pprint
import re
import pickle
path = 'C:/Users/Julien/PycharmProjects/nba/'
data = pd.read_csv(path + 'free_throws.csv')
def main(URL):
    def grab_soup(url_, browser = "firefox"):
        if browser == 'chrome':
            driver = webdriver.Chrome()
        else:
            driver = webdriver.Firefox()
        driver.get(url_)
        html = driver.page_source
        time.sleep(1)
        html = driver.execute_script("return document.body.outerHTML;")
        soup_ = bs.BeautifulSoup(html, 'lxml')
        return soup_, driver

    soup, driver = grab_soup(URL)
    try:
        reg = r'\/.\w{1,}-\w{1,}'
        players = {'1':[], '2':[]}
        for each in range(1,3):
            for xx in soup.find_all('table')[each]:
                b = xx.find_all('td',  {'class': 'name'})
                for i in range(len(b)):
                    try:
                        y = b[i].find_all(href = True)[0]
                        players[str(each)].append(re.search(reg, y['href'])[0].replace('/', '').replace('-', ' '))
                    except:
                        pass
        driver.quit()
    except:
        driver.quit()
    return players

timee = datetime.datetime.now()
print(timee)
pickle_in = open("game_id_player_mapping.pickle","rb")
game_id_dict = pickle.load(pickle_in)
print(len(game_id_dict.keys()))

# for x in list(game_id_dict.keys()):
#     if len(game_id_dict[x]['1']) == 0:
#         print(x)
#         try:
#             del game_id_dict[x]
#         except KeyError:
#             pass
# for x in data['game_id'].unique():
#     try:
#         time1 = datetime.datetime.now()
#         x = int(x)
#         if str(x) not in list(game_id_dict.keys()):
#             url = "http://www.espn.com/nba/boxscore?gameId={}".format(x)
#             teams = main(url)
#             game_id_dict[str(x)]=teams
#             print(datetime.datetime.now()-time1, x, teams)
#             pickle_out = open("game_id_player_mapping.pickle", "wb")
#             pickle.dump(game_id_dict, pickle_out)
#             pickle_out.close()
#             # time.sleep(1)
#     except:
#         pass
print(datetime.datetime.now()-timee)



