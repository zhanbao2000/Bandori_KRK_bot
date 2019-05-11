#!/usr/bin/python
# coding:utf-8

import requests
import re
from pyquery import PyQuery


def gettw(keyword, number=5):
    # 限制只能查询1~20条推文
    if number < 1 or number > 20:
        return None
    result = []

    r = requests.get('https://twitter.com/i/search/timeline?f=tweets&vertical=default&q=' + keyword,
                     headers={'User-Agent': 'Mozilla'})
    r.encoding = "utf-8"
    d = PyQuery(r.json()['items_html'])

    for i in range(0, number):
        item = d('.js-stream-item').eq(i)
        user_profile = item('.js-profile-popup-actionable')
        char = item('.js-tweet-text-container').text()
        time = item('.js-relative-timestamp').attr('data-time')
        user = user_profile.attr('data-name') + ' [@' + user_profile.attr('data-screen-name') + '](https://twitter.com/' + user_profile.attr('data-screen-name') + ')'
        # example: 愛美 [@aimi_sound](https://twitter.com/aimi_sound)
        char = re.sub('@\n', '@', char)
        char = re.sub('#\n', '#', char)
        result.append(char)  # 推文正文
        result.append(time)  # 是Unix时间戳
        result.append(user)  # 注意：使用了Markdown语法
    return result


