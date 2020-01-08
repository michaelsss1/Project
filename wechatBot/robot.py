import itchat
import time
from CSV import csvOpertaion
import pandas
import re
import os
import configparser

@itchat.msg_register(itchat.content.TEXT)	
def reply(msg):
    
    # read conf file
    config = configparser.ConfigParser()
    config.read('practise/project/wechatBot/default.conf')

    header = eval(config['csv']['header'])
    default_directory = config['csv']['default_directory']

    # catch time in msg and find file in directory
    pattern = re.compile(r'\d{3}-\d{2}-\d{2}')
    time = re.findall(pattern, msg['Content'])
    filename = time + '.csv'
    file = os.path.join(default_directory, filename)

# monitoring received message
    # case1: received order info
    if len(msg['Content']) > 20:
        data = msg['Content'].split()

        # save in today csv file 
        w1 = csvOpertaion()
        w1.write(data, header, default_directory)
        itchat.send_msg(f'保存成功: {w1.name}', msg['FromUserName'])

        # save in all_data csv
        w2 = csvOpertaion()
        w2.writeAll(data, header, default_directory)
        itchat.send_msg(f'保存成功: {w2.name}', msg['FromUserName'])
        

    #case2: received 我要数据  
    elif '我要数据' in msg['Content']:
        w = csvOpertaion()
        if os.path.exists(file) == False:
            itchat.send_msg('文件不存在', msg['FromUserName'])
        else:
            itchat.send_msg(w.read(file), msg['FromUserName'])
            
    #case2: received 我要文件
    elif '我要文件' in msg['Content']:
        if os.path.exists(file) == False:
            itchat.send_msg('文件不存在', msg['FromUserName'])
        else:
            itchat.send_file(file, msg['FromUserName'])
    #case3: received 完整文件
    elif '完整文件' in msg['Content']:
        if os.path.exists(config['csv']['All_Data_File']) == False:
            itchat.send_msg('完整文件不存在', msg['FromUserName'])
        else:
            itchat.send_file(config['csv']['All_Data_File'], msg['FromUserName'])
    else:
        itchat.send_msg(config['defaultMsg']['standardMsg'], msg['FromUserName'])

#login wechat account
itchat.auto_login(enableCmdQR = True, hotReload = True)
# run wechat robot
itchat.run()