from flask import Flask, render_template, request, url_for, flash, redirect, session, escape, Markup
from forms import UserCreationForm, UserRegistrationForm, LoginForm, AddDogForm, EditDogForm, AddExpenseForm, AddUserForm, addadoptionForm,AdoptionApplicationForm, appreviewform2, EditUserForm
from flask_paginate import Pagination, get_page_args
from flask_mysqldb import MySQL
from wtforms import Form, StringField, validators, PasswordField, TextAreaField
from passlib.hash import sha256_crypt
from datetime import timedelta
import os
from datetime import date
import MySQLdb
import decimal
import email_validator

app = Flask(__name__)
global RoleId
global fname
global status2
global status3

#CSRF secret key to stop cross site request forgery
app.config['SECRET_KEY'] = 'e136d68bbc12329abd9a8ebe64d58d20'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)


#Mysql configs to enable DB connectivity
app.config['MYSQL_HOST'] = 'frontlinemysql1.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'zlupmisjwe'
app.config['MYSQL_PASSWORD'] = '4GJOZZ651ELRSO6D$'
app.config['MYSQL_DB'] = 'savings_education'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

dbconn = MySQLdb.connect(host="frontlinemysql1.mysql.database.azure.com", user="zlupmisjwe", passwd="4GJOZZ651ELRSO6D$", db="savings_education")

#query to populate Role list from DB
def getroles():
	cur = mysql.connection.cursor()
	sql = "SELECT * from UserRole"
	cur.execute(sql)
	global roleresults
	roleresults = cur.fetchall()
	return roleresults

#query to populate role details from DB
def getroledeets(roleid):
	cur = mysql.connection.cursor()
	sql = "SELECT * from UserRole WHERE RoleId = " + str(roleid)
	cur.execute(sql)
	global roledeets
	roledeets = cur.fetchone()
	return roledeets


#query to populate user details
def getuserdet(uid):
	cur = mysql.connection.cursor()
	sql = "SELECT * from UserInfo WHERE UserEmail = '" + uid + "'"
	cur.execute(sql)
	global uresults
	uresults = cur.fetchone()
	return uresults

#route for root and home
@app.route('/')
@app.route('/home')
def home():
    if  'username' in session:
        username = session['username']

        return redirect('dashboard')
    else:
        return redirect('login')



#route for User Registration (Self Registration)
@app.route('/register', methods = ['GET', 'POST'])
def register():
	form = UserRegistrationForm()
	if request.method != 'POST':
		return render_template('register.html', title='Register for an Account', form=form)
	else:
		form = UserRegistrationForm()
		if form.validate_on_submit():
			today = date.today();AppDate = date.today();d1 = today.strftime("%Y-%m-%d")
			Email = request.form['Email']
			FirstName = request.form['FirstName']
			LastName = request.form['LastName']
			Phone = request.form['PhoneNumber']
			Passwrd = request.form['password']
			RoleId2 = 3
			cur = mysql.connection.cursor()
			print(cur)
			cur.execute("Insert Into UserInfo (UserEmail, Passwrd, PhoneNumber, FirstName, LastName, CreatedDate, RoleId, IsEnabled, IsApproved) Values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(str(Email), str(Passwrd), str(Phone), str(FirstName),str(LastName), str(AppDate), int(RoleId2), True, False))
			mysql.connection.commit()
			cur.close()
			message = FirstName + " Account with email: " + Email + " was sucessfully created. Please login below:"
			flash(message, 'success')
			form2 = LoginForm()
			return redirect('login')
		else:
			return render_template('register.html', title='Registration Failed -- Try Again')


#route for User Creation
@app.route('/createUser', methods = ['GET', 'POST'])
def createUser():
	form = UserCreationForm()
	if  'username' in session:
		uid = session['username']
		RoleId = session['role']
		if request.method != 'POST':
			if RoleId == "Admin":
				getroles()
				i=0;
				for row in (roleresults):
					roleval = str(row['RoleName']);
					roleid = str(row['RoleId']);
					i = i + 1;
					form.UserRole.choices += [(roleid, roleval)]
			status2 = 'Logged in as: ' + session['firstname']
			status3 = 'User Mode: ' + session['role']
			return render_template('userCreate.html', title='Create a User Account', form=form ,msg1=status2, msg2=status3, RoleId = RoleId)
		else:
			today = date.today();AppDate = date.today();d1 = today.strftime("%Y-%m-%d")
			Email = request.form['Email']
			FirstName = request.form['FirstName']
			LastName = request.form['LastName']
			Phone = request.form['PhoneNumber']
			Passwrd = request.form['password']
			if request.form['UserRole'] is None:
				RoleId2=1
			else:
				RoleId2 = request.form['UserRole']
			cur = mysql.connection.cursor()
			print("we are about to execute some SQL")
			cur.execute("Insert Into UserInfo (UserEmail, Passwrd, PhoneNumber, FirstName, LastName, CreatedDate, RoleId, IsEnabled, IsApproved) Values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(str(Email), str(Passwrd), str(Phone), str(FirstName),str(LastName), str(AppDate), int(RoleId2), True, False))
			mysql.connection.commit()
			cur.close()
			actionmsg = 'Account created for: ' + FirstName + " " + LastName + " with Email Address: " + Email
			getuserdet(uid)
			return render_template('dashboard.html', title='Frontline Savings Dashboard', uid = uid, RoleId=RoleId, actionmsg = actionmsg)
	else:
		return redirect('login')



#Will update index to show dashboard once logged n
@app.route('/login', methods = ['GET', 'POST'])
def login():
	cur = mysql.connection.cursor()
	if  'username' in session:
		uid = session['username']
		sql2 = "SELECT * FROM UserInfo WHERE UserEmail='" + uid + "'"
		cur.execute(sql2)
		dataresults = cur.fetchone()
		return redirect(url_for('dashboard' ))
	else:
		form = LoginForm()
		if request.method == 'POST':
			uid = request.form["email"]
			pwd = request.form["password"]
			#had to concatenate the strings to get this working - someone who knows python better can clean this up.
			sql = "SELECT UserEmail, Passwrd FROM UserInfo WHERE UserEmail='" + str(uid) + "' AND Passwrd='" + str(pwd) + "'"
			cur.execute(sql)
			dataresults = cur.fetchall()
			#Validate form submission and that sql returns at least one row Since email is unique we should never get more than 1
			if form.validate_on_submit() and len(dataresults) == 1:
				sql = "SELECT * FROM UserInfo WHERE UserEmail='" + uid + "'"
				cur.execute(sql)
				dataresults = cur.fetchone()
				currole = dataresults["RoleId"]
				getroledeets(currole)
				session['role'] = roledeets["RoleName"]
				session['username'] = str(uid);
				session['firstname'] = dataresults["FirstName"]
				message = "Login successful for " + str(uid)
				RoleId = session['role']
				print("we are catching RoleId: " + RoleId)
				fname = session['firstname']
				flash(message, 'success')
				return redirect(url_for('dashboard'))
			else:
				#redirect to login page if login unsuccessful
				flash('Login Unsucessful', 'error')
				return render_template('login.html', title='loginForm', form=form)
		else:
			return render_template('login.html', title='loginForm', form=form)




#@app.route('/dashboard')
@app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
	if  'username' in session:
		username = session['username']
		RoleId = session['role']
		status2 = 'Logged in as: ' + session['firstname']
		status3 = 'User Mode: ' + session['role']

		return render_template('dashboard.html', msg1=status2, msg2=status3, RoleId=RoleId)
	else:
		return redirect(url_for('login' ))




#@app.route('/manageUsers')
@app.route('/manageUsers', methods = ['GET', 'POST'])
def manageUsers():
	form = EditUserForm()
	cur = mysql.connection.cursor()
	if  'username' in session:
		username = session['username']
		RoleId = session['role']
		status2 = 'Logged in as: ' + session['firstname']
		status3 = 'User Mode: ' + session['role']
		sql = "SELECT * FROM UserInfo"
		cur.execute(sql)
		dataresults = cur.fetchall()

		return render_template('manageUsers.html', msg1=status2, msg2=status3, RoleId=RoleId, dresults=dataresults, form=form)
	else:
		return redirect(url_for('login' ))






#Server information for debugging
if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)

