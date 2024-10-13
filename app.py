import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort
# import mysql.connector

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'
app.secret_key = 'your secret key'

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="root",
#     database="mizzou_marketplace"
# )

# cursor = mydb.cursor(dictionary=True)

def get_db_connection():

    conn = sqlite3.connect('database.db')

    conn.row_factory = sqlite3.Row

    return conn

@app.route('/')
def index():

    conn = get_db_connection()

    query = 'SELECT * FROM items'
    items = conn.execute(query).fetchall()

    conn.close()

    # query = 'SELECT * FROM items'
    # cursor.execute(query)
    # items = cursor.fetchall()

    return render_template('index.html', items=items)

@app.route('/about/')
def about():
    
    return render_template('about.html')

@app.route('/itemEntry/')
def itemEntry():
    
    return render_template('itemEntry.html')

@app.route('/product/') 
def product():
    
    return render_template('product.html')

@app.route('/register/')
def register():

    return render_template('register.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():

    if request.method =='POST': 
        email = request.form['email']
        password = request.form['password']

        if email == 'admin' and password == 'admin':
            return redirect(url_for('index'))
        else:
            flash('Invalid Email or Password')

    return render_template('login.html')


app.run(port=5002, debug=True)