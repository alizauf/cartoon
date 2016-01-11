from app import app
from flask import render_template
from config import IMAGE_PATH
from models import User, Contest
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
	#image = '011116.jpg'
	path = IMAGE_PATH
	contest = Contest.query.order_by(Contest.id.desc()).first()
	user = User.query.first()
	dt = contest.nyer_contest_date
	date = dt.strftime("%B %d, %Y")
	return render_template('index.html', title="Cartoon Home", contest=contest, path=path, user=user, date=date)