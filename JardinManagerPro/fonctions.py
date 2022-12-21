# imports
import string
import random
from flask import Flask, request, render_template, flash, redirect
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
    
#fonction gérant la connection
def fct_connection(pseudo, mdp):
    query = """SELECT Pseudo FROM profils"""
    db, cursor = connectDatabase()
    cursor.execute(query)
    liste_pseudo = cursor.fetchall()
    db.close()
    
    query = """SELECT Mail, Mdp, Photo, Ville FROM profils WHERE Pseudo LIKE (?)"""
    args = [pseudo]
    db, cursor = connectDatabase()
    cursor.execute(query, args)
    data = cursor.fetchall()
    db.close()
    
    if pseudo == ("""""") or mdp == ("""""") :
        return render_template("error_profil.html", message = "Veuillez compléter tous les champs !")
    elif pseudo not in str(liste_pseudo) :
        return render_template("error_profil.html", message = "Vous n'êtes pas inscrit !")
    elif str(mdp) != data[0][1] :
        return render_template("error_profil.html", message = "Mauvais mot de passe !")
    else :
        print(data)
        return render_template("profil.html", pseudo=pseudo, items=data)
    
#fonction gérant l'inscription
def fct_inscritpion(pseudo, mail, mdp, ville):
    query = """SELECT Pseudo FROM Profils WHERE (Pseudo LIKE (?) OR Mail LIKE (?));"""
    args = [pseudo,mail]
    db, cursor = connectDatabase()
    cursor.execute(query,args)
    data = cursor.fetchall()
    db.close()
    
    if data == [] :
        query = """INSERT INTO profils (Pseudo, Mail, Mdp, Ville) VALUES (?, ?, ?, ?);"""
        args = (pseudo, mail, mdp, ville)
        db, cursor = connectDatabase()
        cursor.execute(query, args)
        db.commit()
        db.close()
        return redirect("/connection")
    else :
        return render_template("error_profil.html", message = "Pseudo ou mail déjà pris !")
    
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

def connectdbreponseforum():
    """
        Function that returns db connection and the cursor to interact with the database.db file

        Parameters :
            None

        Returns :
            - tuple [Connection, Cursor] : a tuple of the database connection and cursor
    """
    dbrf = sqlite3.connect('reponse.db')
    cursor = dbrf.cursor()
    return dbrf, cursor

def initDBreponseforum():
    query = '''
    DROP TABLE IF EXISTS reponse;
    
    CREATE TABLE reponse
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Sujet TEXT,
        Reponse TEXT
    );
    
    '''
    dbrf, cursor = connectdbreponseforum()
    cursor.execute(query)
    dbrf.commit()
    cursor.close()
    dbrf.close()

def initDBforum():
    query = '''
    DROP TABLE IF EXISTS forum;
    
    CREATE TABLE forum
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Sujet TEXT,
        Message TEXT
    );
    
    '''
    dbf, cursor = connectdbforum()
    cursor.execute(query)
    dbf.commit()
    cursor.close()
    dbf.close()

def fct_creersujet(sujet,message):
    query = """INSERT INTO forum (Sujet,Message) VALUES (?,?);"""
    args = [sujet,message]
    dbf, cursor = connectdbforum()
    cursor.execute(query,args)
    dbf.commit()
    dbf.close()
    return redirect ("/forum")

def fct_creerreponse(sujet,reponse):
    query = """INSERT INTO reponse (Sujet,Reponse) VALUES (?,?);"""
    args = [sujet,reponse]
    dbrf, cursor = connectdbreponseforum()
    cursor.execute(query,args)
    dbrf.commit()
    dbrf.close()
    return redirect ("/reponsesujet")

def affichertableforum():
    query="""SELECT Sujet,Message FROM forum;"""
    dbf,cursor=connectdbforum()
    cursor.execute(query)
    data=cursor.fetchall()
    dbf.close()

    return render_template("forum.html", listdb=data)



