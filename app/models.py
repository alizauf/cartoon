from app import db, oauth
from flask.ext.login import UserMixin

class User(UserMixin, db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	social_id = db.Column(db.String(64), unique=True)
	nickname = db.Column(db.String(64))
	first_name = db.Column(db.String(64))
	last_name = db.Column(db.String(100))
	email = db.Column(db.String(120), index=True, unique=True, nullable=True)
	bio = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime)
	date_joined = db.Column(db.DateTime)
	something_funny = db.Column(db.String(300))
	caption = db.relationship('Caption', back_populates='user')
	vote = db.relationship('Vote', back_populates='user')

	#groups = db.relationship('Group', backref)
#get back to password encryption: http://variable-scope.com/posts/storing-and-verifying-passwords-with-sqlalchemy

	def __repr__(self):
		return '<User %r>' % (self.nickname)

class Contest(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	image_filename = db.Column(db.String(100), unique=True)
	nyer_artist = db.Column(db.String(100))
	nyer_contest_number = db.Column(db.Integer)
	nyer_contest_date = db.Column(db.DateTime)
	contest_number = db.Column(db.Integer, index=True)
	start_date = db.Column(db.DateTime)
	end_date = db.Column(db.DateTime)
	#captions = db.relationship('Caption', backref='contest', lazy='dynamic')
	captions = db.relationship("Caption", back_populates="contest")
	def __repr__(self):
		return '<Contest %r>' % (self.contest_number)

class Caption(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(250))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	contest_id = db.Column(db.Integer, db.ForeignKey('contest.id'))
	timestamp = db.Column(db.DateTime)
	contest = db.relationship('Contest', back_populates="captions") 
	vote = db.relationship('Vote', back_populates='caption')
	user = db.relationship("User", back_populates="caption")

	def __repr__(self):
		return '<Caption %r>' % (self.text)

	def winner(self, contest_id):
		tally = {}
		votes = Vote.query.all()
		for v in votes:
			if v.caption.contest_id == contest_id:
				if v.caption.id not in tally:
					tally[v.caption.id] = 1
				else:
					tally[v.caption.id] += 1
		if tally != {}:
			mx = max(tally.values())
			winners = [k for k, v in tally.items() if v == mx]
			return winners
		else:
			return None
		

class Vote(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	caption_id = db.Column(db.Integer, db.ForeignKey('caption.id'))
	user = db.relationship('User', back_populates='vote')
	caption = db.relationship('Caption', back_populates='vote')

	def __repr__(self):
		return '<Vote %r, %r>' % (self.user_id, self.caption_id)



#image table

# **Group**
# -related to user
# -related to group

# **Group Managment**
# -related to user
# -related to group


# **Avatars**
# -related to user

# **Email Settings for users (maybe)**

# **Email text?**