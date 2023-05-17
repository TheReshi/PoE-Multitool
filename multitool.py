from operator import is_
from tracemalloc import start
import configuration as cfg
import kthread as kt
import numpy as np
import time, keyboard, pyautogui, sys, taskbar

#pyinstaller --onefile --windowed --icon tray.ico --version-file version.txt multitool.py

SETTINGS = cfg.config["SETTINGS"]

cfg.load_config()
pyautogui.PAUSE = 1 / float(SETTINGS["click_speed"])


def run():
    while True:
        time.sleep(0.01)
        if keyboard.is_pressed('ctrl+alt+' + SETTINGS["stash_hotkey"]) or keyboard.is_pressed('ctrl+shift+alt+' + SETTINGS["stash_hotkey"]):
            current_pos = pyautogui.position()
            if in_stash_range(current_pos):
                h_loadin(current_pos)
            else:
                h_loadout(current_pos)
        if keyboard.is_pressed('ctrl+' + SETTINGS["stash_hotkey"]) or keyboard.is_pressed('ctrl+shift+' + SETTINGS["stash_hotkey"]):
            current_pos = pyautogui.position()
            if in_stash_range(current_pos):
                loadin(current_pos)
            else:
                loadout(current_pos)
        if keyboard.is_pressed(SETTINGS["item_use_hotkey"]):
            current_pos = pyautogui.position()
            if in_stash_range(current_pos):
                use_all_stash(current_pos)
            else:
                use_all_inv(current_pos)
        if keyboard.is_pressed(SETTINGS["card_hotkey"]):
            #minutes_diff = (datetime_end - datetime_start).total_seconds() / 60.0
            drop_div_cards()


def loadin(default_pos):
    current_block = get_closest_stash_block()
    current_block_number = cfg.stash_coords.index(current_block)
    for block in cfg.stash_coords[current_block_number:]:
        if keyboard.is_pressed('ctrl+' + SETTINGS["stash_hotkey"]) or keyboard.is_pressed('ctrl+shift+' + SETTINGS["stash_hotkey"]):
            pyautogui.moveTo(block)
            pyautogui.click()
        else:
            break
    pyautogui.moveTo(default_pos)
    time.sleep(1)

def h_loadin(default_pos):
    current_block = get_closest_h_stash_block()
    current_block_number = cfg.h_stash_coords.index(current_block)
    for block in cfg.h_stash_coords[current_block_number:]:
        if keyboard.is_pressed('ctrl+alt+' + SETTINGS["stash_hotkey"]) or keyboard.is_pressed('ctrl+shift+alt+' + SETTINGS["stash_hotkey"]):
            pyautogui.moveTo(block)
            pyautogui.click()
        else:
            break
    pyautogui.moveTo(default_pos)
    time.sleep(1)

def use_all_stash(default_pos):
    current_block = get_closest_stash_block()
    current_block_number = cfg.stash_coords.index(current_block)
    for block in cfg.stash_coords[current_block_number:]:
        if keyboard.is_pressed(SETTINGS["stash_hotkey"]):
            pyautogui.moveTo(block)
            pyautogui.click(button=pyautogui.RIGHT)
        else:
            break
    pyautogui.moveTo(default_pos)
    time.sleep(1)

def use_all_inv(default_pos):
    start_pos = 0
    end_pos = len(cfg.inventory_coords)

    if in_inv_range(default_pos):
        current_block = get_closest_inventory_block()
        current_block_number = cfg.inventory_coords.index(current_block)
        if SETTINGS["safe_columns_direction"].lower() == "left":
            if current_block_number <= start_pos:
                current_block_number = start_pos
        else:
            if current_block_number >= end_pos:
                return
    else:
        current_block_number = start_pos

    for block in cfg.inventory_coords[current_block_number:end_pos]:
        if keyboard.is_pressed(SETTINGS["stash_hotkey"]):
            pyautogui.moveTo(block)
            pyautogui.click(button=pyautogui.RIGHT)
        else:
            break

    pyautogui.moveTo(default_pos)
    time.sleep(1)


def loadout(default_pos):
    start_pos = 0
    end_pos = len(cfg.inventory_coords)
    if SETTINGS["safe_columns_direction"].lower() == "left":
        start_pos = int(SETTINGS["safe_columns"]) * 5
    else:
        end_pos = end_pos - int(SETTINGS["safe_columns"]) * 5

    if in_inv_range(default_pos):
        current_block = get_closest_inventory_block()
        current_block_number = cfg.inventory_coords.index(current_block)
        if SETTINGS["safe_columns_direction"].lower() == "left":
            if current_block_number <= start_pos:
                current_block_number = start_pos
        else:
            if current_block_number >= end_pos:
                return
    else:
        current_block_number = start_pos

    for block in cfg.inventory_coords[current_block_number:end_pos]:
        if keyboard.is_pressed('ctrl+' + SETTINGS["stash_hotkey"]) or keyboard.is_pressed('ctrl+shift+' + SETTINGS["stash_hotkey"]):
            pyautogui.moveTo(block)
            pyautogui.click()
        else:
            break
    pyautogui.moveTo(default_pos)
    time.sleep(1)

def h_loadout(default_pos):
    start_pos = 0
    end_pos = len(cfg.h_inventory_coords)
    if SETTINGS["safe_columns_direction"].lower() == "left":
        start_pos = int(SETTINGS["safe_columns"]) * 5
    else:
        end_pos = end_pos - int(SETTINGS["safe_columns"]) * 5

    if in_inv_range(default_pos):
        current_block = get_closest_h_inventory_block()
        current_block_number = cfg.h_inventory_coords.index(current_block)
        if SETTINGS["safe_columns_direction"].lower() == "left":
            if current_block_number <= start_pos:
                current_block_number = start_pos
        else:
            if current_block_number >= end_pos:
                return
    else:
        current_block_number = start_pos

    for block in cfg.h_inventory_coords[current_block_number:end_pos]:
        if keyboard.is_pressed('ctrl+alt+' + SETTINGS["stash_hotkey"]) or keyboard.is_pressed('ctrl+shift+alt+' + SETTINGS["stash_hotkey"]):
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

def get_closest_h_stash_block():
    current_pos = pyautogui.position()

    xy = np.array(cfg.h_stash_coords).T
    # Euclidean distance
    d = ((xy[0] - current_pos[0]) ** 2 + (xy[1] - current_pos[1]) ** 2) ** 0.5

    closest_idx = np.argmin(d)
    closest_block = cfg.h_stash_coords[closest_idx]

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

def get_closest_h_inventory_block():
    current_pos = pyautogui.position()

    if not in_inv_range(current_pos):
        cfg.h_inventory_coords[0]

    xy = np.array(cfg.h_inventory_coords).T
    # Euclidean distance
    d = ((xy[0] - current_pos[0]) ** 2 + (xy[1] - current_pos[1]) ** 2) ** 0.5

    closest_idx = np.argmin(d)
    closest_block = cfg.h_inventory_coords[closest_idx]

    return closest_block


def in_stash_range(coords):
    stash_start = (int(cfg.config["STASH"][f"start_x{cfg.inv_suffix}"]), int(cfg.config["STASH"][f"start_y{cfg.inv_suffix}"]))
    stash_size = (int(cfg.config["STASH"][f"end_x{cfg.inv_suffix}"]) - int(cfg.config["STASH"][f"start_x{cfg.inv_suffix}"]), int(cfg.config["STASH"][f"end_y{cfg.inv_suffix}"]) - int(cfg.config["STASH"][f"start_y{cfg.inv_suffix}"]))
    if coords[0] not in range(stash_start[0], stash_start[0] + stash_size[0]) or coords[1] \
            not in range(stash_start[1], stash_start[1] + stash_size[1]):
        return False
    return True


def in_inv_range(coords):
    inventory_start = (int(cfg.config["INVENTORY"][f"start_x{cfg.inv_suffix}"]), int(cfg.config["INVENTORY"][f"start_y{cfg.inv_suffix}"]))
    inventory_size = (int(cfg.config["INVENTORY"][f"end_x{cfg.inv_suffix}"]) - int(cfg.config["INVENTORY"][f"start_x{cfg.inv_suffix}"]), int(cfg.config["INVENTORY"][f"end_y{cfg.inv_suffix}"]) - int(cfg.config["INVENTORY"][f"start_y{cfg.inv_suffix}"]))
    if coords[0] not in range(inventory_start[0], inventory_start[0] + inventory_size[0]) or coords[1] \
            not in range(inventory_start[1], inventory_start[1] + inventory_size[1]):
        return False
    return True

if __name__ == '__main__':
    tray_process = kt.KThread(target=taskbar.tray)
    multitool_process = kt.KThread(target=run)
    processes = [tray_process, multitool_process]
    tray_process.start()
    multitool_process.start()
    print("PoE Loadout is running.")
    print("Stash Hotkey is: CTRL + " + SETTINGS["stash_hotkey"])
    print("Divination Card Hotkey is: SHIFT + " + SETTINGS["card_hotkey"])

    while True:
        if not tray_process.is_alive() or not multitool_process.is_alive():
            if multitool_process.is_alive():
                multitool_process.kill()
            if tray_process.is_alive():
                tray_process.kill()
            sys.exit(1)
        time.sleep(2)