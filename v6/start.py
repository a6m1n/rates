import os
import time

def off_windows():
    folder = os.path.dirname(__file__)
    folder += '\\py+bat\\'
    os.system("{}exit60sec.bat 1".format(folder))

def main_no_f():
    folder = os.path.dirname(__file__)
    folder += '\\test.new.py_no_filtr\\'
    os.system("{}test.new.py 1".format(folder))

def st():
    print ('Start st \n\n\n\n\n\n')
    folder = os.path.dirname(__file__)
    folder += '\\stepasha\\'
    os.system("{}st.py 1".format(folder))

def two_5_b_h2h_strategy():
    folder = os.path.dirname(__file__)
    folder += '\\2.5b\\'
    os.system("{}2.5b_h2h.py 1".format(folder))

def two_5_b_strategy():
    folder = os.path.dirname(__file__)
    folder += '\\2.5b\\'
    os.system("{}2.5b.py 1".format(folder))

def main_strategy():
    folder = os.path.dirname(__file__)
    folder += '\\main\\'
    os.system("{}main.py 1".format(folder))

def start(data):
    a = input('Data[0] exaple 01.01.2019: ')
    f = open('data.txt', 'w')
    f.write(a+'\n')
    f.write(data)
    f.close()

if __name__=='__main__':
    data = input('exaple: 01/01:\n')
    start(data)
    main_strategy()
    # time.sleep(40)
    # two_5_b_strategy()
    # time.sleep(40)
    # two_5_b_h2h_strategy()
    # time.sleep(40)
    # st()
    # time.sleep(40)
    # main_no_f()
    os.remove('data.txt')
    off_windows()
