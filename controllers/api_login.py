from flask import *
import hashlib
import uuid

api_login = Blueprint('api_login',__name__, template_folder = 'templates')


@api_login.route('/api/login', methods = ['POST'])
def login_api_route():
	request_data = request.get_json()

	errors_array = []

	#Error checking
	if not ('username' in request_data):
		errors_array.append({"message": "You did not provide the necessary fields"})
		return jsonify(errors=errors_array), 422
	if not ('password' in request_data):
		errors_array.append({"message": "You did not provide the necessary fields"})
		return jsonify(errors=errors_array), 422


	#Get the username and password from the incoming json data
	user = request_data['username']
	pswd = request_data['password']

	#This is copy and pasted from login.py; same logic as before
	db = connect_to_database()
	cur = db.cursor()

	#Check for errors
	if user == "" and pswd == "":
		errors_array.append({"message": "Username may not be left blank"})
		errors_array.append({"message": "Password may not be left blank"})

	#If user is blank but any password is entered
	if user == "" and not(pswd == ""):
		errors_array.append({"message": "Username may not be left blank"})

	#If password is blank 
	if pswd == "":
		cur.execute('SELECT username FROM User WHERE username = %s', (user))
		check = cur.fetchall()
		#If username does not exist
		if not check:
			errors_array.append({"message": "Username does not exist"})
			errors_array.append({"message": "Password may not be left blank"})
		else:
			errors_array.append({"message": "Password may not be left blank"})

	cur.execute('SELECT username FROM User WHERE username = %s', (user))
	check_name = cur.fetchall()

	if not check_name:
		errors_array.append({"message": "Username does not exist"})
		return jsonify(errors=errors_array), 404
		

	#Check that password is correct
	cur.execute('SELECT password FROM User WHERE username = %s', (user))
	fetch = cur.fetchall()
	correct_pass = fetch[0]['password']
	algorithm = correct_pass[:correct_pass.find('$')]
	salt = correct_pass[correct_pass.find('$') + 1:correct_pass.rfind('$')]
	m = hashlib.new(algorithm)
	m.update(str(salt + pswd).encode('utf-8'))
	password_hash = m.hexdigest()
	test = "$".join([algorithm,salt,password_hash])

	#If login not successful
	if not (test == correct_pass):
		errors_array.append({"message": "Password is incorrect for the specified username"})
	#If there were errros

	#If there were errors, reload login page with error messages
	if len(errors_array) > 0:
		return jsonify(errors=errors_array), 422

	#If login successful, return the logged in page and create a new session

	if test == correct_pass:
		session['username'] = user 
		cur.execute('SELECT firstname,lastname FROM User WHERE username = %s', (user))
		names = cur.fetchall()
		session['firstname'] = names[0]['firstname']
		session['lastname'] = names[0]['lastname']

		return jsonify(username=user)

	return 0

@api_login.route('/api/v1/logout', methods = ['POST'])
def logout_api_route():
	db = connect_to_database()
	cur = db.cursor()

	#Error checking
	if not ('username' in session):
		errors_array = []
		errors_array.append({"message": "You do not have the necessary credentials for the resource"})
		return jsonify(errors=errors_array), 401

	#At this point the user has hit the logout button so we can pop their session
	session.pop('username', None)
	session.pop('firstname', None)
	session.pop('lastname', None)

	return ('', 204)

