class ProcessingPipeline:

    def __init__(self, steps=None):
        self.steps = list(steps) if steps is not None else []

    def get_steps(self):
        return self.steps.copy()

    def __or__(self, processor):
        return ProcessingPipeline(self.steps + [processor])

    def process(self, record):
        for processor in self.steps:
            if record is None:
                return None

            record = processor.process(record)

        return record

    def process_stream(self, records):
        for record in records:
            result = self.process(record)

            if result is not None:
                yield result