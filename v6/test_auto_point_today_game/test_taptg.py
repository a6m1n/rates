import os
import csv
import re

def next3(point_and_id):
    text=[]
    p=[]
    name_chemp =[]
    f = open('text.txt', 'r') #написать не .техт  а сцв формат. нужно сделдать словарь: {'Имя команды 1, имая команды 2': "очки"}
    for line in f:
        text.append(line)
    for t in text:
        name_chemp.append( t.strip() )
        f = t.rfind('-')
        t=t[f+2:]
        t=t.strip()
        p.append(t)
    for i,j in zip(p,name_chemp):
        for key,value in point_and_id.items():
            if int(i)==int(key) and int(i)==9  or int(i)==5 and int(i)==int(key) or int(i)==4 and int(i)==int(key) or int(i)==6 and int(i)==int(key) or int(i)==13 and int(i)==int(key) or int(i)==14 and int(i)==int(key):
                print (int(value*100),i,j)

def next2():
    a = os.path.dirname(__file__)
    file = 'one,two'
    with open (a+'\\{}.csv'.format(file), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        id = 0
        id1=[]
        id2=[]
        for line in reader:
            id+=1
            if id==3:
                continue
            for key,value in line.items():
                if id==1 and value != '0':
                    id1.append({key:value})
            for idsh in id1:
                for key2,value2 in idsh.items():
                    for key3,value3 in line.items():
                        if key2==key3 and id==2:
                            id2.append({key3:value3})
                        # if id==2 and key3==key2:

                # print (type(value))
    f.closed
    # print (id1) #all game
    # print (id2) #goal in first time
    point_and_id = {}
    for idsh1,idsh2 in zip(id1,id2):
        for key1,value1 in idsh1.items():
            for key2,value2 in idsh2.items():
                if key1==key2:
                    # print(key2,round(int(value2)/int(value1),2))
                    point_and_id[key2]=round(int(value2)/int(value1),2)
                    continue
    return point_and_id

def next1(t):
    point = []
    name = []
    for i in t:
        j = i.split(',')
        f = j[0].find(':')
        m = j[1].find(':')
        j[0] = j[0][f+2:]
        j[1] = j[1][m+2:]
        point.append(int (j[0]) + int (j[1]))

    for name_team in t:
        name_team = re.sub('\'','',name_team)
        name_team = name_team.split(',')
        f = name_team[0].find(':')
        m = name_team[1].find(':')
        name_team[0] = name_team[0][:f]
        name_team[1] = name_team[1][:m]
        name.append(name_team[0]+' , '+name_team[1])

    for j,h in zip(name,point):
        print (j,h)
        f = open('text.txt', 'a')
        f.write(j +' - ' +str(h) + '\n')

def read_point_today(day):
    test=[]
    folder = r'C:\Users\Артем\Desktop\work\dev\python\Rates\v2\v5\test_auto_point_today_game\\'+day
    with open (folder+'.csv', 'r', encoding='utf-8') as f:
     reader = csv.DictReader(f)
     for line in reader:
         test.append(line['strategy 2'][1:-1])
     return test

def main():
    day = '27.03.2019'
    t=read_point_today(day)
    # next1(t)
    point_and_id=next2()
    next3(point_and_id)

if __name__=='__main__':
    main()
