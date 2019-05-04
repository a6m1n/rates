import os
import csv
import re


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
            a=round((float(j[0])+float(j[1])),3)
            res_sm_data[a]=bg_data[i][g]
            b.append(res_sm_data)
    return b

def read_point_today(day):
    dd = {}
    folder = os.path.dirname(__file__)
    with open (folder+'\\{}.csv'.format(day), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for line in reader:
            dd[line['strategy 1'][1:-1]] = line['team']
    return dd

def main():
    day = 'today'
    t=[]
    t.append(read_point_today(day))
    t=point_game(t)
    print ('_________________________________ ALL _________________________________')
    for i in t:
        for it,tm in i.items():
            print (it,tm)
            # if it>4 and it<6:
            #     print (tm)
    print ('______________________________________________________________________')
    print ('________________________________ TRUE _________________________________')
    for i in t:
        for it,tm in i.items():
            if it>4 and it<6:
                print (it,tm)
    print ('______________________________________________________________________')

if __name__=='__main__':
    main()
    a=input()
