# imports
import string
import random
from flask import Flask, request, render_template, flash, redirect, session
import sqlite3
from flask_session import Session


#importation des fonctions créée:
from fonctions import *


# flask app creation
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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

#connexion
@app.route("/connection", methods=["GET","POST"])
def connection():
    if request.method == "GET":
        return render_template("connection.html")
    if request.method == "POST":
        pseudo = request.form.get("pseudo")
        mdp = request.form.get("mdp")
        return fct_connection(pseudo, mdp)


#deconnexion
@app.route("/deconnexion")
def deconnexion():
    session["name"] = None
    return redirect("/")


#profil
@app.route("/profil")
def profil():
    if not session.get("name"):
        return redirect("/connection")
    else :
        pseudo = session.get("name")
        return fct_profil(pseudo)


#inscription
@app.route("/inscription", methods = ["GET","POST"])
def inscription():
    if request.method == "GET" :
        return render_template("inscription_profil.html")
    if request.method == "POST" :
        pseudo=request.form.get("pseudo")
        mail=request.form.get("mail")
        mdp=request.form.get("mdp")
        ville=request.form.get("ville")
        
        return fct_inscritpion(pseudo, mail, mdp, ville)
        

#mise a jour donnee profil
@app.route("/maj/<string:donnee>", methods = ["GET", "POST"])
def maj(donnee : str):
    if request.method == "GET" :
        return render_template(f"maj_{ donnee }.html")
    if request.method == "POST" :
        if donnee == "pseudo" :
            new_pseudo = request.form.get("new_pseudo")
            return maj_db({ session.name }, new_pseudo)
        elif donnee == "mail" :
            new_mail = request.form.get("new_mail")
            return maj_db({ session.name }, new_mail)
        elif donnee == "mdp" :
            new_mdp = request.form.get("new_mdp")
            return maj_db({ session.name }, new_mdp)
        else :
            new_ville = request.form.get("new_ville")
            return maj_db({ session.name }, new_ville)


#main
if __name__ == "__main__":
    if (False):
        initDB()
    if (False):
        initDBforum()    
    
    app.run(debug=1, host='0.0.0.0', port='5454')
