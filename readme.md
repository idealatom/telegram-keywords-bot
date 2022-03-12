## wip

### setup
- install python (https://www.python.org/downloads/)
- install pyrogram and tgcrypto (pip3 install -U pyrogram tgcrypto), more info here: https://docs.pyrogram.org/intro/install
- clone this repo
- copy config_sample.ini to config.ini and edit it with your personal api id and api hash (get here: https://my.telegram.org/auth?to=apps)
- start with python ./main.py

### commands
#### I. Keywords bot
forwards messages that contain specified keywords to Keywords chat
- /add keyword1 keyword2 ...etc - add new keyword(s) to global listener
- /remove keyword1 keyword2 ...etc - remove keyword(s) from global listener
- /removeall - remove all keywords from global listener (turned off currently)
- /show - show all keywords
- /findchat username|first name last name|chat title

#### II. Mentions bot
forwards all your mentions and message replies (counts as mentions) to Mentions chat
wip

#### III. Following Bot
forwards all messages from specified users to Following chat
todo
