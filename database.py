from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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

    # NOTE: for dates, we could use the `db.Datetime` type instead...
    start = db.Column(db.Integer, nullable=False)
    end = db.Column(db.Integer)
