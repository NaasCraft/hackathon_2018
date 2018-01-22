from flask import Flask, request, abort
from database import app, db, Game, GoalEvent
import json

HOST = '127.0.0.1'
PORT = 5444
RESPONSE_STR = 'OK\n'


@app.route('/goal', methods=['POST'])
def goal():
    if request.method != 'POST':
        abort(401)
        return
    json_data = request.get_json(force=True)
    goalEvent = GoalEvent(team=json_data['sensorID'], timestamp=json_data['timestamp'])
    db.session.add(goalEvent)
    db.session.commit()
    return json.dumps({}), 200, {'ContentType':'application/json'}

@app.route('/start', methods=['POST'])
def start():
    if request.method != 'POST':
        abort(401)
        return
    game = Game(name=request.headers.get('name'), score_red=0, score_blue=0, team_red=request.headers.get('team1'), team_blue=request.headers.get('team2'))
    db.session.add(game)
    db.session.commit()
    return json.dumps({}), 200, {'ContentType':'application/json'}


def main():
    db.init_app(app)
    db.create_all()
    app.run(host=HOST, port=PORT, debug=True)


if __name__ == '__main__':
    main()
