import configparser
import ast

config = configparser.ConfigParser()
inventory_coords = None
stash_coords = None

def create_stash_coords():
    stash_width = int(config["STASH"]["end_x"]) - int(config["STASH"]["start_x"])
    stash_height = int(config["STASH"]["end_y"]) - int(config["STASH"]["start_y"])
    step_x = stash_width / 48
    step_y = stash_height / 48
    coords = []
    for i in range(1, 49, 2):
        for j in range(1, 49, 2):
            coords.append((round(int(config["STASH"]["start_x"]) + step_x * i), round(int(config["STASH"]["start_y"]) + step_y *  j)))

    return coords


def create_inventory_coords(safe_cols):
    inv_width = int(config["INVENTORY"]["end_x"]) - int(config["INVENTORY"]["start_x"])
    inv_height = int(config["INVENTORY"]["end_y"]) - int(config["INVENTORY"]["start_y"])
    step_x = inv_width / 24
    step_y = inv_height / 10
    coords = []
    for i in range(1, 25, 2):
        for j in range(1, 11, 2):
            coords.append((round(int(config["INVENTORY"]["start_x"]) + step_x * i), round(int(config["INVENTORY"]["start_y"]) + step_y *  j)))

    return coords

def save_config():
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def load_config():
    config.read("config.ini")
    for section in config.sections():
        for key in config[section]:
            debug((key, config[section][key]))

def debug(text):
    global config
    try:
        if bool(config["SETTINGS"]["debug"]):
            print(text)
    except Exception:
        return

load_config()
inventory_coords = create_inventory_coords(int(config["SETTINGS"]["safe_columns"]))
stash_coords = create_stash_coords()