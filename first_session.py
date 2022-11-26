from configparser import ConfigParser
from config import config_set_and_save

config = ConfigParser()
config.read('config.ini')

def first_session_func():
    if not config.has_section('pyrogram'):
        # print("1")
        config.add_section('pyrogram')

    api_id = config.get(section='pyrogram', option='api2_id', fallback=None)
    api_hash = config.get('pyrogram', 'api2_hash', fallback=None)

    if not api_id:
        inputed_api_id = input("Write api_id")
        # check if the string inputed_api_id is empty
        config_set_and_save('pyrogram', 'api2_id', inputed_api_id)

    if not api_hash:
        inputed_api_hash = input("Write api_hash")
        # check if the string inputed_api_hash is empty
        config_set_and_save('pyrogram', 'api2_hash', inputed_api_hash)


    # 0. Check if config.ini file exists, if it's not - create it.
    # with open('config.ini', 'a') as config_ini_file:
    #     if not api_id and api_hash in config_ini_file:
    #         api_id_input = input("Please, paste your Telegram App's `api_id' here (get it from 'App configuration' at https://my.telegram.org/apps"))
    #         api_id_hash = input("Please, paste your Telegram App's `api_hash' here (get it from 'App configuration' at https://my.telegram.org/apps"))


    # def config_set_and_save(section, param_name, param_value, skip_set=False):
    #     if (not skip_set):
    #         config.set(section, param_name, param_value)
    #     with open('config.ini', 'w') as configfile:
    #         config.write(configfile)


    # if api_id:
    #     print('aCt!')
        # api_id = input("Please, paste your Telegram App's `api_id' here (get it from 'App configuration' at https://my.telegram.org/apps")
#        hash_id = input("Please, paste your Telegram App's `api_hash' here (get it from 'App configuration' at https://my.telegram.org/apps")
