from plserver import app

@app.route('/')
@app.route('/index')
def index():
	return "I am a placeholder. Watch me hold places."
