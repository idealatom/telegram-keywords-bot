### Prerequisites
- [Docker](https://www.docker.com/) installed on your machine
- [Telegram](https://telegram.org/) account 

### Setup and authorization via Terminal
- clone this repo  
- create a new App attached to your Telegram account [here](https://my.telegram.org/auth?to=apps) ('URL' & 'Description' fields may be kept empty, 'Platform' - select 'Web') 
- Run `docker volume create your_volume_name` - to create Docker volume on your host 
- Run `docker run -it --rm -v your_volume_name:/app ghcr.io/ds-jr/telegram-keywords-bot-image_3` - to login to your Telegram account 
- Paste your Telegram App's `api_id` and `api_hash`. Get them from 'App configuration' at https://my.telegram.org/apps 
- Pyrogram asks to enter the phone number attached to your Telegram account (just digits including your Country Code digit(s), other symbols can be omitted)
- Paste confirmation code sent by Telegram to your account 
- If your Telegram account has two-step verification enabled - your password will be required 
- When you see `bot started` phrase in Terminal - four new chats (‘Keywords’, ‘Following’, ‘Mentions’, 'forward_all_messages') will appear in your Telegram account  
- Stop the running script: `Ctrl+C`
- Run `docker run -d -v your_volume_name:/app --restart unless-stopped ghcr.io/ds-jr/telegram-keywords-bot-image_3` - launch bot in a container 

### Commands
#### 1. Keywords bot
Forwards messages that contain specified keywords to 'Keywords' chat  
##### In ‘Keywords’ chat:
- /help - shows Help options
- /add keyword1 keyword2 ... - add new keyword(s)
- /remove keyword1 keyword2 ... - remove keyword(s)
- /show - show all keywords monitored by bot
- /exclude_chat chat_title | chat_id | @username - exclude chat or user or channel from being monitored by Keywords bot (may work slowly, wait for bot's response)
- /excluded_chats_list - show IDs of all excluded chats 
- /delete_from_excluded_chats chat_id - delete a chat from your excluded chats list
- /findid chat_title | first_name last_name | id | @username - find IDs & names of chats or users or channels (may work slowly, wait for bot's response) 
- /removeall - remove all keywords from global listener (turned off currently)
- /forward_all_messages from_chat_id - forward all messages from some chat to 'forward_all_messages' chat. Use /findid command manually to get chat ID

#### 2. Mentions bot
Messages from all chats where your TG account was mentioned (tagged) will be forwarded to 'Mentions' chat
Replies to your messages are also counted as mentions 
#### 3. Following Bot
Forwards all messages from specified TG user(s) to 'Following' chat  
##### In ‘Following’ chat:
- /help - show Help options
- To follow a Telegram user:
  - Variant 1: forward manually any message of this user to your 'Following' chat
  - Variant 2: /follow user_ID   # Enter /findid manually to get user_ID
- /show - check IDs of all Telegram users in your current 'Following' list
- /unfollow user_ID - remove a user from your 'Following' list
- /findid @username | first_name last_name | chat_title - find user_ID (may work slowly, wait for bot\'s response)

### Pay attention:
- This bot is a Telegram client & an app. It is NOT a ‘usual TG bot via BotFather’, so do NOT create a new bot via BotFather 
- [Pyrogram](https://docs.pyrogram.org/) is used in the bot. It is [MTProto API](https://docs.pyrogram.org/topics/mtproto-vs-botapi) framework to interact with the main Telegram API 
- Data about your keywords & Telegram users who you follow is saved to config.ini file 
