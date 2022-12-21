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
        return affichertableforum()


@app.route("/creersujet", methods = ["GET","POST"])
def creersujet():
    if request.method == "GET" :
        return render_template("creersujet.html")
    if request.method == "POST" :
        sujet=request.form.get("sujet")
        message=request.form.get("message")
        return fct_creersujet(sujet,message)

@app.route("/creerreponse", methods = ["GET","POST"])
def creerreponse():
    if request.method == "GET" :
        sujet=request.args.get('sujet')
        return render_template("creerreponse.html", sujet=sujet)
    if request.method == "POST" :
        sujet=request.form.get('sujet')
        reponse=request.form.get("reponse")
        return fct_creerreponse(sujet,reponse)

@app.route("/reponsesujet", methods = ["GET","POST"])
def reponsesujet():
    if request.method == "GET" :
        query="""SELECT Sujet,Reponse FROM reponse;"""
        dbrf,cursor=connectdbreponseforum()
        cursor.execute(query)
        data=cursor.fetchall()
        dbrf.close()
        return render_template("reponse.html", listdbr=data)




#le cabanon (thomas)
@app.route('/cabanon')
def cabanon():
    return render_template('cabanon.html')









#gestion  de profil (étienne)

#connection
@app.route("/connection", methods=["GET","POST"])
def connection():
    if request.method == "GET":
        return render_template("connection.html")
    if request.method == "POST":
        pseudo = request.form.get("pseudo")
        mdp = request.form.get("mdp")
        return fct_connection(pseudo, mdp)


#profil
@app.route("/profil")
def profil():
    return redirect("/connection")



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


#main
if __name__ == "__main__":
    if (False):
        initDB()
    if (False):
        initDBforum()    
    
    app.run(debug=1, host='0.0.0.0', port='5454')