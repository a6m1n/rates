from selenium import webdriver
from bs4 import BeautifulSoup
from os import path
import csv
import time


def write_csv(input_string,data): #с каждым изменением папки, менять автозапись.
    a=path.dirname(__file__)
    a=a[:a.rfind('\\')]
    folder = a+'\\result\\month\\april\\'+data
    with open (folder+'\\{}_new.csv'.format(data), 'a', encoding='utf-8',  newline='') as f:
        writer = csv.writer(f)
        fieldnames = ['id', 'country','team','strategy 2','strategy 1','time','link','goal in first time','team that scored','Both scored','result in first time','result in all time']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if input_string['id']=='1' or input_string['id']==1 :
            writer.writeheader()
        writer.writerow(input_string)
    f.closed #3

def new_data_csv(last_data_csv,retult_t_t):
    new_data_dict = {}
    for i in last_data_csv[0]:
        if last_data_csv[0][i]!=None:
            new_data_dict[i]=last_data_csv[0][i]
    for j in retult_t_t:
        new_data_dict[j]=retult_t_t[j]
    return new_data_dict #i, last_data_csv[0][i]

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
    try:
        home_team = time.find_all('div', class_="detailMS__incidentRow incidentRow--home even") + time.find_all('div', class_="detailMS__incidentRow incidentRow--home odd")
    except:
        return False
    away_team =  time.find_all('div', class_="detailMS__incidentRow incidentRow--away even") + time.find_all('div', class_="detailMS__incidentRow incidentRow--away odd")
    for i in time:
        if i in home_team:
            if i.find('div', class_="icon-box soccer-ball")!=None:
                try:
                    time_goal = i.find('div', class_="time-box").text[:-1]
                except:
                    time_goal = i.find('div', class_="time-box-wide").text[:-1]
                    time_goal = time_goal.split('+')
                    time_goal = str (int(time_goal[0]) + int(time_goal[1]))

                first_time['home_team'].append(time_goal)

        elif i in away_team:
            if i.find('div', class_="icon-box soccer-ball")!=None:
                try:
                    time_goal = i.find('div', class_="time-box").text[:-1]
                except:
                    time_goal = i.find('div', class_="time-box-wide").text[:-1]
                    time_goal = time_goal.split('+')
                    time_goal = str (int(time_goal[0]) + int(time_goal[1]))
                first_time['away_team'].append(time_goal)

    return first_time

def new_data_func(driver,last_data_csv,dmy):
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    dict_name = name_team(soup)
    dict_name2 = first_time(soup)
    if dict_name2:
        res = {dict_name['home team'] : dict_name2['home_team'], dict_name['away team']:dict_name2['away_team'] }
        goal_in_first_time = gift(res)
        team_who_scored = tws(res)
        Both_scored = bs(res)
        result_in_first_time = rift(res,dict_name)
        result_in_all_time = riat(res,dict_name)
        retult_t_t = {'goal in first time':goal_in_first_time,'team that scored':team_who_scored,
                        'Both scored':Both_scored,'result in first time':result_in_first_time,
                        'result in all time':result_in_all_time}
        new_data_arr_format = new_data_csv(last_data_csv,retult_t_t)
        write_csv(new_data_arr_format,dmy)

def data_link(data,url):
    results=[]
    a=path.dirname(__file__)
    a=a[:a.rfind('\\')]
    folder = a+'\\result\\month\\april\\'+data
    with open (folder+'\\{}.csv'.format(data), 'r', encoding='utf-8') as f:
         reader = csv.DictReader(f)
         for line in reader:
             if line['link']==url:
                 results.append(line)
    f.closed
    return results

def new_data(results_link,dmy):
    folder = path.dirname(__file__)
    for url in results_link:
        driver = webdriver.Chrome(executable_path=folder+r'\\chromedriver.exe')
        driver.get(url)
        last_data_csv = data_link(dmy,url)
        new_data_func(driver,last_data_csv,dmy)
        driver.close()
        # return True

def read_csv_and_give_link(data):
    results_link = []
    a=path.dirname(__file__)
    a=a[:a.rfind('\\')]
    folder = a+'\\result\\month\\april\\'+data
    with open (folder+'\\{}.csv'.format(data), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for line in reader:
            results_link.append(line['link'])
    f.closed
    return results_link


def start():
    print ('Введите данные. Пример: 01.01.2000')
    dmy = input('')
    results_link = read_csv_and_give_link(dmy)
    new_data(results_link,dmy)



start()
