
from telethon import TelegramClient, sync, events
from telethon.tl.types import PeerUser
import datetime
import pandas as pd
import subprocess as sp
import sys
import time
import psutil
import logging

import os
import re,json
import schedule
import threading



def run_continuously(schedule, interval=1):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run
    
def restart_program():
    import datetime
    x=datetime.datetime.now()
    if int(x.strftime('%H'))>22:
        sp.call('cls',shell=True)
        conv=pd.DataFrame(columns=['id'])
        conv.to_csv('{}\\history_{}.csv'.format(path_name,name),index=False)

    print('\n\n====================== RESTART PROGRAM ======================= ')
    time.sleep(1)
    sp.call('cls',shell=True)
    os.execv(sys.executable, ['python'] + sys.argv)
    
   
 
    
def make_login(name):
    with open('login_{}.txt'.format(name), 'w+') as f:
        api_id=input('api_id: ')
        api_hash=input('api_hash: ')
        phone_number=input('phone_number: +62')
        f.write("api_id: "+api_id+'\n')
        f.write("api_hash: "+api_hash+'\n')
        f.write("phone_number: +62"+phone_number+'\n')
        
def update_login(name):
    with open('login_{}.txt'.format(name), 'w') as f:
        api_id=input('api_id: ')
        api_hash=input('api_hash: ')
        phone_number=input('phone_number: +62')
        f.write("api_id: "+api_id+'\n')
        f.write("api_hash: "+api_hash+'\n')
        f.write("phone_number: +62"+phone_number+'\n')
        

def make_dir(path):
    try:
        os.mkdir(path)
    except:
        pass
        
name=__file__
if len(name.split('\\'))>1:
    name=name.split('\\')[-1]
name=name.replace('.py','')

path_inti=os.getcwd()
path_name=path_inti+'\\'+name

make_dir(path_name)

file = 'login_{}.txt'.format(name)        
if os.path.isfile(file):
    print('you are logged in as {}'.format(name))
    
else :
    print('\nwelcome {}\n'.format(name))
    make_login(name)
    print('\nyour data has saved {}\n'.format(name))

data=open('login_{}.txt'.format(name)).read().split('\n')

#data login
for i in data:
    if 'api_id' in i:
        api_id=int(i.replace('api_id: ','')) 
    if 'api_hash' in i:
        api_hash=str(i.replace('api_hash: ','')) 
    if 'phone_number' in i:
        phone=str(i.replace('phone_number: ','')) 
        
print('waiting to logged in...')     
client = TelegramClient(name, api_id, api_hash)
client.start(phone)
import json
sp.call('cls',shell=True)
print('=======================LOGIN BERHASIL=====================================')


conv=pd.DataFrame(columns=['id'])
conv.to_csv('{}\\history_{}.csv'.format(path_name,name))
file='{}\\mode_{}.csv'.format(path_name,name)
if os.path.isfile(file)==False:
    mode_=pd.DataFrame(columns=['mode'])
    mode_.loc[len(mode_), ('mode')] = ("off")
    mode_.to_csv('{}\\mode_{}.csv'.format(path_name,name))
    print('mode: off')
    try:
        with open('{}\\reply_{}.json'.format(path_name,name)) as f:
            msg=json.load(f)['message']
        print('respon: {}'.format(msg))
    except:
        msg='respon belum di update'
        print(msg)    

else :
    mode_=pd.read_csv('{}\\mode_{}.csv'.format(path_name,name))
    mode_=mode_[['mode']]
    mod=mode_['mode'][len(mode_)-1]
    print('mode: {}'.format(mod))
    try:
        with open('{}\\reply_{}.json'.format(path_name,name)) as f:
            msg=json.load(f)['message']
        print('respon: {}'.format(msg))
    except:
        msg='respon belum di update'
        print(msg)

       
schedule.clear()
schedule.every(3).hours.do(restart_program)
run_continuously(schedule)


def get_name(id_):
    result=client.get_entity(id_)
    try:
        print(str(datetime.datetime.now()),'>>>',dir(result))
    except Exception as e:
        print(e)  

@client.on(events.NewMessage(incoming=True,func=lambda e:e.is_private))
async def handler_p(event):
    conv=pd.read_csv('{}\\history_{}.csv'.format(path_name,name))
    mode_=pd.read_csv('{}\\mode_{}.csv'.format(path_name,name))
    mode_=mode_[['mode']]
    conv=conv[['id']]
    x=str(datetime.datetime.now().time())
    time= int(x[:2])
    id_=event.message.from_id
    conv.loc[len(conv), ('id')] = (id_)
    conv.to_csv('{}\\history_{}.csv'.format(path_name,name),index=False)

    with open('{}\\reply_{}.json'.format(path_name,name)) as f:
        msg=json.load(f)['message']
        
    mod=mode_['mode'][len(mode_)-1]
    print(str(datetime.datetime.now()),'>>>',id_,'\n')
    import time
    time.sleep(1)
    print('=====================================MODE : {}============================================'.format(mod))
    
    import random
    msg=random.choice(str(msg).split('#'))
        
    if (mod=='on' and list(conv['id']).count(id_)%2==1):
        await event.reply(str(msg))
        
    elif mod=='off':
        conv=pd.DataFrame(columns=['id'])
        conv.to_csv('{}\\history_{}.csv'.format(path_name,name),index=False) 

	
client.run_until_disconnected()




