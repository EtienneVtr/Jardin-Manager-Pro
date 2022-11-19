from flask import Flask 
from flask import request 
from flask import render_template  
app=Flask(__name__)

@app.route('/forum',methods=['GET','POST'])
def forum():     
    if request.method=='GET':
        return render_template('forum.html')