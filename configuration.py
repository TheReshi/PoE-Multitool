import configparser
import ast

config = configparser.ConfigParser()
inventory_coords = None
stash_coords = None

def create_stash_coords():
    stash_width = int(config["STASH"][f"end_x{inv_suffix}"]) - int(config["STASH"][f"start_x{inv_suffix}"])
    stash_height = int(config["STASH"][f"end_y{inv_suffix}"]) - int(config["STASH"][f"start_y{inv_suffix}"])
    step_x = stash_width / 48
    step_y = stash_height / 48
    coords = []
    for i in range(1, 49, 2):
        for j in range(1, 49, 2):
            coords.append((round(int(config["STASH"][f"start_x{inv_suffix}"]) + step_x * i), round(int(config["STASH"][f"start_y{inv_suffix}"]) + step_y *  j)))

    return coords


def create_inventory_coords():
    inv_width = int(config["INVENTORY"][f"end_x{inv_suffix}"]) - int(config["INVENTORY"][f"start_x{inv_suffix}"])
    inv_height = int(config["INVENTORY"][f"end_y{inv_suffix}"]) - int(config["INVENTORY"][f"start_y{inv_suffix}"])
    step_x = inv_width / 24
    step_y = inv_height / 10
    coords = []
    for i in range(1, 25, 2):
        for j in range(1, 11, 2):
            coords.append((round(int(config["INVENTORY"][f"start_x{inv_suffix}"]) + step_x * i), round(int(config["INVENTORY"][f"start_y{inv_suffix}"]) + step_y *  j)))

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
        if config["SETTINGS"]["debug"] == "True":
            print(text)
    except Exception:
        return

load_config()
inv_suffix = ""
if config["SETTINGS"]["widescreen"].lower() == "true":
    inv_suffix = "_1080p_wide"
inventory_coords = create_inventory_coords()
stash_coords = create_stash_coords()