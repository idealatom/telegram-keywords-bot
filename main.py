from posixpath import split
from re import match
import re
from pyrogram import Client, filters, idle
from configparser import ConfigParser

# read config
config = ConfigParser()
config.read('config.ini')

# start apps
user = Client('user')

user.start()
user_info = user.get_me()

if(not config.has_section('bot_params')):
    config.add_section('bot_params')

keywords = set(filter(None, config.get(
    'bot_params', 'keywords', fallback='').split(',')))

dummy_bot_name = config.get('bot_params', 'dummy_bot_name', fallback='SearchKeywordsBot')
keywords_chat_id = config.get('bot_params', 'keywords_chat_id', fallback='')
mentions_chat_id = config.get('bot_params', 'mentions_chat_id', fallback='')
following_chat_id = config.get('bot_params', 'following_chat_id', fallback='')

# store


def save_keywords(keywords):
    keywords = set(filter(None, keywords))
    config.set('bot_params', 'keywords', ','.join(keywords))
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


# bot commands handler
def kwhandler(client, message):
    if message.from_user.id != user_info.id:
        return
    if not message.text or message.text[0] != "/":
        return

    args = message.text.split(' ')
    comm = args.pop(0)

    match comm:
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

# process incoming messages
# limit to <not me> : ~filters.me (by config?)
# exclude forwards ?
# limit to some types of updates (plain text?)
# limit to private chats / groups / channels (by config?)

# b1: search for keywords
# b2: limit to mentions

@user.on_message(~filters.me)
def echo(client, message):
    if message.text:
        # search keywords
        if len(keywords) and re.search("|".join(keywords), message.text, re.IGNORECASE):
            keywords_forward(message)

    # message can be a reply with attachment with no text
    if message.mentioned:
        mentions_forward(message)

    



def keywords_forward(message):
    message.forward(keywords_chat_id)


def mentions_forward(message):
    message.forward(mentions_chat_id)

def following_forward(message):
    message.forward(following_chat_id)



# init message
user.send_message(keywords_chat_id, 'bot started')
user.send_message(mentions_chat_id, 'bot started')
# user.send_message(following_chat_id, 'bot started')

idle()

# stop message
user.send_message(keywords_chat_id, 'bot stopped')
user.send_message(mentions_chat_id, 'bot stopped')
# user.send_message(following_chat_id, 'bot stopped')

user.stop()