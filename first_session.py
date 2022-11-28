from configparser import ConfigParser

def first_session_func():
    config = ConfigParser()
    config.read('config.ini')  # ? Can config.ini file be read, if it has NOT been created yet?

    if not config.has_section('pyrogram'):  # ? How does the script understand that config.ini file should be opened?
        config.add_section('pyrogram')  # ? Can 'pyrogram' section be added, if config.ini file has NOT been created yet?
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    api_id = config.get('pyrogram', 'api_id', fallback=None)  # ? Is this line vital now? If yes - is it in the right place?
    api_hash = config.get('pyrogram', 'api_hash', fallback=None)  # ? Is this line vital now? If yes - is it in the right place?

    if not api_id:
        inputed_api_id = input("Paste your Telegram App's `api_id' here: ")
        # check if the string inputed_api_id is empty
        config.set('pyrogram', 'api_id', inputed_api_id)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    if not api_hash:
        inputed_api_hash = input("Paste your Telegram App's `api_hash' here: ")
        # check if the string inputed_api_hash is empty
        config.set('pyrogram', 'api_hash', inputed_api_hash)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)


# first_session_func()   #  for testing


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
