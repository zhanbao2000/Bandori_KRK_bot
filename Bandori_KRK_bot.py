#!/usr/bin/python
# coding:utf-8
# https://core.telegram.org/bots/api#messageentity
# https://blog.csdn.net/umi_sensei/article/details/78508074

import telebot
import logging
import sys
import time
from config import *
from tw_spider import gettw

# 这里解决UTF-8对ascii的奇葩问题
reload(sys)
sys.setdefaultencoding('utf8')

# logging，控制台输出，用来debug
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TOKEN)
Bandori_keyword = '%23%E3%83%90%E3%83%B3%E3%83%89%E3%83%AA%E5%8D%94%E5%8A%9B%20%23%E3%82%AC%E3%83%AB%E3%83%91%E5%8D%94%E5%8A%9B'


def gettime(timestamp):
    time_local = time.localtime(int(timestamp))
    result = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return result


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    return False


# 处理推文
def tw_handle(word, n):
    result = ''
    char = gettw(word, number=n, newest=True)
    now = time.time()

    if char[0] == n:
        result = '搜索结果所返回的%d条推文，全部是无效推文☹️' % n
    else:
        for i in range(1, len(char) - 1, 3):
            result += '---- ---- ---- ----\n来自 %s 的推车：\n%s(%d秒前)\n\n%s\n\n\n' % (
                char[i + 2], gettime(char[i + 1]), now - int(char[i + 1]), char[i])
            if char[0] != 0:
                result += "\n已经丢弃%d条无效推文" % char[0]
    return result


# Admin认证
def verify(chat_id):
    return chat_id in ADMINS


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,
                     '这是一个给邦邦日服玩家使用的bot\n\n你使用 /search 命令后，它会在推特上自动搜寻包含\n#ガルパ協力 #バンドリ協力\n标签的推文并返回给用户\n\n需要帮助请使用 /help 指令',
                     parse_mode='Markdown')


@bot.message_handler(commands=["help"])
def help(message):
    if verify(message.chat.id + 1):
        char = """
可用的指令：
/start - 开始
/help - 帮助
/search - 查找推车
"""
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, char, )


@bot.message_handler(commands=["search"])
def search(message):
    number = message.text[8:]
    if not is_number(number):
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, '请输入1至20之间的数字！')
        return
    elif int(number) < 1 or int(number) > 20:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, '请输入1至20之间的数字！')
        return

    bot.send_chat_action(message.chat.id, 'typing')
    char = tw_handle(Bandori_keyword, int(number))
    bot.send_message(message.chat.id, char, parse_mode='Markdown')


# 快速命令：搜寻最新的5辆推车
@bot.message_handler(commands=["search5"])
def search(message):
    bot.send_chat_action(message.chat.id, 'typing')
    char = tw_handle(Bandori_keyword, 5)
    bot.send_message(message.chat.id, char, parse_mode='Markdown')


if __name__ == '__main__':
    bot.polling()

'''
来自 xxxxxxx(@XXXXXXX) 的推车
发布时间：XXXXXXXXXX（在X秒前）
内容：XXXXXXXX
'''
