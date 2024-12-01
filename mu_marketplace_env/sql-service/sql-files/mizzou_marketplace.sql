DROP DATABASE IF EXISTS `mizzou_marketplace`;
CREATE DATABASE `mizzou_marketplace`;

USE `mizzou_marketplace`;

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    `userID` INT AUTO_INCREMENT PRIMARY KEY,
    `firstName` VARCHAR(50) NOT NULL,
    `lastInitial` VARCHAR(1) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    UNIQUE (`email`)
);

DROP TABLE IF EXISTS `items`;
CREATE TABLE `items` (
    `itemID` INT AUTO_INCREMENT PRIMARY KEY,
    `posted` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `itemName` VARCHAR(40) NOT NULL,
    `itemDescription` TEXT NOT NULL,
    `itemCondition` ENUM('New', 'Good', 'Acceptable', 'Poor'),
    `itemType` ENUM('Furniture', 'Textbooks', 'Supplies', 'Clothing'),
    `price` decimal(10,2) NOT NULL,
    `listed` BOOLEAN DEFAULT TRUE,
    `userID` INT NOT NULL,
    FOREIGN KEY (`userID`) REFERENCES `users` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE
    -- KEY `email` (`email`),
    -- CONSTRAINT `items_ibfk_1` FOREIGN KEY (`email`) REFERENCES `users` (`email`)
);

/* Sample data for MU Marketplace DB */

-- users entries
INSERT INTO users (firstName, lastInitial, email, password) VALUES ("Karla", "J", "kyjhgg@umsystem.edu", "$2b$12$X6frsUibnsh9akDiNWAMceZwHx2ReaQB.C/XN54wcFsOPllHxWgbK"); -- Atotally0riginalpassword!
INSERT INTO users (firstName, lastInitial, email, password) VALUES ("Jordan", "A", "jeafh4@umsystem.edu", "$2b$12$z2yGDbEkvS6EQWrwwbQ0begypwXAMNN7mgfOlW455RQEr44xKc3oW"); --Testtest1!
INSERT INTO users (firstName, lastInitial, email, password) VALUES ("Angel", "S", "as2mf@umsystem.edu", "AveryCLEVERpassword");
INSERT INTO users (firstName, lastInitial, email, password) VALUES ("Daniel", "T", "dbthbw@umsystem.edu", "GraphicDesignismyburden");

-- items entries
INSERT INTO items(itemName, itemDescription, itemCondition, itemType, price, userID) VALUES ("IKEA Nightstand", "An IKEA nightstand that took way too long to put together.", 'Good', 'Furniture', '100.00', "1");
INSERT INTO items(itemName, itemDescription, itemCondition, itemType, price, userID) VALUES ("Chemistry Matters", "That one chemistry textbook with the chemistry pun in the credits.", 'New', 'Textbooks', '200.00', "2");
INSERT INTO items(itemName, itemDescription, itemCondition, itemType, price, userID) VALUES ("Apple MacBook Pro 16-inch w/ M1 chip", "This MacBook has seen some things. Don't open Xcode or Adobe After Effects on this.", 'Acceptable', 'Supplies', '1000.00', "4");
INSERT INTO items(itemName, itemDescription, itemCondition, itemType, price, userID) VALUES ("Plain blue T-shirt", "A simple T-shirt. A few holes in the seams. Maybe you can fix it?", 'Acceptable', 'Clothing', '3.00', "1");

UPDATE items SET listed = FALSE WHERE itemID = 4;

/* Interesting little fact! BOOLEAN isn't really a data type in MySQL, but you can use it and it creates a TINYINT value instead.
SELECT * FROM items WHERE listed = TRUE and SELECT * FROM items WHERE listed = 1 work the same!
But yeah, TRUE is 1 and FALSE is 0. I'll probably treat it like a typical boolean, though. */