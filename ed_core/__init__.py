from importlib.metadata import entry_points

from ed_core import streamdeck
from ed_core.streamdeck_config import load_config

VERSION = "0.0.1"


def run():
    print("El Decko Core running.")
    load_config()
    backends = entry_points(group='eldecko.backend')
    streamdeck.initialize(backends)
