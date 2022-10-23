FROM python:3.10

ADD . /telegram-keywords-bot
WORKDIR /telegram-keywords-bot

RUN make /container1

RUN sudo apt update && sudo apt upgrade -y

RUN sudo apt install software-properties-common -y
RUN sudo add-apt-repository ppa:deadsnakes/ppa -y
RUN sudo apt install python3.10

RUN sudo apt install python3-pip

RUN sudo pip install -r requirements.txt

# (?) copy config_sample.ini to config.ini and edit it with your personal App api_id and api_hash (get here: https://my.telegram.org/auth?to=apps)

CMD python3.10 container1/main.py



