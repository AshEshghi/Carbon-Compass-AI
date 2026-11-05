
from pathlib import Path
from database_manager import DatabaseManager
from energy_stream import EnergyStream

db_path = Path(__file__).parent / "carbon_compass.db"

database = DatabaseManager(db_path)
database.create_table()
records = database.fetch_records()

stream = EnergyStream(records)

print("Iterator results:")
for record in stream:
    print(record)

print("Generator results:")
for record in stream.generate_records():
    print(record)
