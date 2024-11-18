# import sqlite3
import re
from flask import Flask, render_template, request, url_for, flash, redirect, abort, get_flashed_messages, session
from flask_session import Session
from flask_bcrypt import Bcrypt
import mysql.connector

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'
app.secret_key = 'your secret key'
bcrypt = Bcrypt(app)

def get_db_connection():
    try:

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            port="6603",
            database="mizzou_marketplace"
        )
        print("Connection was successful!")
        return mydb

    except Exception as err:

        print(f"Connection failed. {err}")
        return None

# def get_db_connection():

#     conn = sqlite3.connect('database.db')

#     conn.row_factory = sqlite3.Row

#     return conn

@app.route('/', methods=('GET', 'POST'))
def index():

    conn = get_db_connection()
    if conn is None:
        flash("Could not connect to database")
        return render_template('errorPage.html')
    
    cursor = conn.cursor(dictionary=True)
    query = 'SELECT * FROM items'
    cursor.execute(query)
    items = cursor.fetchall()
    

    if request.method == 'POST':
        #Get the form data to query the api
        sortBy = request.form['sort']

        if sortBy == "":
            query = 'SELECT * FROM items'
            cursor.execute(query)
            items = cursor.fetchall()
            flash("Showing everything.")
            return render_template('index.html', items=items)
        if sortBy == "furniture" or sortBy == "textbooks" or sortBy == "supplies":
            query = f"SELECT * FROM items WHERE itemType = '{sortBy.capitalize()}'"
            cursor.execute(query)
            items = cursor.fetchall()
            flash(f"Showing {sortBy}.")
            return render_template('index.html', items=items)

    # items = conn.execute(query).fetchall()

    cursor.close()
    conn.close()

    return render_template('index.html', items=items)

@app.route('/about/')
def about():
    
    return render_template('about.html')

@app.route('/itemEntry/', methods=('GET', 'POST'))
def itemEntry():

    if 'user_id' not in session:
        flash("You must be logged in to access this page")
        return redirect(url_for('login'))

    if request.method == 'POST':

        item_name = request.form['itemName']
        item_description = request.form['description']
        '''
        The program has trouble adding items with apostrophes in the description,
        so the below block of code should fix that.
        Honestly, there's probably a cleaner way to do this...
        '''
        indexes_with_apostrophes = []
        for x in range(len(item_description)):
            if item_description[x] == "'":
                indexes_with_apostrophes.append(x)
        offset = 0
        for value in indexes_with_apostrophes:
            item_description = item_description[:value + offset] + "\\" + item_description[value + offset:]
            offset += 1

        item_condition = request.form['itemCondition']
        item_type = request.form['itemType']
        price = float(request.form['askingPrice'])
        poster = request.form['poster']

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = f"""
                    INSERT INTO items(itemName, itemDescription, itemCondition, itemType, price, email) VALUES ('{item_name}', '{item_description}', '{item_condition.capitalize()}', '{item_type.capitalize()}', '{price}', '{poster}')
                    """
            cursor.execute(query)
            conn.commit()
            flash('Item added successfully!')

        except Exception as e:
            flash(e)
    
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
        lastInitial = request.form['lastInitial']
        email = request.form['email']
        password = request.form['password']
        passwordConfirm = request.form['passwordConfirm']

        validPassword, errorMessage = passwordCheck(password) #checks if password meets minimum requirements, if not rejects with message detailing what's missing

        conn = get_db_connection()

        cursor = conn.cursor(dictionary=True)
        query = f"SELECT email FROM users WHERE email = '{email}'"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()

        if not email.endswith('@umsystem.edu'): #checks if user email ends in umsystem.edu. If not, clears fields and asks for an email associated w/ university. If true, redirects to index page
            flash('You must use an email associated with the University')
            return redirect(url_for('register'))
        elif not validPassword:
            flash(errorMessage)
            return redirect(url_for('register'))
        elif password != passwordConfirm: #checks if passwords match
            flash('Passwords must match!')
            return redirect(url_for('register'))
        elif conn is None: #checks if connection to database was successful
            flash("Could not connect to database")
            return redirect(url_for('register'))
        elif result != None: #checks if email exists in database
            flash(f"{email} is already in use. Please choose another email.")
            return redirect(url_for('register'))
        elif len(lastInitial) > 1:
            flash("Enter only your last initial.")
            return redirect(url_for('register'))
        else:
            hashedPass = bcrypt.generate_password_hash(password).decode('utf-8') #Hashes password before storing
            try:
                cursor = conn.cursor(dictionary=True)
                query = f"INSERT INTO users (firstName, lastInitial, email, password) VALUES ('{firstName}', '{lastInitial}', '{email}', '{hashedPass}')"
                cursor.execute(query)
                conn.commit()
                flash('Registered successfully!')
                return redirect(url_for('index'))
            except Exception as e:
                flash(f"{e}. Try again?")
                return redirect(url_for('register'))
            finally:
                cursor.close()
                conn.close()

    return render_template('register.html')
        

@app.route('/login/', methods=['GET', 'POST'])
def login():

    if request.method =='POST': 
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        if conn is None:
            flash("Could not connect to database")
            return redirect(url_for('login'))
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT userID, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = user['userID']
            flash('Logged in successfully!')
            return redirect(url_for('index'))
        
        else:
            flash("Invalid Email or Password")

    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash("Logout Successful!")
    return redirect(url_for('login'))

@app.route('/go_mu_homepage/')
def go_mu_homepage():
    return redirect("https://missouri.edu/", code=302)

@app.route('/faq/')
def faq():
    return render_template('faq.html')

@app.route('/policy/')
def policy():
    return render_template('policy.html')
    

app.run(port=5002, debug=True)