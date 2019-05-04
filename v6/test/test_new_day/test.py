from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time



def read_day():
    folder = os.path.dirname(__file__)
    # folder = path.dirname(__file__)
    # folder = folder[:folder.rfind('\\')]
    f = open(folder+'\\data.txt', 'r')
    data_arr = []
    for line in f:
        data_arr.append(line.strip())
    f.close()
    return data_arr


def start(data):
    a = input('Data[0] exaple 01.01.2019: ')
    f = open('data.txt', 'w')
    f.write(a+'\n')
    f.write(data)
    f.close()

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
    data = input('exaple: 01/01:\n')
    start(data)
    data_arr = read_day()
    data_day = data_arr[0]
    folder = os.path.dirname(__file__)
    folder = folder[:folder.rfind('\\')]
    url = 'https://www.myscore.com.ua/'
    driver = webdriver.Chrome(executable_path=folder+'\\chromedriver.exe')
    driver.get(url)
    new_day(driver,data_arr[1])
    driver.close()

if __name__ == '__main__':
    main()
# нью дей
# рид дей
# 2-3 строчки маина
# вызов нью дей
