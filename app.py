import sqlite3
import re
from flask import Flask, render_template, request, url_for, flash, redirect, abort, get_flashed_messages
# import mysql.connector

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'
app.secret_key = 'your secret key'

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="root",
#     port="6603"
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

def passwordCheck(password): #function to enforce password requirements
    if not re.search(r"[A-Z]", password):
        return False, "Password missing an uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password missing a lowercase letter"
    if not re.search(r"[0-9]", password):
        return False, "Password missing a number"
    if not re.search(r"[$#@'&()*+,-./:;<=>|?!@^_'{}~]", password):
        return False, "Password missing a symbol"
    
    return True, ""


@app.route('/register/', methods=['GET', 'POST'])
def register():

    if request.method =='POST':
        get_flashed_messages() #clears any flashed messages from previous attempts

        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        passwordConfirm = request.form['passwordConfirm']

        if not email.endswith('@umsystem.edu'): #checks if user email ends in umsystem.edu. If not, clears fields and asks for an email associated w/ university. If true, redirects to index page
            flash('You must use an email associated with the University')
            return redirect(url_for('register'))
        
        validPassword, errorMessage = passwordCheck(password) #checks if password meets minimum requirements, if not rejects with message detailing what's missing
        if not validPassword:
            flash(errorMessage)
            return redirect(url_for('register'))
        
        if password != passwordConfirm: #checks if passwords match
            flash('Passwords must match!')
            return redirect(url_for('register'))
        
        else:
            flash('Registered Successfully!')
            return redirect(url_for('index'))

    return render_template('register.html')
        

@app.route('/login/', methods=['GET', 'POST'])
def login():

    if request.method =='POST': 
        email = request.form['email']
        password = request.form['password']

        if email == 'admin' and password == 'admin': #Block will be used to verify email/pass w/ database, for now redirects to index if email/pass are 'admin' 
            return redirect(url_for('index'))
        else:
            flash('Invalid Email or Password')

    return render_template('login.html')

@app.route('/go_mu_homepage/')
def go_mu_homepage():
    return redirect("https://missouri.edu/", code=302)

@app.route('/faq/')
def faq():
    return render_template('faq.html')

app.run(port=5002, debug=True)