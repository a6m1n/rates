from selenium import webdriver
from bs4 import BeautifulSoup
from os import path
import csv
import time


def read_csv(data):
    results = []
    folder = path.dirname(__file__)
    with open (folder+'\\{}.csv'.format(data), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for line in reader:
            results.append(line['link'])
    f.closed
    return results

def all_data_csv(data):
     results = []
     # line_text = 0
     folder = path.dirname(__file__)
     with open (folder+'\\{}.csv'.format(data), 'r', encoding='utf-8') as f:
         reader = csv.DictReader(f)
         for line in reader:
             # line_text +=1
             results.append(line)
     f.closed
     return results

def new_data_csv(last_data_csv,retult_t_t):
    new_data_dict = {}
    a=[]
    for i in last_data_csv:
        for j in i:
            if i[j]==None:
                # for h in retult_t_t
                pass
            else:
                print (i[j])

#просто старые и новые данные грузить в массив. потом записовать по ключу.

def new_data(results):
    folder = path.dirname(__file__)
    last_data_csv=all_data_csv('12.02.2019')
    for url in results:
        driver = webdriver.Chrome(executable_path=folder+r'\\chromedriver.exe')
        driver.get(url)
        goal_in_first_time(driver,last_data_csv)
        driver.close()
        return True


def goal_in_first_time(driver,last_data_csv):
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    dict_name = name_team(soup)
    dict_name2 = first_time(soup)
    # print (dict_name2)
    res = {dict_name['home team'] : dict_name2['home_team'], dict_name['away team']:dict_name2['away_team'] }
    goal_in_first_time = gift(res)
    team_who_scored = tws(res)
    Both_scored = bs(res)
    result_in_first_time = rift(res,dict_name)
    result_in_all_time = riat(res,dict_name)
    retult_t_t = {'goal in first time':goal_in_first_time,'team who scored':team_who_scored,
                    'Both scored':Both_scored,'result in first time':result_in_first_time,
                    'result in all time':result_in_all_time}
    new_data_arr_format = new_data_csv(last_data_csv,retult_t_t)
    print(new_data_arr_format)


def gift(res):
    a = 'No'
    for j in res:
        for jj in res[j]:
            if int(jj)<=45:
                a = 'Yes'
                return a
    return a

def tws(res):
    a = '0'
    for j in res:
        for jj in res[j]:
            if int(jj)<=45:
                a = j
                return a
    return a

def bs(res):
    bs=0
    for j in res:
        for jj in res[j]:
            bs+=1
    return bs

def rift(res,dict_name):
    team = 0
    f_1 = {dict_name['home team']:0,dict_name['away team']:0}
    for j in res:
        team += 1
        c = 0
        for jj in res[j]:
            if int(jj)<45:
                c = 1
                if team ==1:
                    f_1[dict_name['home team']] +=c
                elif team == 2:
                    f_1[dict_name['away team']] +=c
    return (f_1)

def riat(res,dict_name):
    team = 0
    f_1 = {dict_name['home team']:0,dict_name['away team']:0}
    for j in res:
        team += 1
        c = 0
        for jj in res[j]:
            if int(jj)<90:
                c = 1
                if team ==1:
                    f_1[dict_name['home team']] +=c
                elif team == 2:
                    f_1[dict_name['away team']] +=c
    return (f_1)

def name_team(soup):
    name_chemp = soup.find_all('a', class_='participant-imglink')
    f = 0
    for name in name_chemp:
        name = name.text.strip()
        if len(name)>1 and f == 0:
            home_team_name = name
            f+=1
        elif len(name)>1 and f == 1:
            away_team_name = name
    return {'home team':home_team_name, 'away team':away_team_name}



def first_time(soup):
    goal_in_game = []
    first_time = {'home_team':[], 'away_team': []}
    time = soup.find('div', class_="detailMS")
    home_team = time.find_all('div', class_="detailMS__incidentRow incidentRow--home even") + time.find_all('div', class_="detailMS__incidentRow incidentRow--home odd")
    away_team =  time.find_all('div', class_="detailMS__incidentRow incidentRow--away even") + time.find_all('div', class_="detailMS__incidentRow incidentRow--away odd")
    for i in time:
        if i in home_team:
            if i.find('div', class_="icon-box soccer-ball")!=None:
                time_goal = i.find('div', class_="time-box").text[:-1]
                first_time['home_team'].append(time_goal)

        elif i in away_team:
            if i.find('div', class_="icon-box soccer-ball")!=None:
                time_goal = i.find('div', class_="time-box").text[:-1]
                first_time['away_team'].append(time_goal)

    return first_time

def start():
    retults = read_csv('12.02.2019')
    new_data(retults)



start()
