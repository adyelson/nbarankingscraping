import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

url = "https://www.nba.com/stats/players/traditional/?sort=PLAYER_NAME&dir=1"
top10ranking = {}
#aprendido com canal CODIFO FONTE TV
#lista de rankings relacionados com cabeçalho da tabela de ranking no site da NBA
rankings = {
    '3points':{'field':'FG3M','label':'3PM'},
    'points':{'field':'PTS','label':'PTS'},
    'assistants':{'field':'AST','label':'AST'},
    'rebounds':{'field':'REB','label':'REB'},
    'steals':{'field':'STL','label':'STL'},
    'blocks':{'field':'BLK','label':'BLK'},
}
def buildrank(type): 
    field = rankings[type]['field']   
    label = rankings[type]['label']

    #click para organizar na tabela dinamica do site, a ordem desejada para rankear
    driver.find_element_by_xpath(
    f"//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='{field}']"
    ).click()

    element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")
    html_content = element.get_attribute('outerHTML')

    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    df_full = pd.read_html(str(table))[0].head(10)
    df = df_full[['Unnamed: 0','PLAYER','TEAM',label]]
    df.columns = ['pos','player','team','total']

    print(df)

    return df.to_dict('records')

option = Options()
option.headless = True
option.add_argument("--unlimited-storage")
driver = webdriver.Chrome()

#options=option
driver.get(url)

#espera para carregar elementos
driver.implicitly_wait(10)
#click para fechar popup de aceitação de cookieas
driver.find_element_by_xpath("//*[@id='onetrust-accept-btn-handler']"
    ).click()

#loop para buscar todos os rankings definidos, faz as chamadas da função buildrank
for k in rankings:
    top10ranking[k]=buildrank(k)
driver.quit()

#criação do json
js = json.dumps(top10ranking)
fp= open('ranking.json','w')
fp.write(js)
fp.close