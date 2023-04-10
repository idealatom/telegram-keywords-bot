import re
from pyrogram import Client, filters, idle
# from datetime import datetime
from config import config, keywords_chat_id, following_chat_id, mentions_chat_id, dump_all_messages_chat_id, dump_replies_chat_id, \
    edited_and_deleted_chat_id, pinned_messages_chat_id, findid_chat_id, keywords, save_keywords, excluded_chats, \
    save_excluded_chats, add_keywords_to_includes, includes_dict, following_set, save_following, config_set_and_save, \
    mentions_monitoring_switcher, save_mentions_switcher
# from threading import Timer

# start app
# (CDL) (OLD version that was working well)
user = Client("user")  # (CDL) Temporarily rolled back to the OLD solution. Delete it after I test the new solution below
# (?) (CDL) (NEW version, NOT tested yet)
# user = Client(workdir="./config_resources", session_name="user_1", config_file="my_config.ini")  # (?) Test these updates w/ a new login session from scratch

# init chats
chat_dict = {
    "1.Mentions": "mentions_chat_id",
    "2.Pinned_messages": "pinned_messages_chat_id",
    "3.Find_Telegram_ID": "findid_chat_id",
    "4.Keywords": "keywords_chat_id",
    "5.Following": "following_chat_id",
    "6.Edited_and_Deleted_messages_monitoring": "edited_and_deleted_chat_id",
    "7.Dump_all_messages": "dump_all_messages_chat_id", # (?) Rename the chat to 'Dump_all_from_selected_chat' OR 'Dump_from_a_chat' OR 'Backup_from_chat'
    "8.Dump_replies": "dump_replies_chat_id"
}


def is_id(val):
    try:
        int(val)
        return True
    except ValueError:
        return False


def find_chats(client, args):
    dialogs = []
    if len(args) == 1 and (is_id(args[0]) or args[0][0] == '@'):
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


def find_users(client, args):
    result = []
    users = client.get_users(args)
    for user in users:
        result.append(
            [str(user.id),
             ' '.join(list(filter(None, [user.first_name, user.last_name])))
             ]
        )
    return result


# def get_history_count(from_chat_id):   #  ? (test) Is this function necessary
#     pass


def dump_messages_of_target_user_from_chat(client, from_chat_id, target_user_id):

    if client.get_history_count(from_chat_id) == 0:
        client.send_message(dump_replies_chat_id, f"Sorry, chat {from_chat_id} is empty.\n Try to enter another from_chat_id")
        return # (?) Is this line necessary? ***Test in TG if this solution works fine

    from_chat_size = client.get_history_count(from_chat_id)
    chat_initial_size = client.get_history_count(dump_replies_chat_id)
    skipped_messages = 0
    # counter = 0
    # ++ Get ALL messages of the target user (via user ID) & forward them:  # Already tested
    for message in client.iter_history(from_chat_id):  # iter_history is used in Pyrogram v.1.4. instead of get_chat_history in v2.0.
        # if message is None:  # (??) AttributeError: 'NoneType' object has no attribute 'id'
        # if type(message.from_user) == None:
        # if type(message.from_user) is None:
        # if message == None:
        # if message is None:
        #  (??)  How to check here correctly?
        #     continue
        # print(type(message.from_user))
        try:
            if str(message.from_user.id) == target_user_id:
                # counter += 1
                if message.service:
                    skipped_messages += 1
                    continue
            # if type(message) is None: # (??) (CDL) Is this verification correct?
            #     continue
                message.forward(dump_replies_chat_id)
        except AttributeError:
            skipped_messages += 1
            continue  # (?) Or use "pass" here?

    chat_final_size = client.get_history_count(dump_replies_chat_id)
    client.send_message(dump_replies_chat_id,
                        "RESULTS:\n"
                        f"Forwarding of all messages of target user {target_user_id} from chat with chat_ID {from_chat_id} is FINISHED\n"
                        f"Size of {from_chat_id} chat: {from_chat_size} messages\n"
                        # f"Number of messages forwarded by bot: {counter}\n"
                        f"Number of messages forwarded by bot: {chat_final_size - chat_initial_size}\n"  # (?) (CDL) Delete this line & use "counter" ?!
                        f"Number of messages from target user skipped by bot (Ex.: 'joined chat', 'removed from chat', 'pinned message', etc): {skipped_messages}\n"
                        "/help - show Help options"
                        )






def dump_replies(client, from_chat_id, target_user_id):

    if client.get_history_count(from_chat_id) == 0:
        client.send_message(dump_replies_chat_id, f"Sorry, chat {from_chat_id} is empty.\n Try to enter another from_chat_id")
        return # (?) Is this line necessary? ***Test in TG if this solution works fine

    # print(f"'from_chat_id' == {from_chat_id}, tYpE == {type(from_chat_id)}")  # (CDL) For testing only
    # print(f"'target_user_id' == {target_user_id}, tYpE == {type(target_user_id)}")  # (CDL) For testing only

    # (?) About the code block below: is it the optimal solution?!
    for message in client.iter_history(from_chat_id):  # iter_history is used in Pyrogram v.1.4. instead of get_chat_history in v2.0.
        # print(message.from_user.id)  # (CDL) For testing only
        # print(type(message.from_user.id))  # (CDL) For testing only
        # return  # (CDL) For testing only

        # ++ If message IS a reply  =>  Get details about it & about its' original message
        # if message.reply_to_message:
        #     print(f"{message.from_user.username} // {message.from_user.id} // {message.text}")  # (CDL) For testing only
        #     print(f"{message.reply_to_message.from_user.username} // {message.reply_to_message.from_user.id} // {message.reply_to_message.text}\n")  # (CDL) For testing only

        # ++ If target user's message has replies - print this reply.
        # if message.reply_to_message and str(message.reply_to_message.from_user.id) == target_user_id:  # If message IS a reply  &  if message AUTHOR_ID of its' ORIGINAL message == target user ID
            # print(f"{message.from_user.username} // {message.from_user.id} // {message.text}")  # (CDL) For testing only
            # print(message.reply_to_message.from_user.id, type(message.reply_to_message.from_user.id))
            # print("target_user_id == ", target_user_id, type(target_user_id)) # (CDL) For testing only

        # ++ Get every ORIGINAL message of the TARGET user that HAS some replies:  # Already tested
        # if message.reply_to_message and str(message.reply_to_message.from_user.id) == target_user_id:
        #     client.send_message(dump_replies_chat_id,
        #                         f"{message.reply_to_message.from_user.username} // {message.reply_to_message.from_user.id} // {message.reply_to_message.text}"
        #                         )

        # +++ VARIANT N1: put TEXTS of original message & reply into a new single message:
        # Get & forward both:
        # 1.Every ORIGINAL message of the TARGET user that HAS some replies
        # 2.All REPLIES to these original messages
        # if message.reply_to_message and str(message.reply_to_message.from_user.id) == target_user_id:  # Works correctly. # Already tested.
        #     client.send_message(dump_replies_chat_id,
        #                         f"1. Original message of target user with user_ID {message.reply_to_message.from_user.id}: \n{message.reply_to_message.text}\n"
        #                         f"2. Reply of user '{message.reply_to_message.from_user.username}' with user_ID {message.reply_to_message.from_user.id} to this original message: \n{message.text}"
        #                         )

        # +++ VARIANT N2. FORWARD every original message & reply as SEPARATE messages.
        if message.reply_to_message and str(message.reply_to_message.from_user.id) == target_user_id:  # Works correctly. # Already tested.
            # dump_replies_forward(client, message)  # (CDL)
            message.reply_to_message.forward(dump_replies_chat_id)  # Forward the original message
            message.forward(dump_replies_chat_id)  # Forward the reply to this original message

        # + Get the ORIGINAL message from any user if the selected (specified, target) message is a reply:  # Already tested
        # (?) (CDL) BUT: I can NOT get ANY details about this "reply" message itself with "reply_to_message" param
        # if message.reply_to_message:
        #     print(message.from_user.username, message.reply_to_message.message_id, message.reply_to_message.text)


        # if message.from_user.id == target_user_id:  #  ??
        #     print("\n\n1.'message.text' == \n", message.text)
        #     print("\n\n2.'message.reply_to_message' == \n", message.reply_to_message)
        #     print("\n\n3.'message.reply_to_message.text' == \n", message.reply_to_message.text)


        # Get all replies to a (single) selected message from a specific user in a selected chat
        # (?) ... PROCEED here!


        # + Parts of this code block are useful & can be used in my final solution:
        # if message.from_user.id == target_user_id and message.reply_to_message:
            # print("'message' parameter == \n", message)
            # print("1.'message.text' == \n", message.text) # Text of replies made by target user to smb's messages
            # print("\n\n2.'message.reply_to_message' == \n", message.reply_to_message) # All details about the original message(s) from other user(s) that had replies made by target user
            # print("\n\n3.'message.reply_to_message.text' == \n", message.reply_to_message.text) # Text of original message(s) from other user(s) that had replies made by target user
            # print("4.'message.reply_text()' == ", message.reply_text("accEpt"))

        # print(f"'message.from_user.id' param == {message.from_user.id}")
        # print(f"'message_id' param == {message.id}\n 'message' section == {message}")

        # if message.from_user == target_user_id: # (?) Verify if the message belongs to the target user
        #     print(f"'message_id' param == {message.id}\n 'message' content == {message}")

        # + (NOT relevant for my task?!) Get every original message from smb that target user made a reply to:
        # if message.from_user.id == target_user_id and message.reply_to_message:
        #     print(message.from_user.username, message.reply_to_message.message_id, message.reply_to_message.text)

        # if message.reply_to_message:
        #     print(message.reply_to_message.reply_to_message) # (CDL) Wrong




def dump_all_messages(client, from_chat_id):
    from_chat_full_message_history = client.get_history_count(from_chat_id)
    if from_chat_full_message_history == 0:
        client.send_message(dump_all_messages_chat_id,
                            f"Sorry, NO messages to backup: chat {from_chat_id} is empty.\n Try to use another from_chat_id"
                            )
        return # (?) Is this line necessary? ***Test in TG if this solution works fine
    backup_all_messages_chat_size = client.get_history_count(dump_all_messages_chat_id)
    skipped_service_messages = 0
    counter = 0
    # current_time = int(datetime.now().timestamp())
    for message in client.iter_history(from_chat_id):  # iter_history is used in Pyrogram v.1.4. instead of get_chat_history in v2.0.
        counter += 1
        if message.service:
            skipped_service_messages += 1
            continue
        # message_datetime = datetime.fromtimestamp(message.date)
        # client.send_message(chat_id=dump_all_messages_chat_id,
        #                     text=message_datetime.strftime("%A, %d. %B %Y %I:%M%p")) # To show the exact time
        # Timer(counter * 50, message.forward(dump_all_messages_chat_id)).start()
        message.forward(dump_all_messages_chat_id)
        #message.forward(dump_all_messages_chat_id, schedule_date=current_time + counter);
        #forwarded_message = message.forward(dump_all_messages_chat_id)
        #print(forwarded_message.id, forwarded_message.text)
    forward_chat_full_message_history = client.get_history_count(dump_all_messages_chat_id)
    client.send_message(dump_all_messages_chat_id,
                        "RESULTS:\n"
                        f"Forwarding of all messages from chat with chat_ID {from_chat_id} is FINISHED\n"
                        f"Size of your chat to forward from: {from_chat_full_message_history} messages\n"
                        f"Number of messages forwarded by bot: {forward_chat_full_message_history - backup_all_messages_chat_size}\n"
                        f"Number of service messages skipped by bot (Ex.: 'joined chat', 'removed from chat', 'pinned message', etc): {skipped_service_messages}\n"
                        "/help - show Help options"
                        )

############## bot commands handlers #################

# Commands used in all bot chats in Telegram ("4.Keywords"; "1.Mentions"; "5.Following"; etc.) must be listed here:
filtered_commands_list = ['help', 'help_general', 'add', 'show', 'remove', 'findid', 'exclude_chat', 'excluded_chats_list',
                          'delete_from_excluded_chats', 'dump_all_messages', 'dump_replies', 'include', 'follow', 'unfollow',
                          'on', 'off', 'dump_messages_of_target_user_from_chat']

list_of_ids_of_all_created_chats = [keywords_chat_id, following_chat_id, mentions_chat_id, dump_all_messages_chat_id,
                                    edited_and_deleted_chat_id, pinned_messages_chat_id, findid_chat_id, dump_replies_chat_id]

help_general_text = """
...
(Beverly Sills) There are NO short cuts to any place worth going. 
...
""" # (?) Add text w/ all instructions from the final version of ReadMe AFTER main changes in code are finished

# command messages listener
@user.on_message(filters.me & ~filters.edited & filters.command(filtered_commands_list))
def command_messages_handler(client, message):
    # accept commands only for bot chat ids
    if not message.chat or not str(message.chat.id) in list_of_ids_of_all_created_chats:
        return

    chat_id = str(message.chat.id)

    if chat_id == keywords_chat_id:
        keywords_handler(client, message)
    elif chat_id == following_chat_id:
        following_handler(client, message)
    elif chat_id == mentions_chat_id:
        mentions_handler(client, message)
    elif chat_id == dump_all_messages_chat_id:
        dump_all_messages_handler(client, message)
    elif chat_id == edited_and_deleted_chat_id:
        edited_and_deleted_chat_input_handler(client, message)
    elif chat_id == pinned_messages_chat_id:
        pinned_messages_chat_input_handler(client, message)
    elif chat_id == findid_chat_id:
        findid_input_handler(client, message)
    elif chat_id == dump_replies_chat_id:
        dump_replies_chat_input_handler(client, message)


# (?) Variant N2:
@user.on_message(filters.me & ~filters.edited & ~filters.command(filtered_commands_list))
def not_command_handler(client, message):  # (?) Draft

    # accept commands only for bot chat ids
    if not message.chat or not str(message.chat.id) in list_of_ids_of_all_created_chats:
        return # (?) Add some text reply outputed to user via TG? (Ex.: "NOT valid. Try again")

    # Variant N2 to find Telegram ID via forwarding a message from a target chat to “FindID” chat
    # (current status)  Turned OFF now because:
    # 1. Works only for user chats (NOT for: group chats, channels)
    # 2. 'forward_from.id' output is NOT clear & it confuses the customer
    # Listen to messages forwarded manually by me to catch them in "3.Find_Telegram_ID" chat
    # if message.forward_from and str(message.chat.id) == findid_chat_id:
    #     return message.reply('The chat (user / group / channel / bot / etc.) you\'ve just forwarded a message from '
    #                   'has Telegram ID: \n{} '.format(message.forward_from.id)
    #                   )
    # else:
    #     return message.reply_text(
    #         'NOT found\n'
    #         'Please, try another way to find Telegram ID\n'
    #         'Enter /help')

    # (Variant 1) (How to follow a TG user) Forward manually any message of this user to your '5.Following' chat
    # Listen to messages forwarded manually by me to catch them in "5.Following" chat
    if message.forward_from and str(message.chat.id) == following_chat_id:
        if str(message.forward_from.id) in following_set:
            message.reply('Following already works for id {}'.format(
                message.forward_from.id))
        else:
            following_set.add(str(message.forward_from.id))
            save_following(following_set)
            message.reply('id {} is added to Following list'.format(
                message.forward_from.id))
        return

    message.reply_text( # (?) Is this line used in the correct place? As I've added code below
        'Sorry, this command is NOT in the list of valid commands. \nEnter /help to see all valid commands'
    )


# "1.Mentions" chat input handler
def mentions_handler(client, message):
    args = message.command
    comm = args.pop(0)
    # print("priNt 'args':", args) # CDL (for testing purposes)
    # print("priNt 'comm':", comm) # CDL (for testing purposes)
    match comm:
        case 'help_general':
            message.reply_text(help_general_text)
        case 'help':
            message.reply_text(
                '/help - show Help options for this chat\n'
                '/help_general - show Help options for all chats\n\n'
                '"1.Mentions" chat works automatically\n'
                'No need to enter any input in "1.Mentions" chat\n\n'
                'Messages from all chats where your TG account was mentioned (tagged) will be forwarded to "1.Mentions" chat\n'
                'Replies to your messages are also counted as mentions'
            )
        case 'on':
            # mentions_monitoring_switcher.clear()
            # mentions_monitoring_switcher.format('mentions_monitoring_switcher'='on') # Var1 (??)  TEST this line!
            # mentions_monitoring_switcher_on = mentions_monitoring_switcher.replace("off", "on") # Var2 (?) TEST this line!
            # mentions_monitoring_switcher_on = mentions_monitoring_switcher.replace("off", "on") # Var2 (??) Is using "mentions_monitoring_switcher_on"_== an optimal solution? ***TEST this line!
            print("mentions_monitoring_switcher == ", mentions_monitoring_switcher, "// tYpe == ", type(mentions_monitoring_switcher)) # (CDL) For testing only  ***Use global var for testin?!
            mentions_monitoring_switcher = mentions_monitoring_switcher.replace("off", "on") # Var3 (??) Test it!
            print("mentions_monitoring_switcher == ", mentions_monitoring_switcher, "// tYpe == ", type(mentions_monitoring_switcher)) # (CDL) For testing only
            # print("mentions_monitoring_switcher_on == ", mentions_monitoring_switcher_on, "// tYpe == ", type(mentions_monitoring_switcher_on)) # (CDL) For testing only
            # mentions_monitoring_switcher.add('on')  # (CDL) For "set"
            # save_mentions_switcher(mentions_monitoring_switcher_on) # Var2. (??) Test it!
            save_mentions_switcher(mentions_monitoring_switcher) # Var3. (??) Test it!
            message.reply_text(
                'Automatic monitoring is turned ON\n'
                '"Mentions" feature is working now'
            )
        case 'off':
            # mentions_monitoring_switcher.clear()
            # mentions_monitoring_switcher.format('off') # Var1 (??)  TEST this line!
            # mentions_monitoring_switcher.replace() # Var2 (??) NOT tried yet
            print("mentions_monitoring_switcher == ", mentions_monitoring_switcher, "// tYpe == ", type(mentions_monitoring_switcher)) # (CDL) For testing only
            # mentions_monitoring_switcher_off = mentions_monitoring_switcher.replace("on", "off") # Var2 (?) TEST this line!
            mentions_monitoring_switcher_off = mentions_monitoring_switcher.replace("on", "off") # Var2 (??) Is using "mentions_monitoring_switcher_off"_== an optimal solution? ***TEST this line!
            print("mentions_monitoring_switcher == ", mentions_monitoring_switcher, "// tYpe == ", type(mentions_monitoring_switcher)) # (CDL) For testing only
            print("mentions_monitoring_switcher_off == ", mentions_monitoring_switcher_off, "// tYpe == ", type(mentions_monitoring_switcher_off)) # (CDL) For testing only
            # mentions_monitoring_switcher.add('off')
            save_mentions_switcher(mentions_monitoring_switcher_off)
            message.reply_text(
                'Automatic monitoring is turned OFF\n'
                '"Mentions" feature is NOT working now'
            )
        case _:
            message.reply_text('Sorry, this command is not valid')


# "6.Edited_and_Deleted_messages_monitoring" chat handler
def edited_and_deleted_chat_input_handler(client, message): # (?) Or two SEPARATE handlers necessary for “Edited” & for “Deleted”?
    args = message.command
    comm = args.pop(0)
    match comm:
        case 'help_general':
            message.reply_text(help_general_text)
        case 'help':
            message.reply_text(
                '/help - show Help options for this chat\n'
                '/help_general - show Help options for all chats\n\n'
                '"6.Edited_and_Deleted_messages_monitoring" chat works automatically\n'
                'No need to enter any input in this chat\n\n'
                '..??..  \n'
                '(?) ADD here the text description of this feature from the final version of ReadMe ..??..\n'
            )
        case _:
            message.reply_text('Sorry, this command is not valid')


# "2.Pinned_messages" chat handler
def pinned_messages_chat_input_handler(client, message):
    args = message.command
    comm = args.pop(0)
    match comm:
        case 'help_general':
            message.reply_text(help_general_text)
        case 'help':
            message.reply_text(
                '/help - show Help options for this chat\n'
                '/help_general - show Help options for all chats\n\n'
                'Pinned messages from all chats are automatically forwarded to your "2.Pinned_messages" chat\n'   
                'No need to enter any input in this chat'
            )
        case _:
            message.reply_text('Sorry, this command is not valid')


# "3.Find_Telegram_ID" chat handler
def findid_input_handler(client, message):
    args = message.command
    comm = args.pop(0)
    match comm:
        case 'help_general':
            message.reply_text(help_general_text)
        case 'help':
            message.reply_text(
                '/help - show Help options for this chat\n'
                '/help_general - show Help options for all chats\n\n'
                'To find Telegram ID of any chat (user / group / channel / bot / etc.)\n'
                'Enter manually in "3.Find_Telegram_ID" chat:\n'
                '/findid @username | first_name last_name | chat_title\n\n'
               # '\tVariant 2: Forward manually any message from target chat to "3.Find_Telegram_ID" chat. Get automatic reply with target chat ID\n\n' 
                '(Finding IDs may work slowly. Wait for Bot\'s reply)\n'
            )
        case 'findid':
            if (not args):
                return message.reply_text('Smth must be entered manually after /findid command: chat_title | first_name last_name | @username')
            dialogs = find_chats(client, args)
            message.reply_text('\n'.join([' - '.join(dialog) for dialog in dialogs]) if len(
                dialogs) else 'Sorry, nothing is found. Enter manually after /findid - chat_title | first_name last_name | @username')
        case _:
            message.reply_text('Sorry, this command is not valid')


# "7.Dump_all_messages" chat handler
def dump_all_messages_handler(client, message):
    args = message.command
    comm = args.pop(0)
    match comm:
        case 'help_general':
            message.reply_text(help_general_text)
        case 'help':
            message.reply_text(
                '/help - show Help options for this chat\n'
                '/help_general - show Help options for all chats\n'
                '/findid @username | first_name last_name | chat_title - find from_chat_id (may work slowly)\n\n'
                '/dump_all_messages from_chat_id -\n'
                'All messages from a single selected chat are copied & forwarded to "7.Dump_all_messages" chat\n' 
                'Single-time manual backup (NOT automatic, NOT real time monitoring)\n'
            )
        case 'dump_all_messages': # (?)
            if len(args) == 0:
                message.reply_text('Sorry, from_chat_id is not found\n'
                                   'from_chat_id (Telegram ID of the chat to backup messages from) must be entered manually after /dump_all_messages\n\n'
                                   'Please, use this format: /dump_all_messages from_chat_id\n'
                                   'Use /findid to get from_chat_id')  # chat_title | chat_id | @username
            if len(args) > 1:
                message.reply_text('Wrong input:\n' + '\n'.join([arg for arg in args]) + '\n\nPlease enter a single valid from_chat_id after /dump_all_messages')
            if len(args) == 1:
                from_chat_id = args[0]
                try:
                    from_chat_id = int(from_chat_id)
                except ValueError:
                    message.reply("Sorry, from_chat_id is not valid\n "
                                  "from_chat_id (Telegram ID of the chat to backup messages from) must be entered manually after /dump_all_messages\n\n"
                                  'Please, use this format: /dump_all_messages from_chat_id\n'
                                  "Use /findid to get from_chat_id")
                dump_all_messages(user, args[0])
        case 'findid': # (?)
            if (not args):
                return message.reply_text('Smth must be entered manually after /findid command: chat_title | first_name last_name | @username')
            dialogs = find_chats(client, args)
            message.reply_text('\n'.join([' - '.join(dialog) for dialog in dialogs]) if len(
                dialogs) else 'Sorry, nothing is found. Enter manually after /findid - chat_title | first_name last_name | @username')
        case _:
            message.reply_text('Sorry, this command is not valid')


# "8.Dump_replies" chat handler
def dump_replies_chat_input_handler(client, message):
    args = message.command
    comm = args.pop(0)
    match comm:
        case 'help_general':
            message.reply_text(help_general_text)
        case 'help':
            message.reply_text(
                '/help - show Help options for this chat\n'
                '/help_general - show Help options for all chats\n'
                '/findid chat_title | first_name last_name | @username - find "from_chat_id" and "target_user_id"\n\n'
                '/dump_messages_of_target_user_from_chat from_chat_id target_user_id - \n'
                'forward all messages of target user from a selected chat to "8.Dump_replies" chat. \n'
                'Single-time backup launched manually (NOT real time monitoring)\n\n'                
                '/dump_replies from_chat_id target_user_id - \n'
                'forward from a selected chat to "8.Dump_replies" chat:\n'
                'messages of target user that had replies & all these replies.\n' 
                'Single-time backup launched manually (NOT real time monitoring)\n'
            )
        case 'dump_replies': # (?)
            if len(args) != 2:
                # (?) Is "return" necessary to add here?
                message.reply_text('Wrong input\n' 
                                   'Please, enter valid data in this format:\n' 
                                   '/dump_replies from_chat_id target_user_id\n\n'
                                   'Use /findid command to find valid from_chat_id and target_user_id'
                                   )
            if len(args) == 2:
                from_chat_id = args[0]
                target_user_id = args[1]
                try:
                    check_from_chat_id = int(from_chat_id) # (?)
                except ValueError:
                    message.reply_text('Sorry, from_chat_id is not found\n'
                                       'Please, enter valid data in this format:\n'
                                       '/dump_replies from_chat_id target_user_id\n\n'
                                       'Use /findid command to find valid from_chat_id and target_user_id'
                                       )
                try:
                    check_target_user_id = int(target_user_id) # (?)
                except ValueError:
                    message.reply_text('Sorry, target_user_id is not found\n'
                                       'Please, enter valid data in this format:\n'
                                       '/dump_replies from_chat_id target_user_id\n\n'
                                       'Use /findid command to find valid from_chat_id and target_user_id'
                                       )
                # Verifying "from_chat_id" and "target_user_id" are valid Telegram IDs:
                # if not find_chats(client, from_chat_id):
                #     client.send_message(dump_replies_chat_id,
                #                         'Sorry, from_chat_id is not found\n'
                #                         'Please, enter valid data in this format:\n'
                #                         '/dump_replies from_chat_id target_user_id\n\n'
                #                         'Use /findid command to find valid from_chat_id and target_user_id'
                #                         )
                #     return # (?) Did I use "return" in a correct way & place?
                # if not find_chats(client, target_user_id):
                #     client.send_message(dump_replies_chat_id,
                #                         'Sorry, target_user_id is not found\n'
                #                         'Please, enter valid data in this format:\n'
                #                         '/dump_replies from_chat_id target_user_id\n\n'
                #                         'Use /findid command to find valid from_chat_id and target_user_id'
                #                         )
                #     return # (?) Did I use "return" in a correct way & place?

                # (?) (CDL)  Is it correct to use two args in the line below?  (?)Try "client" instead of "user" ?
                dump_replies(user, from_chat_id, target_user_id) # (CDL) This solution works fine now

        case 'dump_messages_of_target_user_from_chat':
            if len(args) != 2:
                # (?) Is "return" necessary to add here?
                message.reply_text('Wrong input\n' 
                                   'Please, enter valid data in this format:\n' 
                                   '/dump_messages_of_target_user_from_chat from_chat_id target_user_id\n\n'
                                   'Use /findid command to find valid from_chat_id and target_user_id'
                                   )
            if len(args) == 2:
                from_chat_id = args[0]
                target_user_id = args[1]
                try:
                    check_from_chat_id = int(from_chat_id) # (?)
                except ValueError:
                    message.reply_text('Sorry, from_chat_id is not found\n'
                                       'Please, enter valid data in this format:\n'
                                       '/dump_messages_of_target_user_from_chat from_chat_id target_user_id\n\n'
                                       'Use /findid command to find valid from_chat_id and target_user_id'
                                       )
                try:
                    check_target_user_id = int(target_user_id) # (?)
                except ValueError:
                    message.reply_text('Sorry, target_user_id is not found\n'
                                       'Please, enter valid data in this format:\n'
                                       '/dump_messages_of_target_user_from_chat from_chat_id target_user_id\n\n'
                                       'Use /findid command to find valid from_chat_id and target_user_id'
                                       )
                # Verifying "from_chat_id" and "target_user_id" are valid Telegram IDs:  # (??) NOT tested yet.
                if not find_chats(client, from_chat_id):  # (??) Is it a good idea to use "find_chats" function here for verification?
                    client.send_message(dump_replies_chat_id,
                                        'Sorry, from_chat_id is not found\n'
                                        'Please, enter valid data in this format:\n'
                                        '/dump_messages_of_target_user_from_chat from_chat_id target_user_id\n\n'
                                        'Use /findid command to find valid from_chat_id and target_user_id'
                                        )
                    return # (?) Did I use "return" in a correct way & place?
                if not find_chats(client, target_user_id):
                    client.send_message(dump_replies_chat_id,
                                        'Sorry, target_user_id is not found\n'
                                        'Please, enter valid data in this format:\n'
                                        '/dump_messages_of_target_user_from_chat from_chat_id target_user_id\n\n'
                                        'Use /findid command to find valid from_chat_id and target_user_id'
                                        )
                    return # (?) Did I use "return" in a correct way & place?
                dump_messages_of_target_user_from_chat(user, from_chat_id, target_user_id)
        case 'findid': # (?)
            if (not args):
                return message.reply_text('Smth must be entered manually after /findid command: chat_title | first_name last_name | @username')
            dialogs = find_chats(client, args)
            message.reply_text('\n'.join([' - '.join(dialog) for dialog in dialogs]) if len(
                dialogs) else 'Sorry, nothing is found. Enter manually after /findid - chat_title | first_name last_name | @username')
        case _:
            message.reply_text('Sorry, this command is not valid')
            print("Printed at the END of 'dump_replies_chat_input_handler' ")  # (CDL) For testing only


# "4.Keywords" chat handler
def keywords_handler(client, message):
    args = message.command
    comm = args.pop(0)
    match comm:
        case 'help_general':
            message.reply_text(help_general_text)
        case 'help':
            message.reply_text(
                '/help - show Help options for this chat\n'
                '/help_general - show Help options for all chats\n'
                '/findid chat_title | first_name last_name | id | @username` - find Telegram ID of chat / user / channel (may work slowly)\n' 
                '/show - show all keywords monitored by bot\n'
                '/add keyword1 keyword2 ... - add new keyword(s)\n'
                '/remove keyword1 keyword2 ... - remove keyword(s)\n'
                '/exclude_chat chat_title | chat_id | @username - exclude chat or user or channel from being monitored by 4.Keywords bot (may work slowly)\n'
                '/excluded_chats_list - show IDs of all excluded chats\n' 
                '/delete_from_excluded_chats chat_id - delete a chat from your excluded chats list\n'
                '/removeall - remove all keywords (turned off currently)\n'
            )
        case 'add':
            for keyword in args:
                keywords.add(keyword.strip().replace(',', ''))
            message.reply_text('processed ' + str(len(args)) + ' keywords')
            save_keywords(keywords)
        case 'show':
            if not keywords:
                message.reply_text('No keywords, add with /add command')
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
        case 'findid':
            if(not args):
                return message.reply_text("Smth must be entered manually after /findid command: chat_title | first_name last_name | id | @username")
            dialogs = find_chats(client, args)
            message.reply_text('\n'.join([' - '.join(dialog) for dialog in dialogs]) if len(
                dialogs) else 'Sorry, nothing is found. Enter manually after /findid - chat_title | chat_id | @username')
        case 'exclude_chat':
            if not args:
                return
            dialogs = find_chats(client, args)
            if(len(dialogs) != 1):
                message.reply_text('More than one chat is found:\n' + '\n'.join([' - '.join(
                    dialog) for dialog in dialogs]) if len(dialogs) else 'Sorry, nothing is found. Paste manually after /exclude_chat - chat_title | chat_id | @username')
            else:
                excluded_chats.add(dialogs[0][0])
                save_excluded_chats(excluded_chats)
                message.reply_text(
                    'This chat was added to excluded chats list:\n' + ' - '.join(dialogs[0]))
        case 'excluded_chats_list':
            dialogs = find_chats(client, args)  # ?
            if not excluded_chats:
                message.reply_text('No excluded chats yet')
            else:
                chatid_chatname_string = ""
                for chat_id in excluded_chats:
                    for dialog in dialogs:
                        if dialog[0] == chat_id:
                            chatid_chatname_string += 'Chat ID: ' + str(chat_id) + ' \tChat name: ' + str(dialog[1]) + '\n'
                message.reply_text('Excluded chats:\n' + chatid_chatname_string)
        case 'delete_from_excluded_chats':
            if not args or not args[0] in excluded_chats:
                message.reply('Not found, use chat_id from your list of excluded chats')
            else:
                excluded_chats.discard(args[0])
                save_excluded_chats(excluded_chats)
                message.reply('{} - this chat was deleted from your list of excluded chats'.format(args[0]))
        case 'include':
            if len(args) < 2:
                return
            chat_name = args.pop(0)
            dialogs = find_chats(client, [chat_name])
            if(len(dialogs) != 1):
                message.reply_text('More than one chat is found:\n' + '\n'.join([' - '.join(
                    dialog) for dialog in dialogs]) if len(dialogs) else 'Sorry, nothing is found')
            else:
                add_keywords_to_includes(dialogs[0][0], args)
                message.reply_text('4.Keywords #{} for the chat:\n'.format(', #'.join(
                    includes_dict[dialogs[0][0]])) + ' - '.join(dialogs[0]))
        case _:
            message.reply_text('Sorry, this command is not valid')

# "5.Following" chat handler
def following_handler(client, message):
    if str(message.chat.id) != following_chat_id: # (?) Why using this line here?
        return
    args = message.command
    comm = args.pop(0)
    match comm:
        case 'help_general':
            message.reply_text(help_general_text)
        case 'help':
            message.reply_text(
                '/help - show Help options for this chat\n'
                '/help_general - show Help options for all chats\n\n'
                'To follow a Telegram user:\n'
                '\tVariant 1: forward manually any message of this user to your "5.Following" chat\n'
                '\tVariant 2: /follow user_ID   # Enter /findid manually to get user_ID\n\n'
                '/show - check IDs of all Telegram users in your current "Following" list\n'
                '/unfollow user_ID - remove a user from your "Following" list\n'
                '/findid @username | first_name last_name | chat_title - find user_ID (may work slowly)'
            )
        case 'findid':
            if (not args):
                return message.reply_text('Smth must be entered manually after /findid command: chat_title | first_name last_name | id | @username')
            dialogs = find_chats(client, args)
            message.reply_text('\n'.join([' - '.join(dialog) for dialog in dialogs]) if len(
                dialogs) else 'Sorry, nothing is found. Paste manually after /findid - @username | first_name last_name | chat_title')
        case 'show':
            message.reply('\n'.join([' - '.join(user) for user in find_users(
                client, following_set)]) if following_set else 'The list is empty')
        case 'unfollow':
            if not args or not args[0] in following_set:
                message.reply('Not found')
            else:
                following_set.discard(args[0])
                save_following(following_set)
                message.reply('{} Deleted from Following'.format(args[0]))
        # (Variant 2) (How to follow a TG user) Follow via inputing manually user's TG id
        case 'follow':
            if len(args) == 0:
                message.reply_text('Sorry, ID is not found. Enter manually Telegram ID of the target user after /follow\n'
                                   'Use /findid to get Telegram ID')  # chat_title | chat_id | @username
            if len(args) > 1:
                message.reply_text('More than one ID entered:\n' + '\n'.join([arg for arg in args]) + '\n\nPlease enter a single valid ID after /follow')
            if len(args) == 1:
                user_id = args[0]
                try:
                    user_id = int(user_id)
                except ValueError:
                    message.reply("Sorry, ID is not valid. Enter manually valid Telegram ID of the target user after /follow\n"
                                  "Use /findid to get Telegram ID")
                if user_id in following_set:
                    message.reply('Following already works for id {}'.format(user_id))  # ..??..
                else:
                    following_set.add(user_id)
                    save_following(following_set)
                    message.reply_text('This ID was added to "following" list:\n' + user_id)
        case _:
            message.reply('Sorry, this command is not valid')


# process incoming messages
# limit to <not me> : ~filters.me (by config?)
# exclude forwards ?
# limit to some types of updates (plain text?)
# limit to private chats / groups / channels (by config?)

# b1: search for keywords
# b2: limit to mentions

# listen to only other users' messages;
# skip message edits for now (TODO: handle edited messages) (?)
@user.on_message(~filters.me & ~filters.edited)  # (?)
def not_my_messages_handler(client, message):
    # process keywords
    if message.text and not str(message.chat.id) in excluded_chats:
        # maybe search -> findall and mark all keywords?
        keyword = re.search("|".join(keywords),
                            message.text, re.IGNORECASE)
        if len(keywords) and keyword:
            keywords_forward(client, message, keyword.group())


    # process mentions
    # message can be a reply with attachment with no text

    # if "Turned_ON" in mentions_monitoring_switcher:
    #     print("aCCept reAliTy")  # (CDL) For testing only
    #     if message.mentioned:
    #         print("acTioN crEaTs mooD")  # (CDL) For testing only
    #         mentions_forward(client, message)

    # if message.mentioned and "Turned_ON" in mentions_monitoring_switcher:
    #     print(" (Ben Franklin) Perform w/ courage what’s necessary, NO exceptions")  # (CDL) For testing only
    #     mentions_forward(client, message)

    if message.mentioned:
        print(mentions_monitoring_switcher)
        print(type(mentions_monitoring_switcher))
        print("aCCept reAliTy")  # (CDL) For testing only
        # print(set(mentions_monitoring_switcher))
        # print(type(set(mentions_monitoring_switcher)))
        # print(mentions_monitoring_switcher[0])
        c1 = config.get('chats_monitoring_switcher_section', 'mentions_monitoring_switcher', fallback='eRroR with get()')
        print(c1)
        print(type(c1))

        # if mentions_monitoring_switcher == "on": # (??) This line does NOT work. Why?
        # if c1 == "on":  # (??) This line does NOT work. Why?
        if c1 == "on":  # (??) This line does NOT work. Why?
            print("(Ben Franklin) Perform w/ courage what’s necessary, NO exceptions")  # (CDL) For testing only
            mentions_forward(client, message)


    # process following
    if message.from_user and str(message.from_user.id) in following_set:
        following_forward(client, message)


# process Pinned messages
@user.on_message(filters.pinned_message, 1)  # "1" - group identifier parameter for the decorator
def pinned_messages_handler(client, message):
    pinned_messages_forward(client, message)
    # (?) (CDL) Also if necessary, use "message.pinned_message" method from https://docs.pyrogram.org/api/types/Message#pyrogram.types.Message


# process Deleted messages
@user.on_deleted_messages(~filters.me)  # (?) "NOT-me" filter does NOT work correctly now
def deleted_messages_handler(client, message): # https://docs.pyrogram.org/api/decorators#pyrogram.Client.on_deleted_messages
    # print("2. (Watts)  At EVERY moment of life: you are already “there” = liberated = enlightened = in the optimal place / state / moment = where you tried & dreamed to get."!
    deleted_messages_forward(client, message)


# process Edited messages
# Variant N2   *** https://docs.pyrogram.org/api/decorators#pyrogram.Client.on_message
@user.on_message(~filters.me & filters.edited & filters.private) # (?)
def edited_messages_handler(client, message):
    edited_messages_forward(client, message)
# process Edited messages
# Variant N1.  *** on_edited_message decorator did NOT work for Pyrogram 1.4  https://docs.pyrogram.org/api/decorators#pyrogram.Client.on_edited_message
# @user.on_edited_message(~filters.me)  # (?)
# def edited_messages_handler(client, message):
#     if message: # (?)
#         edited_messages_forward(client, message)  # (?)



def make_user_mention(user):
    name = str(user.first_name) + ' ' + str(user.last_name).strip()
    return '[{}](tg://user?id={})'.format(name, user.id)


def make_message_description(message):
    # Direct Messages
    if message.chat.type == 'private':
        source = 'in Direct Messages ({})'.format(make_user_mention(message.from_user))
    # Channels
    elif message.chat.type == 'channel':
        source = 'in channel {} @{}'.format(message.chat.title, message.chat.username)
    # Groups and Supergroups
    else:
        source_chat_name = str(message.chat.title) if message.chat.title else '<unnamed chat>'
        source_chat_link = ' @' + str(message.chat.username) if message.chat.username else ''
        source = 'in chat "{}" {} by {}'.format(source_chat_name, source_chat_link, make_user_mention(message.from_user))

    # forward of forward loses the first person
    if message.forward_from:
        return '{}, forwarded from - {}'.format(source, make_user_mention(message.forward_from))

    return source


# def dump_replies_forward(client, message):  # (CDL) This function is NOT used now
#     source = make_message_description(message)
#     # client.send_message(dump_replies_chat_id, '"Reply" to target user\'s message {}'.format(source))
#     message.forward(dump_replies_chat_id)
#     client.mark_chat_unread(dump_replies_chat_id)


def keywords_forward(client, message, keyword):
    source = make_message_description(message)
    client.send_message(keywords_chat_id, '#{} {}'.format(keyword, source))
    message.forward(keywords_chat_id)
    client.mark_chat_unread(keywords_chat_id)


def mentions_forward(client, message):
    source = make_message_description(message)
    client.send_message(mentions_chat_id, 'Your Telegram account was mentioned {}'.format(source))
    message.forward(mentions_chat_id)
    client.mark_chat_unread(mentions_chat_id)


def following_forward(client, message):
    source = make_message_description(message)
    client.send_message(following_chat_id, 'Action detected {}'.format(source))
    message.forward(following_chat_id)
    client.mark_chat_unread(following_chat_id)


def deleted_messages_forward(client, message):
    # source = make_message_description(message)
    # client.send_message(edited_and_deleted_chat_id, 'Deleted message {}:'.format(source))
    # message.forward(edited_and_deleted_chat_id)
    client.send_message(edited_and_deleted_chat_id, "Deleted message detected:\n"
                                                    f"message_id: {message[0]['message_id']}\n"
                                                    "(?) Date & time of deletion: ... \n" # (?) Try tu use message_id OR just use the time of the notification
                                                    "(later feature) Chat ID where deletion happened: ...\n"  # (?) Try to use message_id 
                                                    "(later feature) Original message BEFORE being deleted: ..."
                        )
    client.mark_chat_unread(edited_and_deleted_chat_id)


def edited_messages_forward(client, message):
    source = make_message_description(message)
    client.send_message(edited_and_deleted_chat_id, 'Message AFTER being edited {}:'.format(source))
    message.forward(edited_and_deleted_chat_id)
    client.mark_chat_unread(edited_and_deleted_chat_id)


def pinned_messages_forward(client, message): # (?) “Pinned” forwarding is NOT working at ALL.  ***Other commands in “Pinned” chat work fine.  ***Function pinned_messages_forward is NOT called,
    print("(Doris Lessing) Whatever you're meant to do, do it now. The conditions are always impossible.") # (?) (CDL) For testing only
    client.send_message(pinned_messages_chat_id, f"PiNNed message detected:\n {message}")  # (?) TEST it & the lines below
    # source = make_message_description(message)
    # client.send_message(pinned_messages_chat_id, 'Pinned message {}:'.format(source))
    # message.forward(pinned_messages_chat_id)
    client.mark_chat_unread(pinned_messages_chat_id)


def start_bot():
    # TODO catch 401 error when session is expired / removed, delete user.session file and try again
    user.start()
    user_info = user.get_me()

    for k in chat_dict:
        # print("(priNting fRom bot.py) 'globals()[chat_dict[k]]' == ", globals()[chat_dict[k]], " // 'k' == ", k)  # (CDL) For testing only
        if not globals()[chat_dict[k]]: # (??) How does this line work for the first session launch?
            new_chat = user.create_group(k, user_info.id)
            globals()[chat_dict[k]] = new_chat.id
            config_set_and_save('bot_params', chat_dict[k], str(new_chat.id))

    # print("(V1. priNting fRom bot.py) 'globals()['mentions_monitoring_switcher']' == ", globals()['mentions_monitoring_switcher'])  # (CDL) For testing only
    if not globals()['mentions_monitoring_switcher']:
        # print("(V2. priNting fRom bot.py) 'globals()['mentions_monitoring_switcher']' == ", globals()['mentions_monitoring_switcher'])  # (CDL) For testing only
        config_set_and_save('chats_monitoring_switcher_section', 'mentions_monitoring_switcher', 'on')


    # init message
    # user.send_message(keywords_chat_id, 'bot started')
    # user.send_message(mentions_chat_id, 'bot started')
    # user.send_message(following_chat_id, 'bot started')
    print('bot started')
    idle()

    # stop message
    # user.send_message(keywords_chat_id, 'bot stopped')
    # user.send_message(mentions_chat_id, 'bot stopped')
    # user.send_message(following_chat_id, 'bot stopped')
    print('stopping bot...')
    user.stop()
    print('bot stopped')
