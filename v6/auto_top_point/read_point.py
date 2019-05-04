import os
import csv
a = os.path.dirname(__file__)
# a = a+'\\'+ input('Input name folder file: ') +'\\'
# a=r'C:\Users\Артем\Desktop\work\dev\python\Rates\v2\v5\auto_top_point\\'
a=os.path.dirname(__file__)+'\\'
# print (a)
a+=input('input filder: ')+'\\'
file = input('input name file: ')
# print(a+file)
with open (a+'{}.csv'.format(file), 'r', encoding='utf-8') as f:
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
print (id1)
print (id2)
for idsh1,idsh2 in zip(id1,id2):
    for key1,value1 in idsh1.items():
        for key2,value2 in idsh2.items():
            if key1==key2:
                print(key2,round(int(value2)/int(value1),2))
                continue
input()         
