from pathlib import Path
from Data_Management.csv_importer import CSVImporter
from Data_Management.data_validator import DataValidator


def validate_csv(file_path):
    importer = CSVImporter(file_path)
    validator = DataValidator()

    valid_records = []
    errors = []
    seen_records = []

    try:
        if not importer.check_columns():
            errors.append("Missing required columns: timestamp, electricity_kwh")
            return {
                "valid_records": valid_records,
                "errors": errors
            }

        records = importer.read_csv()

        for row_number, record in enumerate(records, start=2):
            timestamp = record["timestamp"]
            value = record["electricity_kwh"]

            if not validator.check_missing(timestamp) or not validator.check_missing(value):
                errors.append(f"Row {row_number}: Missing value")
                continue

            if not validator.validate_timestamp(timestamp):
                errors.append(f"Row {row_number}: Invalid date")
                continue

            if not validator.check_numeric(value):
                errors.append(f"Row {row_number}: Invalid number")
                continue

            kwh = float(value)

            if not validator.validate_kwh(kwh):
                errors.append(f"Row {row_number}: Invalid kWh")
                continue

            if validator.check_duplicate((timestamp, kwh), seen_records):
                errors.append(f"Row {row_number}: Duplicate record")
                continue

            seen_records.append((timestamp, kwh))

            valid_records.append({
                "record_id": None,
                "building_id": 1,
                "timestamp": timestamp,
                "electricity_kwh": kwh
            })

    except (OSError, UnicodeDecodeError) as error:
        errors.append(f"Cannot read CSV file: {error}")

    return {
        "valid_records": valid_records,
        "errors": errors
    }


if __name__ == "__main__":
    file_path = Path(__file__).parent / "electricity.csv"

    result = validate_csv(file_path)

    print("Valid records:", result["valid_records"])
    print("Errors:", result["errors"])