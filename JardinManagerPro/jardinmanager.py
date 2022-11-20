# imports
import string
import random
from flask import Flask, request, render_template, flash, redirect

#definition des fonction



# flask app creation
app = Flask(__name__)

#def des routes:
@app.route("/")
def index():
    return "Up and Run"

#route forum (flo)
@app.route('/forum',methods=['GET','POST'])
def forum():     
    if request.method=='GET':
        return render_template('forum.html')


#le cabanon (thomas)
@app.route('/cabanon')
def cabanon():
    return render_template('cabanon.html')




#main
if __name__ == "__main__":
    
    app.run(debug=1, host='0.0.0.0', port='5454')