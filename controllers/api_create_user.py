from flask import *
import string
import hashlib
import uuid
import database
import re

api_create_user = Blueprint('api_create_user',__name__, template_folder = 'templates')

@api_create_user.route('/api/create_user', methods = ['POST'])
def create_user():
	print('creating user')

	request_data = request.get_json()
	errors_array = []

	#Error checking: See if there is a missing field in the json data
	if not ('username' in request_data and 'firstname' in request_data and 'lastname' in request_data and 'password1' in request_data and 
	'password2' in request_data and 'email' in request_data):
		errors_array.append({"message": "You did not provide the necessary fields"})
		return jsonify(errors=errors_array), 422


	#Check that all fields contained something
	user = request_data['username']
	first = request_data['firstname']
	last = request_data['lastname']
	pass1 = request_data['password1']
	pass2 = request_data['password2']
	email = request_data['email']
	rating = request_data['rating']
	city = request_data['city']
	state = request_data['state']

	if user == '' or first == '' or last == '' or pass1 == '' or pass2 == '' or email == '' or rating == '' or city == '' or state == '':
		errors_array.append({'message': 'You did not provide the necessary fields'})
		return jsonify(errors=errors_array), 422

	#Check length requirements
	if len(user) > 20: 
		errors_array.append({'message': 'Username must be no longer than 20 characters'})
	if len(first) > 20: 
		errors_array.append({'message': 'First name must be no longer than 20 characters'})
	if len(last) > 20:
		errors_array.append({'message': 'Last name must be no longer than 20 characters'})
	if len(pass1) > 256 or len(pass2) > 256:
		errors_array.append({'message': 'Password must be no longer than 256 characters'})
	if len(pass1) < 8 or len(pass2) < 8:
		errors_array.append({'message': 'Password must be longer than 8 characters'})
	if len(email) > 40:
		errors_array.append({'message': 'Email must be no longer than 40 characters'})
	if len(rating) > 3:
		errors_array.append({'message': 'Rating must be no longer than 3 characters'})
	if len(city) > 20:
		errors_array.append({'message': 'City must be no longer than 20 characters'})
	if len(state) > 20:
		errors_array.append({'message': 'State must be no longer than 20 characters'})


	#Check if userna is taken
	get_user = 'Select username from Users where username = "%s";' % (user)
	user_taken = database.read_from_db(get_user)
	if user_taken:
		errors_array.append({'message': 'This username is taken. Please try a different username.'})


	#Check for punctuation in usernames and passwords. Usernames can contain letters, numbers, and underscores
	acceptable = list(string.ascii_letters)
	acceptable.extend(list(string.digits))
	acceptable.extend(['_'])
	for letter in user:
		if not letter in acceptable:
			errors_array.append({'message': 'Invalid username. Usernames can only contain letters, numbers, and underscores.'})
			break
	for letter in pass1:
		if not letter in acceptable:
			errors_array.append({'message': 'Invalid password. Passwords can only contain letters, numbers, and underscores.'})
			break

	#Check for at least one letter and number in acceptable
	#Check for one letter and number in a password
	count_letter = 0
	count_digit = 0
	for char in pass1:
		if char.isdigit():
			count_digit += 1
		if char.isalpha():
			count_letter +=1

	if count_digit == 0 or count_letter == 0:
		errors_array.append({"message": "Passwords must contain at least one letter and one number"})

	#Check that the passwords are equal
	if pass1 != pass2:
		errors_array.append({'message': 'Passwords must match'})


	#Check that email is valid
	if not re.match(r"[^@]+@[^@]+\.[^@]+",email):
		errors_array.append({"message": "Email address must be valid"})

	if len(errors_array) > 0:
		return jsonify(errors=errors_array), 422


	#At this point, all inputs are correctly formatted.
	#Hash the password and insert these values into the database
	algorithm = "sha512"
	salt = uuid.uuid4().hex
	m = hashlib.new(algorithm)
	m.update(str(salt + pass1).encode('utf-8'))
	password_hash = m.hexdigest()
	real_pass = "$".join([algorithm,salt,password_hash])

	#Insert values into database
	create_new_user = 'Insert into Users (username,firstname,lastname,password,email,rating,city,state) values ("%s","%s","%s","%s","%s","%s","%s","%s")' % (user,first,last,real_pass,email,rating,city,state)
	print(create_new_user)
	database.write_to_db(create_new_user)

	#Start new session for the user
	session['username'] = user

	#Returns a json object with the same fields that it came with
	return jsonify(username=user,firstname=first,lastname=last,password1=pass1,password2=pass2,email=email,rating=rating,city=city,state=state), 201


