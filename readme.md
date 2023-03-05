### Prerequisites
- [Docker](https://www.docker.com/) installed on your machine
- [Telegram](https://telegram.org/) account 

### Setup and authorization via Terminal
- clone this repo  
- create a new App attached to your Telegram account [here](https://my.telegram.org/auth?to=apps) ('URL' & 'Description' fields may be kept empty, 'Platform' - select 'Web') 
- Run `docker volume create your_volume_name` - to create Docker volume on your host
- Run `docker build -t your_image_name .` - to build image from `Dockerfile`
- Run `docker run -it --rm -v your_volume_name:/app your_image_name` - to login to your Telegram account 
- Paste your Telegram App's `api_id` and `api_hash`. Get them from 'App configuration' at https://my.telegram.org/apps 
- [Pyrogram](https://docs.pyrogram.org/) asks to enter the phone number attached to your Telegram account (just digits including your Country Code digit(s), other symbols can be omitted)
- Paste confirmation code sent by Telegram to your account 
- If your Telegram account has two-step verification enabled - your password will be required 
- When you see `bot started` phrase in Terminal - four new chats (‘Keywords’, ‘Following’, ‘Mentions’, 'Backup_all_messages') will appear in your Telegram account  
- Stop the running script: `Ctrl+C`
- Run `docker run -d -v your_volume_name:/app --restart unless-stopped your_image_name` - launch bot in a container 

### Features
#### 1. Keywords
Forwards incoming messages that contain specified keywords to 'Keywords' chat  
##### In ‘Keywords’ chat:
- `/help` - show Help options
- `/findid chat_title | first_name last_name | id | @username` - find IDs & names of chats or users or channels (may work slowly, wait for bot's response) 
- `/show` - show all keywords monitored by bot
- `/add keyword1 keyword2 ...` - add new keyword(s)
- `/remove keyword1 keyword2 ...` - remove keyword(s)
- `/exclude_chat chat_title | chat_id | @username` - exclude chat or user or channel from being monitored by Keywords bot (may work slowly)
- `/excluded_chats_list` - show IDs of all excluded chats 
- `/delete_from_excluded_chats chat_id` - delete a chat from your excluded chats list
- `/removeall` - remove all keywords from global listener (turned off currently)
~~- `/backup_all_messages from_chat_id` - forward all messages from some chat to 'Backup_all_messages' chat. Use `/findid` command manually to get chat ID~~
#### 2. Mentions
Automatically forwards all messages from chats where your TG account was mentioned (tagged) to 'Mentions' chat   
Replies to your messages are also counted as mentions 
#### 3. Following
Forwards all messages of a specified TG user(s) from chats you participate together to 'Following' chat  
##### In ‘Following’ chat:
- `/help` - show Help options
- `/show` - check IDs of all Telegram users in your current 'Following' list
- To start following a Telegram user:
  - Variant 1: forward manually any message of this user to your 'Following' chat
  - Variant 2: `/follow user_ID`   # Use `/findid` command manually to get user_ID
- `/unfollow user_ID` - remove a user from your 'Following' list
- `/findid @username | first_name last_name | chat_title` - find user_ID (may work slowly)
#### (?) 4. Backup_all_messages  
All messages from some selected chat are copied & forwarded to 'Backup_all_messages' chat 
Single-time manual backup (NOT automatic, NOT in real time)
##### (?) In ‘Backup_all_messages’ chat:
- (?) `/help` - show Help options
- (?) `/backup_all_messages from_chat_id` - forward all messages from some selected chat to 'Backup_all_messages' chat 
- (?) `/findid chat_title | first_name last_name | @username` - find `from_chat_id` (may work slowly)

### Pay attention:
- This bot is a Telegram client & an app. It is NOT a ‘usual TG bot via BotFather’, so NO need to create a new bot via BotFather 
- [Pyrogram](https://docs.pyrogram.org/) (version 1.4, NOT version 2.0) is used - [MTProto API](https://docs.pyrogram.org/topics/mtproto-vs-botapi) framework to interact with the main Telegram API 
- Data about your keywords & Telegram users who you follow is saved to `config.ini` file 
