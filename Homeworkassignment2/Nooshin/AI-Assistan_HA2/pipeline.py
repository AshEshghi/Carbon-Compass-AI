
class Pipeline:
    """
    Combines multiple stream processors.
    """

    def __init__(self, processors=None):
        self.processors = processors or []

    def __add__(self, other):
        if isinstance(other, Pipeline):
            return Pipeline(self.processors + other.processors)

        return Pipeline(self.processors + [other])

    def process(self, record):
        for processor in self.processors:

            if record is None:
                return None

            record = processor.process(record)

        return record
