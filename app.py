from flask import Flask, request, abort, json
from database import app, db, Game, GoalEvent
from flask_sqlalchemy import event

HOST = '127.0.0.1'
PORT = 5444
RESPONSE_STR = 'OK\n'

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
    if request.method != 'POST':
        abort(401)
        return
    json_data = request.get_json(force=True)
    goalEvent = GoalEvent(team=json_data['sensorID'], timestamp=json_data['timestamp'])
    db.session.add(goalEvent)
    current_game = table.get_game()
    if current_game == None:
        abort(401, {'error':'no_active_game'})
        return
    game = Game.query.get(current_game)
    if game == None:
        abort(401, {'error':'no_such_game'})
        return
    if goalEvent.team == '1':
        game.score_red += 1
    elif goalEvent.team == '2'  :
        game.score_blue += 1
    db.session.commit()
    return json.dumps({}), 200, {'ContentType':'application/json'}

@app.route('/start', methods=['POST'])
def start():
    if request.method != 'POST':
        abort(401)
        return
    if table.reserve():
        game = Game(name=request.headers.get('name'), score_red=0, score_blue=0, team_red=request.headers.get('team1'), team_blue=request.headers.get('team2'), paused=False)
        db.session.add(game)
        db.session.commit()
        table.start_game(int(game.id))
        return json.dumps({'id':game.id}), 200, {'ContentType':'application/json'}
    else:
        abort(401, {'error':'table_occupied'})
        return

@app.route('/pause/<game_id>', methods=['POST'])
def pause(game_id):
    if request.method != 'POST':
        abort(401)
        return
    game = Game.query.get(int(game_id))
    if game == None:
        abort(401, {'error':'no_such_game'})
        return
    game.paused = True
    db.session.commit()
    table.release()
    return json.dumps({}), 200, {'ContentType':'application/json'}

@app.route('/resume/<game_id>', methods=['POST'])
def resume(game_id):
    if request.method != 'POST':
        abort(401)
        return
    game = Game.query.get(int(game_id))
    if game == None:
        abort(401, {'error':'no_such_game'})
        return
    if table.reserve():
        game.paused = False
        db.session.commit()
        table.start_game(int(game.id))
        return json.dumps({}), 200, {'ContentType':'application/json'}
    else:
        abort(401, {'error':'table_occupied'})
        return    


@app.route('/end/<game_id>', methods=['POST'])
def end(game_id):
    if request.method != 'POST':
        abort(401)
        return
    game = Game.query.get(int(game_id))
    if game == None:
        abort(401, {'error':'no_such_game'})
        return
    table.release()
    return json.dumps({}), 200, {'ContentType':'application/json'}

@app.route('/status/<game_id>', methods=['GET'])
def status(game_id):
    if request.method != 'GET':
        abort(401)
        return
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
    if request.method != 'POST':
        abort(401)
        return
    json_data = request.get_json(force=True)
    game = Game.query.get(int(game_id))
    if game == None:
        abort(401, {'error':'no_such_game'})
        return
    if json_data['team'] == '1':
        game.score_red += int(json_data['difference'])
        db.session.commit()
    elif json_data['team'] == '2':
        game.score_blue += int(json_data['difference'])
        db.session.commit()
    else:
        abort(401)
        return
    return json.dumps({}), 200, {'ContentType':'application/json'}
    
def main():
    db.init_app(app)
    db.create_all()
    app.run(host=HOST, port=PORT, debug=True)


if __name__ == '__main__':
    main()
