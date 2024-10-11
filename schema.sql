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