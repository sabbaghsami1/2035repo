from config import app
from flask import render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address



@app.route('/')
def index():
    return render_template('home/index.html')



@app.errorhandler(429)
def ratelimit_error(e):
    return render_template("errors/ratelimit.html"), 429

if __name__ == '__main__':
    app.run()
