from flask import *
from controllers.main import main
from controllers.api_login import api_login

app = Flask(__name__, template_folder='templates')

app.register_blueprint(main)
app.register_blueprint(api_login)

#Set secret key
app.secret_key = 'wmQ\xef\x03\xaeV\xa63\x92\xfb\xd6\x914w\xe9\xb4\xbe \x1f5\x1a\x9e\x8b'

if __name__ == '__main__':
	app.run(debug=True)