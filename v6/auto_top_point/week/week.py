import os
import csv
import re
import time

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
    if os.path.isdir(os.path.join(a_dir, name))]

def del_all_garbage(dd):
    for i in dd:
        for k,v in i.items():
            if v==0:
                dd[0]=removekey(dd[0],k)
                dd[1]=removekey(dd[1],k)
                dd[2]=removekey(dd[2],k)
        break
    return dd


def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def get_data_folder():
    a = os.path.dirname(__file__)
    a = a[:a.rfind('\\')]
    a = a[:a.rfind('\\')]
    folder = a+'\\result\\month\\april'
    res_get_immediate_subdirectories = get_immediate_subdirectories(folder)
    return res_get_immediate_subdirectories

def reed_point(data):
    results = []
    goal = []
    dd = {}
    a=os.path.dirname(__file__)
    a=a[:a.rfind('\\')]
    folder=a[:a.rfind('\\')]+'\\result\\month\\april\\'+data
    with open (folder+'\\{}_new.csv'.format(data), 'r', encoding='utf-8') as f:
     reader = csv.DictReader(f)
     for line in reader:
         results.append(line['strategy 2'][1:-1])
         goal.append(line['goal in first time'])
         dd[line['strategy 2'][1:-1]] = line['goal in first time']
    f.closed
    return dd

def point_game(bg_data):
    res_bg_data = {}
    b=[]
    for i in range(len(bg_data)):
        for j,g in zip(bg_data[i],bg_data[i]):
            res_sm_data={}
            j=re.sub('\'','',j)
            j=j.split(',')
            f = j[0].find(':')
            m = j[1].find(':')
            j[0]=j[0][f+2:]
            j[1]=j[1][m+2:]
            a=int(j[0])+int(j[1])
            res_sm_data[a]=bg_data[i][g]
            b.append(res_sm_data)
    return b

def read_bfd_goal(bfd):
    data_num = {'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,
            '11':0,'12':0,'13':0,'14':0,'15':0,'16':0,'17':0,'18':0,'19':0,'20':0,}
    #j=цифры, i[j] = YES|NO, i = all
    for i in bfd:
        for j in i:
            for h in data_num:
                if h==str(j) and i[j]=='Yes':
                    data_num[h]+=1
    return data_num

def read_bfd_no_goal(bfd):
    data_num = {'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,
            '11':0,'12':0,'13':0,'14':0,'15':0,'16':0,'17':0,'18':0,'19':0,'20':0,}
    #j=цифры, i[j] = YES|NO, i = all
    for i in bfd:
        for j in i:
            for h in data_num:
                if h==str(j) and i[j]=='No':
                    data_num[h]+=1
    return data_num

def read_bfd_all(bfd):
    data_num = {'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,
            '11':0,'12':0,'13':0,'14':0,'15':0,'16':0,'17':0,'18':0,'19':0,'20':0,}
    #j=цифры, i[j] = YES|NO, i = all
    for i in bfd:
        for j in i:
            for h in data_num:
                if h==str(j):
                    data_num[h]+=1
    return data_num

def write_csv(input_string,start):
    folder = os.path.dirname(__file__)
    print (folder)
    with open (folder+'.csv', 'a', encoding='utf-8',  newline='') as f:
        writer = csv.writer(f)
        if start:
            writer.writerow(('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20'))
            start = False
        for i in input_string:
            writer.writerow((i['1'],i['2'],i['3'],i['4'],i['5'],i['6'],i['7'],i['8'],i['9'],i['10'],
                    i['11'],i['12'],i['13'],i['14'],i['15'],i['16'],i['17'],i['18'],i['19'],i['20']))
    f.closed

def test(bgd):
    # i[j]=yes|no j=name
    all_data = []
    b_fucking_arr = []
    b_fucking_data = {}
    for i in range(11):
        for j in range(11):
            log = str(i)+' : '+str(j)
            b_fucking_data[log]=0
    for i in bgd:
        for j,g in zip(i,i):
            dict_fuck_res = {}
            j=j.split(',')
            f = j[0].find(':')
            m = j[1].find(':')
            j[0]=j[0][f+2:]
            j[1]=j[1][m+2:]
            res = j[0]+' : '+j[1]
            dict_fuck_res[res] = i[g]
            b_fucking_arr.append(dict_fuck_res)
    #d = num. 0 : 0
    louse_fucking_data = {}
    for f in b_fucking_arr:
        for s in f:
            for d in b_fucking_data:
                if s==d and f[s]=='Yes':
                    b_fucking_data[d]+=1

    all_data.append(test_all(b_fucking_arr))
    all_data.append(b_fucking_data)
    all_data.append(test_no_goal(b_fucking_arr))
    all_data=del_all_garbage(all_data)
    write_csv2(all_data)


def test_no_goal(bfd):
    b_fucking_data = {}
    for i in range(11):
        for j in range(11):
            log = str(i)+' : '+str(j)
            b_fucking_data[log]=0

    for f in bfd:
        for s in f:
            for d in b_fucking_data:
                if s==d and f[s]=='No':
                    b_fucking_data[d]+=1
    return b_fucking_data

def test_all(bfd):
    b_fucking_data = {}
    for i in range(11):
        for j in range(11):
            log = str(i)+' : '+str(j)
            b_fucking_data[log]=0

    for f in bfd:
        for s in f:
            for d in b_fucking_data:
                if s==d:
                    b_fucking_data[d]+=1
    return b_fucking_data

def write_csv2(input_string):
    start = True
    folder = os.path.dirname(__file__)
    print (folder)
    b_fucking_data = {}
    for i in range(11):
        for j in range(11):
            log = str(i)+' : '+str(j)
            b_fucking_data[log]=0
    with open (folder+'_april.csv', 'a', encoding='utf-8',  newline='') as f:
        for i in input_string:
            fieldnames = [x for x in i]
            break
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for string in input_string:
             writer.writerow(string)
    f.closed

def start():
    ddd=True
    bg_data = []
    gdf = get_data_folder()
    for i in gdf:
        for j in range(1,32):
            # if j > 14:
                # ddd = False
            # else:
                # ddd=True
            if j < 10:
                j = "0" + str(j)
            data = '{}.03.2019'.format(j)
            if  i == data and ddd :
                print (i)
                bg_data.append(reed_point(i))
    bg_new_data = point_game(bg_data)
    rb0=read_bfd_all(bg_new_data)
    rb1=read_bfd_goal(bg_new_data)
    rb2=read_bfd_no_goal(bg_new_data)
    m=[]
    m.append(rb0)
    m.append(rb1)
    m.append(rb2)
    # write_csv(m,True)
    # f_you=test(bg_data) #point 1:1 and /....

# reed_point('02.02.02')
start()
# input()
