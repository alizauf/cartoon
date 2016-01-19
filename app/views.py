from app import app, db, oauth
from flask import render_template, flash, redirect, session, url_for, request, current_app, g
from config import IMAGE_PATH
from models import User, Contest, Caption, Vote
from datetime import datetime, date
from forms import CaptionForm, VoteForm, UserForm
from oauth import OAuth1Service, OAuth2Service, OAuthSignIn
from flask.ext.login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from sqlalchemy import func


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	contest = Contest.query.order_by(Contest.id.desc()).first()
	form = CaptionForm()
	if form.validate_on_submit():
		caption = Caption(text=form.caption.data, timestamp=datetime.utcnow(), user=g.user, contest_id = contest.id)
		db.session.add(caption)
		db.session.commit()
		flash("You've submitted your caption! Compete for real on newyorker.com")
		return redirect(url_for('index'))
	path = IMAGE_PATH
	user_captions = [a.user_id for a in contest.captions]
	return render_template('index.html', title="Cartoon Home", form=form, contest=contest, path=path, user_captions = user_captions)

@app.route('/contests')
def contests():
	contests = Contest.query.order_by(Contest.id.desc())
	path = IMAGE_PATH
	return render_template('contests.html', path=path, contests=contests)

	# query(Table.column, func.count(Table.column)).group_by(Table.column).all()
	# votes = [a.user_id for a in Vote.query.join(Caption).join(Contest).filter(Contest.id == contest.id)]


@app.route('/user/<nickname>', methods=['GET', 'POST'])
@login_required
def user(nickname):
	
	user = User.query.filter_by(nickname=nickname).first()
	path = IMAGE_PATH
	if user is None:
		flash('User %s not found.' % nickname)
		return redirect(url_for('index'))
	return render_template('user.html', user=user, path=path)

@app.route('/vote', methods=['GET', 'POST'])
@login_required
def vote():
	contest = Contest.query.order_by(Contest.id.desc()).first()
	path = IMAGE_PATH
	captions = Caption.query.order_by(Caption.text)
	user_captions = [a.user_id for a in contest.captions]
	user = g.user
	form = VoteForm()
	form.vote.choices = [(c.id, c.text) for c in contest.captions]
	choices = form.vote.choices
	votes = [a.user_id for a in Vote.query.join(Caption).join(Contest).filter(Contest.id == contest.id)]
	if request.method == "POST":
		vote = int(request.form['vote'])

	
		if form.validate_on_submit():
			vote = Vote(user_id=g.user.id, caption_id=vote)
			db.session.add(vote)
			db.session.commit()
			flash("Thanks for voting!")
			return redirect(url_for('vote'))

			
	
	return render_template('vote.html', title="Vote", path=path, captions=captions, contest=contest, form=form, choices=choices, user=user, user_captions=user_captions, votes=votes)

@app.route('/signup')
def signup():
	path = IMAGE_PATH
	return render_template('signup.html', title="Signup", path=path)	

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	path = IMAGE_PATH
	form = UserForm()
	captions = Caption.query.all()
	user_captions = [a.user_id for a in captions]
	if form.validate_on_submit():
		g.user.nickname = form.nickname.data
		g.user.email = form.email.data
		g.user.first_name = form.first_name.data
		g.user.last_name = form.last_name.data
		g.user.bio = form.bio.data
		g.user.something_funny = form.something_funny.data
		if g.user.date_joined == None:
			g.user.date_joined = date.today()
		else:
			g.user.date_joined = g.user.date_joined
		db.session.add(g.user)
		db.session.commit()
		if g.user.id not in user_captions:
			flash("Get started with your first caption!")
			return redirect(url_for('index'))
		else:
			flash("Thanks for updating your profile!")
			return redirect(url_for('user', nickname=g.user.nickname))
	return render_template('profile.html', title="Fill in your info", path=path, form=form)

@app.route('/about')
def about():
	path = IMAGE_PATH
	return render_template('about.html', path=path)	


@app.route('/login')
def login():
	path = IMAGE_PATH
	return render_template('login.html', title="Login", path=path)	

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
    if g.user.first_name == None:
    	flash("You're almost there! Just fill in a little more information!")
    	return redirect(url_for('profile'))
    else:
    	return redirect(url_for('index'))