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
    return render_template("home.html")





#route forum (flo)


@app.route('/forum',methods=['GET','POST'])
def forum():     
    if request.method=='GET':
        return render_template('forum.html')

@app.route("/creerunsujet", methods = ["GET","POST"])
def creerunsujet():
    if request.method == "GET" :
        return render_template("creerunsujet.html")
    if request.method == "POST" :
        sujet=request.form.get("sujet")
        message=request.form.get("message")
        query = """INSERT INTO forum (Sujet,Message) VALUES (?, ?);"""
        args = (sujet,message)
        dbf, cursor = connectdbforum()
        cursor.execute(query, args)
        dbf.commit()
        dbf.close()
        
        return fct_creersujet(sujet,message)










#le cabanon (thomas)
@app.route('/cabanon')
def cabanon():
    return render_template('cabanon.html')









#gestion  de profil (étienne)
@app.route("/connection", methods=["GET","POST"])
def connextion():
    if request.method == "GET":
        return render_template("connection.html")
    if request.method == "POST":
        pseudo = request.form.get("pseudo")
        mdp = request.form.get("mdp")


#profil
@app.route("/profil")
def profil():
    return render_template("profil.html")



#inscription
@app.route("/inscription", methods = ["GET","POST"])
def inscription():
    if request.method == "GET" :
        return render_template("inscription_profil.html")
    if request.method == "POST" :
        pseudo=request.form.get("pseudo")
        mail=request.form.get("mail")
        mdp=request.form.get("mdp")
        
        query = """INSERT INTO profils (Pseudo, Mail, Mdp) VALUES (?, ?, ?);"""
        args = (pseudo, mail, mdp)
        db, cursor = connectDatabase()
        cursor.execute(query, args)
        db.commit()
        db.close()
        
        return redirect("/connection")


#main
if __name__ == "__main__":
    if (False):
        initDBforum()
    
    app.run(debug=1, host='0.0.0.0', port='5454')
    
if __name__ == "__main__":
    if (False):
        initDB()
    
    app.run(debug=1, host='0.0.0.0', port='5454')

