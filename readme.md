### Prerequisites
- [Docker](https://www.docker.com/) installed on your machine
- [Telegram](https://telegram.org/) account

### Setup and authorization via Terminal
- clone this repo
- create a new App attached to your Telegram account [here](https://my.telegram.org/auth?to=apps) ('URL' & 'Description' fields may be kept empty, 'Platform' - select 'Web')
- Create `config.ini` (see `config.init.example`) and paste there your Telegram App's `api_id` and `api_hash`. Get them from 'App configuration' at https://my.telegram.org/apps
- Run `docker compose up` - to build and run Docker container
- [Pyrogram](https://docs.pyrogram.org/) asks to enter the phone number attached to your Telegram account (just digits including Country Code, other symbols can be omitted)
- Paste confirmation code sent by Telegram to your account
- If your Telegram account has two-step verification enabled - your password will be required
- When you see `bot started` phrase in Terminal - eight new chats appear in your Telegram account:
  - ‘1.Mentions’
  - '2.Pinned_messages'
  - '3.Find_Telegram_ID'
  - ‘4.Keywords’
  - ‘5.Following’
  - '6.Edited_and_Deleted_messages_monitoring'
  - '7.Dump_all_from_selected_chat'
  - '8.Dump_replies'
- Stop the running script: `Ctrl+C`

- (optional) Run `docker compose up -d` to launch bot 24/7 in a container
- (optional) (in Telegram) Create a new Folder & add to it manually these eight new chats
Then - archive manually each of these eight chats from 'All chats' to 'Archived Chats'
So these eight chats are kept in a separate Folder & do NOT disturb you

- (optional) To launch Bot with the same Telegram account & data on another machine (aka backup, restore & migrate) transfer `config.ini` and `user.session` files from this directory to another host

### Features
#### 1.Mentions
Automatically forwards all messages from chats where your TG account was mentioned (tagged) to '1.Mentions' chat
Replies to your messages are also counted as mentions
#### 2.Pinned_messages
Pinned messages from all chats are automatically forwarded to your '2.Pinned_messages' chat
#### 3.Find_Telegram_ID
To find Telegram ID of any chat (user / group / channel / bot / etc.):
- Enter manually in '3.Find_Telegram_ID' chat: `/findid @username | first_name last_name | chat_title`
_- (??) (NOT build yet!) Variant 3: Enter `/findid` in target chat. Get automatic reply with target chat ID. Reply message is deleted after (?)10 seconds_
#### 4.Keywords
Your chats (all or selected) are monitored in real time. Messages containing specific keywords are forwarded to '4.Keywords' chat
##### In ‘4.Keywords’ chat:
- `/help` - show Help options
- `/findid chat_title | first_name last_name | id | @username` - find Telegram ID of chat / user / channel
- `/show` - show all keywords monitored by bot
- `/add keyword1 keyword2 ...` - add new keyword(s)
- `/remove keyword1 keyword2 ...` - remove keyword(s)
- `/exclude_chat chat_title | chat_id | @username` - exclude chat or user or channel from being monitored by 4.Keywords bot
- `/excluded_chats_list` - show IDs of all excluded chats
- `/delete_from_excluded_chats chat_id` - delete a chat from your excluded chats list
- `/removeall` - remove all keywords from global listener (turned off currently)
#### 5.Following
Forwards all messages of a specified TG user(s) from chats you participate together to '5.Following' chat
##### In ‘5.Following’ chat:
- `/help` - show Help options
- `/show` - check IDs of all Telegram users in your current 'Following' list
- `/findid @username | first_name last_name | chat_title` - find user_ID
- To start following a Telegram user:
  - Variant 1: forward manually any message of this user to your '5.Following' chat
  - Variant 2: `/follow user_ID`   # Use `/findid` command manually to get user_ID
- `/unfollow user_ID` - remove a user from your 'Following' list
#### (?) 6.Edited_and_Deleted_messages_monitoring
_(?) (CDL) # UPDATE these instructions AFTER fixing bugs with 'Deleted' feature_
- Your DMs (direct messages) are monitored in real time
- (?) Details about every edited & deleted message automatically come to your ‘6.Edited_and_Deleted_messages_monitoring’ chat
- Details: user / chat, date, time, message content AFTER being updated (for 'Deleted' - NO content)
- (next feature) Select manually specific user(s) / group(s) / channel(s) to monitor
- (next big feature) Get ORIGINAL version of message - BEFORE being edited / deleted by smb. # Adding a database is necessary to backup your correspondence in real time
#### 7.Dump_all_from_selected_chat
All messages from a single selected chat are copied & forwarded to '7.Dump_all_from_selected_chat' chat
Single-time backup launched manually (NOT real time monitoring)
##### In ‘7.Dump_all_from_selected_chat’ chat:
- `/help` - show Help options
- `/findid chat_title | first_name last_name | @username` - find `from_chat_id`
- `/dump_all_from_selected_chat from_chat_id` - forward all messages from a single selected chat to '7.Dump_all_from_selected_chat' chat
#### 8.Dump_replies
Messages of target user and / or replies to them are forwarded to '8.Dump_replies' chat from a selected chat
Single-time backup launched manually (NOT real time monitoring)
##### In ‘8.Dump_replies’ chat:
- `/help` - show Help options
- `/findid chat_title | first_name last_name | @username` - find `from_chat_id` and `target_user_id`
- `/dump_replies from_chat_id target_user_id` - forward from a selected chat to "8.Dump_replies" chat:
messages of target user that had replies & all these replies
- `/dump_all_messages_of_target_user_from_selected_chat from_chat_id target_user_id` - forward all messages of target user from a selected chat to "8.Dump_replies" chat
### Pay attention:
- This bot is a Telegram client & an app. It is NOT a ‘usual TG bot via BotFather’. NO need to create a new bot via BotFather
- [Pyrogram](https://docs.pyrogram.org/) (version 1.4, NOT version 2.0) is used - [MTProto API](https://docs.pyrogram.org/topics/mtproto-vs-botapi) framework to interact with the main Telegram API
- Data about your keywords & Telegram users who you follow is saved to `config.ini` file
