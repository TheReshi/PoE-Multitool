from pystray import MenuItem as item
import pystray, sys
from PIL import Image

def tray():
    image = Image.open("tray.ico")
    menu = (item('Exit', lambda: icon.stop()),)
    icon = pystray.Icon("Multitool", image, "PoE Multitool", menu)
    icon.run()