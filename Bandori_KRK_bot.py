#!/usr/bin/python
# coding:utf-8
# https://core.telegram.org/bots/api#messageentity
# https://blog.csdn.net/umi_sensei/article/details/78508074

import telebot
import time
import sys
from config import *
from tw_spider import gettw

# 这里解决UTF-8对ascii的奇葩问题
reload(sys)
sys.setdefaultencoding('utf8')

bot = telebot.TeleBot(TOKEN)
Bandori_keyword = '%23%E3%83%90%E3%83%B3%E3%83%89%E3%83%AA%E5%8D%94%E5%8A%9B%20%23%E3%82%AC%E3%83%AB%E3%83%91%E5%8D%94%E5%8A%9B'


def gettime(timestamp):
    """将Unix时间戳转化为可读的时间.

    :param timestamp: Unix时间戳.
    :type timestamp: str or int
    :return: 可读的时间
    :rtype: int
    """
    time_local = time.localtime(int(timestamp))
    result = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return result


def is_number(s):
    """判断字符串是否为数字.

    :param s: 待验证字符串.
    :type s: str or number(int, float etc.)
    :return: 布尔值，字符串是否为数字
    :rtype: bool
    """
    try:
        float(s)
        return True
    except ValueError:
        pass
    return False


# 处理推文
def tw_handle(word, n):
    result = ''
    try:
        char = gettw(word, number=n, newest=True)
    except RuntimeError:
        return '请求Twitter数据时发生错误\n请稍后再试.'
    now = time.time()

    if char[0] == n:
        result = '搜索结果所返回的%d条推文，全部是无效推文☹️' % n
    else:
        for i in range(1, len(char) - 1, 4):
            result += '---- ---- ---- ----\n来自 %s ([@%s](https://twitter.com/%s))的推车：\n%s (%d秒前)\n\n%s\n\n\n' % (
                char[i + 1], char[i], char[i], gettime(char[i + 2]), now - int(char[i + 2]), char[i + 3])
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
                     '这是一个给邦邦日服玩家使用的bot\n\n你使用 /search 或者 /search5 命令后，它会在推特上自动搜寻包含\n#ガルパ協力 #バンドリ協力\n标签的推文并返回给用户\n\n需要帮助请使用 /help 指令',
                     parse_mode='Markdown')


@bot.message_handler(commands=["help"])
def help(message):
    char = """
可用的指令：
/start - 开始
/help - 帮助
/search - 查找推车(使用方法：/search + 数字(1~6))
/search5 - 快速搜寻最新的5辆推车
"""
# TODO(zhanbao2000) 删除维修指示
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, char, )


# 一般方法查找推车
@bot.message_handler(commands=["search"])
def search(message):
    number = message.text[8:]
    if not is_number(number):
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, '请附加1至6之间的整数，如 /search 2')
        # TODO(zhanbao2000) 删除维修指示
        return
    elif int(float(number)) < 1 or int(float(number)) > 6:
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, 'bot正在维修，不能像以前可以输入1~20，现在只能输入1~6的整数，如 /search 2')
        # TODO(zhanbao2000) 完成分割处理的TODO之后，把限制从1~6恢复为1~20，并删除维修指示
        return
    elif int(float(number)) != float(number):
        bot.send_chat_action(message.chat.id, 'typing')
        bot.send_message(message.chat.id, '这是整数？')
        return
        # TODO(zhanbao2000) 添加函数以便于制作MD语法

    bot.send_chat_action(message.chat.id, 'typing')
    char = tw_handle(Bandori_keyword, int(number))
    bot.send_message(message.chat.id, char, parse_mode='Markdown')
    # TODO(zhanbao2000) 由于TG对bot请求md语法时有最大字符限制，要将所有消息分割成5个推文一条


# 快速命令：搜寻最新的5辆推车
@bot.message_handler(commands=["search5"])
def search5(message):
    bot.send_chat_action(message.chat.id, 'typing')
    char = tw_handle(Bandori_keyword, 5)
    bot.send_message(message.chat.id, char, parse_mode='Markdown')


if __name__ == '__main__':
    bot.polling()
