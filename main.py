from posixpath import split
from re import match
import re
from pyrogram import Client, filters, idle
from configparser import ConfigParser

# read config
config = ConfigParser()
config.read('config.ini')


def is_id(val):
    try:
        int(val)
        return True
    except ValueError:
        return False


def save_keywords(keywords):
    keywords = set(filter(None, keywords))
    config_set_and_save('bot_params', 'keywords', str(','.join(keywords)))


def save_excluded_chats(excluded_chats):
    excluded_chats = set(filter(None, excluded_chats))
    config_set_and_save('bot_params', 'excluded_chats',
                        str(','.join(excluded_chats)))


def save_includes(includes):
    includes = set(filter(None, includes))
    for include in includes:
        config.set('chat_specific_keywords', include['id'], str(
            ','.join(include['keywords'])))
    config_set_and_save(skip_set=True)


def config_set_and_save(section, param_name, param_value, skip_set=False):
    if(not skip_set):
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
excluded_chats = set(filter(None, config.get(
    'bot_params', 'excluded_chats', fallback='').split(',')))

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


def find_chat(client, args):
    dialogs = []
    if len(args) == 1 and (is_id(args[0] or args[0][0] == '@')):
        try:
            chat = client.get_chat(args[0])
            dialogs.append([str(chat.id), str(chat.title) if chat.title else str(
                chat.first_name) + ' ' + str(chat.last_name)])
        except:
            return dialogs
    else:
        for dialog in client.iter_dialogs():
            searchStr = ' '.join((str(dialog.chat.title), str(dialog.chat.first_name),
                                  str(dialog.chat.last_name), '@' + str(dialog.chat.username)))
            if re.search(' '.join(args), searchStr, re.IGNORECASE):
                dialogs.append([str(dialog.chat.id), str(dialog.chat.title) if dialog.chat.title else str(
                    dialog.chat.first_name) + ' ' + str(dialog.chat.last_name)])
    return dialogs

# bot commands handlers
# keywords chat


@user.on_message(filters.me & ~filters.edited & filters.command(['help', 'add', 'show', 'remove', 'findchat', 'exclude']))
def kwhandler(client, message):
    # print(message)
    # accept commands only for keywords chat
    if not message.chat or str(message.chat.id) != str(keywords_chat_id):
        return

    args = message.command
    comm = args.pop(0)

    match comm:
        case 'help':
            message.reply_text(
                '/add keyword1 keyword2\n/show\n/remove keyword1 keyword2\n/removeall\n/findchat name|id|@username\n/exclude name|id|@username')
        case 'add':
            for keyword in args:
                keywords.add(keyword.strip().replace(',', ''))
            message.reply_text('processed ' + str(len(args)) + ' keywords')
            save_keywords(keywords)
        case 'show':
            if not keywords:
                message.reply_text('no keywords, add with /add command')
            else:
                message.reply_text('keywords: #' + ', #'.join(keywords))
        case 'remove':
            for keyword in args:
                keywords.discard(keyword.strip().replace(',', ''))
            message.reply_text('processed ' + str(len(args)) + ' keywords')
            save_keywords(keywords)
        case 'removeall':
            message.reply_text('removed ' + str(len(keywords)) + ' keywords')
            keywords.clear()
            save_keywords(keywords)
        case 'findchat':
            if(not args):
                return
            dialogs = find_chat(client, args)
            message.reply_text('\n'.join([' - '.join(dialog) for dialog in dialogs]) if len(
                dialogs) else 'Ничего не найдено')
        case 'exclude':
            if(not args):
                return
            dialogs = find_chat(client, args)
            if(len(dialogs) != 1):
                message.reply_text('Найдено больше одного чата:\n' + '\n'.join([' - '.join(
                    dialog) for dialog in dialogs]) if len(dialogs) else 'Ничего не найдено')
            else:
                message.reply_text(
                    'Чат добавлен в список исключений:\n' + ' - '.join(dialogs[0]))


# process incoming messages
# limit to <not me> : ~filters.me (by config?)
# exclude forwards ?
# limit to some types of updates (plain text?)
# limit to private chats / groups / channels (by config?)

# b1: search for keywords
# b2: limit to mentions

@user.on_message(~filters.me & ~filters.edited)
def echo(client, message):
    # print(message)
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
    # личные
    if message.chat.type == 'private':
        # source_name = str(str(message.from_user.first_name) + ' ' +
        #                   str(message.from_user.last_name)).strip()
        # source_link = '@' + \
        #     str(message.from_user.username) if message.from_user.username else ''
        source = 'в личном сообщении'
    # каналы
    elif message.chat.type == 'channel':
        source = 'в канале {} @{}'.format(message.chat.title,
                                          message.chat.username)
    # группы и супергруппы
    else:
        source_chat_name = str(
            message.chat.title) if message.chat.title else '<без имени>'
        source_chat_link = '@' + \
            str(message.chat.username) if message.chat.username else ''
        # source_name = str(str(message.from_user.first_name) + ' ' +
        #                   str(message.from_user.last_name)).strip()
        # source_link = '@' + \
        #     str(message.from_user.username) if message.from_user.username else ''

        source = 'в чате {} {}'.format(
            source_chat_name, source_chat_link)

    client.send_message(
        keywords_chat_id, '#{} {}'.format(keyword, source))
    message.forward(keywords_chat_id)
    client.mark_chat_unread(keywords_chat_id)


def mentions_forward(client, message):
    # личные
    if message.chat.type == 'private':
        source = 'в личном сообщении'
    # каналы
    elif message.chat.type == 'channel':
        source = 'в канале {} @{}'.format(message.chat.title,
                                          message.chat.username)
    # группы и супергруппы
    else:
        source_chat_name = str(
            message.chat.title) if message.chat.title else '<без имени>'
        source_chat_link = '@' + \
            str(message.chat.username) if message.chat.username else ''
        source = 'в чате {} {}'.format(
            source_chat_name, source_chat_link)

    client.send_message(
        mentions_chat_id, 'Уведомление {}'.format(source))
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
