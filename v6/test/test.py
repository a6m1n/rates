from selenium import webdriver
from bs4 import BeautifulSoup
from os import path, makedirs
import time
import csv


def write_csv(input_string, data):
    folder = path.dirname(__file__)
    with open (folder+'\\{}.csv'.format(data), 'a', encoding='utf-8',  newline='') as f:
        writer = csv.writer(f)
        if int(input_string[-1]['id'])==1:
            writer.writerow(('id','country','team','point','time','link','goal in first time','team that scored','Both scored','result in first time','result in all time'))

        for string in input_string:
            writer.writerow((string['id'],string['country'],string['team'],string['point'],string['time'],string['link']))
    f.closed #3 #Запись в .csv

def all_info(driver,url,id,point_arr,data_day):
    res_name = ''
    test = 1
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    name = soup.find('div', class_="fleft").text
    if name.rfind('-')==name.find('-'):
        name = name[:name.rfind('-')].strip()
    else:
        name = name[:name.rfind('-')].strip()
    team = soup.find_all('a',class_="participant-imglink")
    for t in team:
        res_name += t.text.strip()
        if test == 2:
            res_name += ' - '
        test += 1
    time_game = soup.find('div', id="utime").text

    arr = [{'id':id, 'country':name, 'team':res_name, 'point':point_arr, 'time':time_game, 'link':url }]
    write_csv(arr,data_day) #4

def get_res(driver, name_team):
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    score = soup.find('div',class_="detailMS__headerScore")
    try:
        home_team_goal = score.find('span',class_="p1_home").text.strip()
    except:
        return False
    away_team_goal = score.find('span', class_='p1_away').text.strip()
    find_name = soup.find_all('a', class_="participant-imglink")
    for f in range(len(find_name)):
        find_name[f]=find_name[f].text.strip()
        find_name[f]=find_name[f].upper()
        if find_name[f].find('(')>0 and '(Ж)' not in find_name[f]:

            find_name[f]=find_name[f][:find_name[f].find('(')]
            find_name[f]=find_name[f].strip()

    if name_team == find_name[1]:
        dict_get_res = {find_name[1]:int(home_team_goal)}
    elif name_team == find_name[3]:
        dict_get_res = {find_name[3]:int(away_team_goal)}
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
        if test == 1:
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
                if len(g)<10 and gg ==('0 : 0'):
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
            if len(g)<10 and gg ==('0 : 0'):
                return False
        except:
            return False
        if g.strip() == '0 : 0':
            return False
    return True #2

def get_need_game_upgrage(driver):
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('div', id="fs").find_all('table')
    id=[]
    for td in tds:
        a=td.find('tbody')
        name_country =  td.find('span', class_="country_part").text + td.find('span', class_="tournament_part").text
        if filter(name_country):
            a=td.find('tbody')
            if a==None:
                pass
            else:
                try:
                    d = td.find('tbody').find_all('tr')
                    for b in a:
                        id.append(str(b.get('id')))
                except:
                    d=td.find('tbody').find('tr').get('id')
                    id.append(str(d.get('id')))
                    print(str(d.get('id')))
    return id

def get_all_game(driver):
    all_goal = {}
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    all_table = soup.find_all('div',class_="h2h-wrapper" )[:3]
    if click_show_more_game(driver):
        for i in range(2):
            name_team =all_table[i].find('td').text[16:]
            all_goal[name_team] = 0
            game = all_table[i].find('tbody').find_all('tr')[:10]
            if null_null(driver):
                for g in range(len(game)):
                    try:
                        xpath = '//*[@id="tab-h2h-overall"]/div[{}]/table/tbody/tr[{}]'.format(i+1,g+1)
                        driver.find_element_by_xpath(xpath).click()
                    except:
                        xpath = '//*[@id="tab-h2h-overall"]/div[{}]/table/tbody/tr[47]/td/a'.format(i+1)
                        driver.find_element_by_xpath(xpath).click()
                    window_before2 = driver.window_handles[1]
                    driver.switch_to_window(driver.window_handles[-1])
                    result_get_res = get_res(driver,name_team)
                    if result_get_res:
                        if result_get_res[name_team] == 1:
                            all_goal[name_team] = all_goal.setdefault(name_team)+1
                        elif result_get_res[name_team] >= 2:
                            all_goal[name_team] = all_goal.setdefault(name_team)+1
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

            else:
                return False
        print (all_goal, '\n\n')
        return all_goal #2

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
        if pont_goal:
            all_info(driver,url,id2+1,pont_goal,data_day)
            id2+=1
            driver.close()
            driver.switch_to_window(window_before)
        else:
            driver.close()
            driver.switch_to_window(window_before) #1


def filter(name):
    true_country = ['ЕГИПЕТ: Премьер-лига']
    if name not in true_country:
        print (name)
        return True #1
    else:
        return False


#отключил эту функцию. А так она нужна для показа всех игр.
def click_show_all_game(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('div', id="fs").find_all('table',class_="soccer")
    for td in tds:
        a=td.find('tbody')
        if a==None:
            driver.find_element_by_class_name('expand-league-link').click()
        else:
            pass #1
# __________________________________________________________
def main():
    data_day = '2'
    folder = path.dirname(__file__)
    url = 'https://www.myscore.com.ua/'
    driver = webdriver.Chrome(executable_path=folder+r'\\chromedriver.exe')
    driver.get(url)
    time.sleep(5)
    id = get_need_game_upgrage(driver)
    chek_one_game(id,driver,data_day)
    time.sleep(10)
    driver.close() #1


if __name__ == '__main__':
    # token = bot.bin.misc_bot_st.misc_t_bot
    # url_bot_teleram = 'https://api.telegram.org/bot'+token+'/'
    # # botself.bod.new_day(url_bot_teleram)
    main()
