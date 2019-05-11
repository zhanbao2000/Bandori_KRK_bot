#!/usr/bin/python
# coding:utf-8

import requests
import json
import re


keyword = '%23%E3%83%90%E3%83%B3%E3%83%89%E3%83%AA%E5%8D%94%E5%8A%9B%20%23%E3%82%AC%E3%83%AB%E3%83%91%E5%8D%94%E5%8A%9B'

timeline_Url = 'https://twitter.com/search?q=' + keyword
r = requests.get('https://twitter.com/i/search/timeline?f=tweets&vertical=default&q=' + keyword,
                 headers={'User-Agent': 'Mozilla'})
r.encoding = "utf-8"
html = r.json()['items_html']

print html
