import csv


class CSVImporter:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_file_path(self):
        return self.file_path

    def set_file_path(self, new_path):
        self.file_path = new_path

    def read_csv(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return list(reader)

    def check_columns(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            required_columns = {"timestamp", "electricity_kwh"}
            return required_columns.issubset(reader.fieldnames or [])