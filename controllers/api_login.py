from flask import *
import hashlib
import uuid
import database

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

	if user == '' or pswd == '':
		errors_array.append({"message": "Must submit username and password"})

	#INSERT OTHER ERROR CHECKS HERE


	#Check that Username exists
	get_user = 'Select username from Users where username = %s;' % (user)
	print(get_user)
	check_name = database.read_from_db(get_user)
	print(check_name)
	if not check_name:
		errors_array.append({"message": "Username does not exist"})
		return jsonify(errors=errors_array), 404
		
	#For now, just compare stored passwords
	get_pswd = 'Select password from Users where username = %s;' % (user)
	print(get_pswd)
	check_pswd = database.read_from_db(get_pswd)

	if pswd != check_pswd:
		errors_array.append({"message": "Incorrect Password"})

	#If there were errors, reload login page with error messages
	if len(errors_array) > 0:
		return jsonify(errors=errors_array), 422

	#If we get here, everything is correct and log the user in
	session['username'] = user 
	
	return ('',200)


'''
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
'''
