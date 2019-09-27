from plserver import app
from .database import Database

db = Database()

@app.route('/')
@app.route('/index')
def index():
	return "I am a placeholder. Watch me hold places."

@app.route('/login', methods = ['POST'])
def login():
    pass

@app.route('/logout')
def logout():
    pass