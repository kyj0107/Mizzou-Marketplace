from flask import Flask, render_template, request, url_for, flash, redirect, abort
import mysql.connector

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'
app.secret_key = 'your secret key'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="mizzou_marketplace"
)

cursor = mydb.cursor(dictionary=True)

@app.route('/')
def index():

    query = 'SELECT * FROM items'
    cursor.execute(query)
    items = cursor.fetchall()

    return render_template('index.html', items=items)

@app.route('/about/')
def about():
    
    return render_template('about.html')

@app.route('/register/')
def register():

    return render_template('register.html')

@app.route('/login/')
def login():

    return render_template('login.html')


app.run(port=5002, debug=True)