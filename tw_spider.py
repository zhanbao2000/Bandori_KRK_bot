#!/usr/bin/python
# coding:utf-8

import requests
import re
from pyquery import PyQuery


def gettw(keyword, number=8, newest=True):
    """根据关键字搜索推文.

    :param keyword: 所搜寻的关键字.
    :param number: (optional) 返回的推文数量 (0<number<20 default: 8).
    :param newest: (optional) 是否搜寻最新推文，True:搜寻最新推文，False:搜寻热门推文 (default: True).
    :return: 列表第一个元素是已丢弃的推文数量。从第二个元素开始，每连续四个元素对应同一条推文的发送者ID、发送者用户名、发送时的Unix时间戳、推文正文
    :rtype: List
    :raise: ValueError, AttributeError

    数据流：JSON -> HTML -> List
    """
    result = [0]
    s = ''
    discard_count = 0  # 丢弃推文数计数器

    if number < 1 or number > 20:
        raise ValueError('number is not in the domain of definition(1~20)')

    if newest:
        s = 'f=tweets&'

    # 请求推特搜索页数据
    r = requests.get('https://twitter.com/i/search/timeline?' + s + 'vertical=default&q=' + keyword,
                     headers={'User-Agent': 'Mozilla'})
    r.encoding = "utf-8"
    try:
        d = PyQuery(r.json()['items_html'])
    except ValueError:
        raise RuntimeError('Something wrong with Twitter...')

    for i in range(0, number):
        # 解析从搜索页提取的json
        item = d('.js-stream-item').eq(i)
        user_profile = item('.js-profile-popup-actionable')
        
        # 这是针对Bandori而设置的筛选：如果正文不包含五位数房间号，那么忽略这条推文，并且计数器加一。不需要此功能可以注释掉
        if re.search(r'[0-9]{5}', char) is None and re.search(r'[0-9] [0-9] [0-9] [0-9] [0-9]', char) is None:
            discard_count += 1
            continue
            # TODO(zhanbao2000) 解决对于 '１７２５０' 这种类型的房间号的匹配

        userid = user_profile.attr('data-screen-name')
        username = user_profile.attr('data-name')
        time = item('.js-relative-timestamp').attr('data-time')
        char = item('.js-tweet-text-container').text()

        char = re.sub('@\n', '@', char)
        char = re.sub('#\n', '#', char)
        # 从js-tweet-text-container获取的正文，在'#'和'@'后会被换行，因此这里用正则表达式删去换行

        result.append(userid)
        result.append(username)
        result.append(time)
        result.append(char)

    result[0] = discard_count
    return result
