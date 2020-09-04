from flask import Flask, render_template, redirect, url_for, flash, session, request, g
import pymongo
from pymongo import MongoClient
from flask_login import LoginManager
from werkzeug.security import generate_password_hash,check_password_hash
import bcrypt
from profanityfilter import ProfanityFilter
pf = ProfanityFilter()
from flask_login import login_user,current_user
import time
from datetime import date

ttt=(time.strftime('%H'))
ttt=int(ttt)
if ttt>4 and ttt<12:
    mssg='Good Morning'
elif ttt>=12 and ttt<17:
    mssg='Good Afternoon'
elif ttt>=17 and ttt<=21:
    mssg='Good Evening'
else:
    mssg='Good Night'



client=MongoClient("mongodb+srv://swarnabha:swarnabhadb@cluster0.v3eq0.mongodb.net/Motivation?retryWrites=true&w=majority")
app=Flask(__name__)
db=client['Posts']
db2=client['Users']
det=[1,3]
app.secret_key = 'hellouserapi'

# contents=[{"title":"Flask",
#            "content":"Micro Web framework used for deployment using python",
#            "author":"Someone maybe :-)"}]

@app.route('/posts')
def home():
    if g.user:        
        details=db.details
        return render_template('posts.html',contents=details,user_name=g.user,mssg=mssg)
    flash("Please login before continuing")
    return render_template('login.html')

@app.route('/mypost')
def mypost():
    if g.user:
        pp=db.details
        mq={'author':g.user}
        details=pp.find(mq).sort([("_id", -1)])
        return render_template('my_posts.html',contents=details,user_name=g.user,mssg=mssg)
    flash("Please login before continuing")
    return render_template('login.html')

@app.route('/create')
def create():
    if g.user:        
        return render_template('create_blog.html',name=g.user)
    flash("Please login before continuing")
    return render_template('login.html')


@app.route('/create',methods=['POST'])
def create_p():
    if g.user:    
        title=request.form.get('title')
        content=request.form.get('content')
        author=g.user
        if title=="" or content=="":
            flash("Enter both the fields to proceed")
            return render_template('create_blog.html')
        if title!=None or content!=None:
            if pf.is_clean(content)==False or pf.is_clean(title)==False:
                flash(f"Avoid Abuse!God is watching,{g.user}.")
                return render_template('create_blog.html')
            else:
                doc={'title':title,
                    'content':content,
                    'author':author}
                details=db.details
                details.insert_one(doc)
                return redirect(url_for('home'))
        else:
            flash("Enter both the fields to proceed")
            return render_template('create_blog.html')
    
    return render_template('login.html')


@app.route('/')
def login():
    if g.user:
        return redirect(url_for('home'))
        
    return render_template('login.html')

@app.route('/',methods=['POST'])
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
                # det[0]=name
                # det[1]=email                                  
                return redirect(url_for('home'))
        
    if flag==False:
        flash("Invalid Credentials")
        return redirect(url_for('login'))
    
    return redirect(url_for('login'))

@app.route('/register')
def register():
    if g.user:
        session.pop('user', None)
        
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

@app.route('/logout')
def logout():
    if g.user:
        session.pop('user', None)
        return render_template('login.html')
    flash("Please login before continuing")
    return render_template('login.html')

@app.route('/delete/<string:title>')
def delete_post(title):
    if g.user:
        dp={'title':title}
        details=db.details
        details.delete_one(dp)
        return redirect(url_for('mypost'))
    flash("Please login before continuing")
    return redirect(url_for('login'))

@app.route('/update/<string:title>')
def update_post(title):
    if g.user:
        pp=db.details
        mq={'title':title}
        details=pp.find(mq)
        return render_template('update.html',contents=details)
    flash("Please login before continuing")
    return render_template('login.html')

@app.route('/update/<string:title_old>',methods={'POST'})
def update_post_p(title_old):
    title=request.form.get('title')
    content=request.form.get('content')
    gg=True
    if pf.is_clean(content)==False or pf.is_clean(title)==False:
        gg=False
        flash(f"Avoid Abuse!God is watching,{g.user}.")
        pp=db.details
        mq={'title':title_old}
        details=pp.find(mq)
        return render_template('update.html',contents=details)
    
    if title == None or title=="" or content == None or  content=="":        
        pp=db.details
        mq={'title':title_old}
        details=pp.find(mq)
        flash("Enter both the fields to proceed")
        return render_template('update.html',contents=details)    
          
    title=request.form.get('title')
    content=request.form.get('content')
    author=g.user
    doc={'title':title,
        'content':content,
        'author':author}
    details=db.details
    
    
    details.update_one({"title":title_old},{"$set":doc})
    return redirect(url_for('mypost'))      
    

@app.before_request
def before_request():
    g.user=None
    det=[]
    if 'user' in session:
        g.user=session['user']
    

if __name__=='__main__':
    app.run(debug=True)
