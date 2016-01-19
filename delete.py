from app import db, models

users = models.User.query.all()

for u in users:
	db.session.delete(u)


captions = models.Caption.query.all()

for c in captions:
	db.session.delete(c)

votes = models.Vote.query.all()

for v in votes:
	db.session.delete(v)

contests = models.Contest.query.all()

for c in contests:
	db.session.delete(c)

db.session.commit()