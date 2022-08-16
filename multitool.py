import configuration as cfg
import math, time, keyboard, pyautogui
import numpy as np
from datetime import datetime

cfg.load_config()
pyautogui.PAUSE = 1 / float(cfg.config["SETTINGS"]["click_speed"])

def run():
    while True:
        time.sleep(0.01)
        if keyboard.is_pressed('ctrl+' + cfg.config["SETTINGS"]["stash_hotkey"]) or keyboard.is_pressed('ctrl+shift+' + cfg.config["SETTINGS"]["stash_hotkey"]):
            current_pos = pyautogui.position()
            if in_stash_range(current_pos):
                loadin(current_pos)
            else:
                loadout(current_pos)
        if keyboard.is_pressed('shift+' + cfg.config["SETTINGS"]["card_hotkey"]):
            #minutes_diff = (datetime_end - datetime_start).total_seconds() / 60.0
            drop_div_cards()


def loadin(default_pos):
    current_block = get_closest_stash_block()
    current_block_number = cfg.stash_coords.index(current_block)
    for block in cfg.stash_coords[current_block_number:]:
        if keyboard.is_pressed('ctrl+' + cfg.config["SETTINGS"]["stash_hotkey"]) or keyboard.is_pressed('ctrl+shift+' + cfg.config["SETTINGS"]["stash_hotkey"]):
            pyautogui.moveTo(block)
            pyautogui.click()
        else:
            break
    pyautogui.moveTo(default_pos)
    time.sleep(1)

def loadout(default_pos):
    if int(cfg.config["SETTINGS"]["safe_columns"]) * -5 != 0:
        safe_columns = int(cfg.config["SETTINGS"]["safe_columns"]) * -5
    else:
        safe_columns = len(cfg.inventory_coords)

    if in_inv_range(default_pos):
        current_block = get_closest_inventory_block()
        current_block_number = cfg.inventory_coords.index(current_block)
    else:
        current_block_number = 0
    for block in cfg.inventory_coords[current_block_number:safe_columns]:
        if keyboard.is_pressed('ctrl+' + cfg.config["SETTINGS"]["stash_hotkey"]) or keyboard.is_pressed('ctrl+shift+' + cfg.config["SETTINGS"]["stash_hotkey"]):
            pyautogui.moveTo(block)
            pyautogui.click()
        else:
            break
    pyautogui.moveTo(default_pos)
    time.sleep(1)


def drop_div_cards():
    card_pos = pyautogui.position()
    pyautogui.moveTo(card_pos[0], card_pos[1], 0.025)
    pyautogui.click(button='right')
    time.sleep(0.05)
    pyautogui.moveTo(cfg.inventory_coords[0][0] - 100, cfg.inventory_coords[0][1], 0.05)
    pyautogui.click()
    time.sleep(0.05)
    pyautogui.moveTo(card_pos[0], card_pos[1])
    return


def get_closest_stash_block():
    current_pos = pyautogui.position()

    xy = np.array(cfg.stash_coords).T
    # Euclidean distance
    d = ((xy[0] - current_pos[0]) ** 2 + (xy[1] - current_pos[1]) ** 2) ** 0.5

    closest_idx = np.argmin(d)
    closest_block = cfg.stash_coords[closest_idx]

    return closest_block


def get_closest_inventory_block():
    current_pos = pyautogui.position()

    if not in_inv_range(current_pos):
        cfg.inventory_coords[0]

    xy = np.array(cfg.inventory_coords).T
    # Euclidean distance
    d = ((xy[0] - current_pos[0]) ** 2 + (xy[1] - current_pos[1]) ** 2) ** 0.5

    closest_idx = np.argmin(d)
    closest_block = cfg.inventory_coords[closest_idx]

    return closest_block


def in_stash_range(coords):
    stash_start = (int(cfg.config["STASH"]["start_x"]), int(cfg.config["STASH"]["start_y"]))
    stash_size = (int(cfg.config["STASH"]["end_x"]) - int(cfg.config["STASH"]["start_x"]), int(cfg.config["STASH"]["end_y"]) - int(cfg.config["STASH"]["start_y"]))
    if coords[0] not in range(stash_start[0], stash_start[0] + stash_size[0]) or coords[1] \
            not in range(stash_start[1], stash_start[1] + stash_size[1]):
        return False
    return True


def in_inv_range(coords):
    inventory_start = (int(cfg.config["INVENTORY"]["start_x"]), int(cfg.config["INVENTORY"]["start_y"]))
    inventory_size = (int(cfg.config["INVENTORY"]["end_x"]) - int(cfg.config["INVENTORY"]["start_x"]), int(cfg.config["INVENTORY"]["end_y"]) - int(cfg.config["INVENTORY"]["start_y"]))
    if coords[0] not in range(inventory_start[0], inventory_start[0] + inventory_size[0]) or coords[1] \
            not in range(inventory_start[1], inventory_start[1] + inventory_size[1]):
        return False
    return True


if __name__ == '__main__':
    print("PoE Loadout is running.")
    run()