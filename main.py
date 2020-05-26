from flask import Flask, render_template, request, redirect,session,flash,url_for,g
from datetime import  timedelta
app=Flask(__name__)
import os
import mysql.connector
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=5)
mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database = 'covid'
)
@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user=session['user']
    print(g.user)
@app.route("/")
def home():
    return render_template('index.html')
@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        name=request.form.get('name')
        type = request.form.get('type')
        phone=request.form.get('phone')
        email=request.form.get('email')
        password=request.form.get('password')
        query="insert into  signup(name,type,phone,email,password) VALUES (%s,%s,%s,%s,%s)"
        val = (name,type,phone,email,password)
        mycursor = mydb.cursor()
        mycursor.execute(query, val)
        mydb.commit()
    return render_template('contact.html')
@app.route("/login", methods=['GET','POST'])
def login():
    if(request.method=='POST'):
        session.pop('user', None)
        email=request.form.get('email')
        password=request.form.get('password')
        try:
            mycursor = mydb.cursor()
            mycursor.execute('SELECT * FROM signup WHERE email=%s and password=%s', (email,password))
            records = mycursor.fetchall()
            session['user'] = email
            # session.permanent = True
            if "user" in session :
                user = session['user']
            for row in records:
                type=str(row[1])
            if(type=='mentor'):
                return redirect(url_for('mentor'))
            if(type=='mentee'):
                return redirect(url_for('mentee'))
        except:
            print("Wrong email password")
            flash("Wrong Details")
            return render_template("login.html")
    try:
        return render_template('login.html',user=user)
    except:
        return render_template('login.html')
@app.route('/mentor')
def mentor():
    if(g.user):
        return render_template('mentor1.html',user=session['user'])
    return render_template('login.html')

@app.route('/addsched', methods=['POST','GET'])
def addsc():
    if 'user' in session:
        user = session['user']
    if (request.method == 'POST') :
        name=request.form.get('name')
        day=request.form.get('day')
        time=request.form.get('time')
        zoomlink=request.form.get('zoomlink')
        query = "insert into  schedule(name,day,time,zoomlink) VALUES (%s,%s,%s,%s)"
        val = (name,day,time,zoomlink)
        mycursor = mydb.cursor()
        mycursor.execute(query, val)
        mydb.commit()
    return render_template('addsch.html')
@app.route("/viewapp",methods=['POST','GET'])
def viewapp():
    if 'user' in session :
        user = session['user']
    if (request.method == 'POST') :

        try:
            mname=request.form.get("mname")
            mycursor=mydb.cursor()
            mycursor.execute('SELECT * FROM appointment WHERE mname=%s',(mname,))
            myresult=mycursor.fetchall()
            for x in myresult:
                print(x)
            mydb.commit()
        except:
            render_template('viewap.html',user=user)
    try:
        return render_template('viewap.html',data=myresult,user=user)
    except:
        return render_template('viewap.html',  user=user)
@app.route('/mentee')
def mentee():
    if(g.user):
        return render_template('mentee1.html',user=session['user'])
    return render_template('login.html')

@app.route("/viewschp",methods=['POST','GET'])
def viewschp():
    if 'user' in session :
        user = session['user']
    if (request.method == 'POST') :

        try:
            name=request.form.get("name")
            mycursor=mydb.cursor()
            mycursor.execute('SELECT * FROM schedule WHERE name=%s',(name,))
            myresult=mycursor.fetchall()
            for x in myresult:
                print(x)
            mydb.commit()
        except:
            render_template('viewps.html',user=user)
    try:
        return render_template('viewps.html',data=myresult,user=user)
    except:
        return render_template('viewps.html',  user=user)
@app.route('/bookap')
def bookap():
    if(g.user):
        return render_template('book.html',user=session['user'])
    return render_template('book.html')
@app.route('/bookapp', methods=['POST','GET'])
def bookapp():
    if (request.method == 'POST') :
        name=request.form.get('name')
        emailid=request.form.get('emailid')
        mname=request.form.get('mname')
        day=request.form.get('day')
        time=request.form.get('time')
        print("1")
        query = "insert into  appointment(name,emailid,mname,day,time) VALUES (%s,%s,%s,%s,%s)"
        val = (name,emailid, mname, day, time)
        mycursor = mydb.cursor()
        mycursor.execute(query, val)
        print("2")
        mydb.commit()
    return render_template('zoom.html')
@app.route('/disp')
def disp():
    if(g.user):
        return render_template('zoom.html',user=session['user'])
    return render_template('zoom.html')
@app.route("/dispzoom",methods=['POST','GET'])
def dispzoom():
    if 'user' in session :
        user = session['user']
    if (request.method == 'POST') :

        try:
            name=request.form.get("name")
            mycursor=mydb.cursor()
            mycursor.execute('SELECT * FROM schedule WHERE name=%s',(name,))
            myresult=mycursor.fetchall()
            for x in myresult:
                print(x)
            mydb.commit()
        except:
            render_template('zoom.html',user=user)
    try:
        return render_template('zoom.html',data=myresult,user=user)
    except:
        return render_template('zoom.html',  user=user)
@app.route("/logout")
def logout():
    session.pop('user', None)
    return render_template('login.html')
app.run(debug=True)