import csv
import datetime
import os
import pandas as pd

class csvOpertaion():
    def __init__(self, name = None):
        self.name = name
    def write(self, data, header, default_directory, name = None):
        if name is None:
            now = datetime.datetime.now().strftime("%Y-%m-%d")
            name = f'{now}.csv'
        with open(os.path.join(default_directory, name), "a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerow(data)
            csvfile.close()
    def writeAll(self, data, header, default_directory, name = 'All_Data.csv'):
        with open(os.path.join(default_directory, name), 'a') as csvAll:
            writer = csv.writer(csvAll)
            writer.writerow(header)
            writer.writerow(data)
            csvAll.close()
    def read(self, filename):
        try:
            data = pd.read_csv(filename)
            return data
        except Exception:
            return "查无数据"

# default_directory = r'/home/smc/Desktop/practise/project/wechatBot/datafiles'

# received from msg 
# data = 
# data1 = "ugg压钻 广西省南宁市良庆区平乐大道37号华润二十四城1期3栋1805 15994302524 罗小粒".split()
# data2 = "红色高跟鞋 上海市杨浦区政府路  13918744813 是许枫".split()
# header = ['产品', '地址', '电话', '姓名']
