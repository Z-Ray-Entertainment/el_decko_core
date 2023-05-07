import threading
from importlib.metadata import entry_points

from ed_core import streamdeck
from ed_core.streamdeck_config import load_config, apply_config

VERSION = "2023.5.7"
BACKENDS = {}


def run(standalone: bool = True):
    try:
        print("El Decko Core running.")
        load_config()
        discovered_backends = entry_points(group='eldecko.backend')
        for edb in discovered_backends:
            edb_id = edb.value.split(":")[0]
            edb_function = edb.load()
            edb_name: str = edb.name
            if edb_name.lower() == "init":
                edb_function()
            else:
                if edb_id not in BACKENDS:
                    BACKENDS[edb_id] = {}
                BACKENDS[edb_id][edb_name] = edb_function

        streamdeck.initialize(BACKENDS)
        if standalone:
            for t in threading.enumerate():
                try:
                    t.join()
                except RuntimeError:
                    pass
    except KeyboardInterrupt:
        streamdeck.shutdown()
        for backend in BACKENDS:
            print(backend)
            shutdown = BACKENDS[backend]["stop"]
            shutdown()


def backends():
    return BACKENDS
