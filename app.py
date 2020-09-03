from flask import Flask, render_template, redirect, url_for, flash, session, request, g
import pymongo
from pymongo import MongoClient
from flask_login import LoginManager
from werkzeug.security import generate_password_hash,check_password_hash
import bcrypt
from flask_login import login_user,current_user

client=MongoClient("mongodb+srv://swarnabha:swarnabhadb@cluster0.v3eq0.mongodb.net/Motivation?retryWrites=true&w=majority")
app=Flask(__name__)
db=client['Posts']

# contents=[{"title":"Flask",
#            "content":"Micro Web framework used for deployment using python",
#            "author":"Someone maybe :-)"}]

@app.route('/')
def home():
    details=db.details
    return render_template('posts.html',contents=details)

@app.route('/create')
def create_p():
    return render_template('create_blog.html')

@app.route('/create',methods=['POST'])
def create():
    title=request.form.get('title')
    content=request.form.get('content')
    author="SD"
    doc={'title':title,
         'content':content,
         'author':author}
    details=db.details
    details.insert_one(doc)
    return redirect(url_for('home'))

@app.route('/mypost')
def mypost():
    details=db.details
    return render_template('my_posts.html',contents=details)
    

if __name__=='__main__':
    app.run(debug=True)
