import os
from configparser import ConfigParser

from bot import start_bot

def create_configini_file():
    config = ConfigParser()
    config.read('config.ini')

    if not config.has_section('pyrogram'):
        config.add_section('pyrogram')
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    api_id = config.get('pyrogram', 'api_id', fallback=None)
    if not api_id:
        raise Exception("Please specify your Telegram App's `api_id' in config.ini file.")

    api_hash = config.get('pyrogram', 'api_hash', fallback=None)
    if not api_hash:
        raise Exception("Please specify your Telegram App's `api_hash' in config.ini file.")


if __name__ == '__main__':
    os.environ['PYTHONBREAKPOINT']="pudb.set_trace"
    create_configini_file()  # Should this line be here or below?
    start_bot()
