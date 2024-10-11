/* Mizzou Marketplace database and tables*/

CREATE DATABASE mizzou_marketplace;

DROP TABLE IF EXISTS items;
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    posted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    itemName VARCHAR(40) NOT NULL,
    -- itemType ENUM ('Furniture','Textbook','Supplies'),
    -- condition ENUM ('Excellent','Good','Acceptable','Bad','Terrible'),
    itemDescription TEXT NOT NULL,
    price decimal(10,2) NOT NULL,
    poster TEXT NOT NULL
);

/* Sample data for MU Marketplace DB */
INSERT INTO items (itemName, itemDescription, price, poster) VALUES ("Nightstand", "A simple nightstand.",'50.00', "Karla Jaime");
INSERT INTO items (itemName, itemDescription, price, poster) VALUES ("Chemistry Textbook", "That one textbook with the chemistry pun in the credits.", '150.00', "Jordan Andersen");
INSERT INTO items (itemName, itemDescription, price, poster) VALUES ("Apple MacBook Pro 16-inch", "This MacBook has seen some things.", '1000.00', "Daniel Thompson");
