from flask import Flask, session, redirect, url_for, render_template, request, jsonify
import os, string, random, simplejson
from datetime import timedelta
from controllers.UserController import UserController
from controllers.AccountController import AccountController

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTING'])
app.permanent_session_lifetime = timedelta(seconds=86400)

user = UserController()
account = AccountController()

## home page
@app.route('/')
def index():
	try:
		if session['logged_in'] == True:
			return redirect(url_for('viewAccounts'))
	except KeyError:
		return render_template('index.html')

## dashboard
@app.route('/dashboard/<account_id>', methods=['GET'])
def dashboard(account_id):
	try:
		if session['logged_in'] == True:
			meta_data = account.getAccountData(session['username'], account_id)
			if not meta_data:
				return render_template('dashboard.html', error="This account is not associated with this user!")
			else:
				return render_template('dashboard.html', data=meta_data, account_id=account_id)
	except KeyError:
		return redirect(url_for('index'))

## accounts
@app.route('/accounts', methods=['GET'])
def viewAccounts():
	try:
		if session['logged_in'] == True:
			account_ids = account.getAccounts(session['username'])
			return render_template('accounts.html',ids = account_ids)
	except KeyError:
		return redirect(url_for('index'))

@app.route('/create_account', methods=['POST','GET'])
def createAccount():
	try:
		if session['logged_in'] == True:
			if request.method == 'POST':

				# csrf check
				csrf_token = session.pop('csrf_token', None)
				if not csrf_token or csrf_token != request.form['csrftoken']:
					return redirect(url_for('logout'))

				# get form data and create account
				credit_limit = request.form['creditlimit']
				apr = request.form['apr']
				a_id = account.createAccount(session['username'],credit_limit, apr)

				return redirect(url_for('dashboard', account_id = a_id))
			else:
				return render_template('create_account.html')
	except KeyError:
		return redirect(url_for('index'))

## transactions
@app.route('/view_transactions/<account_id>',methods=['GET'])
def viewTransactions(account_id):
	try:
		if session['logged_in'] == True:

			# attempt to get transaction data
			transactions = account.getTransactions(session['username'],account_id)

			if transactions == False:
				# error
				return render_template('view_transactions.html', error="This account is not associated with this user!")
			else:
				# render data
				return render_template('view_transactions.html', data=transactions)
	except KeyError:
		return redirect(url_for('index'))

@app.route('/create_transaction/<account_id>',methods=['GET','POST'])
def createTransaction(account_id):
	try:
		if session['logged_in'] == True:
			if request.method =="POST":

				# csrf check
				csrf_token = session.pop('csrf_token', None)
				if not csrf_token or csrf_token != request.form['csrftoken']:
					return redirect(url_for('logout'))

				# create transaction from form data
				amount = request.form['amount']
				trans_type = request.form['trans_type']
				transaction_day = request.form['transaction_day']

				account.createTransaction(account_id, transaction_day, amount, trans_type)
				return redirect(url_for('dashboard',account_id=account_id))
			else:
				return render_template('create_transaction.html', account_id=account_id)
	except KeyError:
		return redirect(url_for('index'))

#### User pages
@app.route('/auth/register', methods=['GET','POST'])
def register():
	error = None
	if request.method == 'POST':
		# complete user reg
		username = request.form['username']
		password = request.form['password']
		is_registered = user.registerUser(username,password)
		if is_registered == True:
			# add the user data to session
			session['logged_in'] = True
			session['username'] = username
			return redirect(url_for('createAccount'))
		else:
			error = is_registered
	
	return render_template('auth/register.html',error=error)

@app.route('/login', methods=['POST','GET'])
def login():
	error = None
	if request.method =='POST':
		username = request.form['username']
		password = request.form['password']

		is_authenticated = user.authenticateUser(username,password)

		if is_authenticated == True:
			session.permanent = True
			session['logged_in'] = True
			session['username'] = username
     
			# go to user dashboard
			return redirect(url_for('viewAccounts'))
		else:
			error = is_authenticated
	return render_template('auth/login.html', error=error)

@app.route('/logout', methods=['GET'])
def logout():
	session.pop('logged_in', None)
	session.pop('username', None)
	session.pop('csrf_token',None)

	return redirect(url_for('index'))

def generate_csrf_token():
	try:
		if 'csrf_token' not in session or session['csrf_token'] is None:
			session['csrf_token'] = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])
		return session['csrf_token']
	except:
		raise

# give jinja ability to store and create a csrf token
app.jinja_env.globals['csrf_token'] = generate_csrf_token

if __name__ == '__main__':
	app.run()
