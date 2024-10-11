import sqlite3

connection = sqlite3.connect("database.db")

with open("schema.sql") as database_schema:
    connection.executescript(database_schema.read())

cur = connection.cursor()

cur.execute("INSERT INTO items (itemName, itemDescription, price, poster) VALUES (?, ?, ?, ?)", ("Nightstand", "A simple nightstand.",'50.00', "Karla Jaime"))
cur.execute("INSERT INTO items (itemName, itemDescription, price, poster) VALUES (?, ?, ?, ?)", ("Chemistry Textbook", "That one textbook with the chemistry pun in the credits.", '150.00', "Jordan Andersen"))
cur.execute("INSERT INTO items (itemName, itemDescription, price, poster) VALUES (?, ?, ?, ?)", ("Apple MacBook Pro 16-inch", "This MacBook has seen some things.", '1000.00', "Daniel Thompson"))

# cur.execute("INSERT INTO items (itemName, itemType, condition, itemDescription, price, poster) VALUES (?, ?, ?, ?, ?, ?)", ("Nightstand", 1, 2, "A simple nightstand.", '50.00', "Karla Jaime"))
# cur.execute("INSERT INTO items (itemName, itemType, condition, itemDescription, price, poster) VALUES (?, ?, ?, ?, ?, ?)", ("Chemistry Textbook", 2, 1, "That one textbook with the chemistry pun in the credits.", '150.00', "Jordan Andersen"))
# cur.execute("INSERT INTO items (itemName, itemType, condition, itemDescription, price, poster) VALUES (?, ?, ?, ?, ?, ?)", ("Apple MacBook Pro 16-inch", 3, 3, "This MacBook has seen some things.", '1000.00', "Daniel Thompson"))

connection.commit()
connection.close()