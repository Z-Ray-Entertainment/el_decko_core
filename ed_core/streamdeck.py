import threading

from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.Devices.StreamDeck import StreamDeck

from ed_core import streamdeck_config

stream_decks = DeviceManager().enumerate()
backends = []


def initialize(edbs):
    global backends
    backends = edbs
    for index, deck in enumerate(stream_decks):
        if not deck.is_visual():
            continue

        deck.open()
        deck.reset()

        print("Opened '{}' device (serial number: '{}', fw: '{}')".format(
            deck.deck_type(), deck.get_serial_number(), deck.get_firmware_version()
        ))

        streamdeck_config.apply_config(deck)
        deck.set_key_callback(__key_change_callback)

        for t in threading.enumerate():
            try:
                t.join()
            except RuntimeError:
                pass


# Returns a list of all available Stream Decks
def get_stream_decks():
    return stream_decks


def get_supported_image_formats(deck: StreamDeck):
    deck.key_image_format()


def get_key_layout(deck: StreamDeck):
    deck.key_layout()


def get_key_count(deck: StreamDeck):
    deck.key_count()


def set_brightness(deck, brightness: int):
    deck.set_brightness(brightness)


def __key_change_callback(deck: StreamDeck, key, state):
    if state:
        cfg = streamdeck_config.DECK_CFG[deck.get_serial_number()]
        edb_id: str = cfg["key_config"][str(key)]["backend"]
        edb_event: str = cfg["key_config"][str(key)]["event"]
        edb_params: dict = cfg["key_config"][str(key)]["event_parameters"]
        if edb_id:
            fire = backends[edb_id]["fire"]
            fire(edb_event, edb_params)
