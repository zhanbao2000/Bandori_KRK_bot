# Bandori_KRK_bot
邦邦日服协力Live机器人，半自动获取推特上的邦邦协力车

# 依赖
`pip install pyTelegramBotAPI requests pyquery telebot
`</br>

# 运行
创建一个`config.py`，包含一个TOKEN</br>
``` python
TOKEN = "..."
```
TOKEN是形如`233333333:AAA3AA33A-AAAAAAAAA3AAAAA333AAA-3AA`的一段字符串<br>你应当在 @BotFather 处自行获取</br></br>
然后运行</br>
``` bash
python Bandori_KRK_bot.py
```
# F.A.Q.
## pip install找不到模块
pip各大源都会经常崩，pip install不上那就多试几次
## Bot偶尔停止运行
API的锅
