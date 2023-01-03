# imports
import string
import random
import datetime
import base64
import os
from flask import Flask, request, render_template, flash, redirect, session, url_for
from flask_session import Session
#from sqlalchemy import bindparam
import sqlite3

#fonction permettant de se connecter à la base de donnée
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

#fonctions initialisant la base de donnée
def initDB():
    query = '''
    DROP TABLE IF EXISTS profils;
    
    CREATE TABLE profils 
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Pseudo TEXT,
        Mail TEXT,
        Mdp TEXT,
        Photo TEXT,
        Ville TEXT
    );
    
    '''
    db, cursor = connectDatabase()
    cursor.execute(query)
    db.commit()
    cursor.close()
    db.close()

#LES DONNEES RECUPEREES DANS LA BASE DE DONNE SONT DE LA FORME SUIVANTE : data=[('donne1',),]
#C'EST UNE LISTE DE LISTE !!!!!
#ON A DONC data[0][0] = donne1


#fonction qui vérifie qu'une donnée est déjà dans la liste donnée en entrée
def verif_donnee(donnee,liste):
    for i in range(len(liste)):
        if donnee == liste[i][0]:
            return True
    return False


#fonction qui vérifie si c'est le bon mot de passe
def verif_mdp(pseudo,mdp):
    query = """SELECT Mdp FROM profils WHERE Pseudo LIKE (?)"""
    args = [pseudo]
    db, cursor = connectDatabase()
    cursor.execute(query, args)
    data = cursor.fetchall()
    db.close()
    
    if data[0][0] == str(mdp):
        return True
    else :
        return False


#fonction gérant la connection
def fct_connection(pseudo, mdp):
    #on récupère la liste de pseudo
    query = """SELECT Pseudo FROM profils"""
    db, cursor = connectDatabase()
    cursor.execute(query)
    liste_pseudo = cursor.fetchall()
    db.close()
    
    #on récupère le mail, la ville, la photo et le mdp associés au pseudo donné en entrée
    query = """SELECT Mail, Mdp, Photo, Ville FROM profils WHERE Pseudo LIKE (?)"""
    args = [pseudo]
    db, cursor = connectDatabase()
    cursor.execute(query, args)
    data = cursor.fetchall()
    db.close()
    
    #on vérifie que les champs ne sont pas vides
    if pseudo == ("""""") or mdp == ("""""") :
        flash("Veuillez compléter tous les champs !")
        return redirect("/connection")
    
    #on vérifie que le pseudo est déjà dans la base de donnée
    elif verif_donnee(pseudo,liste_pseudo) == False :
        flash("Vous n'êtes pas encore inscrit !")
        return redirect("/connection")
    
    #on vérifie que c'est le bon mot de passe
    elif str(mdp) != data[0][1] :
        flash("Mauvais mot de passe !")
        return redirect("/connection")
    
    else :
        session["name"] = pseudo
        flash("Connexion réussie !")
        return redirect("/profil")


#fonction gérant affichage profil une fois connecté
def fct_profil(pseudo):
    #récupération des données liées au pseudo donné en entrée
    query = """SELECT Mail, Mdp, Photo, Ville FROM profils WHERE Pseudo LIKE (?)"""
    args = [pseudo]
    db, cursor = connectDatabase()
    cursor.execute(query, args)
    data = cursor.fetchall()
    db.close()
    return render_template("profil.html", items = data, pseudo = pseudo)
    
    
#fonction gérant l'inscription
def fct_inscritpion(pseudo, mail, mdp, conf_mdp, ville):
    #on récupère les pseudos pour vérifier si l'adresse mail ou le pseudo existent déjà dans la database
    query = """SELECT Pseudo FROM Profils WHERE (Pseudo LIKE (?) OR Mail LIKE (?));"""
    args = [pseudo,mail]
    db, cursor = connectDatabase()
    cursor.execute(query,args)
    data = cursor.fetchall()
    db.close()
    
    #il ne faut pas qu'il y ait de pseudo lié au pseudo donné en entrée pour garantir l'unicité
    if data == [] :
        #il faut être sûr que l'utilisateur ne s'est pas trompé lorsqu'il a rentré son mot de passe
        if conf_mdp == mdp:
            #ici on insert une nouvelle ligne dans la base de donnée
            query = """INSERT INTO profils (Pseudo, Mail, Mdp, Ville) VALUES (?, ?, ?, ?);"""
            args = (pseudo, mail, mdp, ville)
            db, cursor = connectDatabase()
            cursor.execute(query, args)
            db.commit()
            db.close()
            flash("Inscription réussie ! Veuillez vous connecter pour accéder à votre profil !")
            return redirect("/connection")
        
        else :
            flash("Les deux mots de passe que vous avez rentrés ne sont pas identiques. Veuillez recommencer !")
            return redirect("/inscription")
    
    else :
        flash("Le pseudo ou le mail que vous avez choisi est déjà utilisé par un autre utilisateur. Veuillez en choisir un nouveau !")
        return redirect("/inscription")
    
    
# fonction pour changer de pseudo,...
def maj_db(pseudo, nouvelle_donnee, donnee_a_changer):
    #on différencie les cas suivant s'il faut changer le mail,...
    if donnee_a_changer == "Pseudo":
        #on récupère la liste des pseudos de la base de donnée afin de garantir l'unicité du nouveau pseudo
        query = """SELECT Pseudo FROM profils"""
        db, cursor = connectDatabase()
        cursor.execute(query)
        liste_pseudo = cursor.fetchall()
        db.close()

        if verif_donnee(nouvelle_donnee,liste_pseudo)==False:
            #mise à jour de la base de donnée
            session["name"] = nouvelle_donnee
            query = """UPDATE profils SET Pseudo = ? WHERE Pseudo LIKE ?;"""
            args = [nouvelle_donnee,pseudo]
            db, cursor = connectDatabase()
            cursor.execute(query,args)
            db.commit()
            db.close()
            return redirect("/profil")
        
        else :
            flash("Ce pseudo est déjà utilisé par un autre utilisateur. Veuillez en choisir un autre !")
            return redirect("/maj/pseudo")

    elif donnee_a_changer == "Mail":
        #idem que pour la liste de pseudo
        query = """SELECT Mail FROM profils"""
        db, cursor = connectDatabase()
        cursor.execute(query)
        liste_mail = cursor.fetchall()
        db.close()

        if verif_donnee(nouvelle_donnee,liste_mail) == False:
            #mise a jour de la base de donnée
            query = """UPDATE profils SET Mail = ? WHERE Pseudo LIKE ?;"""
            args = [nouvelle_donnee,pseudo]
            db, cursor = connectDatabase()
            cursor.execute(query,args)
            db.commit()
            db.close()
            return redirect("/profil")
        
        else :
            flash("Ce mail est déjà utilisé par un autre utilisateur. Veuillez en choisir un autre !")
            return redirect("/maj/mail")

    elif donnee_a_changer == "Mdp":
        #mise a jour de la base de donnée
        query = """UPDATE profils SET Mdp = ? WHERE Pseudo LIKE ?;"""
        args = [nouvelle_donnee,pseudo]
        db, cursor = connectDatabase()
        cursor.execute(query,args)
        db.commit()
        db.close()
        return redirect("/profil")
    
    else :
        #mise a jour de la base de donnée
        query = """UPDATE profils SET Ville = ? WHERE Pseudo LIKE ?;"""
        args = [nouvelle_donnee,pseudo]
        db, cursor = connectDatabase()
        cursor.execute(query,args)
        db.commit()
        db.close()
        return redirect("/profil")
    
    
# fonction gérant affichage profil public
def fct_profil_public(pseudo):
    #on récupère les données liées au pseudo
    query = """SELECT Mail, Ville FROM profils WHERE Pseudo LIKE (?)"""
    args = [pseudo]
    db, cursor = connectDatabase()
    cursor.execute(query, args)
    data = cursor.fetchall()
    db.close()
    return render_template("profil_public.html", items = data, pseudo = pseudo)
    
    
#base de donnéé forum

def connectdbforum():
    """
        Function that returns db connection and the cursor to interact with the database.db file

        Parameters :
            None

        Returns :
            - tuple [Connection, Cursor] : a tuple of the database connection and cursor
    """
    dbf = sqlite3.connect('forum.db')
    cursor = dbf.cursor()
    return dbf, cursor

def fct_creersujet(sujet,message,pseudo,date):
    query = """INSERT INTO forum (Sujet,Message,pseudo,date) VALUES (?,?,?,?);"""
    args = [sujet,message,pseudo,date]
    dbf, cursor = connectdbforum()
    cursor.execute(query,args)
    dbf.commit()
    dbf.close()
    return redirect ("/forum")

def fct_creerreponse(sujet,reponse,pseudo,date):
    query = """INSERT INTO reponse (Sujet,Reponse,pseudo,date) VALUES (?,?,?,?);"""
    args = [sujet,reponse,pseudo,date]
    dbf, cursor = connectdbforum()
    cursor.execute(query,args)
    dbf.commit()
    dbf.close()
    return redirect(url_for('reponsesujet',sujet=sujet))

def fct_creeroffre(annonce, prix, localisation, pseudo, date, image):
    image_data = image.read()
    image_b64 = base64.b64encode(image_data).decode('utf-8')
    query = """INSERT INTO annonce (Annonce,Prix,Localisation,Pseudo,Date,Image) VALUES (?,?,?,?,?,?);"""
    args = [annonce, prix, localisation, pseudo, date, image_b64]
    dbf, cursor = connectdbforum()
    cursor.execute(query, args)
    dbf.commit()
    dbf.close()
    
    return redirect(url_for('cabanon'))

def affichertableforum():
    query="""SELECT Sujet,Message,pseudo,date FROM forum;"""
    dbf,cursor=connectdbforum()
    cursor.execute(query)
    data=cursor.fetchall()
    dbf.close()

    return render_template("forum.html", listdb=data)

def affichertableannonce():
    query="""SELECT Annonce,Prix,Localisation,Pseudo,Date FROM annonce;"""
    dbf,cursor=connectdbforum()
    cursor.execute(query)
    data=cursor.fetchall()
    dbf.close()

    return render_template("cabanon.html", listdb=data)

def affichertableannoncefiltre(prix_min,prix_max):
    query="""SELECT Annonce,Prix,Localisation,Pseudo,Date FROM annonce WHERE Prix > ? AND Prix < ?;"""
    args=[prix_min,prix_max]
    dbf,cursor=connectdbforum()
    cursor.execute(query,args)
    data=cursor.fetchall()
    dbf.close()

    return render_template("cabanon.html", listdb=data,prix_min=prix_min,prix_max=prix_max)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#def initdbforum():
#    CREATE TABLE forum( id INTEGER PRIMARY KEY AUTOINCREMENT, Sujet TEXT,Message TEXT, pseudo TEXT,date TEXT);
#def initdbreponseforum():
#    CREATE TABLE reponse( id INTEGER PRIMARY KEY AUTOINCREMENT, Sujet TEXT,Reponse TEXT, pseudo TEXT,date TEXT);
#def initdbannonceforum():
#    CREATE TABLE annonce( id INTEGER PRIMARY KEY AUTOINCREMENT, Annonce TEXT,Prix FLOAT,Localisation TEXT, Pseudo TEXT,Date TEXT);
#Au cas ou




#Base de donné mon jardin: (thomas)
def connectdbjardin():
    """
        Function that returns db connection and the cursor to interact with the database.db file

        Parameters :
            None

        Returns :
            - tuple [Connection, Cursor] : a tuple of the database connection and cursor
    """
    dbj = sqlite3.connect('jardin.db')
    cursor = dbj.cursor()
    return dbj, cursor

def initDBjardin():
    query = '''
    DROP TABLE IF EXISTS jardin;
    
    CREATE TABLE jardin
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        culture TEXT,
        largeur INTEGER,
        longueur INTEGER,
        dernier_arrosage DATETIME,
        futur_arrosage DATETIME
        
    );
    
    '''
    dbj, cursor = connectdbjardin()
    cursor.executescript(query)
    dbj.commit()
    cursor.close()
    dbj.close()
    
#base de données de légume et fruit
def connectdblegume():
    """
        
        Function that returns db connection and the cursor to interact with the database.db file

        Parameters :
            None

        Returns :
            - tuple [Connection, Cursor] : a tuple of the database connection and cursor
    """
    dbl = sqlite3.connect('legume.db')
    cursor = dbl.cursor()
    return dbl, cursor

def initDBlegume():
    """
        Stocke la liste des fruits et légumes ainsi que des informations sur chacun
    """
    
    query = '''
    DROP TABLE IF EXISTS legume;
    
    CREATE TABLE legume
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_vegetal TEXT,
        type_vegetal TEXT,
        photo TEXT,
        eau TEXT,
        conservation TEXT
        
    );
    
    '''
    dbl, cursor = connectdblegume()
    cursor.executescript(query)
    dbl.commit()
    cursor.close()
    dbl.close()


