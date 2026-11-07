CREATE DATABASE IF NOT EXISTS carbon_compass;
USE carbon_compass;

CREATE TABLE `consumption_records` (
  `record_id` int NOT NULL AUTO_INCREMENT,
  `building_id` int NOT NULL,
  `timestamp` date NOT NULL,
  `electricity_kwh` double NOT NULL,
  PRIMARY KEY (`record_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO consumption_records VALUES (1, 1, '2026-01-01', 120.0);
INSERT INTO consumption_records VALUES (2, 1, '2026-01-02', 150.0);
