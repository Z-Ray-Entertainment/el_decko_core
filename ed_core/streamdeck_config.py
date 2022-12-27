import json
import os

from StreamDeck.DeviceManager import DeviceManager
from xdg import (
    xdg_cache_home,
    xdg_config_dirs,
    xdg_config_home,
    xdg_data_dirs,
    xdg_data_home,
    xdg_runtime_dir,
    xdg_state_home,
)

CONFIG_PATH: str = str(xdg_config_home()) + "/eldecko/"
CONFIG_FILE: str = CONFIG_PATH + "streamdeck.json"
DECK_CFG: dict = {}


def load_config():
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)
    if not os.path.isfile(CONFIG_FILE):
        __create_default_config()
    try:
        with open(CONFIG_FILE) as input_file:
            global DECK_CFG
            DECK_CFG = json.load(input_file)
    except json.decoder.JSONDecodeError as e:
        print(e)


def get_config():
    return DECK_CFG


def apply_config(deck):
    serial = deck.get_serial_number()
    deck.set_brightness(DECK_CFG[serial]["brightness"])


def __create_default_config():
    stream_decks = DeviceManager().enumerate()
    for index, deck in enumerate(stream_decks):
        if not deck.is_visual():
            continue

        deck.open()
        deck.reset()

        serial = deck.get_serial_number()

        key_config: dict = {}
        for i in range(0, deck.key_count()):
            key_config[str(i)] = {
                "backend": None,
                "event": None,
                "event_parameters": {

                },
                "image": None
            }

        DECK_CFG[serial] = dict(brightness=30, key_config=key_config)
        deck.close()
        with open(CONFIG_FILE, "w+", encoding="utf-8") as outfile:
            json.dump(DECK_CFG, outfile, ensure_ascii=False, indent=2)
