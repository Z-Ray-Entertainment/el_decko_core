from importlib.metadata import entry_points

VERSION = "0.0.1"

backends = entry_points(group='eldecko.backend')


def run():
    print("El Decko Core running.")
    print(backends)
    run_backend = backends['start'].load()
    run_backend()
    fire = backends['fire'].load()
    fire("SwitchScene", {"name": "S: Gaming"})
