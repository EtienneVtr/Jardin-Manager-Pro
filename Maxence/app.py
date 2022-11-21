"""
    Author : Maxence Bouchadel
    Email : maxence.bouchadel@telecomnancy.eu
    Date : 19/11/2022
"""
#imports
from flask import Flask, request, render_template, flash, redirect
import sqlite3

#flask app creation

app = Flask(__name__)

#/home
@app.route("/")
def home():
    return render_template("home.html")






if __name__ == "__main__":

    app.run(debug=1, host='0.0.0.0', port='8484')