#!/usr/bin/python
# coding:utf-8
# https://core.telegram.org/bots/api#messageentity
# 参考 https://blog.csdn.net/umi_sensei/article/details/78508074

import telebot
import logging
import sys
from config import *

# from telebot import types

# 这里解决UTF-8对ascii的奇葩问题
reload(sys)
sys.setdefaultencoding('utf8')

# logging，控制台输出，用来debug
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 载入机器人，状态标识初始化
bot = telebot.TeleBot(TOKEN)


# 处理推文
def tw_handle(char):
    result = char
    return result


# Admin认证
def verify(chat_id):
    return chat_id in ADMINS


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,
                     "这是一个给邦邦日服玩家使用的bot\n\n你使用 /search 命令后，它会在推特上自动搜寻包含\n#ガルパ協力 #バンドリ協力\n标签的推文。并且在自动分析之后，把包含的信息格式化输出，返回给你。\n\n需要帮助请使用 /help 指令",
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
        bot.send_message(message.chat.id, char)


@bot.message_handler(commands=["search"])
def search(message):
    bot.send_chat_action(message.chat.id, 'typing')
    msg_id = bot.send_message(message.chat.id, "正在查找最近的推文").message_id
    bot.send_chat_action(message.chat.id, 'typing')
    bot.delete_message(message.chat.id, msg_id)
    bot.send_message(message.chat.id, tw_handle(...))


if __name__ == '__main__':
    bot.polling()
