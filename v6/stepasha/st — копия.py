from selenium import webdriver
from bs4 import BeautifulSoup
from os import path , makedirs
import time
import csv
#Исправить стратегию с кликами. Кликает не на те игры. смотреть сколько игр+табличка и следуая цифра клика. может проблема в функции которая кликает.

def strategy_st2(driver):
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    try:
        table_today = soup.find('div',id="fs").find('tbody').find_all('tr')
    except AttributeError:
        print ('AttributeError: ',name_chemp, '    (при просмотре сегодняшних игр)')
        return False
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
            if today[0]!=last[0]:
                true_game+=1
            elif re_today>=re_true:
                true_game +=1
        last = today
        if go == False:
            go = True
    if true_game==all_game:
    # print (driver.current_url, true_game, '   ' ,all_game)
    # новый цикл отбор 7+ ничьтх
    # soup.find('div',class_="page-tabs").find('li',class_="li1 ")
    driver.find_element_by_class_name('li1 ').click()
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    all_table=soup.find('div',id="fs-results").find('tbody').find_all('tr')
    match = []
    a_t_g=True
    for td in all_table:
        if a_t_g:
            if 'stage-finished' in td.get('class'):
                test = td.find('td',class_='score').text
                test2 = test.split(':')
                test2[0]=test2[0].replace('\\xa0', '').strip()
                test2[1]=test2[1].replace('\\xa0', '').strip()
                if test[0] == test[-1] or test2[0]==test2[1]:
                    print(len(match))
                    print ('okkk')
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
    print (round(len(all_game) / draw,3) )





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
    driver.find_element_by_xpath(xpath).click()
def show_game_show(driver,num2):
    xpath = '//*[@id="live-table"]/div[3]/div[{}]/div[2]/span[1]'.format(num2)
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
                 show_game_show2(driver,id+1)
                 test+=1
            elif 'event__header' in td2.get('class'):
                show_game_show(driver,id+1)
                test+=1
            # strategy_st(driver)
            strategy_st2(driver)
            return False
            driver.get('https://www.myscore.com.ua/')
            time.sleep(1)
    print (test)

def connecet():
    folder = path.dirname(__file__)
    folder = folder[:folder.rfind('\\')]
    url = 'https://www.myscore.com.ua/'
    driver = webdriver.Chrome(executable_path=folder+r'\\chromedriver.exe')
    driver.get(url)
    time.sleep(2)
    return driver

def main():
    driver=connecet()
    get_all_game(driver)
    driver.close()


if __name__ =='__main__':
    main()
