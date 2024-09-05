from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1802Jarin@160'
app.config['MYSQL_DB'] = 'students'

mysql = MySQL(app)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST':
		id = request.form['id']
		username = request.form['username']
		dept = request.form['dept']
		sessions= request.form['sessions']
		email = request.form['email']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
			return redirect(url_for('login'))
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO accounts VALUES (%s, %s, %s, %s, %s, %s)', (id, username, dept,sessions, email, password, ))
			mysql.connection.commit()
			flash ('You have successfully registered !')
			return redirect(url_for('login'))
	
	return render_template('register.html', msg = msg)

@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			session['sessions'] = account['sessions']
			session['dept'] = account['dept']
			flash('Logged in successfully !')
			return redirect(url_for('dashboard'))
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/dashboard')
def dashboard():
	if 'loggedin' in session:
		batch=session['sessions']
		if batch=='2018-19':
			dept=session['dept']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT * FROM batch18 WHERE dept=%s',(dept,))
			results = cursor.fetchall()
			
		elif batch=='2023-24':
			dept=session['dept']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT * FROM batch23 WHERE dept=%s',(dept,))
			results = cursor.fetchall()	
		else: 
			flash('Enter Valid Session')
			return redirect(url_for('register'))
	return render_template('dashboard.html',username=session['username'],dept=dept,results=results)


		

@app.route('/pvc', methods =['GET', 'POST'])
def pvc():
	msg = ''
	if request.method == 'POST':
		degree= request.form['degree']
		username = request.form['username']
		father = request.form['father']
		address = request.form['address']
		id = request.form['id']
		sessions= request.form['sessions']
		dept = request.form['dept']
		cgpa= request.form['cgpa']
		result_date = request.form['result_date']
		last_examination_date = request.form['last_examination_date']
		payment= request.form['payment']
		trx=request.form['trx']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('INSERT INTO pvc VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (degree, username, father,address,id,sessions,dept, cgpa,result_date,last_examination_date, payment,trx, ))
		mysql.connection.commit()
		return redirect(url_for('dashboard'))
	return render_template('pvc.html')

@app.route('/transcript')
def transcript():
	return render_template('transcript.html')

@app.route('/others')
def others():
	return render_template('others.html')

@app.route('/greenbook')
def greenbook():
	return render_template('greenbook.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

	