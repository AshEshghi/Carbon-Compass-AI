
from pathlib import Path
import sys

data_folder = Path(__file__).resolve().parent.parent / "Data_Management"
sys.path.insert(0, str(data_folder))

from database_manager import DatabaseManager
from energy_stream import EnergyStream

db_path = data_folder / "carbon_compass.db"

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
