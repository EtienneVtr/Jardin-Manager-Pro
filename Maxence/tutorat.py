"""
    Author : Thibault Cheneviere
    Email : thibault.cheneviere@telecomnancy.eu
    Date : 25/10/2022
"""

# imports
import string
import random
from flask import Flask, request, render_template, flash, redirect
import sqlite3

# connect db
def connectDatabase():
    """
        Function that returns db connection and the cursor to interact with the database.db file

        Parameters :
            None

        Returns :
            - tuple [Connection, Cursor] : a tuple of the database connection and cursor
    """
    db = sqlite3.connect('tutorat.db')
    cursor = db.cursor()
    return db, cursor

# short code
def checkShortCode(shortCode: str) -> bool:
    query = '''SELECT * FROM urls WHERE shortCode=?;'''
    arg = (shortCode, )

    db, cursor = connectDatabase()
    cursor.execute(query, arg)
    result = cursor.fetchall()
    db.close()

    return (len(result) == 0)

def generateUniqueCode(codeLength: int) -> str:
    alphabet = string.ascii_letters + string.digits 
    shortCode =''.join(random.choice(alphabet)for i in range(codeLength))

    query = '''SELECT * FROM urls WHERE shortCode=?;'''
    arg = (shortCode, )

    db, cursor = connectDatabase()
    cursor.execute(query, arg)
    result = cursor.fetchall()
    db.close()

    if checkShortCode(shortCode):
        return shortCode
    else:
        return generateUniqueCode(codeLength)

# function to create db


def initDB():
    query = '''
    DROP TABLE IF EXISTS urls;
    
    CREATE TABLE urls 
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        shortCode TEXT UNIQUE,
        visitNumber INTEGER
    );
    
    INSERT INTO urls (url, shortCode, visitNumber) VALUES ('https://telecomnancy.univ-lorraine.fr/','tn', 42);
    INSERT INTO urls (url, shortCode, visitNumber) VALUES ('https://gitlab.telecomnancy.univ-lorraine.fr/','gitlab', 666);
    '''
    db, cursor = connectDatabase()
    cursor.executescript(query)
    db.commit()
    cursor.close()
    db.close()


# flask app creation
app = Flask(__name__)

app.config['SECRET_KEY'] = '1sZn3QAl35qIYaoqjLbB9JxuYxqOyVN3'

# routes

# /status
@app.route("/status", methods=['GET'])
def status() -> string:
    return "Up and Running!"

# /display
@app.route('/display', methods=['GET', 'POST'])
def displayDisplay() -> str:
    if request.method == 'GET':
        db, cursor = connectDatabase()
        query = '''SELECT url, shortCode, visitNumber FROM urls;'''
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        db.close()


        return render_template('tutoratDisplay.html', data=result)

# /add
@app.route('/add', methods=['GET', 'POST'])
def addCodeAdd() -> str:
    if request.method == 'GET':
        query = '''SELECT url, shortCode, visitNumber FROM urls;'''
        db, cursor = connectDatabase()
        cursor.execute(query)
        data = cursor.fetchall()
        db.close()

        return render_template('tutoratAdd.html', data=data)
    elif request.method == 'POST':
        url = request.form['target_url']
        shortCode = request.form['short_code']

        if shortCode == "" or url == "":
            flash("Failed ! You must specify a url and a shortCode before submit.", "Red_flash")
            return redirect("/add")
        
        elif not checkShortCode(shortCode):
            flash("Failed ! You must enter a unique shortCode.", "Red_flash")
            return redirect("/add")

        else:
            query = '''INSERT INTO urls (url, shortCode, visitNumber) VALUES (?, ?, ?);'''
            args = (url, shortCode, 0)

            db, cursor = connectDatabase()
            cursor.execute(query, args)
            db.commit()
            db.close()

        return redirect('/add')

# /shorten
@app.route('/shorten', methods=['GET', 'POST'])
def addCodeShorten():
    if request.method == 'GET':
        query = '''SELECT url, shortCode, visitNumber FROM urls;'''
        db, cursor = connectDatabase()
        cursor.execute(query)
        data = cursor.fetchall()
        db.close()

        return render_template('tutoratShorten.html', data=data)
    
    elif request.method == 'POST':
        url = request.form['target_url']
        shortCode = generateUniqueCode(7)

        query = '''INSERT INTO urls (url, shortCode, visitNumber) VALUES (?, ?, ?);'''
        args = (url, shortCode, 0)

        db, cursor = connectDatabase()
        cursor.execute(query, args)
        db.commit()
        db.close()

        return redirect('/shorten')

# /r/:shortCode
@app.route('/r/<string:shortCode>')
def redirectR(shortCode: str):
    query = '''SELECT url, visitNumber FROM urls WHERE shortCode=?;'''
    arg = (shortCode, )

    db, cursor = connectDatabase()

    cursor.execute(query, arg)
    data = cursor.fetchall()[0]
    
    updateQuery = '''UPDATE urls SET visitNumber=? WHERE shortCode=?;'''
    args = (data[1]+1, shortCode)

    cursor.execute(updateQuery, args)
    db.commit()
    db.close()

    return redirect(data[0])

# Delete
@app.route('/<string:route>/deleteShortCode/<string:shortCode>', methods=['GET'])
def addCodeDeleteShortCode(route: str, shortCode: str):
    if request.method == 'GET':
        query = '''DELETE FROM urls WHERE shortCode=?;'''
        arg = (shortCode, )

        db, cursor = connectDatabase()
        cursor.execute(query, arg)
        db.commit()
        db.close()

        return redirect(f"/{route}")

# Error 404
@app.errorhandler(404)
def pageNotFound(error):
    flash("HTTP 404 Not Found", "Red_flash")
    return redirect('/display')


if __name__ == "__main__":
    if (False):
        initDB()

    app.run(debug=1, host='0.0.0.0', port='5454')
