from flask.ext.wtf import Form
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from app.models import User


class CaptionForm(Form):
    caption = StringField('caption', validators=[DataRequired()])

# ###not using this one anymore
# class UpdateForm(Form):
#     nickname = StringField('nickname', validators=[DataRequired()])

#     def __init__(self, original_nickname, *args, **kwargs):
#         Form.__init__(self, *args, **kwargs)
#         self.original_nickname = original_nickname

#     def validate(self):
#         if not Form.validate(self):
#             return False
#         if self.nickname.data == self.original_nickname:
#             return True
#         user = User.query.filter_by(nickname=self.nickname.data).first()
#         if user != None:
#             self.nickname.errors.append('This nickname is already in use. Please choose another one.')
#             return False
#         return True

class UserForm(Form):
    nickname = StringField('nickname', default="g.user.nickname", validators=[DataRequired()])
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', default="g.user.last_name")
    email = StringField('email', default="g.user.email", validators=[DataRequired()])
    bio = StringField('bio', default="g.user.bio")
    something_funny = StringField('something_funny', default="g.user.something_funny")

class VoteForm(Form):
    vote = SelectField(u'vote', choices=[], coerce=int, validators=[DataRequired()])