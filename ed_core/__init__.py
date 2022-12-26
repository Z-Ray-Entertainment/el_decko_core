from importlib.metadata import entry_points
from StreamDeck.DeviceManager import DeviceManager

VERSION = "0.0.1"

backends = entry_points(group='eldecko.backend')
streamdecks = DeviceManager().enumerate()


def run():
    print("El Decko Core running.")
    print(backends)
    init_backend = backends['init'].load()
    init_backend()
    print(get_stream_decks())
    # fire = backends['fire'].load()
    # fire("SwitchScene", {"name": "S: Gaming"})


# Returns a list of all available Stream Decks
def get_stream_decks():
    return streamdecks
