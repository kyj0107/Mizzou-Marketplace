DROP TABLE IF EXISTS items;

CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    posted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    itemName TEXT NOT NULL,
    itemDescription TEXT NOT NULL
    poster TEXT NOT NULL
);

-- itemType ENUM('Furniture', 'Textbook', 'Supplies') NOT NULL
-- condition ENUM('Excellent', 'Good', 'Acceptable', 'Bad', 'Terrible') NOT NULL
-- price decimal(10,2) NOT NULL