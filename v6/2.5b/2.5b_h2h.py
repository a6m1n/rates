from selenium import webdriver
from bs4 import BeautifulSoup
from os import path
import time
import csv
def write_csv(input_string,data_day):
    a = path.dirname(__file__)
    a = a[:a.rfind('\\')]
    folder = a + '\\result\\month\\april\\' + data_day
    with open (folder+'\\{}_2.5b_h2h.csv'.format(data_day), 'a', encoding='utf-8',  newline='') as f:
        writer = csv.writer(f)
        if int(input_string['id'])==1:
            writer.writerow(('id','team','point','link','result in all time'))
        writer.writerow((input_string['id'],input_string['team'],input_string['point'],input_string['link']))
    f.closed #5
def result(res_two_5_b,id2,link,data_day):
    res=[]
    res_name=[]
    data={}
    for key,value in res_two_5_b.items():
        try:
            value=value.split(':')
        except AttributeError:
            return False
        try:
            result=int(value[0])/int(value[1])
        except ZeroDivisionError:
            return False
        res.append(result)
        res_name.append(key)
    res_name=res_name[0]+' - '+res_name[1]
    res=res[0]+res[1]
    data[res_name]=round(res,2)
    data={'id':str(id2),'team':res_name,'point':str(round(res,2)),'link':link}
    print (data)
    write_csv(data,data_day)
def two_5_b(driver):
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('div',id="tab-h2h-home").find('div',class_="h2h-wrapper").find('tbody').find_all('tr')[:12]
    home={'goal':0,'los':0}
    for td in tds:
        score_game=td.find('span',class_="score").text.strip()
        if len(score_game)>7:
            score_game = score_game[:score_game.find('(')]
        try:
            home['goal']+=int(score_game[0])
        except:
            return False
        try:
            home['los']+=int(score_game[-1])
        except:
            return False
    tds = soup.find('div',id="tab-h2h-away").find('div',class_="h2h-wrapper").find('tbody').find_all('tr')[:12]
    away={'goal':0,'los':0}
    for td in tds:
        score_game=td.find('span',class_="score").text.strip()
        if len(score_game)>7:
            score_game = score_game[:score_game.find('(')]
        try:
            away['goal']+=int(score_game[0])
        except:
            return False
        try:
            away['los']+=int(score_game[-1])
        except:
            return False #тут ошибка
    res_home = str(home['goal'])+' : '+str(home['los'])
    res_away =str(away['goal'])+' : '+str(away['los'])
    home_name=soup.find('div', class_="home-box").find('div',class_='tname__text').text.strip()
    away_name=soup.find('div', class_="away-box").find('div',class_='tname__text').text.strip()
    res={home_name:res_home,away_name:res_away}
    return res
def is_ready_id(driver, element,id=0):
    try:
        time.sleep(2)
        if id>10:
            print ('\n'*2,'Eror #00001',driver.current_url, '\n'*2)
            return False
        driver.find_element_by_id(element).click()
        return True
    except:
        id+=1
        is_ready_id(driver, element,id)#1
def chek_one_game(id,driver,data_day):
    id2=1
    for i in id:
        is_ready_id(driver,i)
        window_before = driver.window_handles[0]
        driver.switch_to_window(driver.window_handles[-1])
        try:
            url = driver.current_url
        except Traceback:
            continue
        is_ready_id(driver,'a-match-head-2-head')
        pont_goal = get_all_game(driver)
        if pont_goal:
            res_two_5_b=two_5_b(driver)
            if res_two_5_b:
                result(res_two_5_b,id2,url,data_day)
                id2+=1
                driver.close()
                driver.switch_to_window(window_before) #1
            else:
                driver.close()
                driver.switch_to_window(window_before)
        else:
            driver.close()
            driver.switch_to_window(window_before) #1
def get_need_game_upgrage(driver):
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('div', id="live-table").find('div',class_="event")
    id=[]
    for td in tds:
        a = td.get('id')
        if a!=None:
            id.append(a)

        try:
            b = td.find('div', class_='icon--flag').text
        except AttributeError:
            continue
    return id
def get_all_game(driver):
    time.sleep(1.2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    all_table = soup.find_all('div',class_="h2h-wrapper" )[:3]
    if click_show_more_game(driver):
        for i in range(2):
            if null_null(driver):
                return True
def click_show_more_game(driver):
    test = 1
    all_tbody=[]
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    home_team = soup.find('table', class_="head_to_head h2h_home").find('tbody')
    away_team =  soup.find('table', class_="head_to_head h2h_away").find('tbody')
    all_tbody.append(home_team)
    all_tbody.append(away_team)
    for a_t in all_tbody:
        tr_find = a_t.find_all('tr')
        if test==1:
            first_range = len(tr_find)
            xpath='//*[@id="tab-h2h-overall"]/div[1]/table/tbody/tr[{}]/td/a'.format(first_range)
            try:
                driver.find_element_by_xpath(xpath).click()
            except:
                return False

        elif test==2:
            two_range = len(tr_find)
            xpath='//*[@id="tab-h2h-overall"]/div[2]/table/tbody/tr[{}]/td/a'.format(two_range)
            try:
                driver.find_element_by_xpath(xpath).click()
            except:
                return False
        test+=1 #2
    return True
def null_null(driver): #раньше было game
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    all_table = soup.find_all('div',class_="h2h-wrapper" )[:3]
    for i in range(2):
        game = all_table[i].find('tbody').find_all('tr')[:10]
        for g in game:
            try:
                g = g.find('span', class_='score').text
                gg= g[g.find('('):]
                if len(g)<10 and gg=='(0 : 0)':
                    return False
            except:
                return False
            if g.strip() == '0 : 0' or gg == '(0 : 0)' or gg=='0 : 0':
                return False
    h2h_meeting = all_table[-1]
    game_h2h = h2h_meeting.find('tbody').find_all('tr')[:5]
    if len(game_h2h) < 4:
        return False
    for g in game_h2h:
        try:
            g = g.find('span', class_='score').text
            gg= g[g.find('('):]
            if len(g)<10 and gg =='(0 : 0)':
                return False
        except:
            return False
        if g.strip() == '0 : 0':
            return False
    return True #2
def read_day():
    folder = path.dirname(__file__)
    folder = folder[:folder.rfind('\\')]
    f = open(folder+'\\data.txt', 'r')
    data_arr = []
    for line in f:
        data_arr.append(line.strip())
    f.close()
    return data_arr

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

def main():
    data_arr = read_day()
    data_day = data_arr[0]
    folder = path.dirname(__file__)
    folder = folder[:folder.rfind('\\')]
    url = 'https://www.myscore.com.ua/'
    driver = webdriver.Chrome(executable_path=folder+r'\\chromedriver.exe')
    driver.get(url)
    new_day(driver,data_arr[1])
    time.sleep(5)
    id = get_need_game_upgrage(driver)
    chek_one_game(id,driver,data_day)
    driver.close() #1
if __name__ == '__main__':
    print ('start 2.5b_h2h')
    main()
