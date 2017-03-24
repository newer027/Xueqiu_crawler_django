# -*- coding: utf-8 -*-
from login import login
import requests
import re
from bs4 import BeautifulSoup

agent = 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
headers = {
    'User-Agent': agent,
    'Host': "xueqiu.com",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6",
    "Connection": "keep-alive"
}
session = requests.session()


telephone = '18154377749'
password  = 'ML34gbxq'

def dashboard(title):
    url = 'https://xueqiu.com/'+title
    headers = login(telephone, password)
    data = session.get(url, headers=headers).text
    soup = BeautifulSoup(data, "lxml")
    followers = soup.find('li', class_="gender_info" )
    followers = followers.find_next_siblings("li")[0]
    followers = followers.contents[0]
    slug = soup.find('a', class_="setRemark" )['data-user-id']
    print(followers,slug)
    try:

        #try:

        #except:
        #    followers = "无可奉告"

        print(followers)
    except:
        print("错误的title")



if __name__ == "__main__":
    print("what is this")
    dashboard("wufaling")


            """
        url0 = 'https://xueqiu.com/stock/portfolio/stocks.json?size=1000&pid=-1&tuid='+ new_item.title +'&cuid=1180102135&_=1477728185503'
        headers = login(telephone, password)
        data = session.get(url0, headers=headers).text
        data = json.loads(data)
        if "stocks" in data:
        """
