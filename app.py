import json

from flask import Flask, request
from database import db_session, init_db
from models import Game, GoalEvent

app = Flask(__name__)

HOST = '127.0.0.1'
PORT = 5444


@app.route('/goal', methods=['POST'])
def goal():
    json_data = request.get_json(force=True)

    goal_event = GoalEvent(
        team=json_data['sensorID'],
        timestamp=json_data['timestamp']
    )
    db_session.add(goal_event)
    db_session.commit()

    body = json.dumps(goal_event.serialize())
    return body, 201, {'ContentType': 'application/json'}


@app.route('/start', methods=['POST'])
def start():
    json_data = request.get_json(force=True)

    game = Game(
        name=json_data['name'],
        score_red=0,
        score_blue=0,
        team_red=json_data['team1'],
        team_blue=json_data['team2'],
        max_goals=json_data.get('max_goals', 10)
    )
    db_session.add(game)
    db_session.commit()

    body = json.dumps(game.serialize())
    return body, 201, {'ContentType': 'application/json'}


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def main():
    init_db()
    app.run(host=HOST, port=PORT, debug=True)


if __name__ == '__main__':
    main()
