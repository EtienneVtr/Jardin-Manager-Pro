import string
import random
from flask import Flask, render_template, request, redirect
import sqlite3
from fonctions import *

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
    data = to_string(cursor.fetchall())
    db.close()
    
    print(data[1])
    
    return render_template("profil.html", pseudo=pseudo)

#inscription
@app.route("/inscription")
def inscription():
    return render_template("inscription.html")




if __name__ == "__main__":
    if (False):
        initDB()
        
    app.run(debug=1, host='0.0.0.0', port='5454')