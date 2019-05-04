import os
import time


# a=os.path.dirname(__file__)
# a=a[:a.rfind('\\')]
# a=a+'\\test_30.py'
# os.system("{} 1".format(a))
# print (a)
# os.system("test.bat 1")
# print (time.time())
b=time.time()+(3600*3)
while True:
    if b<=time.time():
        a=os.path.dirname(__file__)
        a=a[:a.rfind('\\')]
        a=a+'\\test_30.py'
        os.system("{} 1".format(a))
        break
    else:
        time.sleep(500)

c=time.time()+(3600*2)
while True:
    if c<=time.time():
        os.system("exit60sec.bat 1")
        break
    else:
        time.sleep(200)
f = open('text.txt', 'w')
f.write('complete. 30.')
