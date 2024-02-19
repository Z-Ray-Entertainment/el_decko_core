import os

from PIL import Image, ImageDraw, ImageFont
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.Devices.StreamDeck import StreamDeck
from StreamDeck.ImageHelpers import PILHelper

from ed_core import dyn_data

CONFIG_FILE: str = "streamdeck.json"
DECK_CFG: dict = {}
KEY_CONFIG_INDEX: dict = {}


def load_config(config_file_overwrite=""):
    global DECK_CFG
    if not config_file_overwrite:
        if not dyn_data.config_exists(dyn_data.CONFIG_ROOT, CONFIG_FILE):
            __create_default_config()
        DECK_CFG = dyn_data.load_config(dyn_data.CONFIG_ROOT, CONFIG_FILE)
    else:
        if not dyn_data.config_exists(dyn_data.CONFIG_ROOT, config_file_overwrite):
            print("Config file override " + config_file_overwrite + " not found, loading default")
            load_config()
        else:
            DECK_CFG = dyn_data.load_config(dyn_data.CONFIG_ROOT, config_file_overwrite)


def get_config():
    return DECK_CFG


def apply_config(deck: StreamDeck):
    serial = deck.get_serial_number()
    deck.set_brightness(DECK_CFG[serial]["brightness"])
    for i in range(0, deck.key_count()):
        image_path: str = DECK_CFG[deck.get_serial_number()]["key_configs"][KEY_CONFIG_INDEX[deck.get_serial_number()]][str(i)]["image_idle"]
        label: str = DECK_CFG[deck.get_serial_number()]["key_configs"][KEY_CONFIG_INDEX[deck.get_serial_number()]][str(i)]["label"]
        if image_path and image_path.startswith(dyn_data.ASSETS_ROOT) and os.path.isfile(image_path):
            icon = Image.open(image_path)
            image = PILHelper.create_scaled_image(deck, icon)
            if label != "":
                image = PILHelper.create_scaled_image(deck, icon, margins=[0, 0, 20, 0])
                draw = ImageDraw.Draw(image)
                font = ImageFont.truetype("NotoSans-Regular.ttf", 12)  # ToDo: Replace with actual ttf from assets
                draw.text((image.width / 2, image.height - 5), text=label, font=font, anchor="ms", fill="white")
            native_image = PILHelper.to_native_format(deck, image)
            deck.set_key_image(i, native_image)
        else:
            print("Invalid icon path: {} for Deck: {} and key: {}".format(image_path, deck.get_serial_number(), i))
            print("Image must be located at: {}".format(dyn_data.ASSETS_ROOT))


def __create_key_image(deck, image_file, font_style, label):
    pass


def __create_default_config():
    stream_decks = DeviceManager().enumerate()
    for index, deck in enumerate(stream_decks):
        if not deck.is_visual():
            continue

        deck.open()
        deck.reset()

        serial = deck.get_serial_number()

        key_config_array = []
        key_config: dict = {}
        for i in range(0, deck.key_count()):
            key_config[str(i)] = {"backend": None, "event": None, "event_parameters": {

            }, "image_idle": None, "image_pressed": None, "label": ""}
        key_config_array.append(key_config)

        DECK_CFG[serial] = dict(brightness=30, key_configs=key_config_array)
        deck.close()
        dyn_data.store_config(dyn_data.CONFIG_ROOT, CONFIG_FILE, DECK_CFG)
