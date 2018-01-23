
from functools import wraps
import json
import time

from flask import Flask, request, abort

from database import db_session, init_db
from models import Game, GoalEvent

app = Flask(__name__)

HOST = '127.0.0.1'
PORT = 5444


class Table(object):
    def __init__(self):
        self.in_use = False
        self.game_id = None

    def reserve(self):
        if self.in_use:
            return False
        self.in_use = True
        return True

    def start_game(self, game_id):
        self.game_id = game_id

    def release(self):
        self.in_use = False
        self.game_id = None

    def get_game(self):
        return self.game_id


table = Table()


def reserve_table(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not table.reserve():
            abort(401, {'error': 'Table is occupied.'})
            return
        return func(*args, **kwargs)
    return wrapper


def get_game(game_id):
    game = Game.query.get(int(game_id))
    if game is None:
        abort(404, {'error': 'No such game.'})
        return
    return game


def compute_duration(game):
    if game.paused:
        return game.last_duration
    now = int(time.time())
    duration = now - game.start
    if game.last_duration is not None:
        duration += game.last_duration
    return duration


@app.route('/goal', methods=['POST'])
def goal():
    json_data = request.get_json(force=True)

    goal_event = GoalEvent(
        sensor=json_data['sensorID'],
        timestamp=json_data['timestamp']
    )
    db_session.add(goal_event)

    current_game = table.get_game()
    if current_game is None:
        abort(404, {'error': 'No active game.'})
        return

    game = get_game(current_game)

    if goal_event.sensor == 1:
        game.score_red += 1
    elif goal_event.sensor == 2:
        game.score_blue += 1

    db_session.commit()

    return app.response_class(
        response=json.dumps(goal_event.serialize()),
        status=201,
        mimetype='application/json'
    )


@app.route('/start', methods=['POST'])
@reserve_table
def start():
    json_data = request.get_json(force=True)

    game = Game(
        name=json_data['name'],
        score_red=0,
        score_blue=0,
        team_blue=json_data['team_blue'],
        team_red=json_data['team_red'],
        max_goals=json_data.get('max_goals', None),
        start=int(time.time())
    )

    db_session.add(game)
    db_session.commit()

    table.start_game(game.id)

    return app.response_class(
        response=json.dumps(game.serialize()),
        status=201,
        mimetype='application/json'
    )


@app.route('/pause/<game_id>', methods=['POST'])
def pause(game_id):
    game = get_game(game_id)
    game.last_duration = compute_duration(game)
    game.paused = True
    db_session.commit()

    table.release()
    return '{}', 200, {'ContentType': 'application/json'}


@app.route('/resume/<game_id>', methods=['POST'])
@reserve_table
def resume(game_id):
    game = get_game(game_id)
    game.paused = False
    game.start = int(time.time())
    db_session.commit()

    table.start_game(int(game.id))
    return '{}', 200, {'ContentType': 'application/json'}


@app.route('/end/<game_id>', methods=['POST'])
def end(game_id):
    game = get_game(game_id)
    game.last_duration = compute_duration(game)
    game.end = int(time.time())

    table.release()

    return app.response_class(
        response=json.dumps(game.serialize()),
        status=200,
        mimetype='application/json'
    )


@app.route('/status/<game_id>', methods=['GET'])
def status(game_id):
    game = get_game(game_id)

    body = game.serialize()
    body.update({'duration': compute_duration(game)})

    return app.response_class(
        response=json.dumps(body),
        status=200,
        mimetype='application/json'
    )


@app.route('/update/<game_id>', methods=['POST'])
def update(game_id):
    json_data = request.get_json(force=True)
    game = get_game(game_id)

    team = json_data['team']
    if team not in ['blue', 'red']:
        abort(400, "Unknown provided team (must be 'red' or 'blue').")
        return

    difference = int(json_data['difference'])
    game.score_red += difference if team == 'red' else 0
    game.score_blue += difference if team == 'blue' else 0

    db_session.commit()
    return app.response_class(
        response=json.dumps(game.serialize()),
        status=200,
        mimetype='application/json'
    )


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def main():
    init_db()
    app.run(host=HOST, port=PORT, debug=True)


if __name__ == '__main__':
    main()
