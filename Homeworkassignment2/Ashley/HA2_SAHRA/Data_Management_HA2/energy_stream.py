
class EnergyStream:
    def __init__(self, records):
        self.records = records
        self.index = 0

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.records):
            raise StopIteration

        record = self.records[self.index]
        self.index += 1
        return record

    def generate_records(self):
        for record in self.records:
            yield record
