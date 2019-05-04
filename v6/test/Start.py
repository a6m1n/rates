def start():
    print ('\n1) Start strategy 1. \n2) Start strategy 2.\n3) Send bot message \n0) Exit')

    try:
        work = int(input('Input num:'))
    except ValueError:
        error_would()
    if work == 1:
        print ('\nStart strategy_1')
    elif work == 2:
        print ('\nStart strategy_2')
    elif work == 3:
        print ('\nSend messgae in telegram...')
    elif work == 0:
        print ('\nExit')
        return False
    else:
        print ('\n\nError...\n\n')
        if error_would() == False:
            return False
    return True#1
def error_would():
    would = input('Would you like to continue work?\n\n1)Yes.\n2)No.\n')
    if int(would)==1:
        return True
    else:
        return False#1

if __name__ == '__main__':
    while True:
        s1 = input('Hello, start?\n\n1)Yes 2)No\n')
        if int(s1) == 1:
            start()
            s2=input('\nRepeat?\n1)Yes\n2)No\n')
            if s2==1:
                pass
            else:
                break
        else:
            break
