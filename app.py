from flask import Flask, request, abort
from database import db, Game, GoalEvent
import json

app = Flask(__name__)

HOST = '127.0.0.1'
PORT = 5444
RESPONSE_STR = 'OK\n'


@app.route('/goal', methods=['POST'])
def goal():
    if request.method != 'POST':
        abort(401)
        return
    json_data = request.get_json(force=True)
    team = json_data['sensorID']
    timestamp = json_data['timestamp']
    goalEvent = GoalEvent(team=team, timestamp=timestamp)
    db.session.add(goalEvent)
    db.session.commit()
    return json.dumps({}), 200, {'ContentType':'application/json'}

@app.route('/start', methods=['POST'])
def start():
    if request.method != 'POST':
        abort(401)
        return
    game_name = request.headers.get('name')
    team1 = request.headers.get('team1')
    team2 = request.headers.get('team2')
    max_goals = request.headers.get('max_goals')
    print(game_name, team1, team2, max_goals)
    game = Game(name=game_name, score_red=0, score_blue=0, team_red=team1, team_blue=team2)
    db.session.add(game)
    db.session.commit()
    return json.dumps({}), 200, {'ContentType':'application/json'}


def main():
    db.init_app(app)
    app.run(host=HOST, port=PORT, debug=True)
    db.create_all()


if __name__ == '__main__':
    main()
