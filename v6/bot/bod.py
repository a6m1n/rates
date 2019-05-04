import requests
# import bin.misc_bot_st
import json




def get_updates(URL):
    url = URL + 'getupdates'
    r = requests.get(url)
    print (r.json())
    return r.json()

def get_message(URL):
    data = get_updates(URL)
    chat_id = data['result'][-1]['message']['chat']['id']
    text =  data['result'][-1]['message']['text']
    message_and_chat_id = {'chat_id':chat_id,
                            'message':text}
    return message_and_chat_id

def send_message(URL,text='Wait...'):
    if type(text)==list:
        test_text = ''
        for i in text:
            test_text += i + '\n'
        text = test_text
        print (text)
    id = ['137404876','694528032']
    for i in id:
        url = URL + 'sendmessage?chat_id={}&text={}'.format(i, text)
        requests.get(url)
    # url = URL + 'sendmessage?chat_id={}&text={}'.format('282025544', text)
    # requests.get(url)

def new_day(URL,text='New day \n\n\nNew day\n\n\n New day\n\n\n'):
    id = ['242532285','282025544','137404876','694528032']
    for i in id:
        url = URL + 'sendmessage?chat_id={}&text={}'.format(i, text)
        requests.get(url)

    # id = '282025544'
    # url = URL + 'sendmessage?chat_id={}&text={}'.format(id, text)
    # requests.get(url)


# def main (URL):
    # message_info = get_message(URL)
    # send_message(URL)

def ok(URL):
    url = URL + 'sendmessage?chat_id={}&text={}'.format(242532285, 'All okey')
    requests.get(url)





if __name__=='__main__':
    # token = bin.misc_bot_st.misc_t_bot
    # URL = 'https://api.telegram.org/bot'+token+'/'
    artem_chat_id = '242532285'
    papa_chat_id = '282025544'
    sergey_chat_id = '137404876' #Степаненко. Сергей Ганс. Sergey Gans
    filipow_witya_chat_id = '694528032' #Дядя витя филипов
    # main(URL)
    # get_updates(URL)
    # send_message(URL)
    # new_day(URL)
