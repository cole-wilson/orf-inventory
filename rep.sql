DROP DATABASE IF EXISTS replicator;
CREATE DATABASE replicator;
USE replicator;

DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS categories;


CREATE TABLE suppliers
(
	sup_abbr	CHAR(3) PRIMARY KEY,
	sup_name	VARCHAR(20) NOT NULL
);

CREATE TABLE categories
(
	cat_abbr	CHAR(1) PRIMARY KEY,
	cat_name	VARCHAR(20) NOT NULL
);

CREATE TABLE items
(
	cat 		CHAR(1) 	NOT NULL REFERENCES category (cat_abbr),
	item_num 	INT 		NOT NULL auto_increment primary key,
	item_name 	VARCHAR(45) 	NOT NULL,
	sup 		CHAR(3) 	NOT NULL,
	sup_part_num	VARCHAR(12),
	item_cost 	DECIMAL		REFERENCES suppliers (sup_abbr),
	qty_stock 	INT 		NOT NULL DEFAULT 0,
	qty_robot 	INT 		NOT NULL DEFAULT 0,
	qty_testing 	INT 		NOT NULL DEFAULT 0
);

ALTER TABLE items AUTO_INCREMENT = 1001;

INSERT INTO categories VALUES ('B','Bearings');
INSERT INTO categories VALUES ('C','Control Systems');
INSERT INTO categories VALUES ('F','Fasteners');
INSERT INTO categories VALUES ('M','Motors');
INSERT INTO categories VALUES ('N','Pnumatics');
INSERT INTO categories VALUES ('P','Pulley/Belts/Cord');
INSERT INTO categories VALUES ('R','Rod Stock');
INSERT INTO categories VALUES ('S','Sensors');
INSERT INTO categories VALUES ('U','Consumables');
INSERT INTO categories VALUES ('W','Wheels');

INSERT INTO suppliers VALUES ("MCM","McMaster Carr");
INSERT INTO suppliers VALUES ("AMK","Andy Mark");
INSERT INTO suppliers VALUES ("VEX","VEX Robotics");
INSERT INTO suppliers VALUES ("REV","Rev Robotics");
#INSERT INTO suppliers VALUES ("AMK","Andy Mark");
