from app import app, db, oauth
from flask import render_template, flash, redirect, session, url_for, request, current_app, g
from config import IMAGE_PATH
from models import User, Contest, Caption, Vote
from datetime import datetime
from forms import CaptionForm, UpdateForm, VoteForm
from oauth import OAuth1Service, OAuth2Service, OAuthSignIn
from flask.ext.login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	contest = Contest.query.order_by(Contest.id.desc()).first()
	form = CaptionForm()
	if form.validate_on_submit():
		caption = Caption(text=form.caption.data, timestamp=datetime.utcnow(), captionist=g.user, contest_id = contest.id)
		db.session.add(caption)
		db.session.commit()
		flash("You've submitted a caption!")
		return redirect(url_for('index'))
	path = IMAGE_PATH
	captions = Caption.query.all()
	dt = contest.nyer_contest_date
	date = dt.strftime("%B %d, %Y")
	return render_template('index.html', title="Cartoon Home", form=form, contest=contest, path=path, date=date, captions=captions)

@app.route('/user/<nickname>', methods=['GET', 'POST'])
@login_required
def user(nickname):
	
	user = g.user.nickname
	#captions = g.user.captions
	#contests = user.captions.contest
	path = IMAGE_PATH
	if user is None:
		flash('User %s not found.' % nickname)
		return redirect(url_for('index'))
	
	form = UpdateForm(g.user.nickname)
	if form.validate_on_submit():
		g.user.nickname = form.nickname.data
		db.session.add(g.user)
		db.session.commit()
		flash("You've updated your username!")
		return redirect(url_for('user', nickname=g.user.nickname))
	else:
		form.nickname.data = g.user.nickname
	return render_template('user.html', user=user, form=form, path=path)

@app.route('/vote', methods=['GET', 'POST'])
@login_required
def vote():
	contest = Contest.query.order_by(Contest.id.desc()).first()
	path = IMAGE_PATH
	captions = Caption.query.order_by(Caption.text)
	form = VoteForm()
	form.vote.choices = [(c.id, c.text) for c in captions]
	choices = form.vote.choices
	if request.method == "POST":
		vote = int(request.form['vote'])
		print vote
		print g.user.id
	
		if form.validate_on_submit():
			vote = Vote(user_id=g.user.id, caption_id=vote)
			db.session.add(vote)
			db.session.commit()
			flash("Thanks for voting!")
			return redirect(url_for('index'))
		else:
			print form.errors
			
	
	return render_template('vote.html', title="Vote", path=path, captions=captions, contest=contest, form=form, choices=choices)
	

lm = LoginManager(app)
lm.login_view = 'index'

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))