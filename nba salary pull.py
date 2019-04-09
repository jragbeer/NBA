from selenium import webdriver
import time
import bs4 as bs
import re
import datetime
import pandas as pd

path = 'C:/Users/xxx/PycharmProjects/nba/salary data/'
def main(year1, year2):
    """

    Grabs data from the URL. It then creates a dataframe with columns: Player, Salary, Adj. Salary and Season (season is used to combine all years)

    :param year1: year to start at --- (year1, year1 +1) salary data
    :param year2: year to end at ---- (year2-1, year2) salary data
    :return: dataframe with player salaries for that year
    """
    def grab_soup(url, browser = "firefox"):
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
        driver.get(url)
        html = driver.page_source
        time.sleep(1)
        html = driver.execute_script("return document.body.outerHTML;")
        soup = bs.BeautifulSoup(html, 'lxml')
        return soup, driver

    URL = "https://hoopshype.com/salaries/players/{}-{}/".format(year1, year2)

    soup, driver = grab_soup(URL)
    players = [x.text.strip() for x in soup.findAll('table')[0].findAll('td', {'class': 'name'})]
    salaries = [x.text.strip().replace('$', '').replace(',', '') for x in soup.findAll('table')[0].findAll('td', {'class': 'hh-salaries-sorted'})] #remove punctuation and find table entry that corresponds to hh-salaries-sorted class
    adjusted_salaries = [x.text.strip().replace('$', '').replace(',', '') for x in soup.findAll('table')[0].findAll('td', {'class': ''})]
    df = pd.DataFrame(data = dict(Player = players[1:], Salary = salaries[1:], AdjustedSalary = adjusted_salaries[1:], Season = ['{}-{}'.format(year1, year2) for x in range(len(players)-1)]))
    driver.quit() #close browser instance
    return df

timee = datetime.datetime.now()
print(timee)
# create a list of the dataframes, to be concatenated to a larger dataframe with all salary data
dataframes = []
for x in range(2006, 2019):
    dataframes.append(main(x, x+1))
bigdf = pd.concat(dataframes)
bigdf.to_csv(path + 'playersalaries.csv', index = False)
print(datetime.datetime.now()-timee)



