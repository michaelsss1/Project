from bs4 import BeautifulSoup
import requests
import csv
import time
import lxml
from base64 import b64decode
from base64 import decodebytes
from fontTools.ttLib import TTFont
from io import BytesIO
import re
from threading import Thread 

#https://bj.58.com/pinpaigongyu/?minprice={1500_2000}&PGTID=0d3111f6-0000-1834-6dcc-bada55da6bdd&ClickID=1
# [房源名称，地址，月租，房源 url 地址]
# XHR
# https://sh.58.com/pinpaigongyu/pn/2/?minprice=1500_2000&PGTID=0d3111f6-0000-1834-6dcc-bada55da6bdd&ClickID=3&segment=true&encryptData=d_5friq6cZIlqdf62BwX-1pnUk82BEQhtq_Kbt_fTMGNEfLd_RyQpugeRlkCnKxzeab6gdfZX-Wbzx2Xq56b4G4npNRcB1ndKNRljXNCRUVsyNTaZR-b7I8WMxPLLMT9
# https://sh.58.com/pinpaigongyu/pn/3/?minprice=1500_2000&PGTID=0d3111f6-0000-1834-6dcc-bada55da6bdd&ClickID=3&segment=true&encryptData=d_5friq6cZIlqdf62BwX-1pnUk82BEQhtq_Kbt_fTMGNEfLd_RyQpugeRlkCnKxzeab6gdfZX-Wbzx2Xq56b4G4npNRcB1ndKNRljXNCRUVsyNTaZR-b7I8WMxPLLMT9


def decodeSuckStr(suckStr):
    ret_num = []
    for char in suckStr:
        if ord(char) in c:
            text = int(c[ord(char)][-2:]) - 1
        else:
            text = char
        ret_num.append(str(text))
    decode_char = ''.join(str(text) for text in ret_num)
    return decode_char


page = 0
csv_file = open("./rent.csv", "w")
csv_writer = csv.writer(csv_file, delimiter = ',')
price = input("insert the price(1000_2000): ")
while True:
    page += 1
    url = f'https://sh.58.com/pinpaigongyu/pn/{page}/'
    print(f'fetch: {url}')
    time.sleep(5)
    param = {'minprice': price, 'PGTID': '0d3111f6-0000-2de9-8bb5-0b043a89b70c', 'ClickID': 3}
    r = requests.get(url , params = param, headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'})
    
    #get base64_string and decode
    base64_string = ''
    base64_string = re.findall(r'(?<=charset=utf-8;base64,).*?(?=\'\))', r.text)[0]
    bindata = decodebytes(base64_string.encode())
    font = TTFont(BytesIO(bindata))
    c = font['cmap'].tables[0].ttFont.tables['cmap'].tables[0].cmap

    #bs4 catch element
    html = BeautifulSoup(r.text, features = 'lxml')
    house_list = html.select(".list > li")
    if not house_list:
        break
    for house in house_list:
        house_title = decodeSuckStr(house.select("h2")[0].string.strip())
        house_url = house.select("a")[0]["href"]
        house_info_list = house_title.split()
    if '公寓' in house_info_list[1] or "青年社区" in house_info_list[1]:
        house_location = house_info_list[0]
    else:
        house_location = house_info_list[1]
    house_money = house.select(".money")[0].select("b")[0].string.strip()
    if '-' in house_money:
        house_money = '-'.join([decodeSuckStr(x.strip()) for x in house_money.split('-')])
    else:
        house_money = decodeSuckStr(house_money)
    
    csv_writer.writerow([house_title, house_location, house_money, house_url])
csv_file.close()
