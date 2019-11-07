class Library:
    REGISTERED_CAPS = {}

    def register(item):
        Library.REGISTERED_CAPS[str(item.__name__)] = item.caps


class Item:
    caps = None


@Library.register
class Item1(Item):
    caps = 'I can do stuff'


@Library.register
class Item2(Item):
    caps = 'I can do other stuff'


