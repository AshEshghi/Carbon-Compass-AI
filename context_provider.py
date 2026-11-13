
import requests


class ContextProvider:

    def __init__(
        self,
        database_manager=None,
        emissions=None,
        api_url="http://127.0.0.1:5050/records"
    ):
        self.database_manager = database_manager
        self.emissions = emissions
        self.api_url = api_url

    # Getter for database_manager
    def get_database_manager(self):
        return self.database_manager

    # Setter for database_manager
    def set_database_manager(self, database_manager):
        self.database_manager = database_manager

    # Getter for emissions
    def get_emissions(self):
        return self.emissions

    # Setter for emissions
    def set_emissions(self, emissions):
        self.emissions = emissions

    # Get electricity consumption data
    def get_consumption(self):
        if self.database_manager is None:
            raise ValueError("Database manager is not configured")

        return self.database_manager.fetch_records()

    # Get all records from the Data Management API
    def get_api_records(self):
        response = requests.get(self.api_url, timeout=10)
        response.raise_for_status()
        return response.json()

    # Get only the main 2016 dataset for final analysis
    def get_main_dataset(self):
        records = self.get_api_records()

        main_records = [
            record for record in records
            if record.get("timestamp", "").startswith("2016-")
        ]

        return main_records
