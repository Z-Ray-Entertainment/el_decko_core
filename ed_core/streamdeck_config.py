import json
import os

from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.Devices.StreamDeck import StreamDeck

from ed_core import dyn_data

CONFIG_FILE: str = "streamdeck.json"
DECK_CFG: dict = {}


def load_config():
    if not dyn_data.config_exists(dyn_data.CONFIG_ROOT, CONFIG_FILE):
        __create_default_config()
    global DECK_CFG
    DECK_CFG = dyn_data.load_config(dyn_data.CONFIG_ROOT, CONFIG_FILE)


def get_config():
    return DECK_CFG


def apply_config(deck: StreamDeck):
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
                "image_idle": None,
                "image_pressed": None
            }

        DECK_CFG[serial] = dict(brightness=30, key_config=key_config)
        deck.close()
        dyn_data.store_config(dyn_data.CONFIG_ROOT, CONFIG_FILE, DECK_CFG)
