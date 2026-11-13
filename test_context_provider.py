from context_provider import ContextProvider


class MockDatabaseManager:

    def fetch_records(self):
        return [
            ("2026-11-01", 1500.0),
            ("2026-11-02", 1700.0)
        ]


database = MockDatabaseManager()

context = ContextProvider(database, emissions=650)

print("Database Manager:", context.get_database_manager())
print("Emissions:", context.get_emissions())

context.set_emissions(700)

print("Updated Emissions:", context.get_emissions())

print("Consumption Data:", context.get_consumption())