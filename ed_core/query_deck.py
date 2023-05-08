from enum import Enum


class QueryType(Enum):
    SERIAL = 0,
    KEY_COUNT = 1,
    KEY_LAYOUT = 2,
    SUPPORTED_IMAGE_TYPE = 3


def query_deck(deck, prop: QueryType):
    deck.open()
    prop_value: any = None
    match prop:
        case QueryType.SERIAL:
            prop_value = deck.get_serial_number()
        case QueryType.KEY_COUNT:
            prop_value = deck.key_count()
        case QueryType.KEY_COUNT:
            prop_value = deck.key_layout()
        case QueryType.SUPPORTED_IMAGE_TYPE:
            prop_value = deck.key_image_format()
    deck.close()
    return prop_value
