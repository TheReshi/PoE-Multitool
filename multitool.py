#Start: 1910, 590
#End: 2545, 850

import configuration as cfg
import math, time, keyboard, pyautogui
import numpy as np

pyautogui.PAUSE = 0.01

def run():
    while True:
        time.sleep(0.01)
        if keyboard.is_pressed('ctrl+' + cfg.config["SETTINGS"]["hotkey"]) or keyboard.is_pressed('ctrl+shift+' + cfg.config["SETTINGS"]["hotkey"]):
            default_pos = pyautogui.position()
            loadout(default_pos)

def loadout(default_pos):
    current_block = get_closest_block()
    current_block_number = cfg.coords.index(current_block)
    for block in cfg.coords[current_block_number:]:
        if keyboard.is_pressed('ctrl+' + cfg.config["SETTINGS"]["hotkey"]) or keyboard.is_pressed('ctrl+shift+' + cfg.config["SETTINGS"]["hotkey"]):
            pyautogui.moveTo(block)
            pyautogui.click()
        else:
            break
    pyautogui.moveTo(default_pos)
    time.sleep(1)

def get_closest_block():
    current_pos = pyautogui.position()

    if not in_inv_range(current_pos):
        cfg.coords[0]

    xy = np.array(cfg.coords).T
    # Euclidean distance
    d = ((xy[0] - current_pos[0]) ** 2 + (xy[1] - current_pos[1]) ** 2) ** 0.5

    closest_idx = np.argmin(d)
    closest_block = cfg.coords[closest_idx]

    return closest_block

def in_inv_range(coords):
    inventory_start = (int(cfg.config["INVENTORY"]["start_x"]), int(cfg.config["INVENTORY"]["start_y"]))
    inventory_size = (int(cfg.config["INVENTORY"]["start_x"]) - int(cfg.config["INVENTORY"]["end_x"]), int(cfg.config["INVENTORY"]["start_y"]) - int(cfg.config["INVENTORY"]["end_y"]))
    if coords[0] not in range(inventory_start[0], inventory_start[0] + inventory_size[0]) or coords[1] \
            not in range(inventory_start[1], inventory_start[1] + inventory_size[1]):
        return False
    return True

def create_inventory_coords(safe_cols):
    inv_width = int(cfg.config["INVENTORY"]["end_x"]) - int(cfg.config["INVENTORY"]["start_x"])
    inv_height = int(cfg.config["INVENTORY"]["end_y"]) - int(cfg.config["INVENTORY"]["start_y"])
    step_x = inv_width / 24
    step_y = inv_height / 10
    coords = []
    for i in range(1, 25 - safe_cols * 2, 2):
        for j in range(1, 11, 2):
            coords.append((round(int(cfg.config["INVENTORY"]["start_x"]) + step_x * i), round(int(cfg.config["INVENTORY"]["start_y"]) + step_y *  j)))

    return coords


def debug(text):
    if bool(cfg.config["SETTINGS"]["debug"]):
        print(text)

if __name__ == '__main__':
    cfg.load_config()
    cfg.coords = create_inventory_coords(int(cfg.config["SETTINGS"]["safe_columns"]))
    run()
    '''
    debug(cfg.config["INVENTORY"]["start_x"])
    cfg.config["INVENTORY"]["start_x"] = str(2000)
    cfg.save_config()
    '''