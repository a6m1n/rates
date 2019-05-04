from selenium import webdriver
from bs4 import BeautifulSoup
from os import path , makedirs
import time
import csv

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


def make_dir(name):
    folder = path.dirname(__file__)
    path_add = 'result\\month\\march'
    data_path = folder + '\\' + path_add
    if not path.exists(data_path + '\\' + name):
        print ('create:   {}'.format(data_path + '\\' + name))
        makedirs(data_path+ '\\' + name) #5


def write_csv(input_string, data):
    make_dir(data)
    a = path.dirname(__file__)
    folder = a + '\\result\\month\\march\\' + data
    with open (folder+'\\{}.csv'.format(data), 'a', encoding='utf-8',  newline='') as f:
        writer = csv.writer(f)
        if int(input_string[-1]['id'])==1:
            writer.writerow(('id','country','team','strategy 2','strategy 1','time','link','goal in first time','team that scored','Both scored','result in first time','result in all time'))
        for string in input_string:
            writer.writerow((string['id'],string['country'],string['team'],string['strategy 2'],string['strategy 1'],string['time'],string['link']))
    f.closed #5

def all_info(driver,url,id,point_arr,rst_1,data_day):
    res_name = ''
    test = 1
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    name = soup.find('div', class_="fleft").text
    if name.rfind('-')==name.find('-'):
        name=name[:name.rfind('-')].strip()
    else:
        name=name[:name.rfind('-')].strip()
    team = soup.find_all('a',class_="participant-imglink")
    for t in team:
        res_name += t.text.strip()
        if test==2:
            res_name +=' - '
        test+=1
    time_game = soup.find('div', id="utime").text

    arr = [{'id':id,'country':name,'team':res_name,'strategy 2':point_arr,'strategy 1':rst_1,'time':time_game,'link':url}]
    write_csv(arr,data_day) #4

def get_res(driver, name_team):
    time.sleep(1)
    try:
        html = driver.page_source
    except:
        return False
    soup = BeautifulSoup(html, 'lxml')
    score = soup.find('div',class_="detailMS__headerScore")
    try:
        home_team_goal = score.find('span',class_="p1_home").text.strip()
    except:
        return False
    try:
        away_team_goal = score.find('span', class_='p1_away').text.strip()
    except:
        return False
    find_name=soup.find_all('a', class_="participant-imglink")
    for f in range(len(find_name)):
        find_name[f]=find_name[f].text.strip()
        find_name[f]=find_name[f].upper()
        if find_name[f].find('(')>0 and '(Ж)' not in find_name[f]:

            find_name[f]=find_name[f][:find_name[f].find('(')]
            find_name[f]=find_name[f].strip()

    if name_team == find_name[1]:
        try:
            dict_get_res={find_name[1]:int(home_team_goal)}
        except:
            return False
    elif name_team == find_name[3]:
        try:
            dict_get_res={find_name[3]:int(away_team_goal)}
        except:
            return False
    else:
        dict_get_res={}
        print (name_team, find_name)
        print ('\n\n\n ERROR IN FUNCTION get_res \n\n\n')
        return False
    return dict_get_res #2

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
                if len(g)>10 and gg == '(0 : 0)':
                    return False
            except:
                return False
            if g.strip() == '0 : 0':
                return False
    h2h_meeting = all_table[-1]
    game_h2h = h2h_meeting.find('tbody').find_all('tr')[:5]
    if len(game_h2h) < 4:
        return False
    for g in game_h2h:
        try:
            g = g.find('span', class_='score').text
            gg= g[g.find('('):]
            # print (gg)
            if len(g)>10 and gg == '(0 : 0)':
                # print ('false')
                return False
        except:
            return False
        if g.strip() == '0 : 0':
            return False
    return True #2

def get_all_game(driver):
    all_goal = {}
    time.sleep(1.2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    all_table = soup.find_all('div',class_="h2h-wrapper" )[:3]
    if click_show_more_game(driver):
        for i in range(2):
            name_team =all_table[i].find('td').text[16:]
            all_goal[name_team] = 0
            game = all_table[i].find('tbody').find_all('tr')[:10]
            for g in range(len(game)):
                try:
                    xpath = '//*[@id="tab-h2h-overall"]/div[{}]/table/tbody/tr[{}]'.format(i+1,g+1)
                    driver.find_element_by_xpath(xpath).click()
                except:
                    xpath = '//*[@id="tab-h2h-overall"]/div[{}]/table/tbody/tr[47]/td/a'.format(i+1)
                    try:
                        driver.find_element_by_xpath(xpath).click()
                    except:
                        return False
                window_before2 = driver.window_handles[1]
                driver.switch_to_window(driver.window_handles[-1])
                result_get_res = get_res(driver,name_team)
                if result_get_res:
                    if result_get_res[name_team] == 1:
                        all_goal[name_team]=all_goal.setdefault(name_team)+1
                    elif result_get_res[name_team] >= 2:
                        all_goal[name_team]=all_goal.setdefault(name_team)+1
                    elif result_get_res[name_team] ==0:
                        pass
                    else:
                        print ('Error')
                    driver.close()
                    driver.switch_to_window(window_before2)
                else:
                    driver.close()
                    driver.switch_to_window(window_before2)
                    return False
        print (all_goal, '\n\n')
        return all_goal #2

def strategy_1(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    all_table = soup.find_all('div',class_="h2h-wrapper" )[:3]
    team_1_point = team_1(driver,all_table[0])
    team_2_point = team_1(driver,all_table[1])
    output = result(team_1_point, team_2_point)
    return output

def team_1(driver,all_table):
    name_team =all_table.find('td').text[16:]
    game = all_table.find('tbody').find_all('tr')[:5]
    point = {'Name':name_team,
             'Ball in his field': 0,                #Забитый мяч на своем поле – 1 очко;
             'Ball on foreign field':0,             #Забитый мяч на чужом поле – 2 очка;
             'Missed ball in his field':0,          #Пропущенный мяч на своем поле – 2 очка;
             'Missed ball on foreign field':0}      #Пропущенный мяч на чужом поле – 1 очко;
    for g in game:
        g_or_h = g.find_all(class_="name")
        try:
            home_team = g_or_h[0].text
        except IndexError:
            continue

        try:
            guest_team = g_or_h[1].text
        except IndexError:
            continue

        score = g.find(class_="score").text
        if len(score)>7:
            score = score[:5]
        if name_team == home_team.upper():
            try:
                reult_goal = int(score[:score.find(':')])
            except:
                continue
            try:
                result_feed =  int(score[score.find(':')+1:])*2
            except:
                continue
            point['Ball in his field'] = reult_goal
            point['Missed ball in his field'] += result_feed

        elif name_team == guest_team.upper():
            try:
                reult_goal = int(score[:score.find(':')])
            except:
                continue
            try:
                result_feed =  int(score[score.find(':')+1:])*2
            except:
                continue
            point['Ball on foreign field'] += reult_goal
            point['Missed ball on foreign field'] += result_feed
    return point

def result(team_1, team_2):
    if team_1['Ball in his field']==0:
        sum_res_team_1_1 = 0
    elif team_2['Missed ball on foreign field']==0:
        sum_res_team_1_1 = team_1['Ball in his field']
    else:
        sum_res_team_1_1 = team_1['Ball in his field']/team_2['Missed ball on foreign field']
    if team_1['Ball on foreign field'] == 0:
        sum_res_team_1_2 = 0
    elif team_2['Missed ball in his field'] == 0:
        sum_res_team_1_2 = team_1['Ball on foreign field']
    else:
        sum_res_team_1_2 = team_1['Ball on foreign field']/team_2['Missed ball in his field']
    if team_2['Ball in his field'] == 0:
        sum_res_team_2_1 = 0
    elif team_1['Missed ball on foreign field'] == 0:
        sum_res_team_2_1 = team_2['Ball in his field']
    else:
        sum_res_team_2_1 = team_2['Ball in his field']/team_1['Missed ball on foreign field']
    if team_2['Ball on foreign field'] == 0:
        sum_res_team_2_2 = 0
    elif team_1['Missed ball in his field'] == 0 :
        sum_res_team_2_2 = team_2['Ball on foreign field']
    else:
        sum_res_team_2_2 = team_2['Ball on foreign field']/team_1['Missed ball in his field']
    result_team_1 = sum_res_team_1_1 + sum_res_team_1_2
    result_team_2 = sum_res_team_2_1 + sum_res_team_2_2

    output_value = {team_1['Name']:round(result_team_1,2),
                     team_2['Name']:round(result_team_2,2)
                    }
    return output_value


def is_ready_id(driver, element):
    try:
        time.sleep(2)
        driver.find_element_by_id(element).click()
    except:
        is_ready_id(driver, element)#1

def chek_one_game(id,driver,data_day):
    id2=0
    for i in id:
        is_ready_id(driver,i)
        window_before = driver.window_handles[0]
        driver.switch_to_window(driver.window_handles[-1])
        url = driver.current_url
        is_ready_id(driver,'a-match-head-2-head')
        pont_goal = get_all_game(driver)
        rst_1 = strategy_1(driver)
        if pont_goal:
            all_info(driver,url,id2+1,pont_goal,rst_1,data_day)
            id2+=1
            driver.close()
            driver.switch_to_window(window_before)
        else:
            driver.close()
            driver.switch_to_window(window_before) #1


def filter(name):
    true_country = [
 'МИР: Международные товарищеские матчи - женщины','МИР: Клубные товарищеские матчи','МИР: Международные товарищеские матчи',
 'МИР: SheBelieves Cup Women'
]
    # for i in true_country:
    if name not in true_country:
        return True #1


def get_need_game_upgrage(driver):
    time.sleep(2)
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
    main()
    # print (path.dirname(__file__))
