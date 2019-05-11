#!/usr/bin/python
# coding:utf-8

# 内容 时间

import requests
import re
from pyquery import PyQuery


# d = PyQuery(filename="H:\\Developer\\Python\\Telegram bots\\Bandori_KRK_bot\\output.html")
# keyword = '%23%E3%83%90%E3%83%B3%E3%83%89%E3%83%AA%E5%8D%94%E5%8A%9B%20%23%E3%82%AC%E3%83%AB%E3%83%91%E5%8D%94%E5%8A%9B'
def gettw(keyword, number=5):
    if number < 1 or number > 20:
        return None
    result = []
    r = requests.get('https://twitter.com/i/search/timeline?f=tweets&vertical=default&q=' + keyword,
                     headers={'User-Agent': 'Mozilla'})
    r.encoding = "utf-8"
    d = PyQuery(r.json()['items_html'])
    for i in range(0, number):
        char = d('.js-tweet-text-container').eq(i).text()
        time = d('.stream-item-header').eq(i).attr('data-time')
        user = d('.js-profile-popup-actionable').eq(i).attr('data-name') + data-screen-name
        char = re.sub('@\n', '@', char)
        char = re.sub('#\n', '#', char)
        result.append(char)
        result.append(time)
        result.append(user)
    return result


print gettw('%23%E3%83%90%E3%83%B3%E3%83%89%E3%83%AA%E5%8D%94%E5%8A%9B%20%23%E3%82%AC%E3%83%AB%E3%83%91%E5%8D%94%E5%8A%9B')[1]
print gettw('%23%E3%83%90%E3%83%B3%E3%83%89%E3%83%AA%E5%8D%94%E5%8A%9B%20%23%E3%82%AC%E3%83%AB%E3%83%91%E5%8D%94%E5%8A%9B')[2]

# print c

# f = PyQuery(c)('.TweetTextSize').text()

# print f  # ('.TweetTextSize  js-tweet-text tweet-text').html()
