class ConsumptionRecord:
    def __init__(self, record_id, building_id, timestamp, electricity_kwh):
        self.__record_id = record_id
        self.__building_id = building_id
        self.__timestamp = timestamp
        self.__electricity_kwh = electricity_kwh

    def get_record_id(self):
        return self.__record_id

    def set_record_id(self, new_id):
        self.__record_id = new_id

    def get_building_id(self):
        return self.__building_id

    def set_building_id(self, new_id):
        self.__building_id = new_id

    def get_timestamp(self):
        return self.__timestamp

    def set_timestamp(self, new_timestamp):
        self.__timestamp = new_timestamp

    def get_electricity_kwh(self):
        return self.__electricity_kwh

    def set_electricity_kwh(self, new_value):
        if new_value >= 0:
            self.__electricity_kwh = new_value
