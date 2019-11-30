#coding: UTF-8
import requests
import csv
import random
import time
import socket
import http.client
from bs4 import BeautifulSoup

def get_content(url, data = None):
    """
    获取网页中的html代码
    :param url:网页链接
    :param data:
    :return:html页面
    """
    header = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection':'keep-alive',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }
    timeout = random.choice(range(80, 180))     #设置超时时间
    while True:
        try:
            rep = requests.get(url, headers=header,timeout=timeout)
            rep.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print('3:', e)
            time.sleep(random.choice(range(8, 15)))
        except socket.error as e:
            print('4:', e)
            time.sleep(random.choice(range(20, 60)))
        except http.client.BadStatusLine as e:
            print('5:', e)
            time.sleep(random.choice(range(30, 80)))
        except http.client.IncompleteRead as e:
            print('6:', e)
            time.sleep(random.choice(range(5, 15)))
    return rep.text


def get_data(html_text):
    """
    利用BeautifulSoup获取我们所需要的字段
    :param html_text:html页面
    :return:所需要的字段
    """
    final = []
    bs = BeautifulSoup(html_text, "html.parser")    # 创建BeautifulSoup对象
    body = bs.body                                  # 获取body部分
    data = body.find('div', {'id': '7d'})           # 找到id为7d的div
    ul = data.find('ul')                            # 获取ul部分
    li = ul.find_all('li')                          # 获取所有的li
    # print(type(li))                               <class 'bs4.element.ResultSet'>

    for day in li:                          # 对每个li标签中的内容进行遍历
        temp = []
        date = day.find('h1').string        # 找到日期
        temp.append(date)                   # 日期添加到temp中
        inf = day.find_all('p')             # 找到li中的所有p标签
        temp.append(inf[0].string, )        # 第一个p标签中的内容（天气状况，如小雨）加到temp中
        if inf[1].find('span') is None:     # 最高气温存于span，最低气温存于i
            temperature_highest = None      # 天气预报可能没有当天的最高气温（到了傍晚，就是这样），需要加个判断语句,来输出最低气温
        else:
            temperature_highest = inf[1].find('span').string               # 找到最高温
            temperature_highest = temperature_highest.replace('℃', '')  # 到了晚上网站会变，最高温度后面也有个℃
        temperature_lowest = inf[1].find('i').string                # 找到最低温
        temperature_lowest = temperature_lowest.replace('℃', '')  # 最低温度后面有个℃，去掉这个符号
        temp.append(temperature_highest)  # 将最高温添加到temp中
        temp.append(temperature_lowest)  # 将最低温添加到temp中
        final.append(temp)              # 将temp加到final中

    return final

def write_data(data, file_name):
    """
    写入文件csv
    :param data:天气数据
    :param file_name:文件名称
    :return:
    """
    with open(file_name, 'a', errors='ignore', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)           #写入多行，1个li一行

if __name__ == '__main__':
    url ='http://www.weather.com.cn/weather/101190401.shtml'
    html = get_content(url)
    result = get_data(html)
    write_data(result, 'weather.csv')
