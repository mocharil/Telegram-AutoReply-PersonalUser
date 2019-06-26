import os
import json,re
import sys
import time
import psutil
import logging
import subprocess as sp
import pandas as pd

import schedule
import threading, datetime
from telegram.ext import CommandHandler,Filters, Updater

sp.call('cls',shell=True)
print('\n================BOT READY=================')
print('ketik: /respon <username> name <respon> untuk mengganti respon')
print('ketik: /mode <username> name <mode> untuk mengganti mode, ON atau OFF')
print('ketik: /status untuk melihat status')

def make_dir(path):
    try:
        os.mkdir(path)
    except :
        pass
path = os.getcwd()


def mode(bot, update):
    msg=update.message.text.split(None,1)[-1]
    print(msg)
    name=re.findall(r'<username>(.*)<mode>',msg)[0].replace(' ','')
    if 'on' in msg.lower():
        print('====================MODE : ON==========================\n')
        msg='Autoreply Activate'
        mode_=pd.DataFrame(columns=['mode'])
        mode_.loc[len(mode_), ('mode')] = ('on')
        
    elif 'off' in msg.lower():
        print('====================MODE : OFF==========================\n')
        msg='Autoreply NonActivate'
        mode_=pd.DataFrame(columns=['mode'])
        mode_.loc[len(mode_), ('mode')] = ("off")
        
    else :
        msg='mode yang anda pilih salah, pilihan mode : ON atau OFF'   
    path_name=path+'/'+name
    make_dir(path_name)
    mode_.to_csv('{}\\mode_{}.csv'.format(path_name,name),index=False)
    
    update.message.reply_text('{}'.format(msg)) 


        
def posting(bot, update):
    msg=update.message.text.split(None,1)[-1]
    name=re.findall(r'<username>(.*)<respon>',msg)[0].replace(' ','')
    respon=re.findall(r'<respon>(.*)',msg)[0]
    path_name=path+'/'+name   
    make_dir(path_name)
    with open('{}\\reply_{}.json'.format(path_name,name),'w') as f:
        json.dump({'message':respon,'username':name,'update':str(datetime.datetime.now())},f)    
    
    print('====================Update Respon ==========================\n')
    print(msg)
    pesan='respon telah terupdate menjadi : {}\n'.format(respon)
    update.message.reply_text('{}'.format(pesan)) 
    
def status(bot, update):
    print('\n=======================status saat ini===========================')
    st=0
    for name in os.listdir():
        try:
            for i in os.listdir(path+'\\'+name):
                if 'reply' in i:
                    with open(path+'\\'+name+'\\'+i) as f:
                        msg=json.load(f)['message']
                    update.message.reply_text('respon {} : {}'.format(name, msg))
                    st=1
                if 'mode' in i :
                    mode_=pd.read_csv(path+'\\'+name+'\\'+i)
                    mode_=mode_[['mode']] 
                    mod=mode_['mode'][len(mode_)-1]
                    update.message.reply_text('mode {} : {}'.format(name, mod))
                    st=1
        except:
            pass
    if st==0:
        t1='Belum ada yang diaktifkan\n'
        t2='/mode <username> name <mode> ON/OFF\n/respon <username> name <respon> responnya'
        update.message.reply_text('{}{}'.format(t1,t2))
        
def help(bot,update):
    print('\n=================================HELP============================\n')
    t2='/mode <username> name <mode> ON/OFF\n/respon <username> name <respon> responnya'
    print(t2)
    update.message.reply_text(t2)
        
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
    
def main():
    #akun broadcast_telegram_bot
    #TOKEN='727564606:AAHShdPk_OVYzwnUylXZEyoOrHKlcwHUW2Q'  #wa
    
    TOKEN='818429046:AAFhWUPJQi2pIavmb4oDi1sC4WSVq_evZ9I'
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('mode',mode,filters=Filters.private))
    
    dp.add_handler(CommandHandler('respon',posting,filters=Filters.private))
    
    dp.add_handler(CommandHandler('status',status,filters=Filters.private))
 
    dp.add_handler(CommandHandler('help',help,filters=Filters.private))

    updater.start_polling()
  
    updater.idle()
    
def restart_program():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """
   

    print('\n\n====================== RESTART PROGRAM ======================= ')
    time.sleep(1)
    sp.call('cls',shell=True)
    os.execv(sys.executable, ['python'] + sys.argv)


if __name__ == '__main__':  
    
    schedule.clear()
    schedule.every(6).hours.do(restart_program)
    run_continuously(schedule)
    main()
    
    