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
db2=client['Users']

app.secret_key = 'hellouserapi'

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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def login_p():
    session.pop('user',None)
    email=request.form.get('email')
    password=request.form.get('pass')
    data=db2.credentials
    flag=False
    
    if email is None or password is None:
        flash("Please fill both the fields and try again")
        return render_template(url_for('login'))
    
    for i in data.find():
        if i['email']==email:
            name=i['username']            
            if check_password_hash(i['password'], password):    
                flag=True
                session['user']=name 
                print(session['user'])  
                det[0]=name
                det[1]=email                                  
                return redirect(url_for('/'))
        
    if flag==False:
        flash("Invalid Credentials")
        return redirect(url_for('login'))
    
    return redirect(url_for('login'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register',methods=['POST'])
def register_p():
    name=request.form.get('name')
    email=request.form.get('email')
    password=request.form.get('pass')
    password=generate_password_hash(password, method='sha256')    
    
    data=db2.credentials
    for i in data.find():
        if i['email']==email:  
            flash("Your Email Address is already registered with us")
            print("registred")
            return redirect(url_for('login')) 
       
    user_info={'username': name,
            'email': email,
            'password': password} 
    print('not regis')
    data.insert_one(user_info)
        
    return redirect(url_for('login'))
    


@app.route('/mypost')
def mypost():
    details=db.details
    return render_template('my_posts.html',contents=details)

    

if __name__=='__main__':
    app.run(debug=True)
