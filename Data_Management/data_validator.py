from datetime import datetime


class DataValidator:
    def __init__(self):
        self.__is_valid = True

    def get_is_valid(self):
        return self.__is_valid

    def set_is_valid(self, value):
        self.__is_valid = value

    def validate_kwh(self, kwh):
        if kwh >= 0:
            self.__is_valid = True
        else:
            self.__is_valid = False

        return self.__is_valid

    def check_missing(self, value):
        if value is None or value == "":
            return False
        else:
            return True

    def check_duplicate(self, record, records):
        if record in records:
            return True
        else:
            return False

    def check_numeric(self, value):
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    def validate_timestamp(self, timestamp):
        try:
            datetime.strptime(timestamp, "%Y-%m-%d")
            return True
        except (ValueError, TypeError):
            return False