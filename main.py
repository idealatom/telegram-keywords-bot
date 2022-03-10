from posixpath import split
from re import match
import re
from pyrogram import Client, filters, idle
from configparser import ConfigParser

# read config
config = ConfigParser()
config.read('config.ini')

# store


def save_keywords(keywords):
    keywords = set(filter(None, keywords))
    config_set_and_save('bot_params', 'keywords', str(','.join(keywords)))


def config_set_and_save(section, param_name, param_value):
    config.set(section, param_name, param_value)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


# start app
user = Client('user')

user.start()
user_info = user.get_me()

if(not config.has_section('bot_params')):
    config.add_section('bot_params')

keywords = set(filter(None, config.get(
    'bot_params', 'keywords', fallback='').split(',')))

dummy_bot_name = config.get(
    'bot_params', 'dummy_bot_name', fallback='MyLittleDummyBot')
keywords_chat_id = config.get('bot_params', 'keywords_chat_id', fallback='')
mentions_chat_id = config.get('bot_params', 'mentions_chat_id', fallback='')
following_chat_id = config.get('bot_params', 'following_chat_id', fallback='')

# init chats
chat_dict = {
    "Keywords": "keywords_chat_id",
    "Mentions": "mentions_chat_id",
    "Following": "following_chat_id"
}
for k in chat_dict:
    if not globals()[chat_dict[k]]:
        new_chat = user.create_group(k, dummy_bot_name)
        globals()[chat_dict[k]] = new_chat.id
        config_set_and_save('bot_params', chat_dict[k], str(new_chat.id))


# bot commands handler
def kwhandler(client, message):
    if not message.text or message.text[0] != "/":
        return

    args = message.text.split(' ')
    comm = args.pop(0)

    match comm:
        case '/help':
            message.reply_text('''
                /add keyword1 keyword2\n
                /show\n
                /remove keyword1 keyword2\n
                /removeall
            ''')
        case '/add':
            for keyword in args:
                keywords.add(keyword.strip().replace(',', ''))
            message.reply_text('processed ' + str(len(args)) + ' keywords')
            save_keywords(keywords)
        case '/show':
            if not keywords:
                message.reply_text('no keywords, add with /add command')
            else:
                message.reply_text('keywords: #' + ', #'.join(keywords))
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


@user.on_message()
def echo(client, message):
    print(message)

    if message.from_user and message.from_user.id == user_info.id:
        # process commands
        if message.chat and str(message.chat.id) == str(keywords_chat_id):
            kwhandler(client, message)
    else:
        # process keywords
        if message.text:
            # maybe search -> findall and mark all keywords?
            keyword = re.search("|".join(keywords),
                                message.text, re.IGNORECASE)
            if len(keywords) and keyword:
                keywords_forward(client, message, keyword.group())

        # process mentions
        # message can be a reply with attachment with no text
        if message.mentioned:
            mentions_forward(client, message)

        # process following


def keywords_forward(client, message, keyword):
    source_chat = 'Личное'
    if(message.chat):
        source_chat = message.chat.title

    source_name = ''
    if(message.from_user):
        # ??? make link from id ???
        source_name = " ".join(
            set(filter(None, (message.from_user.first_name, message.from_user.last_name))))

    client.send_message(
        keywords_chat_id, 'Замечен тег #{} в канале/чате {} от {}'.format(keyword, source_chat, source_name))
    message.forward(keywords_chat_id)
    client.mark_chat_unread(keywords_chat_id)


def mentions_forward(client, message):
    message.forward(mentions_chat_id)
    client.mark_chat_unread(keywords_chat_id)


def following_forward(client, message):
    message.forward(following_chat_id)
    client.mark_chat_unread(keywords_chat_id)


# init message
# user.send_message(keywords_chat_id, 'bot started')
# user.send_message(mentions_chat_id, 'bot started')
# user.send_message(following_chat_id, 'bot started')

idle()

# stop message
# user.send_message(keywords_chat_id, 'bot stopped')
# user.send_message(mentions_chat_id, 'bot stopped')
# user.send_message(following_chat_id, 'bot stopped')

user.stop()
