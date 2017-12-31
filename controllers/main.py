from flask import *

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/', methods=['GET'])
def main_route():

	#This is if they try to navigate to the home page
	if request.method == 'GET':

		logged = False
		username = ''

		if 'username' in session:
			logged = True
			username = session['username']

	return render_template("main.html",logged=logged,user=username)