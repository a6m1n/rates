﻿from selenium import webdriver
from bs4 import BeautifulSoup
from os import path , makedirs
import time
import csv
#Исправить стратегию с кликами. Кликает не на те игры. смотреть сколько игр+табличка и следуая цифра клика. может проблема в функции которая кликает.
def new_day(driver,data):
    assert "MyScore" in driver.title
    driver.find_element_by_class_name('calendar__datepicker').click()
    time.sleep(0.5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('div',class_="calendar__datepicker--dates").find_all('div',class_='day')
    go = False
    for td,i in zip(tds,range(len(tds))):
        xpath='//*[@id="live-table"]/div[2]/div/div[2]/div[2]/div[{}]'.format(i+1)
        a = td.text
        a=a[:a.find('/')+3]
        if go and a==data:
            driver.find_element_by_xpath(xpath).click()
            go = False
            break
        if len(td.get('class'))>1:
            go = True
    if go:
        driver.find_element_by_class_name('calendar__datepicker').click()
    time.sleep(1)
def read_day():
    folder = path.dirname(__file__)
    folder = folder[:folder.rfind('\\')]
    f = open(folder+'\\data.txt', 'r')
    data_arr = []
    for line in f:
        data_arr.append(line.strip())
    f.close()
    return data_arr


def get_table(table_today,driver):
    # print (table_today)
    last = table_today[0].text
    go = False
    true_game = 0
    all_game = 0
    for td in table_today:
        try:
            today = td.find('td',class_="cell_ad").text
        except:
            continue
        if go:
            all_game+=1
            today = today.split()
            try:
                last = last.split()
            except:
                pass
            today[1] = today[1].split(':')
            try:
                last[1] = last[1].split(':')
            except AttributeError:
                pass
            re_today = (int(today[1][0])*60)+int(today[1][1])
            re_last = (int(last[1][0])*60)+int(last[1][1])
            re_true = re_last+120
            re_true2 = re_last-120
            if today[0]!=last[0]:
                true_game+=1
            elif re_today>=re_true:
                true_game +=1
                # print (today,last)
        last = today
        if go == False:
            go = True
    # print ( true_game, '   ' ,all_game)
    return true_game==all_game


def strategy_st2(driver):
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    name_chemp = soup.find('div',class_='tournament-name').text
    try:
        table_today = soup.find('div',id="fs").find('tbody').find_all('tr')
    except AttributeError:
        print ('AttributeError: ',name_chemp, '    (при просмотре сегодняшних игр)')
        return False
    try:
        schedule = soup.find('div',id="block-summary-fixtures").find('tbody').find_all('tr')
    except AttributeError:
        print ('AttributeError: ',name_chemp, '    (при просмотре расписания игр)')
        return False
        block-summary-results
    try:
        last_results = soup.find('div',id="block-summary-results").find('tbody').find_all('tr')
    except AttributeError:
        print ('AttributeError: ',name_chemp, '    (при просмотре прошлых результатов игр)')
        return False
    a1 = get_table(table_today,driver) #1
    a2 = get_table(schedule,driver) #3
    a3 = get_table(last_results,driver) #2
    print (a1,a2,a3, ' -  ', name_chemp)
    if a1 and a2 and a3:
        print (driver.current_url)
        driver.find_element_by_class_name('li1 ').click()
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        try:
            all_table=soup.find('div',id="fs-results").find('tbody').find_all('tr')
        except AttributeError:
            print ('check #00001. Error in line, no table-game.')
            return False
        match = []
        a_t_g=True
        for td in all_table:
            if a_t_g:
                if 'stage-finished' in td.get('class'):
                    test = td.find('td',class_='score').text
                    # print (name_chemp, '\n', 'КУБОК' in name_chemp.upper())
                    test2 = test.split(':')
                    test2[0]=test2[0].replace('\\xa0', '').strip()
                    test2[1]=test2[1].replace('\\xa0', '').strip()
                    if test[0] == test[-1] or test2[0]==test2[1]:
                        a_t_g=False
                    else:
                        match.append(test2[0]+' : '+test2[1])
        all_game = []
        for td2 in all_table:
            if 'stage-finished' in td2.get('class'):
                test_2 = td2.find('td',class_='score').text
                test2_2 = test_2.split(':')
                test2_2[0]=test2_2[0].replace('\\xa0', '').strip()
                test2_2[1]=test2_2[1].replace('\\xa0', '').strip()
                all_game.append(test2_2[0]+':'+test2_2[1])
        draw = 0
        for a_g in all_game:
            if 'stage-finished' in td.get('class'):
                a_g=a_g.split(':')
                if a_g[0]==a_g[1]:
                    draw+=1
        print ('Name: ',name_chemp)
        print ('URL: ',driver.current_url)
        try:
            print ('Средний показатель: ',round(len(all_game) / draw,3) )
        except ZeroDivisionError:
            print ('Средний показатель: ',len(all_game) )
        print ('Уже сыграно игр без ничьих: ',len(match))
        print ('_______________________\n\n')

    # # новый цикл отбор 7+ ничьтх
    # soup.find('div',class_="page-tabs").find('li',class_="li1 ")





def strategy_st(driver):
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    name_chemp = soup.find('div',class_='tournament-name').text
    try:
        table_next_day = soup.find('div',id="fs-summary-fixtures").find('tbody').find_all('tr')
    except AttributeError:
        print ('AttributeError: ',name_chemp, '    (при просмотре расписания игр)')
        return False
    last = table_next_day[0].text
    go = False
    true_game = 0
    all_game = 0
    for td in table_next_day:
        try:
            today=td.find('td',class_="cell_ad").text
        except:
            continue
        if go:
            all_game+=1
            today = today.split()
            try:
                last = last.split()
            except:
                pass
            today[1] = today[1].split(':')
            try:
                last[1] = last[1].split(':')
            except AttributeError:
                pass
            re_today = (int(today[1][0])*60)+int(today[1][1])
            re_last = (int(last[1][0])*60)+int(last[1][1])
            re_true = re_last+110
            if today[0]!=last[0]:
                true_game+=1
            elif re_today>=re_true:
                true_game +=1
        last = today
        if go == False:
            go = True
    if true_game==all_game:
        print (driver.current_url)
    else:
        print (true_game, '  ' ,all_game)
def show_game_show2(driver,num2):#игры которы показать игры(*)
    xpath = '//*[@id="live-table"]/div[3]/div[{}]/div[1]/span[1]'.format(num2)
    try:
        driver.find_element_by_xpath(xpath).click()
    except:
        xpath = '//*[@id="live-table"]/div[3]/div[{}]/div[1]/span[1]'.format(num2+1)
        driver.find_element_by_xpath(xpath).click()
def show_game_show(driver,num2):
    xpath = '//*[@id="live-table"]/div[3]/div[{}]/div[2]/span[1]'.format(num2)

    try:
        driver.find_element_by_xpath(xpath).click()
    except:
        xpath = '//*[@id="live-table"]/div[3]/div[{}]/div[2]/span[1]'.format(num2+1)
        driver.find_element_by_xpath(xpath).click()
def get_all_game(driver):
    time.sleep(4)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    tds=soup.find('div', id="live-table").find('div',class_="event").find_all('div')
    tds2=[]
    gold = "event__header top"
    show_games = 'event__header'
    test=0
    n_show_games = 'event__header event__header--no-my-games'
    for td in tds:
        if show_games in td.get('class'):
            tds2.append(td)
        elif 'event__match' in td.get('class'):
            tds2.append(td)
    for td2,id in zip(tds2,range(len(tds2))):
        if show_games in td2.get('class'):
            if 'event__header--no-my-games' in td2.get('class'):
                # print (id)
                show_game_show2(driver,id+1)
                test+=1
            elif show_games in td2.get('class'):
                # print (id)
                show_game_show(driver,id+1)
                test+=1
            # xpath = '//*[@id="live-table"]/div[3]/div[6]/div[1]/span[1]'
            # driver.find_element_by_xpath(xpath).click()
            strategy_st2(driver)
            # return False
            driver.get('https://www.myscore.com.ua/')
            print (test)
            # driver.back()
            time.sleep(1)
    print (test)

def connecet():
    data_arr = read_day()
    data_day = data_arr[0]
    folder = path.dirname(__file__)
    folder = folder[:folder.rfind('\\')]
    url = 'https://www.myscore.com.ua/'
    driver = webdriver.Chrome(executable_path=folder+r'\\chromedriver.exe')
    driver.get(url)
    new_day(driver,data_arr[1])
    time.sleep(4)
    return driver

def main():
    driver = connecet()
    get_all_game(driver)
    driver.close()


if __name__ =='__main__':
    main()
