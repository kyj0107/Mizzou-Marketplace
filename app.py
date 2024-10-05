import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

app = Flask(__name__)
app.config["DEBUG"] = True

app.config['SECRET KEY'] = 'your secret key'

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/about/')
def about():
    
    return render_template('about.html')

app.run(host="0.0.0.0", port=5002)