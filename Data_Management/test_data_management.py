from pathlib import Path
from database_manager import DatabaseManager
from csv_importer import CSVImporter
from data_validator import DataValidator
from consumption_record import ConsumptionRecord

file_path = Path(__file__).parent / "electricity.csv"
db_path = Path(__file__).parent / "carbon_compass.db"

importer = CSVImporter(file_path)
validator = DataValidator()
database = DatabaseManager(db_path)

database.create_table()

building_id = 1

if importer.check_columns():
    records = importer.read_csv()

    for record in records:
        timestamp = record["timestamp"]
        value = record["electricity_kwh"]

        if (
            validator.check_missing(timestamp)
            and validator.check_missing(value)
            and validator.validate_timestamp(timestamp)
            and validator.check_numeric(value)
        ):
            kwh = float(value)

            if validator.validate_kwh(kwh):
                consumption = ConsumptionRecord(
                    None, building_id, timestamp, kwh
                )

                existing_records = database.fetch_records()
                already_exists = False

                for saved in existing_records:
                    if (
                        saved["building_id"] == building_id
                        and saved["timestamp"] == timestamp
                        and saved["electricity_kwh"] == kwh
                    ):
                        already_exists = True
                        break

                if already_exists:
                    print(timestamp, "Already exists")
                else:
                    new_id = database.save_record(
                        consumption.get_building_id(),
                        consumption.get_timestamp(),
                        consumption.get_electricity_kwh()
                    )

                    consumption.set_record_id(new_id)
                    print(timestamp, "Saved with ID:", new_id)

            else:
                print(timestamp, "Invalid kWh")
        else:
            print(timestamp, "Invalid record")
else:
    print("Missing required columns")