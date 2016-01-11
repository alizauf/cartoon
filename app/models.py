from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	password = db.Column(db.String(100))
	email = db.Column(db.String(120), index=True, unique=True)
	bio = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime)
	something_funny = db.Column(db.String(300))
	captions = db.relationship('Caption', backref='user', lazy='dynamic')
	#groups = db.relationship('Group', backref)
#get back to password encryption: http://variable-scope.com/posts/storing-and-verifying-passwords-with-sqlalchemy

	def __repr__(self):
		return '<User %r>' % (self.username)

class Contest(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	image_filename = db.Column(db.String(100), unique=True)
	nyer_artist = db.Column(db.String(100))
	nyer_contest_number = db.Column(db.Integer)
	nyer_contest_date = db.Column(db.DateTime)
	contest_number = db.Column(db.Integer, index=True)
	start_date = db.Column(db.DateTime)
	end_date = db.Column(db.DateTime)
	captions = db.relationship('Caption', backref='contest', lazy='dynamic')

	def __repr__(self):
		return '<Contest %r>' % (self.contest_number)

class Caption(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(250))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	contest_id = db.Column(db.Integer, db.ForeignKey('contest.id'))
	submission_date = db.Column(db.DateTime)

	def __repr__(self):
		return '<Caption %r>' % (self.text)




# **User**

#   -related to group
#   -related to caption



#   Username
#   Email
#   Bio
#   Display Name
#   Link to avatar
#   Link to email settings
  



# **Group**
# -related to user
# -related to group

# **Group Managment**
# -related to user
# -related to group

# **Contest**
# -related to multiple groups
# -related to caption

# **Caption**
# -related to contest
# -related to user

# **Avatars**
# -related to user

# **Email Settings for users (maybe)**

# **Email text?**