from importlib.metadata import entry_points

from ed_core import streamdeck
from ed_core.streamdeck_config import load_config, apply_config

VERSION = "0.0.1"
BACKENDS = {}


def run():
    print("El Decko Core running.")
    load_config()
    discovered_backends = entry_points(group='eldecko.backend')
    for edb in discovered_backends:
        edb_id = edb.value.split(":")[0]
        edb_function = edb.load()
        edb_name = edb.name
        if edb_id not in BACKENDS:
            BACKENDS[edb_id] = []
        BACKENDS[edb_id].append({
            "name": edb_name,
            "function": edb_function
        })

    streamdeck.initialize(discovered_backends)
