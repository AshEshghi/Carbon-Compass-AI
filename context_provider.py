class ContextProvider:

    def __init__(self, database_manager, emissions=None):
        self.database_manager = database_manager
        self.emissions = emissions

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
        return self.database_manager.fetch_records()