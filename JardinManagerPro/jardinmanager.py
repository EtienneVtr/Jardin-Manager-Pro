# imports
import string
import random
from flask import Flask, request, render_template, flash, redirect
import sqlite3


#importation des fonctions créée:
from fonctions import *


# flask app creation
app = Flask(__name__)

#def des routes:

#/home (max)
@app.route("/")
def home():
    return render_template("test.html")





#route forum (flo)
@app.route('/forum',methods=['GET','POST'])
def forum():     
    if request.method=='GET':
        return render_template('forum.html')








#le cabanon (thomas)
@app.route('/cabanon')
def cabanon():
    return render_template('cabanon.html')









#gestion  de profil (étienne)
@app.route("/connextion", methods=["GET","POST"])
def connextion():
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









#main
if __name__ == "__main__":
    
    app.run(debug=1, host='0.0.0.0', port='5454')