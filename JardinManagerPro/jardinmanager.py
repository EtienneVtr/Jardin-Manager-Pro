# imports
import string
import random
import datetime
from flask import Flask, request, render_template, flash, redirect, session, url_for
from flask_session import Session
import sqlite3


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
        return affichertableforum()


@app.route("/creersujet", methods = ["GET","POST"])
def creersujet():
    if request.method == "GET" :
        return render_template("creersujet.html")
    if request.method == "POST" :
        sujet=request.form.get("sujet")
        message=request.form.get("message")
        if  ('name' in session) and (session['name']!=None):
            pseudo = session['name']
            date= datetime.datetime.now()
            date= date.strftime("%d/%m/%Y %H:%M")
            return fct_creersujet(sujet,message,pseudo,date)
        else :
            return render_template("connection.html")
            

@app.route("/creerreponse", methods = ["GET","POST"])
def creerreponse():
    if request.method == "GET" :
        sujet=request.args.get('sujet')
        return render_template("creerreponse.html", sujet=sujet)
    if request.method == "POST" :
        sujet=request.form.get('sujet')
        reponse=request.form.get("reponse")
        if  ('name' in session) and (session['name']!=None):
            pseudo = session['name']
            date= datetime.datetime.now()
            date= date.strftime("%d/%m/%Y %H:%M")
            return fct_creerreponse(sujet,reponse,pseudo,date)
        else :
            return render_template("connection.html")
            

@app.route("/reponsesujet", methods = ["GET","POST"])
def reponsesujet():
    if request.method == "GET" :
        sujet = request.args.get('sujet')
        query="""SELECT Reponse,pseudo,date FROM reponse WHERE Sujet=?"""
        args=[sujet]
        dbf,cursor=connectdbforum()
        cursor.execute(query,args)
        data=cursor.fetchall()
        dbf.close()
        return render_template("reponse.html", listdb=data,sujet=sujet)




#le cabanon (thomas)
@app.route('/cabanon')
def cabanon():
    return render_template('cabanon.html')



#Jardin (max et thomas)
@app.route('/jardin')
def jardin():
    return render_template('jardin.html')


@app.route('/info')
def info():
    return render_template('info.html')






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
    flash("Déconnexion réussie !")
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
        pseudo = session.get("name")
        if donnee == "pseudo" :
            new_pseudo = request.form.get("new_pseudo")
            session["name"] = new_pseudo
            return maj_db(pseudo, new_pseudo, "Pseudo")
        elif donnee == "mail" :
            new_mail = request.form.get("new_mail")
            return maj_db(pseudo, new_mail, "Mail")
        elif donnee == "mdp" :
            ancien_mdp = request.form.get("ancien_mdp")
            if verif_mdp(pseudo,ancien_mdp):
                new_mdp = request.form.get("new_mdp")
                return maj_db(pseudo, new_mdp, "Mdp")
            else :
                return render_template("error_maj_profil.html", message="Vous vous êtes trompés dans votre ancien mot de passe !")
        else :
            new_ville = request.form.get("new_ville")
            return maj_db(pseudo, new_ville, "Ville")
        
#profil public
@app.route("/user/<string:donnee>")
def user(donnee : str):
    return fct_profil_public(donnee)

#main
if __name__ == "__main__":
    if (False):
        initDB()
    if (False):
        initDBforum()   
    if (False):
        initDBjardin()
    if (True):
        initDBlegume()
 
    
    app.run(debug=1, host='0.0.0.0', port='5454')
