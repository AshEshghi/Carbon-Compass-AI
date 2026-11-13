CREATE TABLE IF NOT EXISTS consumption_records (
    record_id INT NOT NULL AUTO_INCREMENT,
    building_id INT NOT NULL,
    timestamp DATE NOT NULL,
    electricity_kwh DOUBLE NOT NULL,
    PRIMARY KEY (record_id)
);