
import json
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
        else:
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

@app.route('/goal', methods=['POST'])
def goal():
    json_data = request.get_json(force=True)

    goal_event = GoalEvent(
        team=json_data['sensorID'],
        timestamp=json_data['timestamp']
    )
    db_session.add(goal_event)

    current_game = table.get_game()
    if current_game == None:
        abort(401, {'error':'no_active_game'})
        return
    game = Game.query.get(current_game)
    if game == None:
        abort(401, {'error':'no_such_game'})
        return
    if goal_event.team == '1':
        game.score_red += 1
    elif goal_event.team == '2'  :
        game.score_blue += 1

    db_session.commit()

    body = json.dumps(goal_event.serialize())
    return body, 201, {'ContentType': 'application/json'}


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/start', methods=['POST'])
def start():
    json_data = request.get_json(force=True)

    if table.reserve():
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
        table.start_game(int(game.id))
        
        body = json.dumps(game.serialize())
        return body, 201, {'ContentType': 'application/json'}
    else:
        abort(401, {'error':'table_occupied'})
        return

@app.route('/pause/<game_id>', methods=['POST'])
def pause(game_id):
    game = Game.query.get(int(game_id))
    if game == None:
        abort(401, {'error':'no_such_game'})
        return
    game.paused = True
    db_session.commit()
    table.release()
    return json.dumps({}), 200, {'ContentType':'application/json'}

@app.route('/resume/<game_id>', methods=['POST'])
def resume(game_id):
    game = Game.query.get(int(game_id))
    if game == None:
        abort(401, {'error':'no_such_game'})
        return
    if table.reserve():
        game.paused = False
        db_session.commit()
        table.start_game(int(game.id))
        return json.dumps({}), 200, {'ContentType':'application/json'}
    else:
        abort(401, {'error':'table_occupied'})
        return    


@app.route('/end/<game_id>', methods=['POST'])
def end(game_id):
    game = Game.query.get(int(game_id))
    if game == None:
        abort(401, {'error':'no_such_game'})
        return
    table.release()
    return json.dumps({}), 200, {'ContentType':'application/json'}

@app.route('/status/<game_id>', methods=['GET'])
def status(game_id):
    game = Game.query.get(int(game_id))
    #TODO // add duration
    response = app.response_class(
        response=json.dumps({'name':game.name, 'team_1_score':game.score_red, 'team_2_score':game.score_blue}),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/update/<game_id>', methods=['POST'])
def update(game_id):
    json_data = request.get_json(force=True)
    game = Game.query.get(int(game_id))
    if game == None:
        abort(401, {'error':'no_such_game'})
        return
    if json_data['team'] == '1':
        game.score_red += int(json_data['difference'])
        db_session.commit()
    elif json_data['team'] == '2':
        game.score_blue += int(json_data['difference'])
        db_session.commit()
    else:
        abort(401)
        return
    return json.dumps({}), 200, {'ContentType':'application/json'}
    
def main():
    init_db()
    app.run(host=HOST, port=PORT, debug=True)


if __name__ == '__main__':
    main()
