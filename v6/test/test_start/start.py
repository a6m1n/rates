import os
import time

a=input('Data: ')
f = open('data.txt', 'w')
f.write(a)
f.close()

# time.sleep(2)
os.system("1.py 1")
# # time.sleep(2)
os.system("2.py 1")
# # time.sleep(2)
os.system("3.py 1")
os.remove('data.txt')
