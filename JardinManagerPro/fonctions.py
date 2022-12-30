# imports
import string
import random
import datetime
from flask import Flask, request, render_template, flash, redirect, session, url_for
from flask_session import Session
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
        return render_template("error_profil.html", message = "Veuillez compléter tous les champs !")
    
    #on vérifie que le pseudo est déjà dans la base de donnée
    elif verif_donnee(pseudo,liste_pseudo) == False :
        return render_template("error_profil.html", message = "Vous n'êtes pas inscrit !")
    
    #on vérifie que c'est le bon mot de passe
    elif str(mdp) != data[0][1] :
        return render_template("error_profil.html", message = "Mauvais mot de passe !")
    
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
def fct_inscritpion(pseudo, mail, mdp, ville):
    #on récupère les pseudos pour vérifier si l'adresse mail ou le pseudo existent déjà dans la database
    query = """SELECT Pseudo FROM Profils WHERE (Pseudo LIKE (?) OR Mail LIKE (?));"""
    args = [pseudo,mail]
    db, cursor = connectDatabase()
    cursor.execute(query,args)
    data = cursor.fetchall()
    db.close()
    
    #il ne faut pas qu'il y ait de pseudo lié au pseudo donné en entrée pour garantir l'unicité
    if data == [] :
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
        return render_template("error_profil.html", message = "Pseudo ou mail déjà pris !")
    
    
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
            return render_template("error_maj_profil.html", message="Ce pseudo est déjà utilisé ! Veuillez en choisir un autre !")

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
            return render_template("error_maj_profil.html", message="Ce mail est déjà utilisé ! Veuillez en choisir une autre !")

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
    query = """SELECT Ville FROM profils WHERE Pseudo LIKE (?)"""
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

def affichertableforum():
    query="""SELECT Sujet,Message,pseudo,date FROM forum;"""
    dbf,cursor=connectdbforum()
    cursor.execute(query)
    data=cursor.fetchall()
    dbf.close()

    return render_template("forum.html", listdb=data)

#def initdbforum():
#    CREATE TABLE forum( id INTEGER PRIMARY KEY AUTOINCREMENT, Sujet TEXT,Message TEXT, pseudo TEXT,date TEXT);
#def initdbreponseforum():
#    CREATE TABLE reponse( id INTEGER PRIMARY KEY AUTOINCREMENT, Sujet TEXT,Reponse TEXT, pseudo TEXT,date TEXT);
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


