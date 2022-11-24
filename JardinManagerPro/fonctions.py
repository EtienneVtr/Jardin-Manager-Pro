# imports
import string
import random
from flask import Flask, request, render_template, flash, redirect
import sqlite3

#fonction permettant de mettre les données récupérées de profils.db sous forme de chaîne de caractère
def to_string(chaine):
    n = len(chaine)
    T = n*[0]
    for i in range (n):
        T[i] = str(chaine[i])
        m = len(T[i])
        T[i] = T[i][2:m-3]
    return T

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
    liste_pseudo = to_string(cursor.fetchall())
    db.close()
    
    query = """SELECT Mdp FROM profils WHERE Pseudo LIKE (?)"""
    args = [pseudo]
    db, cursor = connectDatabase()
    cursor.execute(query, args)
    data = to_string(cursor.fetchall())
    db.close()
    
    print(pseudo)
    
    if pseudo == ("""""") or mdp == ("""""") :
        return render_template("error_profil.html", message = "Veuillez compléter tous les champs !")
    elif pseudo not in liste_pseudo :
        return render_template("error_profil.html", message = "Vous n'êtes pas inscrit !")
    elif mdp != data :
        return render_template("error_profil.html", message = "Mauvais mot de passe !")
    else :
        return render_template("profil.html")