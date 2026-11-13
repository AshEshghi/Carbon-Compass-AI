CREATE DATABASE IF NOT EXISTS carbon_compass;
USE carbon_compass;

CREATE TABLE IF NOT EXISTS consumption_records (
    record_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    building_id INT NOT NULL,
    `timestamp` DATE NOT NULL,
    electricity_kwh DOUBLE NOT NULL
);
