from posixpath import split
from re import match
import re
from pyrogram import Client, filters, idle
from configparser import ConfigParser

# read config
config = ConfigParser()
config.read('config.ini')
keywords_bot_name = config.get('pyrogram', 'keywords_bot_name', fallback=None)
keywords_bot_token = config.get(
    'pyrogram', 'keywords_bot_token', fallback=None)
mention_bot_name = config.get('pyrogram', 'mention_bot_name', fallback=None)
mention_bot_token = config.get('pyrogram', 'mention_bot_token', fallback=None)

# start apps
user = Client('user')
kwbot = Client('kwbot', bot_token=keywords_bot_token)
mbot = Client('mbot', bot_token=mention_bot_token)


user.start()
kwbot.start()
mbot.start()

user_info = user.get_me()

if(not config.has_section('bot_params')):
    config.add_section('bot_params')

keywords = set(filter(None, config.get(
    'bot_params', 'keywords', fallback='').split(',')))

# store


def save_keywords(keywords):
    keywords = set(filter(None, keywords))
    config.set('bot_params', 'keywords', ','.join(keywords))
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


# bots handlers

@kwbot.on_message()
def kwhandler(client, message):
    if message.from_user.id != user_info.id:
        return
    if not message.text or message.text[0] != "/":
        return

    args = message.text.split(' ')
    comm = args.pop(0)

    match comm:
        case '/start':
            message.reply_text('bot started')
        case '/add':
            for keyword in args:
                keywords.add(keyword.strip().replace(',', ''))
            message.reply_text('processed ' + str(len(args)) + ' keywords')
            save_keywords(keywords)
        case '/show':
            message.reply_text('keywords: ' + ', '.join(keywords))
        case '/remove':
            for keyword in args:
                keywords.discard(keyword.strip().replace(',', ''))
            message.reply_text('processed ' + str(len(args)) + ' keywords')
            save_keywords(keywords)
        case '/removeall':
            message.reply_text('removed ' + str(len(keywords)) + ' keywords')
            keywords.clear()
            save_keywords(keywords)


@mbot.on_message()
def mhandler(client, message):
    if message.from_user.id != user_info.id:
        return
    if not message.text or message.text[0] != "/":
        return

    args = message.text.split(' ')
    comm = args.pop(0)

    match comm:
        case '/start':
            message.reply_text('bot started')


# process incoming messages
# limit to <not me> : ~filters.me (by config?)
# exclude forwards ?
# limit to some types of updates (plain text?)
# limit to private chats / groups / channels (by config?)

# b1: search for keywords
# b2: limit to mentions

@user.on_message(~filters.me)
def echo(client, message):
    # print(message)
    # we don't want to process messages from our bots
    if message.from_user.username in (keywords_bot_name, mention_bot_name):
        return

    if message.text:
        # search keywords
        if len(keywords) and re.search("|".join(keywords), message.text, re.IGNORECASE):
            message.forward(keywords_bot_name)

    if message.mentioned:
        message.forward(mention_bot_name)


# init dialogs with bots, so that they can start sending messages to you
user.send_message(keywords_bot_name, '/start')
user.send_message(mention_bot_name, '/start')

idle()


kwbot.send_message(user_info.id, 'stopping bot')
mbot.send_message(user_info.id, 'stopping bot')

user.stop()
kwbot.stop()
mbot.stop()
