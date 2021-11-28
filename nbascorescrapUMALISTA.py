import time
import requests
import pandas as pd
from bs4 import BeautifulSoup, element
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

url = "https://www.nba.com/stats/players/traditional/?sort=PLAYER_NAME&dir=1"

option = Options()
option.headless = True
option.add_argument("--unlimited-storage")
driver = webdriver.Chrome()

#options=option
driver.get(url)

time.sleep(10)
driver.find_element_by_xpath("//*[@id='onetrust-accept-btn-handler']"
    ).click()

time.sleep(10)
driver.find_element_by_xpath(
    "//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='PTS']"
    ).click()

element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")
html_content = element.get_attribute('outerHTML')

soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')

df_full = pd.read_html(str(table))[0].head(10)
df = df_full[['Unnamed: 0','PLAYER','TEAM','PTS']]
df.columns = ['pos','player','team','total']

print(df)

top10ranking = {}
top10ranking['points'] = df.to_dict('records')

driver.quit()

js = json.dumps(top10ranking)
fp= open('ranking.json','w')
fp.write(js)
fp.close