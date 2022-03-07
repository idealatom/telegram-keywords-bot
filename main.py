from posixpath import split
from re import match
from pyrogram import Client, filters, idle
from configparser import ConfigParser

# read config
config = ConfigParser()
config.read('config.ini')
keywords_bot_name = config.get("pyrogram", "keywords_bot_name", fallback=None)
keywords_bot_token = config.get(
    "pyrogram", "keywords_bot_token", fallback=None)
mention_bot_name = config.get("pyrogram", "mention_bot_name", fallback=None)
mention_bot_token = config.get("pyrogram", "mention_bot_token", fallback=None)

# start apps
user = Client('user')
kwbot = Client('kwbot', bot_token=keywords_bot_token)
# mbot = Client('mbot', bot_token=mention_bot_token)


user.start()
kwbot.start()
# mbot.start()

user_info = user.get_me()

if(not config.has_section('keywords')):
    config.add_section('keywords')

keywords = set(filter(None, config.get("keywords", str(
    user_info.id), fallback="").split(',')))

# store


def save_keywords(keywords):
    keywords = list(filter(None, keywords))
    config.set('keywords', str(user_info.id), ','.join(keywords))
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


# bots handlers

@kwbot.on_message()
def kwhandler(client, message):
    if message.from_user.id != user_info.id:
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


# process incoming messages ~filters.me
@user.on_message()
def echo(client, message):
    message.forward(keywords_bot_name)
    # message.reply_text(message.text)


# init dialogs with bots, so that they can start sending messages to you
user.send_message(keywords_bot_name, '/start')
# user.send_message(mention_bot_name, '/start')

idle()

user.stop()
kwbot.stop()
# mbot.stop()
