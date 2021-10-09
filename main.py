
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.secret_key = 'mysecretkey'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'logindb'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'user_id' in request.form and 'password' in request.form:
		user_id = request.form['user_id']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user_data WHERE user_id = % s AND password = % s', (user_id, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['user_id'] = account['user_id']
			msg = 'Logged in successfully !'
			return redirect(url_for('home'))
		else:
			cursor.execute('SELECT * FROM user_data WHERE user_id = % s', (user_id, ))
			account = cursor.fetchone()
			if account:
				msg = 'Incorrect password, please try again !'
			else:
				msg = 'The given User ID is not registered, please click on register to continue !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('user_id', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'user_id' in request.form and 'mobile_no' in request.form and 'password' in request.form  and 'confirm_password' in request.form :
		user_id = request.form['user_id']
		password = request.form['password']
		mobile_no = request.form['mobile_no']
		confirm_password = request.form['confirm_password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user_data WHERE user_id = % s', (user_id, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not user_id or not password or not mobile_no:
			msg = 'Please fill out the form !'
		elif password != confirm_password:
			msg = 'Password does not match confirmed password !'
		else:
			cursor.execute('INSERT INTO user_data VALUES (NULL, % s, % s, % s)', (user_id, password, mobile_no, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
			return render_template('login.html', msg = msg)
	elif request.method == 'POST':
		msg = 'Please fill the form properly!'
	return render_template('register.html', msg = msg)

@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['user_id'])
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
