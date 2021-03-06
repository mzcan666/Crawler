import sys
import urllib.request as urllib2
import pymysql
import re

from urllib import error
from tqdm import tqdm
from sql import Sql_insert
from log import log_run

row=0
#判空函数
def IsNone(S):
    if (len(S)):
        return False
    else:
        return True

#爬取充电人数和up主名字
def crawbilibili(*numbers):
    global row
    #print('numbers',numbers[0][0])
    userid=numbers[0][0]
    url_elec = 'https://elec.bilibili.com/api/query.rank.do?mid=' + str(userid)
    url_name= 'https://space.bilibili.com/' + str(userid)
    url_fans='https://api.bilibili.com/x/relation/stat?vmid='+str(userid)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://space.bilibili.com/6758258/',
        'Origin': 'http://space.bilibili.com',
        'Host': 'space.bilibili.com',
        'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
    }
    try:
        request_elec = urllib2.Request(url_elec)
        request_fans = urllib2.Request(url_fans)
        response_elec = urllib2.urlopen(request_elec)
        response_fans = urllib2.urlopen(request_fans)
        response_name = urllib2.urlopen(url_name)
        content_elec = response_elec.read().decode('utf-8')
        content_fans = response_fans.read().decode('utf-8')
        content_name = response_name.read().decode('UTF-8')
        pattern_elec = re.compile('"total_count":(.*?),"list"', re.S)
        items_elec = re.findall(pattern_elec,content_elec)
        if(IsNone(items_elec)):
            items_elec='0'
            return 0
       # print(items_elec[0])
        pattern_name = re.compile('<title>(.*?)的个人空间 - 哔哩哔哩', re.S)
        items_name = re.findall(pattern_name, content_name)
        pattern_fans = re.compile('"follower":(.*?)}}',re.S)
        fans_nums = re.findall(pattern_fans, content_fans)
        Sql_insert(userid,items_name[0],int(items_elec[0]),int(fans_nums[0]))
        log_run('F:\daydayup\Crawler\\test_log.txt',"run seccuss Crawlerbilibili",sys._getframe().f_code.co_name)
        print(items_name[0])

    except error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)

if __name__ == '__main__':

    i=1
    crawbilibili(i)
