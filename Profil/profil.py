import string
import random
from flask import Flask, render_template, request, redirect
import sqlite3

def to_string(chaine):
    tmp = str(chaine)
    n = len(tmp)
    

def connectDatabase():
    """
        Function that returns db connection and the cursor to interact with the database.db file

        Parameters :
            None

        Returns :
            - tuple [Connection, Cursor] : a tuple of the database connection and cursor
    """
    db = sqlite3.connect('profils.db')
    cursor = db.cursor()
    return db, cursor

def initDB():
    query = '''
    DROP TABLE IF EXISTS profils;
    
    CREATE TABLE profils 
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Pseudo TEXT,
        Mail TEXT,
        Mdp TEXT,
        Photo TEXT
    );
    
    '''
    db, cursor = connectDatabase()
    cursor.execute(query)
    db.commit()
    cursor.close()
    db.close()

app = Flask(__name__)

#routes:

#index
@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    
    if request.method == "POST":
        pseudo=request.form.get("pseudo")
        mail=request.form.get("mail")
        mdp=request.form.get("mdp")
        
        query = """INSERT INTO profils (Pseudo, Mail, Mdp) VALUES (?, ?, ?);"""
        args = (pseudo, mail, mdp)
        db, cursor = connectDatabase()
        cursor.execute(query, args)
        db.commit()
        db.close()
        
    return redirect("/")

#profil
@app.route("/profil", methods=["POST"])
def profil():
    pseudo=request.form.get("pseudo")
    
    query = """SELECT Pseudo FROM profils"""
    db, cursor = connectDatabase()
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    
    mot = str(data[1])
    print(mot[1])
    
    return render_template("profil.html", pseudo=pseudo)

#inscription
@app.route("/inscription")
def inscription():
    return render_template("inscription.html")




if __name__ == "__main__":
    if (False):
        initDB()
        
    app.run()