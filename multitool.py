import configuration as cfg
import math, time, keyboard, pyautogui
import numpy as np

pyautogui.PAUSE = 0.0125


def run():
    while True:
        time.sleep(0.01)
        if keyboard.is_pressed('ctrl+' + cfg.config["SETTINGS"]["hotkey"]) or keyboard.is_pressed('ctrl+shift+' + cfg.config["SETTINGS"]["hotkey"]):
            current_pos = pyautogui.position()
            if in_stash_range(current_pos):
                loadin(current_pos)
            else:
                loadout(current_pos)


def loadin(default_pos):
    current_block = get_closest_stash_block()
    current_block_number = cfg.stash_coords.index(current_block)
    for block in cfg.stash_coords[current_block_number:]:
        if keyboard.is_pressed('ctrl+' + cfg.config["SETTINGS"]["hotkey"]) or keyboard.is_pressed('ctrl+shift+' + cfg.config["SETTINGS"]["hotkey"]):
            pyautogui.moveTo(block)
            pyautogui.click()
        else:
            break
    pyautogui.moveTo(default_pos)
    time.sleep(1)

def loadout(default_pos):
    if in_inv_range(default_pos):
        current_block = get_closest_inventory_block()
        current_block_number = cfg.inventory_coords.index(current_block)
    else:
        current_block_number = 0
    for block in cfg.inventory_coords[current_block_number:]:
        if keyboard.is_pressed('ctrl+' + cfg.config["SETTINGS"]["hotkey"]) or keyboard.is_pressed('ctrl+shift+' + cfg.config["SETTINGS"]["hotkey"]):
            pyautogui.moveTo(block)
            pyautogui.click()
        else:
            break
    pyautogui.moveTo(default_pos)
    time.sleep(1)


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


def create_stash_coords():
    stash_width = int(cfg.config["STASH"]["end_x"]) - int(cfg.config["STASH"]["start_x"])
    stash_height = int(cfg.config["STASH"]["end_y"]) - int(cfg.config["STASH"]["start_y"])
    step_x = stash_width / 48
    step_y = stash_height / 48
    coords = []
    for i in range(1, 49, 2):
        for j in range(1, 49, 2):
            coords.append((round(int(cfg.config["STASH"]["start_x"]) + step_x * i), round(int(cfg.config["STASH"]["start_y"]) + step_y *  j)))

    return coords


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
    cfg.inventory_coords = create_inventory_coords(int(cfg.config["SETTINGS"]["safe_columns"]))
    cfg.stash_coords = create_stash_coords()
    run()
    '''
    debug(cfg.config["INVENTORY"]["start_x"])
    cfg.config["INVENTORY"]["start_x"] = str(2000)
    cfg.save_config()
    '''