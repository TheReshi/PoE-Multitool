import configparser

config = configparser.ConfigParser()
inventory_coords = None
stash_coords = None

def save_config():
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def load_config():
    global config
    config.read("config.ini")
    for section in config.sections():
        for key in config[section]:
            print((key, config[section][key]))