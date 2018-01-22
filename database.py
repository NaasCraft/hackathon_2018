from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.sqlite3'
db = SQLAlchemy(app)

class GoalEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    score_red = db.Column(db.Integer, nullable=False)
    score_blue = db.Column(db.Integer, nullable=False)
    team_red = db.Column(db.String(60), nullable=False)
    team_blue = db.Column(db.String(60), nullable=False)
    paused = db.Column(db.Boolean, nullable=False)
