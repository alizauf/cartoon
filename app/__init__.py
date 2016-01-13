from flask import Flask, redirect, url_for, render_template
from flask.ext.sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models