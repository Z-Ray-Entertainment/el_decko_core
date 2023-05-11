from StreamDeck.DeviceManager import DeviceManager

CACHE = list()


# Builds a cache of all connected Stream Decks for interaction ith UIs as someone can not interact with a
# Stream Deck if it is already opened. Hence, if the core is running.
def build_cache():
    for index, deck in enumerate(DeviceManager().enumerate()):
        properties = {}
        deck.open()
        properties["serial"] = deck.get_serial_number()
        properties["key_count"] = deck.key_count()
        properties["key_layout"] = deck.key_layout()
        properties["key_image_format"] = deck.key_image_format()
        properties["deck_type"] = deck.deck_type()
        properties["firmware_version"] = deck.get_firmware_version()
        properties["id"] = deck.id()
        properties["product_id"] = deck.product_id()
        properties["vendor_id"] = deck.vendor_id()
        CACHE.append(properties)
        deck.close()


build_cache()
