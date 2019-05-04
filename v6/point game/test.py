import os
import csv
import re

def min():
    arr_min=[]
    num1=0
    for i in range(1,21):
        num1+=0.5
        arr_min.append(num1)
    return arr_min
def max():
    arr_max=[]
    num1=10.5
    for i in range(1,21):
        num1-=0.5
        arr_max.append(num1)
    return arr_max

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

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
    if os.path.isdir(os.path.join(a_dir, name))]

def get_data_folder():
    a = os.path.dirname(__file__)
    a = a[:a.rfind('\\')]
    folder = a+'\\result\\month\\april'
    res_get_immediate_subdirectories = get_immediate_subdirectories(folder)
    return res_get_immediate_subdirectories

def read_point_today(day):
    dd = {}
    folder = os.path.dirname(__file__)
    folder = folder[:folder.rfind('\\')] + '\\result\\month\\april\\' + day
    with open (folder+'\\{}_new.csv'.format(day), 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for line in reader:
            dd[line['strategy 1'][1:-1]] = line['goal in first time']
    return dd

def main(max,min):
    bg_data = []

    gdf = get_data_folder()
    for i in gdf:
        if i != '15.04.2019' and i != '16.04.2019' and i != '17.04.2019':
            bg_data.append(read_point_today(i))
    bg_new_data = point_game(bg_data)
    for tt in min:
        for ff in max:
            t=[]
            f=[]
            # tt=9.5
            # ff=10
            all=0
            for j in bg_new_data:
                for item,key in j.items():
                    if item>tt and item<ff:
                        all+=1
                        if key=='Yes':
                            t.append(j)
                        else:
                            f.append(j)
            if all>20 and int(len(t)/all*100)>=80:
                print ('Условия: ',tt, 'and', ff)
                print ('all=', all)
                # print ('Flase: ', len(f))
                print (round(len(t)/all*100,2),'\n\n')
if __name__=='__main__':
    max=max()
    min=min()
    main(max,min)
    # for mmax in max:
    #     for mmin in min:
    #         print (mmin,'-',mmax,'_____________________________________')
    #         # print ('_____________________________________')
    #         break
# 5-7 - april 75% and 20G march -80.64% and 31G
# 4-7 - april 78.37% and 37G march -78.78% and 66G
# 3.5-7.5 - april 75% and 60G march -80.4% and 97G
# 4.4-6 - april 90% and 21G march -73.17% and 41G
