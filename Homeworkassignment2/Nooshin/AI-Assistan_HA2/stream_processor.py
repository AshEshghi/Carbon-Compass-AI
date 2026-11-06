
class EventStream:
    """
    Reads events one by one from a data stream.
    """

    def __init__(self, events):
        self.events = iter(events)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.events)


def event_generator(records):
    """
    Generates energy and carbon events one by one.
    """

    for record in records:
        yield record
