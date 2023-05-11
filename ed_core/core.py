from StreamDeck.Devices.StreamDeck import StreamDeck
from StreamDeck.DeviceManager import DeviceManager

from ed_core import config

backends = []
__stream_decks = DeviceManager().enumerate()


def initialize(edbs):
    global backends
    backends = edbs
    for index, deck in enumerate(__stream_decks):
        if not deck.is_visual():
            continue

        deck.open()
        deck.reset()

        print("Opened '{}' device (serial number: '{}', fw: '{}')".format(
            deck.deck_type(), deck.get_serial_number(), deck.get_firmware_version()
        ))

        config.apply_config(deck)
        deck.set_key_callback(__key_change_callback)


def shutdown():
    for index, deck in enumerate(__stream_decks):
        if not deck.is_visual():
            continue
        deck.reset()
        deck.close()


def set_brightness(deck, brightness: int):
    deck.set_brightness(brightness)


def get_key_config(deck_serial: str, key_num: int):
    config.load_config()
    return config.DECK_CFG[deck_serial]["key_config"][str(key_num)]


def __key_change_callback(deck: StreamDeck, key, state):
    if state:
        cfg = config.DECK_CFG[deck.get_serial_number()]
        edb_id: str = cfg["key_config"][str(key)]["backend"]
        edb_event: str = cfg["key_config"][str(key)]["event"]
        edb_params: dict = cfg["key_config"][str(key)]["event_parameters"]
        if edb_id:
            fire = backends[edb_id]["fire"]
            fire(edb_event, edb_params)
